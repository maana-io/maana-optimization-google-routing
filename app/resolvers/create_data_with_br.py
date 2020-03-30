from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import json
from collections import defaultdict

# import logging

from copy import deepcopy

from app.utils.routing_solver_utils import dummify, add_dummy_entries_for_draft, create_draft_dummy_cargos
from app.resolvers.optimizer_types import Cargo
from app.logger import logger


def calc_empty_draft(vehicle):
    md = vehicle["vehicleDimensions"]["depth"]["max"]
    mw = vehicle["weightCapacity"]["value"]
    s = vehicle["vehicleDimensions"]["depth"]["massMultiplier"]

    empty_draft = md - (mw / s) * 0.01

    if empty_draft < 0:
        logger.warn(f"empty_draft of {empty_draft} detected, setting to 0")
        return 0

    return empty_draft


def convert_vehicle_data(vehicles):

    vehicle_data = {"vehicle_volume_capacities": [],
                    "vehicle_weight_capacities": [],
                    "vessel_speeds": [],
                    "vessel_empty_draft": [],
                    "immersion_summer": [],
                    "starting_locations": [],
                    }

    vehicle_ind_to_id = {}

    for ind, vehicle in enumerate(vehicles):
        vehicle_data["vehicle_volume_capacities"].append(
            vehicle["volumeCapacity"]["value"])
        vehicle_data["vehicle_weight_capacities"].append(
            vehicle["weightCapacity"]["value"])
        vehicle_data["vessel_speeds"].append(
            vehicle["vehicleSpeed"]["value"])
        empty_draft = calc_empty_draft(vehicle)
        logger.info(f"vehicle ind: {ind}, empty_draft: {empty_draft}")
        vehicle_data["vessel_empty_draft"].append(
            empty_draft)
        vehicle_data["immersion_summer"].append(
            vehicle["vehicleDimensions"]["depth"]["massMultiplier"])
        vehicle_data["starting_locations"].append(
            vehicle["startingLocation"]["id"])

        vehicle_ind_to_id[ind] = vehicle["id"]

    vehicle_data["vehicle_ind_to_id"] = vehicle_ind_to_id
    vehicle_data["vehicle_id_to_ind"] = {
        v: k for k, v in vehicle_data["vehicle_ind_to_id"].items()}

    return vehicle_data


def convert_distance_matrix(input_distances):

    data = {}

    distance_rows = []

    distance_rows.append(
        [0 for _ in range(len(input_distances["rows"]) + 1)])

    for row in input_distances["rows"]:
        distance_rows.append([0] + row["values"])

    distance_rows = np.array(distance_rows, dtype=np.int)
    np.fill_diagonal(distance_rows, 0)

    # need to convert back to list otherwise strange issues with callback
    data["distance_matrix"] = distance_rows.tolist()

    return data


def get_ports_mapping(input_distances):

    port_to_ind = {row["id"]: ind for ind,
                   row in enumerate(input_distances["rows"], 1)}

    return port_to_ind


def convert_cost_matrix(input_cost_of_vehicle_routes_matrix):

    cost_matrix = []

    cost_matrix.append(
        [0 for _ in range(len(input_cost_of_vehicle_routes_matrix["rows"]) + 1)])

    for row in input_cost_of_vehicle_routes_matrix["rows"]:
        cost_matrix.append([0] + row["values"])

    cost_matrix = np.array(cost_matrix, dtype=np.int)
    np.fill_diagonal(cost_matrix, 0)

    # need to convert back to list, otherwise strange issues with callback
    return cost_matrix.tolist()


def convert_cost_matrices(input_cost_matrices):

    data = {}
    cost_matrices = []
    for cost_matrix in input_cost_matrices["costMatrices"]:
        cost_matrices.append(convert_cost_matrix(cost_matrix))

    data["cost_matrixes"] = cost_matrices

    return data


def convert_cargo(input_cargos):

    cargos = []

    for input_cargo in input_cargos:
        cargo = Cargo()

        cargo.id = input_cargo["id"]
        cargo.volume = input_cargo["volume"]
        cargo.weight = input_cargo["weight"]
        cargo.origin = input_cargo["routePair"]["origin"]["id"]
        cargo.destination = input_cargo["routePair"]["destination"]["id"]
        cargo.laycanFrom = input_cargo["loadWindow"]["timeWindow"]["start"]
        cargo.laycanTo = input_cargo["loadWindow"]["timeWindow"]["end"]
        cargo.dischargeDateFrom = input_cargo["unloadWindow"]["timeWindow"]["start"]
        cargo.dischargeDateTo = input_cargo["unloadWindow"]["timeWindow"]["end"]
        cargo.revenue = input_cargo["revenue"]

        cargos.append(cargo)

    return cargos


def modify_cargo_ports(cargos, port_to_ind):
    for cargo in cargos:
        cargo.origin = port_to_ind[cargo.origin.split("::")[0]]
        cargo.destination = port_to_ind[cargo.destination.split("::")[0]]

    return cargos


def add_port_draft(cargos_json, port_to_ind):

    port_draft_max = {}

    port_to_max_draft = {}
    for cargo in cargos_json:
        origin_port_id = cargo["routePair"]["origin"]["id"].split("::")[0]
        origin_port_max_depth = cargo["routePair"]["origin"]["dimension"]["depth"]["max"]
        logger.debug(
            f"origin_port_id: {origin_port_id}, origin_port_max_depth: {origin_port_max_depth}")
        port_to_max_draft[origin_port_id] = origin_port_max_depth
        destination_port_id = cargo["routePair"]["destination"]["id"].split("::")[
            0]
        destination_port_max_depth = cargo["routePair"]["destination"]["dimension"]["depth"]["max"]
        logger.debug(
            f"destination_port_id: {destination_port_id}, destination_port_max_depth: {destination_port_max_depth}")
        port_to_max_draft[destination_port_id] = destination_port_max_depth

    logger.debug(f"port_to_max_draft: {port_to_max_draft}")

    ind_to_draft = {
        port_to_ind[port_id]: draft for port_id, draft in port_to_max_draft.items()}

    logger.debug("ind_to_draft: {}".format(ind_to_draft))

    large_number = 1000 * 1000 * 1000

    port_to_max_draft_orig = {0: large_number}

    port_to_max_draft_orig.update(ind_to_draft)
    port_to_max_draft_orig[len(ind_to_draft) +
                           1] = large_number  # For draft dummy
    port_to_max_draft_orig[len(ind_to_draft) +
                           2] = large_number  # For draft dummy

    logger.debug("port_to_max_draft_orig: {}".format(port_to_max_draft_orig))

    draft_data = {}

    draft_data["port_max_draft_orig"] = port_to_max_draft_orig

    return draft_data


def make_ind_to_dummys(dummy_to_ind):
    ind_to_dummys = defaultdict(list)
    for dummy, ind in dummy_to_ind.items():
        ind_to_dummys[ind].append(dummy)
    return ind_to_dummys


def add_port_to_allowed_vehicles(cargos_json,
                                 vehicle_id_to_ind,
                                 cargo_node_ind_start
                                 ):

    port_to_allowed_vehicles = []
    cargo_to_port_inds = {}

    cargo_inds = [(x, x+1)
                  for x in range(cargo_node_ind_start,
                                 cargo_node_ind_start+len(cargos_json) * 2,
                                 2)]

    for cargo, origin_dest in zip(cargos_json, cargo_inds):
        origin_port_ind, destination_port_ind = origin_dest

        if "candiateVehicles" not in cargo or not cargo["candiateVehicles"]:

            port_to_allowed_vehicles.append(
                {"port": origin_port_ind, "vehicles": []})
            port_to_allowed_vehicles.append(
                {"port": destination_port_ind, "vehicles": []}
            )

        else:
            vehicles = cargo["candiateVehicles"]
            vehicle_inds = [vehicle_id_to_ind[v["id"]] for v in vehicles]
            port_to_allowed_vehicles.append(
                {"port": origin_port_ind, "vehicles": vehicle_inds})
            port_to_allowed_vehicles.append(
                {"port": destination_port_ind, "vehicles": vehicle_inds}
            )

    return port_to_allowed_vehicles


def create_data_model_with_br(vehicles, requirements, costMatrix, distanceMatrix, routingTimeWindow):
    """Stores the data for the problem."""

    vehicles_json = vehicles
    distance_matrix_json = distanceMatrix
    cost_matrices_json = costMatrix
    cargos_json = requirements

    data = {}

    vehicle_data = convert_vehicle_data(vehicles_json)
    data.update(vehicle_data)

    distance_matrix_data = convert_distance_matrix(distance_matrix_json)
    data.update(distance_matrix_data)

    cost_matrices_data = convert_cost_matrices(cost_matrices_json)
    data.update(cost_matrices_data)

    original_cargos = convert_cargo(cargos_json)

    print(f"original_cargos: {original_cargos}")

    port_to_ind = get_ports_mapping(distance_matrix_json)
    original_cargos = modify_cargo_ports(original_cargos, port_to_ind)

    logger.debug(f"port_to_ind: {port_to_ind}")

    ind_to_port = {v: k for k, v in port_to_ind.items()}
    data["port_to_ind"] = port_to_ind
    data["ind_to_port"] = ind_to_port

    # data["total_revenue"] = sum(c.revenue for c in original_cargos)
    data["orig_distance_matrix"] = data["distance_matrix"]

    draft_dummy_origin = 0
    draft_dummy_destinations = [port_to_ind[x]
                                for x in data["starting_locations"]]

    draft_dummy_cargos = create_draft_dummy_cargos(data["vessel_empty_draft"],
                                                   data["immersion_summer"],
                                                   from_port=draft_dummy_origin,
                                                   starting_locations=draft_dummy_destinations
                                                   )
    data["cargo_ind_to_revenue"] = {
        ind: c.revenue for ind, c in enumerate(draft_dummy_cargos + original_cargos)}

    data["original_cargo_id_to_ind"] = {c.id:
                                        len(draft_dummy_cargos) + i for i, c in enumerate(original_cargos)}

    data["original_cargo_ind_to_id"] = {
        v: k for k, v in data["original_cargo_id_to_ind"].items()}

    print(f"original_cargo_ind_to_id:")
    print(data["original_cargo_ind_to_id"])

    temp = dummify(data["distance_matrix"],
                   draft_dummy_cargos, original_cargos)

    new_dist, dummy_to_ind, volume_demands, weight_demands, draft_demands, pickups_deliveries, time_windows = temp
    n = len(data["distance_matrix"])
    draft_dummy_inds_to_zero_out = range(
        n + 1, n + 2 * len(draft_dummy_cargos), 2)

    ind_to_dummys = make_ind_to_dummys(dummy_to_ind)

    # draft_demands = deepcopy(weight_demands)

    logger.debug(f"dummy_to_ind: {dummy_to_ind}")

    for ind in draft_dummy_inds_to_zero_out:
        draft_demands[ind] = 0

    logger.info("Distance Matrix size: {}".format(len(new_dist)))

    data["dummy_to_ind"] = dummy_to_ind
    data["pickups_deliveries"] = pickups_deliveries
    data["time_windows"] = time_windows

    data["distance_matrix"] = new_dist
    data["volume_demands"] = volume_demands
    data["weight_demands"] = weight_demands
    # data["draft_demands"] = draft_demands

    logger.debug("volume_demands")
    logger.debug(data["volume_demands"])

    logger.debug("weight_demands")
    logger.debug(data["weight_demands"])

    data["cost_matrixes"] = [dummify(m, draft_dummy_cargos, original_cargos)[0]
                             for m in data["cost_matrixes"]]

    data["vehicle_starting_time"] = [
        0 for _ in range(len(data["vessel_speeds"]))]

    data["time_matrices"] = [np.array(data["distance_matrix"]) /
                             speed for speed in data["vessel_speeds"]]

    # data["port_to_allowed_vehicles"] = []  # [{"port": 3, "vehicles": [1]}]

    cargo_node_ind_start = len(port_to_ind) + len(draft_dummy_cargos) * 2 + 1

    data["port_to_allowed_vehicles"] = add_port_to_allowed_vehicles(
        cargos_json,
        data["vehicle_id_to_ind"],
        cargo_node_ind_start
    )

    logger.debug("port_to_allowed_vehicles")
    logger.debug(data["port_to_allowed_vehicles"])

    draft_data = add_port_draft(cargos_json, port_to_ind)
    data.update(draft_data)

    data["port_max_draft"] = {}

    for k, v in dummy_to_ind.items():
        if k > 0:
            data["port_max_draft"][k] = data["port_max_draft_orig"][v]

    # Just mocked for now
    data["load_and_dropoff_times"] = [
        {"load": 0, "dropoff": 0} for _ in range(len(original_cargos) + len(draft_dummy_cargos))]

    assert(len(data["pickups_deliveries"]) ==
           len(data["load_and_dropoff_times"]))

    data["vehicle_for_cargo"] = list(range(len(vehicles))) + \
        [None for _ in range(len(original_cargos))]

    assert(len(data["vehicle_for_cargo"]) == len(data["pickups_deliveries"]))

    data['num_vehicles'] = len(data["vessel_speeds"])
    data["starts"] = [0 for _ in range(len(data["vessel_speeds"]))]
    data["ends"] = [0 for _ in range(len(data["vessel_speeds"]))]

    data["timeWindow"] = routingTimeWindow["timeWindow"]

    return data
