from typing import List, Tuple
from copy import deepcopy

from current_data_types import Cargo


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

    for vehicle_id, vehicle in new_schedule["vehicles"].items():
        new_schedule["vehicles"][vehicle_id]["vehicle_path"] = dedummify_vehicle_path(
            vehicle["vehicle_path"], dummy_to_ind)

    return new_schedule


def dedummify_vehicle_path(vehicle_path, dummy_to_ind):

    d_vehicle_path = []

    for path in vehicle_path:

        orig_node = dummy_to_ind[path["Node"]]
        new_path = deepcopy(path)
        new_path["Node"] = orig_node
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
    solution["vehicles"] = {}

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

                step = {"Node": manager.IndexToNode(index),
                        "min_time": assignment.Min(time_var),
                        "max_time": assignment.Max(time_var),
                        "cost": assignment.Min(cost_var),
                        "draft": assignment.Min(draft_var),
                        "volume": route_volume,
                        "cargo_index": cargo_index,
                        "action": action,
                        }

            else:

                step = {"Node": manager.IndexToNode(index),
                        "min_time": assignment.Min(time_var),
                        "max_time": assignment.Max(time_var),
                        "cost": assignment.Min(cost_var),
                        "volume": route_volume,
                        "cargo_index": cargo_index,
                        "action": action,
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

        step = {"Node": manager.IndexToNode(index),
                "min_time": assignment.Min(time_var),
                "max_time": assignment.Max(time_var),
                "cost": assignment.Min(cost_var),
                "volume": route_volume,
                "weight": route_weight,
                "cargo_index": cargo_index,
                "action": action,
                }

        vehicle_path.append(step)

        plan_output += 'Time of the route: {}\n'.format(
            assignment.Min(time_var),
            route_volume)

        plan_output += 'Load of the route: {}\n'.format(route_volume)
        plan_output += 'Cost of the route: {}\n'.format(
            assignment.Min(cost_var))

        vehicle_schedule = {
            "vehicle_path": vehicle_path,
            "time_of_route": assignment.Min(time_var),
            "route_load": route_volume,
            "cost_of_route": assignment.Min(cost_var)
        }

        print(plan_output)
        total_time += assignment.Min(time_var)
        total_volume += route_volume
        total_cost += assignment.Min(cost_var)

        solution["vehicles"][vehicle_id] = vehicle_schedule

    print('Total time of all routes: {}min'.format(total_time))
    print('Total Volume of all routes: {}'.format(total_volume))
    print('Total cost of all routes: {}'.format(total_cost))

    solution["total_time"] = total_time
    solution["total_volume"] = total_volume
    solution["total_cost"] = total_cost

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

    return cargo
