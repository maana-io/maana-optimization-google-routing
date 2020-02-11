from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import json

from copy import deepcopy

# from optimizer import Optimizer
from app.utils.routing_solver_utils import dummify, add_dummy_entries_for_draft, create_draft_dummy_cargos


class Cargo:
    def __init__(self, origin=None,
                 dest=None,
                 volume=None,
                 weight=None,
                 laycanFrom=None,
                 laycanTo=None,
                 dischargeDateFrom=None,
                 dischargeDateTo=None,
                 revenue=None):
        self.origin = origin
        self.destination = dest
        self.volume = volume
        self.weight = weight
        self.laycanFrom = laycanFrom
        self.laycanTo = laycanTo
        self.dischargeDateFrom = dischargeDateFrom
        self.dischargeDateTo = dischargeDateTo
        self.revenue = revenue

# from current_data_types import Cargo

# from mocked_data_types import Capacity, \
#     Speed, \
#     Depth, \
#     Dimension, \
#     RouteNode, \
#     Vehicle, \
#     Row, \
#     DistanceMatrix, \
#     CostOfVehicleRoutesMatrix, \
#     CostMatrices, \
#     TimeWindow, \
#     UnloadWindow, \
#     LoadWindow, \
#     RoutePair, \
#     RequirementToTransport


def make_vehicle(volumeCapacity, weightCapacity, speed, draft, immersion_summer):

    vehicle = Vehicle()
    vehicle.volumeCapacity = Capacity(value=volumeCapacity)
    vehicle.weightCapacity = Capacity(value=weightCapacity)
    vehicle.vehicleSpeed = Speed(value=speed)
    vehicle.vehicleDimensions = Dimension(depth=Depth(
        empty=draft, massMultiplier=immersion_summer))

    return vehicle


def make_distance_matrix(rows):

    distance_matrix = DistanceMatrix()

    for row in rows:
        distance_matrix.rows.append(Row(values=row))

    return distance_matrix


def make_cost_of_vehicle_matrix(rows):

    matrix = CostOfVehicleRoutesMatrix(rows=[])

    for row in rows:
        matrix.rows.append(Row(values=row))

    return matrix


def make_cargo(origin,
               destination,
               load_start,
               load_end,
               unload_start,
               unload_end,
               volume,
               weight
               ):

    depth_a = Depth(max=6)
    dimension_a = Dimension(depth=depth_a)
    port_a = RouteNode(id="a",
                       dimension=dimension_a
                       )

    depth_b = Depth(max=6)
    dimension_b = Dimension(depth=depth_b)
    port_b = RouteNode(id="b",
                       dimension=dimension_b
                       )

    depth_c = Depth(max=6)
    dimension_c = Dimension(depth=depth_c)
    port_c = RouteNode(id="c",
                       dimension=dimension_c
                       )

    depth_d = Depth(max=6)
    dimension_d = Dimension(depth=depth_d)

    port_d = RouteNode(id="d",
                       dimension=dimension_d
                       )

    port_mapping = {"a": port_a,
                    "b": port_b,
                    "c": port_c,
                    "d": port_d,
                    }

    route_pair = RoutePair(
        origin=port_mapping[origin], destination=port_mapping[destination])

    load_window = LoadWindow(timeWindow=TimeWindow(
        start=load_start, end=load_end))
    unload_window = UnloadWindow(timeWindow=TimeWindow(
        start=unload_start, end=unload_end))

    requirement_to_transport = RequirementToTransport(routePair=route_pair,
                                                      volume=volume,
                                                      weight=weight,
                                                      loadWindow=load_window,
                                                      unloadWindow=unload_window
                                                      )

    return requirement_to_transport


def convert_vehicle_data(vehicles):

    vehicle_data = {"vehicle_volume_capacities": [],
                    "vehicle_weight_capacities": [],
                    "vessel_speeds": [],
                    "vessel_empty_draft": [],
                    "immersion_summer": [],
                    "starting_locations": [],
                    }

    for vehicle in vehicles:
        vehicle_data["vehicle_volume_capacities"].append(
            vehicle["volumeCapacity"]["value"])
        vehicle_data["vehicle_weight_capacities"].append(
            vehicle["weightCapacity"]["value"])
        vehicle_data["vessel_speeds"].append(vehicle["vehicleSpeed"]["value"])
        vehicle_data["vessel_empty_draft"].append(
            vehicle["vehicleDimensions"]["depth"]["empty"])
        vehicle_data["immersion_summer"].append(
            vehicle["vehicleDimensions"]["depth"]["massMultiplier"])
        vehicle_data["starting_locations"].append(
            vehicle["startingLocation"]["id"])

    return vehicle_data


def convert_distance_matrix(input_distances):

    data = {}

    data["distance_matrix"] = []

    data["distance_matrix"].append(
        [0 for _ in range(len(input_distances["rows"]) + 1)])

    for row in input_distances["rows"]:
        data["distance_matrix"].append([0] + row["values"])

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

    return cost_matrix


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
        port_to_max_draft[cargo["routePair"]["origin"]["id"].split("::")[0]
                          ] = cargos_json[0]["routePair"]["origin"]["dimension"]["depth"]["max"]
        port_to_max_draft[cargo["routePair"]["destination"]["id"].split("::")[0]
                          ] = cargos_json[0]["routePair"]["destination"]["dimension"]["depth"]["max"]

    ind_to_draft = {
        port_to_ind[port_id]: draft for port_id, draft in port_to_max_draft.items()}

    print("ind_to_draft")
    print(ind_to_draft)

    large_number = 1000

    port_to_max_draft_orig = {0: large_number}

    port_to_max_draft_orig.update(ind_to_draft)
    port_to_max_draft_orig[len(ind_to_draft) +
                           1] = large_number  # For draft dummy
    port_to_max_draft_orig[len(ind_to_draft) +
                           2] = large_number  # For draft dummy

    print("port_to_max_draft_orig")
    print(port_to_max_draft_orig)

    draft_data = {}

    draft_data["port_max_draft_orig"] = port_to_max_draft_orig

    return draft_data


def create_data_model(vehicles, requirements, costMatrix, distanceMatrix):
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

    # port_to_ind = get_ports_mapping(original_cargos)
    port_to_ind = get_ports_mapping(distance_matrix_json)
    original_cargos = modify_cargo_ports(original_cargos, port_to_ind)

    data["total_revenue"] = sum(c.revenue for c in original_cargos)
    # data["distance_matrix"] = add_dummy_entries_for_draft(
    #     data["distance_matrix"], 100 * 10000 * 10000)

    data["orig_distance_matrix"] = data["distance_matrix"]

    # draft_dummy_origin = len(data["distance_matrix"]) - 2
    # draft_dummy_destination = len(data["distance_matrix"]) - 1

    draft_dummy_origin = 0
    # draft_dummy_destinations = [1, 1, 3]
    draft_dummy_destinations = [port_to_ind[x]
                                for x in data["starting_locations"]]

    draft_dummy_cargos = create_draft_dummy_cargos(data["vessel_empty_draft"],
                                                   data["immersion_summer"],
                                                   from_port=draft_dummy_origin,
                                                   starting_locations=draft_dummy_destinations
                                                   )

    # data["draft_dummy_origin"] = draft_dummy_origin
    # data["draft_dummy_destination"] = draft_dummy_destinations

    # cargos = draft_dummy_cargos + original_cargos

    temp = dummify(data["distance_matrix"],
                   draft_dummy_cargos, original_cargos)

    new_dist, dummy_to_ind, volume_demands, weight_demands, pickups_deliveries, time_windows = temp
    n = len(data["distance_matrix"])
    draft_dummy_inds_to_zero_out = range(
        n + 1, n + 2 * len(draft_dummy_cargos), 2)

    draft_demands = deepcopy(weight_demands)

    for ind in draft_dummy_inds_to_zero_out:
        draft_demands[ind] = 0

    print("Distance Matrix size: {}".format(len(new_dist)))

    data["dummy_to_ind"] = dummy_to_ind
    data["pickups_deliveries"] = pickups_deliveries
    data["time_windows"] = time_windows

    data["distance_matrix"] = new_dist
    data["volume_demands"] = volume_demands
    data["weight_demands"] = weight_demands
    data["draft_demands"] = draft_demands

    # data["cost_matrixes"] = [add_dummy_entries_for_draft(
    #     cost_matrix, 0) for cost_matrix in data["cost_matrixes"]]

    data["cost_matrixes"] = [dummify(m, draft_dummy_cargos, original_cargos)[0]
                             for m in data["cost_matrixes"]]

    # data["vessel_speeds"] = [1, 1, 1]
    data["vehicle_starting_time"] = [
        0 for _ in range(len(data["vessel_speeds"]))]

    data["time_matrices"] = [np.array(data["distance_matrix"]) /
                             speed for speed in data["vessel_speeds"]]

    data["port_to_allowed_vehicles"] = []  # [{"port": 3, "vehicles": [1]}]

    draft_data = add_port_draft(cargos_json, port_to_ind)
    data.update(draft_data)

    data["port_max_draft"] = {}

    for k, v in dummy_to_ind.items():
        if k > 0:
            data["port_max_draft"][k] = data["port_max_draft_orig"][v]

    # data["pickups_deliveries"] = [[1, 2], [3, 4]]
    # data["pickups_deliveries"] = [[5, 6], [7, 8]]
    # data["time_windows"] = [{"load_window": (1, 15), "dropoff_window": (2, 18)},
    # {"load_window": (1, 15), "dropoff_window": (11, 24)}]

    # data["load_and_dropoff_times"] = [{
    #     "load": 0, "dropoff": 0}, {"load": 0, "dropoff": 0}, {"load" :0, "dropoff": 0}, {"load": 0, "dropoff": 0}
    #     ]

    # Just mocked for now
    data["load_and_dropoff_times"] = [
        {"load": 0, "dropoff": 0} for _ in range(len(original_cargos) + len(draft_dummy_cargos))]

    assert(len(data["pickups_deliveries"]) ==
           len(data["load_and_dropoff_times"]))

    # data["vehicle_for_cargo"] = [
    #     None for _ in range(len(data["pickups_deliveries"]))]

    # data["vehicle_for_cargo"] = [
    #     None for _ in range(len(data["pickups_deliveries"]))]

    # the first part is needed for draft dummy cargos

    data["vehicle_for_cargo"] = list(range(len(vehicles))) + \
        [None for _ in range(len(original_cargos))]

    assert(len(data["vehicle_for_cargo"]) == len(data["pickups_deliveries"]))

    data['num_vehicles'] = len(data["vessel_speeds"])
    # data['depot'] = 0
    data["starts"] = [0 for _ in range(len(data["vessel_speeds"]))]
    data["ends"] = [0 for _ in range(len(data["vessel_speeds"]))]

    # data["demands_to_pickup"] = [0, 2, -2, 3, -3]
    # data["vehicle_volume_capacities"] = [8, 8, 12]
    # data["vehicle_weight_capacities"] = [8, 8, 12]

    return data
