
def get_solution(num_vehicles, manager, routing, assignment):
    """Prints assignment on console."""
    total_distance = 0
    schedule = []
    for vehicle_id in range(num_vehicles):
        entry = {"id": vehicle_id, "nodesToVisit": []}
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            plan_output += ' {} -> '.format(node)
            entry["nodesToVisit"].append(node)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        node = manager.IndexToNode(index)
        plan_output += '{}\n'.format(node)
        entry["nodesToVisit"].append(node)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_distance += route_distance
        schedule.append(entry)
    print('Total Distance of all routes: {}m'.format(total_distance))

    formatted_schedule = {"id": "schedule", "vesselSchedules": schedule}

    return formatted_schedule
