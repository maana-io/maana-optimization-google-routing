

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

from app.resolvers.optimizer import Optimizer
from app.resolvers.random_optimizer import random_optimizer_wrapper
from app.resolvers.create_data import create_data_model
from app.utils.helpers import save_data_to_file

# import logging
# from logging.config import fileConfig
# fileConfig("../log_config.ini")

from app.logger import logger


# logger = logging.getLogger("optimizer")
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# fh = logging.FileHandler('log_file_test.log')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)

# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# ch.setFormatter(formatter)

# logger.addHandler(fh)
# logger.addHandler(ch)


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
        logging.info("Could not compute schedule")


def resolve_pickups_and_deliveries_mapper(query):
    query.set_field("solverMakeSchedules", resolve_pickups_and_deliveries)


def resolve_routing_solver(*_, vehicles, requirements, costMatrix, distanceMatrix, objective, routingTimeWindow):

    save_data_to_file(vehicles, "vehicles")
    save_data_to_file(requirements, "requirements")
    save_data_to_file(costMatrix, "cost_matrix")
    save_data_to_file(distanceMatrix, "distanceMatrix")
    save_data_to_file(objective, "objective")

    report = {"n_vehicles": len(vehicles),
              "n_requirements": len(requirements)
              }

    save_data_to_file(report, "report")

    data = create_data_model(vehicles, requirements,
                             costMatrix, distanceMatrix, routingTimeWindow)

    if "randomOptimizer" in objective["firstSolutionStrategy"]["id"]:
        n_iterations = int(
            objective["firstSolutionStrategy"]["id"].split("_")[1])
        logger.info(f"using random optimizer")
        solution = random_optimizer_wrapper(
            requirements, vehicles, costMatrix, distanceMatrix, n_iterations)

    else:

        manager = pywrapcp.RoutingIndexManager(
            len(data['distance_matrix']
                ), data['num_vehicles'], data["starts"], data["ends"])

        optimizer = Optimizer(objective["firstSolutionStrategy"]["id"],
                              objective["localSearchStrategy"]["id"],
                              objective["timeLimit"],
                              objective["solutionLimit"]
                              )

        routing = pywrapcp.RoutingModel(manager)

        raw_solution = optimizer.optimize(data, manager, routing)

        save_data_to_file(raw_solution["d_solution"], "solution")

        return raw_solution["d_solution"]


def resolve_routing_solver_mapper(query):
    query.set_field("routingSolverMakeSchedules", resolve_routing_solver)
