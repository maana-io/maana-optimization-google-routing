

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from app.utils.routing_solver_utils import get_solution, dedummify
from app.resolvers.optimizer_parameters import parameters as p

from app.logger import logger


class OptimizerMaxProfit:
    def __init__(self,
                 first_solution_strategy,
                 local_search_metaheuristic,
                 time_limit,
                 solution_limit):
        self.set_first_solution_strategy(first_solution_strategy)
        self.set_local_search_metaheuristic(local_search_metaheuristic)
        self.time_limit = time_limit
        self.solution_limit = solution_limit

    def set_first_solution_strategy(self, first_solution_strategy):
        if not first_solution_strategy:
            logger.info("using automatic as first solution strategy")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
        elif first_solution_strategy.lower() == "automatic":
            logger.info("using automatic as first solution strategy")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
        elif first_solution_strategy.lower() == "parallel_cheapest_insertion":
            logger.info(
                "using parallel cheapest insertion as first solution strategy")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
        elif first_solution_strategy.lower() == "path_most_constrained_arc":
            logger.info(
                "using path most constrained arc as first solution strategy")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
        elif first_solution_strategy.lower() == "path_cheapest_arc":
            logger.info("using path cheapest arc as first solution strategy")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        elif first_solution_strategy.lower() == "global_cheapest_arc":
            logger.info(
                "using global cheapest arc as first solution strategy")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC
        elif first_solution_strategy.lower() == "sweep":
            logger.info("using sweep as first solution strategy")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.SWEEP
        elif first_solution_strategy.lower() == "christofides":
            logger.info("using christofides as first solution strategy")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES
        else:
            logger.info(
                f"{first_solution_strategy} is not a valid first solution strategy, defaulting to AUTOMATIC")
            self.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC

    def set_local_search_metaheuristic(self, local_search_metaheuristic):
        if not local_search_metaheuristic:

            self.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT
        elif local_search_metaheuristic.lower() == "greedy_descent":
            logger.info(
                "using local search metaheuristic: greedy descent")
            self.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT
        elif local_search_metaheuristic.lower() == "tabu_search":
            logger.info("using local search metaheuristic: tabu search")
            self.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH
        elif local_search_metaheuristic == "simulated_annealing":
            logger.info(
                "using local search metaheuristic: simulated_annealing")
            self.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING
        else:
            logger.info(
                f"{local_search_metaheuristic} is not a valid local search metaheuristic, defaulting to GREEDY_DESCENT")
            self.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT

    def optimize(self, data, manager, routing):

        def make_time_callbacks(vehicle_ind):
            def time_callback(from_index, to_index):
                """Returns the travel time between the two nodes."""
                # Convert from routing variable Index to time matrix NodeIndex.
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                result = data['time_matrices'][vehicle_ind][from_node][to_node]
                # print(
                # f"time_callback: from_node: {from_node}, to_node: {to_node}, result: {result}")
                return result
            return time_callback

        def make_cost_callback(vehicle_ind):
            def cost_callback(from_index, to_index):
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                result = data["cost_matrixes"][vehicle_ind][from_node][to_node]
                # print(
                # f"cost_callback: from_node: {from_node}, to_node: {to_node}, result: {result}")
                return result
            return cost_callback

        def make_draft_callback(vehicle_ind):
            def draft_callback(to_index, from_index):

                # NON_CARGO_WEIGHT = 2500
                # dwt = 4000  # comes from vessel description
                # immersion_summer = 200000  # comes from vessel description
                # draft = 100  # comes from vessel description

                # if from_index == 0:
                #     # This gets hit multiple times
                #     print(f"hitting from_index_0, {vehicle_ind}")
                #     return data["vessel_empty_draft"][vehicle_ind]

                # if from_index == -1:
                #     print(
                #         f"setting the default draft: {vehicle_ind} to {data['vessel_empty_draft'][vehicle_ind]}")
                #     return data["vessel_empty_draft"][vehicle_ind]

                from_node = manager.IndexToNode(from_index)
                cargo = data["draft_demands"][from_node]
                # dwt = data["dwt"][vehicle_ind]
                immersion_summer = data["immersion_summer"][vehicle_ind]
                # draft = data["draft"][vehicle_ind]

                # cargo_capacity = dwt - NON_CARGO_WEIGHT
                # cargo_capacity_unused = cargo_capacity - cargo_on_board
                centimeter_change_in_draft = cargo / immersion_summer * 0.01

                return centimeter_change_in_draft
            return draft_callback

        def make_draft_callback_2(vehicle_ind):
            def draft_callback(to_index, from_index):

                to_node = manager.IndexToNode(to_index)
                cargo = data["draft_demands"][to_node]
                immersion_summer = data["immersion_summer"][vehicle_ind]
                centimeter_change_in_draft = cargo / immersion_summer * 0.01

                return centimeter_change_in_draft
            return draft_callback

        def volume_demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            # print(f"volume demand: {data['volume_demands'][from_node]}")
            return data['volume_demands'][from_node]

        def weight_demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            # print(f"weight demand: {data['volume_demands'][from_node]}")
            return data['weight_demands'][from_node]

        # def draft_callback(from_index):
        #     from_node = manager.IndexToNode(from_index)
        #     cargo_on_board = data["weight_demands"][from_node]

        #     NON_CARGO_WEIGHT = 2500
        #     dwt = 4000  # comes from vessel description
        #     immersion_summer = 200000  # comes from vessel description
        #     draft = 100  # comes from vessel description

        #     cargo_capacity = dwt - NON_CARGO_WEIGHT
        #     cargo_capacity_unused = cargo_capacity - cargo_on_board
        #     centimeter_reduction_in_draft = cargo_capacity_unused / immersion_summer

        #     calculated_draft = draft - (0.01 * centimeter_reduction_in_draft)

        #     return calculated_draft

        time_callbacks = [make_time_callbacks(
            x) for x in range(data["num_vehicles"])]

        cost_callbacks = [make_cost_callback(x)
                          for x in range(data["num_vehicles"])]

        draft_callbacks = [make_draft_callback(
            x) for x in range(data["num_vehicles"])]

        draft_callbacks_2 = [make_draft_callback_2(
            x) for x in range(data["num_vehicles"])]

        transit_callback_indexes = [
            routing.RegisterTransitCallback(cb) for cb in time_callbacks]

        transit_callback_cost_indexes = [
            routing.RegisterTransitCallback(cb) for cb in cost_callbacks
        ]

        transit_callback_draft_indexes = [
            routing.RegisterTransitCallback(cb) for cb in draft_callbacks
        ]

        transit_callback_draft_2_indexes = [
            routing.RegisterTransitCallback(cb) for cb in draft_callbacks_2
        ]

        for ind, cb_index in enumerate(transit_callback_cost_indexes):
            routing.SetArcCostEvaluatorOfVehicle(cb_index, ind)

        time_for_vehicles = "time_for_vehicles"

        routing.AddDimensionWithVehicleTransits(
            transit_callback_indexes,
            p.time_slack,
            p.time_capacity,
            p.time_fix_cumul_to_zero,
            time_for_vehicles)

        cost_for_vehicles = "cost_for_vehicles"

        routing.AddDimensionWithVehicleTransits(
            transit_callback_cost_indexes,
            p.cost_slack,
            p.cost_capacity,
            p.cost_fix_cumul_to_zero,
            cost_for_vehicles
        )

        time_dimension = routing.GetDimensionOrDie(time_for_vehicles)

        if "draft_demands" in data:

            draft_for_vehicles = "draft_for_vehicles"
            routing.AddDimensionWithVehicleTransits(
                transit_callback_draft_indexes,
                p.draft_slack,
                p.draft_capacity,  # sets max draft any vessel can have
                p.draft_fix_cumul_to_zero,
                draft_for_vehicles
            )

            draft_for_vehicles_2 = "draft_for_vehicles_2"

            routing.AddDimensionWithVehicleTransits(
                transit_callback_draft_2_indexes,
                p.draft_slack,
                p.draft_capacity,  # sets max draft any vessel can have
                p.draft_fix_cumul_to_zero,
                draft_for_vehicles_2
            )

            draft_dimension = routing.GetDimensionOrDie(draft_for_vehicles)
            draft_dimension_2 = routing.GetDimensionOrDie(draft_for_vehicles_2)

        # Add capacity restraints
        volume_demand_callback_index = routing.RegisterUnaryTransitCallback(
            volume_demand_callback)

        routing.AddDimensionWithVehicleCapacity(
            volume_demand_callback_index,
            p.volume_slack,  # null capacity slack
            data['vehicle_volume_capacities'],  # vehicle maximum capacities
            p.volume_fix_cumul_to_zero,  # start cumul to zero
            "volume")

        weight_demand_callback_index = routing.RegisterUnaryTransitCallback(
            weight_demand_callback)

        routing.AddDimensionWithVehicleCapacity(
            weight_demand_callback_index,
            p.weight_slack,  # null capacity slack
            data['vehicle_weight_capacities'],  # vehicle maximum capacities
            p.weight_fix_cumul_to_zero,  # start cumul to zero
            "weight")

        weight_dimension = routing.GetDimensionOrDie("weight")

        for pickups_deliveries, vehicle_for_cargo in zip(data['pickups_deliveries'], data["vehicle_for_cargo"]):
            pickup, dropoff = pickups_deliveries

            pickup = manager.NodeToIndex(pickup)
            dropoff = manager.NodeToIndex(dropoff)

            routing.AddPickupAndDelivery(pickup, dropoff)
            if vehicle_for_cargo is not None:
                routing.solver().Add(routing.VehicleVar(pickup) == vehicle_for_cargo)
                routing.solver().Add(routing.VehicleVar(pickup) ==
                                     routing.VehicleVar(dropoff))
            else:
                routing.solver().Add(routing.VehicleVar(pickup) ==
                                     routing.VehicleVar(dropoff))
            routing.solver().Add(time_dimension.CumulVar(pickup)
                                 <= time_dimension.CumulVar(dropoff))

            if "draft_demands" in data:
                draft_dimension.CumulVar(pickup).SetMax(
                    data["port_max_draft"][pickup])
                draft_dimension_2.CumulVar(dropoff).SetMax(
                    data["port_max_draft"][dropoff])

        # add constraints on pickup and dropoff locations
        for pickup_dropoff, time_window, load_and_dropoff_times in zip(data["pickups_deliveries"], data["time_windows"], data["load_and_dropoff_times"]):
            pickup = pickup_dropoff[0]
            dropoff = pickup_dropoff[1]
            load_time = load_and_dropoff_times["load"]
            dropoff_time = load_and_dropoff_times["dropoff"]

            start_load, end_load = time_window["load_window"]
            start_dropoff, end_dropoff = time_window["dropoff_window"]

            # I think this does what it is supposed to do, but it is also slow
            # routing.solver().Add(time_dimension.CumulVar(pickup) >= (start_load + load_time))
            # routing.solver().Add(time_dimension.CumulVar(pickup) < end_load)

            # routing.solver().Add(time_dimension.CumulVar(dropoff) >= start_dropoff)
            # routing.solver().Add(time_dimension.CumulVar(
            #     dropoff) < (end_dropoff - dropoff_time))

            time_dimension.CumulVar(pickup).SetRange(
                start_load + load_time, end_load)
            time_dimension.CumulVar(dropoff).SetRange(
                start_dropoff, end_dropoff - dropoff_time)

        # This allows for incomplete solutuon,
        # for node in range(1, len(data['distance_matrix'])):
        #     routing.AddDisjunction(
        #         [manager.NodeToIndex(node)], p.punishment_for_missing_cargo)

        print("cargo_to_revenue: {}".format(data["cargo_to_revenue"]))
        print("dummy_to_ind: {}".format(data["dummy_to_ind"]))

        from collections import defaultdict

        d = defaultdict(list)

        for dummy, ind in data["dummy_to_ind"].items():
            d[ind].append(dummy)

        print(f"ind_to_dummys: {d}")

        # for cargo, revenue in data["cargo_to_revenue"]:
        #     origin, destination = cargo
        #     for dummy_ind in d[destination]:
        #         routing.AddDisjunction(
        #             [manager.NodeToIndex(dummy_ind)], revenue
        #         )

        #     for dummy_ind in d[origin]:
        #         routing.AddDisjunction(
        #             [manager.NodeToIndex(dummy_ind)], 0
        #         )

        for origin, destination, revenue in data["actual_pickup_deliveries"]:

            routing.AddDisjunction(
                [manager.NodeToIndex(destination)], int(revenue)
            )

            routing.AddDisjunction(
                [manager.NodeToIndex(origin)], 0
            )

            # Just testing minStart and minEnd

            # It looks like it is working

            # vehicle_index = routing.Start(0)
            # time_dimension.CumulVar(vehicle_index).SetRange(0, 20)
            # routing.AddToAssignment(time_dimension.SlackVar(vehicle_index))

            # end testing minStart and min End

        for pv in data["port_to_allowed_vehicles"]:
            index = manager.NodeToIndex(pv["port"])
            routing.VehicleVar(index).SetValues([-1] + pv["vehicles"])

        # for ind, start_time in enumerate(data["vehicle_starting_time"]):
        #     index = routing.Start(ind)
        #     time_dimension.CumulVar(index).SetRange(start_time, start_time)
        #     routing.AddToAssignment(time_dimension.SlackVar(index))

        for i in range(data['num_vehicles']):
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.Start(i)))
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.End(i)))

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        # PARALLEL_CHEAPEST_INSERTION is faster, but not finding the solution...

        search_parameters.first_solution_strategy = (
            self.first_solution_strategy
        )
        search_parameters.time_limit.seconds = self.time_limit
        # we can set a limit, but it won't guarantee to find a solution!
        # if time expires before we find first solution
        # we get nothing back
        search_parameters.solution_limit = self.solution_limit

        search_parameters.local_search_metaheuristic = (
            self.local_search_metaheuristic
        )

        search_parameters.log_search = True

        assignment = routing.SolveWithParameters(search_parameters)

        status_map = {0: "ROUTING_NOT_SOLVED",
                      1: "ROUTING_SUCCESS",
                      2: "ROUTING_FAIL",
                      3: "ROUTING_FAIL_TIMEOUT",
                      4: "ROUTING_INVALID",
                      }

        status = routing.status()

        if assignment:
            solution = get_solution(data, manager, routing, assignment)
            d_solution = dedummify(solution,
                                   data["dummy_to_ind"],
                                   data["ind_to_port"],
                                   data["starting_locations"]
                                   )
            d_solution["status"] = status_map[status]

            return {"solution": solution, "d_solution": d_solution}
        else:
            logger.warn(f"solver did not succeed status: {status}")

            none_solution = {'vehicleSchedules': None,
                             'id': "none-solution",
                             'totalTime': None,
                             'totalVolume': None,
                             'totalCost': None,
                             'totalProfit': None,
                             'notDeliveredRequirementIds': None,
                             'notUsedVehicleIds': None,
                             'timeWindow': None,
                             'status': status_map[status]
                             }

            return {"d_solution": none_solution}
