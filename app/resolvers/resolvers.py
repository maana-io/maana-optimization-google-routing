

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

from app.resolvers.optimizer import Optimizer

# Assignment Resolver


def resolve_solverAssignmentWithSizes(*_, costs, constraints, objective):
    id = "Assignment With CP-SAT"

    # Create model
    model = cp_model.CpModel()
    # Get the number of workers
    num_workers = len(costs["row"])
    # Get the number of tasks
    num_tasks = len(costs["row"][0]["values"])

    # Create the variables

    x = []
    for i in range(num_workers):
        t = []
        for j in range(num_tasks):
            t.append(model.NewIntVar(0, 1, "x[%i,%i]" % (i, j)))
        x.append(t)

    # Constraints
    for constraint in constraints:
        if(constraint["nodeSet"]):
            # this is a constraint about workers
            [model.Add(sum(x[i][j] for i in range(num_workers)) >=
                       constraint["lowerBound"]) for j in range(num_tasks)]
        else:
            #       #this is a constraint about task
            [model.Add(sum(constraint["vectorOfCoefficients"]["value"][j]["value"] * x[i][j]
                           for j in range(num_tasks)) <= constraint["upperBound"]) for i in range(num_workers)]

    # # Create the objective function
    if objective["minimize"]:
        model.Minimize(sum([costs["row"][i]["values"][j] * x[i][j] for i in range(num_workers)
                            for j in range(num_tasks)]))

      # Run the solver and return results

        # declare solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

# if status != cp_model.OPTIMAL:
#      print(status)
# else:
    status = "OPTIMAL"

    nodeSetA = []
    nodeSetB = []
    cost = []

    for i in range(num_workers):
        for j in range(num_tasks):
            if solver.Value(x[i][j]) == 1:
                nodeSetA.append(i)
                nodeSetB.append(j)
                cost.append(costs["row"][i]["values"][j])

    return {
        "id": id,
        "nodeSetA": nodeSetA,
        "nodeSetB": nodeSetB,
        "cost": cost,
        "objectiveValue": solver.ObjectiveValue(),
        "status": status
    }


def resolve_solverAssignmentWithSizes_mapper(query):
    query.set_field("solverAssignmentWithSizes",
                    resolve_solverAssignmentWithSizes)


def resolve_solveRealLinearProblem(*_, vars, constraints, objective):

    id = 'GLOP_LINEAR_PROGRAMMING'

    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver(id,
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Create variables
    varDict = {}
    for var in vars:
        varDict[var["id"]] = solver.NumVar(
            var["lowerBound"],
            var["upperBound"],
            var["id"])

    # Create constraints
    for constraint in constraints:
        ct = solver.Constraint(
            constraint["lowerBound"],
            constraint["upperBound"],
            constraint["id"])
        for coef in constraint["coefficients"]:
            ct.SetCoefficient(varDict[coef["id"]], coef["value"])

    # Create the objective function
    obj = solver.Objective()
    for coef in objective["coefficients"]:
        obj.SetCoefficient(varDict[coef["id"]], coef["value"])
    if objective["maximize"]:
        obj.SetMaximization()

    solver.Solve()

    varValues = []
    for key, item in varDict.items():
        varValues.append({"id": key, "value": item.solution_value()})

    return {
        "id": id,
        "objectiveValue": obj.Value(),
        "varValues": varValues
    }


def resolve_solveRealLinearProblem_mapper(query):
    query.set_field("solveRealLinearProblem",
                    resolve_solveRealLinearProblem)


def resolve_solveLinearCPProblem(*_, vars, constraints, objective):
    id = 'CP_SAT_SOLVER'

    # Create the model
    model = cp_model.CpModel()

    # Create variables
    varDict = {}
    for var in vars:
        varDict[var["id"]] = model.NewIntVar(
            var["lowerBound"],
            var["upperBound"],
            var["id"])

    # Create Constraints
    # model.Add(var1*coeff1 + var2*coeff2 <= upperBound)

    for constraint in constraints:
        model.Add(sum((varDict[coef["id"]] * coef["value"]
                       for coef in constraint["coefficients"])) <= constraint["upperBound"])

    # Create Objective

    if(objective["maximize"]):
        model.Maximize(sum((varDict[coef["id"]] * coef["value"]
                            for coef in objective["coefficients"])))

    # Run Solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        status = "OPTIMAL"
        varValues = []
        for key, item in varDict.items():
            varValues.append({"id": key, "value": solver.Value(item)})

        return {
            "id": id,
            "status": status,
            "objectiveValue": solver.ObjectiveValue(),
            "varValues": varValues
        }


def resolve_solveLinearCPProblem_mapper(query):
    query.set_field("solveLinearCPProblem",
                    resolve_solveLinearCPProblem)


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

    data = create_data(vehicles, requirements, costMatrix, distanceMatrix)

    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']
            ), data['num_vehicles'], data["starts"], data["ends"])

    optimizer = Optimizer(objective["firstSolutionStrategy"]["id"])

    raw_solution = optimizer.optimize(data, manager, routing)

    # fix raw_solution, and return prettified solution
