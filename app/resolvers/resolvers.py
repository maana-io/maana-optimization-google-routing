

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

from app.resolvers.optimizer import Optimizer
from app.resolvers.create_data import create_data_model


def resolve_pickups_and_deliveries(*_, cost, constraints, objectives):

    from app.utils.utils import get_solution

    distances = []
    for ele in cost["distanceMatrix"]:
        distances.append(ele["values"])

    pickups_deliveries = []
    for ele in constraints["pickupsDeliveries"]:
        pickups_deliveries.append((ele["origin"], ele["destination"]))

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(distances),
                                           constraints['numVehicles'], constraints['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc.

    def distance_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distances[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Define Transportation Requests.
    for request in pickups_deliveries:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(
                delivery_index))
        routing.solver().Add(
            distance_dimension.CumulVar(pickup_index) <=
            distance_dimension.CumulVar(delivery_index))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        schedule = get_solution(
            constraints["numVehicles"], manager, routing, assignment)
        return schedule
    else:
        print("Could not compute schedule")


def resolve_pickups_and_deliveries_mapper(query):
    query.set_field("solverMakeSchedules", resolve_pickups_and_deliveries)


def resolve_routing_solver(*_, vehicles, requirements, costMatrix, distanceMatrix, objective):

    data = create_data_model(vehicles, requirements,
                             costMatrix, distanceMatrix)

    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']
            ), data['num_vehicles'], data["starts"], data["ends"])

    optimizer = Optimizer(objective["firstSolutionStrategy"]["id"],
                          objective["localSearchStrategy"]["id"],
                          objective["solutionLimit"]
                          )

    routing = pywrapcp.RoutingModel(manager)

    raw_solution = optimizer.optimize(data, manager, routing)

    print("all solution")
    print(f"raw_solution: {raw_solution}")
    print("dedummyfied solution")
    temp = raw_solution["d_solution"]
    print(f"dedummyfied solution: {temp}")

    return raw_solution["d_solution"]


def resolve_routing_solver_mapper(query):
    query.set_field("routingSolverMakeSchedules", resolve_routing_solver)
