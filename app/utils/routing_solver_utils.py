from typing import List, Tuple
from copy import deepcopy

import random as rn


class Cargo:
    def __init__(self, origin=None,
                 dest=None,
                 volume=None,
                 weight=None,
                 laycanFrom=None,
                 laycanTo=None,
                 dischargeDateFrom=None,
                 dischargeDateTo=None):
        self.origin = origin
        self.destination = dest
        self.volume = volume
        self.weight = weight
        self.laycanFrom = laycanFrom
        self.laycanTo = laycanTo
        self.dischargeDateFrom = dischargeDateFrom
        self.dischargeDateTo = dischargeDateTo


def buildDistanceMatrix(raw_distances, ports):
    # id: ID!
    # start: PortAsInput!
    # end: PortAsInput!
    # distance: Float!

    distance_matrix = [[0 for _ in range(len(ports) + 1)]
                       for _ in range(len(ports) + 1)]

    id_to_ind = {port.id: port.index for port in ports}

    for raw_distance in raw_distances:
        begin_port_id = raw_distance['start']['id']  # required
        end_port_id = raw_distance['end']['id']  # required
        distance = raw_distance['distance']  # required

        distance_matrix[id_to_ind[begin_port_id]
                        ][id_to_ind[end_port_id]] = distance

    return distance_matrix


def add_dummy_entry(data: List[List[int]], n: int) -> (List[List[int]], int):
    """
    Args:
        data: is square matrix usually of distances and costs
        n: is the index we are creating a dummy entry too
           for example if we create dummy entry to n=1, then
           another row will be added that has distance 0 to row 1
           and large distance (big_val) to other rows

    Output:
        (new square matrix, index of row that was inserted)
    """

    new_data = []
    for row in data:
        new_row = row + [row[n]]
        new_data.append(new_row)

    new_data.append(new_data[n])
    return new_data, len(new_data) - 1


def dummify(matrix, cargos):
    dummy_to_ind = {x: x for x in range(len(matrix))}
    volume_demands = {x: 0 for x in range(len(matrix))}
    weight_demands = {x: 0 for x in range(len(matrix))}
    pickup_deliveries = []
    time_windows = []

    # matrix, new_ind_origin = add_dummy_entry(matrix, 0)
    # matrix, new_ind_origin = add_dummy_entry(matrix, 0)

    for cargo in cargos:

        matrix, new_ind_origin = add_dummy_entry(matrix, cargo.origin)
        dummy_to_ind[new_ind_origin] = cargo.origin
        volume_demands[new_ind_origin] = cargo.volume
        weight_demands[new_ind_origin] = cargo.weight
        matrix, new_ind_dest = add_dummy_entry(matrix, cargo.destination)
        dummy_to_ind[new_ind_dest] = cargo.destination
        volume_demands[new_ind_dest] = -cargo.volume
        weight_demands[new_ind_dest] = -cargo.weight

        pickup_deliveries.append((new_ind_origin, new_ind_dest))
        time_windows.append(
            {"load_window": (cargo.laycanFrom, cargo.laycanTo),
             "dropoff_window": (cargo.dischargeDateFrom, cargo.dischargeDateTo)})

    # matrix, new_ind_origin = add_dummy_entry(matrix, 0)
    # matrix, new_ind_origin = add_dummy_entry(matrix, 0)

    return matrix, dummy_to_ind, volume_demands, weight_demands, pickup_deliveries, time_windows


def dedummify(schedule, dummy_to_ind):

    new_schedule = deepcopy(schedule)

    for vehicle_id, vehicle in enumerate(new_schedule["vehicleSchedules"]):
        new_schedule["vehicleSchedules"][vehicle_id]["vehiclePath"]["step"] = dedummify_vehicle_path(
            vehicle["vehiclePath"]["step"], dummy_to_ind)

    return new_schedule


def dedummify_vehicle_path(vehicle_path, dummy_to_ind):

    d_vehicle_path = []

    for path in vehicle_path:

        orig_node = dummy_to_ind[path["routeNodeId"]]
        new_path = deepcopy(path)
        new_path["routeNodeId"] = orig_node
        d_vehicle_path.append(new_path)

    return d_vehicle_path


def add_dummy_entries_for_draft(matrix, cost):

    new_data = []
    for ind, row in enumerate(matrix):
        if ind == 0:
            new_data.append(row + [0, 0])
        else:
            new_data.append(row + [cost, 0])

    next_row = [cost for _ in range(len(matrix) + 2)]
    next_row[0] = 0
    next_row[-1] = 0
    next_row[-2] = 0

    new_data.append(next_row)
    last_row = [0 for _ in range(len(matrix) + 2)]
    new_data.append(last_row)

    return new_data


def get_solution(data, manager, routing, assignment):

    solution = {}
    solution["vehicleSchedules"] = []

    time_dimension = routing.GetDimensionOrDie('time_for_vehicles')
    cost_dimension = routing.GetDimensionOrDie("cost_for_vehicles")
    if "draft_demands" in data:
        draft_dimension = routing.GetDimensionOrDie("draft_for_vehicles")
    total_time = 0
    total_volume = 0
    total_weight = 0
    total_cost = 0
    for vehicle_id in range(data['num_vehicles']):

        vehicle_path = []

        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_volume = 0
        route_weight = 0
        while not routing.IsEnd(index):

            node_index = manager.IndexToNode(index)

            print(f"Vehicle id: {vehicle_id}, node_index: {node_index}")

            time_var = time_dimension.CumulVar(index)
            cost_var = cost_dimension.CumulVar(index)

            if "draft_demands" in data:
                draft_var = draft_dimension.CumulVar(index)

            route_volume += data['volume_demands'][node_index]
            route_weight += data["weight_demands"][node_index]

            cargo_index = None
            action = None
            if node_index >= len(data["orig_distance_matrix"]):
                cargo_index = (
                    node_index - len(data["orig_distance_matrix"])) // 2
                if (node_index - len(data["orig_distance_matrix"])) % 2 == 0:
                    action = "pickup"
                else:
                    action = "dropoff"

            if "draft_demands" in data:

                plan_output += '\033[32mNode {0}\033[0m Time({1},{2}) Volume({3}) Weight({4}) Draft({5}) Cost({6}) -> '.format(
                    manager.IndexToNode(index),
                    assignment.Min(time_var),
                    assignment.Max(time_var),
                    route_volume,
                    route_weight,
                    assignment.Min(draft_var),
                    assignment.Min(cost_var)
                )

            else:

                plan_output += '\033[32mNode {0}\033[0m Time({1},{2}) Volume({3}) Weight({4}) Cost({5})-> '.format(
                    manager.IndexToNode(index),
                    assignment.Min(time_var),
                    assignment.Max(time_var),
                    route_volume,
                    route_weight,
                    assignment.Min(cost_var),
                )

            if "draft_demands" in data:

                step = {
                    "id": str(rn.randint(1, 10000000)),
                    "routeNodeId": manager.IndexToNode(index),
                    "minTime": assignment.Min(time_var),
                    "maxTime": assignment.Max(time_var),
                    "cost": assignment.Min(cost_var),
                    "draft": assignment.Min(draft_var),
                    "volume": route_volume,
                    "requirementIndex": cargo_index,
                    "action": {"id": "1", "action": {"value": action}},
                }

            else:

                step = {
                    "id": str(rn.randint(1, 10000000)),
                    "routeNodeId": manager.IndexToNode(index),
                    "minTime": assignment.Min(time_var),
                    "maxTime": assignment.Max(time_var),
                    "cost": assignment.Min(cost_var),
                    "volume": route_volume,
                    "requirementIndex": cargo_index,
                    "action": {"id": "1", "action": {"value": action}},
                }

            vehicle_path.append(step)

            index = assignment.Value(routing.NextVar(index))

        time_var = time_dimension.CumulVar(index)

        if "draft_demands" in data:
            plan_output += '\033[32mNode {0}\033[0m Time({1},{2}) Volume({3}) Weight({4}) Draft({5}) Cost({6})\n'.format(
                manager.IndexToNode(index),
                assignment.Min(time_var),
                assignment.Max(time_var),
                route_volume,
                route_weight,
                assignment.Min(draft_var),
                assignment.Min(cost_var)
            )
        else:
            plan_output += '\033[32mNode {0}\033[0m Time({1},{2}) Volume({3}) Weight({4}) Cost({5})-> '.format(
                manager.IndexToNode(index),
                assignment.Min(time_var),
                assignment.Max(time_var),
                route_volume,
                route_weight,
                assignment.Min(cost_var),
            )

        step = {
            "id": str(rn.randint(1, 10000000)),
            "routeNodeId": manager.IndexToNode(index),
            "minTime": assignment.Min(time_var),
            "maxTime": assignment.Max(time_var),
            "cost": assignment.Min(cost_var),
            "volume": route_volume,
            "weight": route_weight,
            "requirementIndex": cargo_index,
            "action": {"id": "1", "action": {"value": action}},
        }

        vehicle_path.append(step)

        plan_output += 'Time of the route: {}\n'.format(
            assignment.Min(time_var),
            route_volume)

        plan_output += 'Load of the route: {}\n'.format(route_volume)
        plan_output += 'Cost of the route: {}\n'.format(
            assignment.Min(cost_var))

        vehicle_schedule = {
            "id": str(rn.randint(1, 10000000)),
            "vehiclePath": {"id": str(rn.randint(1, 10000000)), "step": vehicle_path},
            "timeOfRoute": assignment.Min(time_var),
            "routeLoad": route_volume,
            "costOfRoute": assignment.Min(cost_var)
        }

        print(plan_output)
        total_time += assignment.Min(time_var)
        total_volume += route_volume
        total_cost += assignment.Min(cost_var)
        

        solution["vehicleSchedules"].append(vehicle_schedule)

    print('Total time of all routes: {}min'.format(total_time))
    print('Total Volume of all routes: {}'.format(total_volume))
    print('Total cost of all routes: {}'.format(total_cost))

    solution["id"] = str(rn.randint(1, 10000000))
    solution["totalTime"] = total_time
    solution["totalVolume"] = total_volume
    solution["totalCost"] = total_cost
    solution["totalProfit"] = data["total_revenue"] - total_cost

    return solution


def create_draft_dummy_cargos(vessel_empty_draft, vessel_immersion_summer, from_port, to_port):

    cargos = []
    for draft, immersion_summer in zip(vessel_empty_draft, vessel_immersion_summer):

        weight_representing_draft = draft * immersion_summer

        # I want to set weight to 0, but it makes the problem unsolvable, (1 does the same thing)
        cargos.append(
            Cargo(origin=from_port, dest=to_port, volume=0, weight=weight_representing_draft, laycanFrom=0,
                  laycanTo=0, dischargeDateFrom=0, dischargeDateTo=0)
        )

    return cargos


# def reformat_solution(d_solution):

#     solution = {}

#     solution["totalVolume"] = d["total_volume"]
#     solution["totalCost"] = d["total_cost"]
#     solution["totalTime"] = d["total_time"]

#     vehicle_paths = []
#     for vehicle in solution["vehicles"]:
#         vehicle_path = {}
#         vehicle_path["timeOfRoute"] = vehicle["time_of_route"]
#         vehicle_path["routeLoad"] = vehicle["route_load"]
#         vehicle_path["costOfRoute"] = vehicle["cost_of_route"]
#         vehicle_path["vehiclePath"] = vehicle["vehicle_path"]

#     solution["vehicleSchedules"] = None
