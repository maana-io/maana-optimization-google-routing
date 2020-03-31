## Optimizer Architecture

OR Tools VRP solver requires input to be in specific format, and therefore we need to convert the data we receive to the format that VRP solver uses. We have three modules that are handling it: `app/resolvers/create_data.py` , `app/resolvers/create_data_with_br.py`, `app/resolvers/create_data_with_br_max_profit.py`. These modules are very similar and only exist because the behavior differs slightly for the needs of the three resolvers that we have.

Speaking of resolvers, we have three resolvers:

`resolve_routing_solver` Finds the solution ignoring business rules and optimizing number of cargo delivered. For the same number of cargo delivered, it will minimize cost. For example if we deliver all the cargo, it will find (attempt to find) a solution with minimum cost. This was the first resolver we started with. The corresponding graphql query is `routingSolverMakeSchedules`.

`resolve_routing_solver_with_br` Same as above except this one uses business rules. The corresponding graphql query is `routingSolverMakeSchedulesWithBR`

`resolve_routing_solver_with_br_max_profit` Uses business rules, and optimizes on revenue. For example, even if it could deliver all the cargo, if it saw a solution that yielded a better profit without delivering all cargo, it would choose the solution that delivered higher profit. The corresponding graphql query is `routingSolverMakeSchedulesWithBRMaxProfit`.

The resolvers live in `app/resolvers/resolvers.py`

## OR Tools VRP Solver logic

Before telling the optimizer to optimize, we need to tell it what exactly it is optimizing for and what constraints it has.

Constraints:

1) Pickup has to happen before delivery.
2) Pickup and delivery have to happen withing given time window.
3) Pickup and delivery have to happen by the same vehicle.
4) Vehicle volume capacity cannot go above certain limit.
5) Vehicle weight capacity cannot go above certain limit.
6) Some ports cannot allow vehicles with draft above certain number; therefore, we keep track of vehicle draft.
7) Ports have a list of vehicles that can visit them (business rules)
8) Each vehicle has a specified starting location.


The optimizer is technically minimizing cost in all three above mentioned resolvers. However, in `resolve_routing_solver` and `resolve_routing_solver_with_br`, the punishment for missing cargo is very large, and therefore tries to deliver as many cargos as it can, while for `resolve_routing_solver_with_br_max_profit` the punishment is set exactly to revenue that cargo would bring, thus the profit is being maximized.


The solver lives in `app/resolvers/optimizer.py`.

To test the vrp solver you can use example query, from: `app/sample_queries/latest_known_working_query.txt`






