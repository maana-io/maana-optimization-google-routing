# from app.resolvers.optimizer_types import Cargo


import random as rn
from copy import deepcopy

import logging


class Cargo:
    def __init__(self,
                 id=id,
                 origin=None,
                 dest=None,
                 volume=None,
                 weight=None,
                 laycanFrom=None,
                 laycanTo=None,
                 dischargeDateFrom=None,
                 dischargeDateTo=None,
                 revenue=0,
                 #  allowed_vehicles=[]
                 ):
        self.id = id
        self.origin = origin
        self.destination = dest
        self.volume = volume
        self.weight = weight
        self.laycanFrom = laycanFrom
        self.laycanTo = laycanTo
        self.dischargeDateFrom = dischargeDateFrom
        self.dischargeDateTo = dischargeDateTo
        self.revenue = revenue
        # self.allowed_vehicles = allowed_vehicles


class RandomOptimizer:
    def __init__(self, vehicles, cargos, port_to_max_draft, port_to_ind, n_iterations):
        self.vehicles = vehicles
        self.cargos = cargos
        self.port_to_max_draft = port_to_max_draft
        self.port_to_ind = port_to_ind
        self.n_iterations = n_iterations
        self.cargo_id_to_cargo = {c.id: c for c in self.cargos}
        self.vehicle_id_to_vehicle = {v.id: v for v in self.vehicles}

    def one_run(self):

        cargos_taken = set()
        vehicle_id_to_steps = {v_id: [] for v_id in self.vehicle_id_to_vehicle}
        active_vehicle_ids = list(self.vehicle_id_to_vehicle)
        vehicle_id_to_vehicle_copy = deepcopy(self.vehicle_id_to_vehicle)

        while active_vehicle_ids:

            vehicle_id = rn.choice(active_vehicle_ids)
            vehicle = vehicle_id_to_vehicle_copy[vehicle_id]

            possible_steps = vehicle.calc_possible_steps(
                self.cargos, cargos_taken, self.port_to_max_draft)
            if not possible_steps:
                active_vehicle_ids.remove(vehicle_id)
                continue
            step = vehicle.choose_step(possible_steps)
            vehicle_id_to_steps[vehicle_id].append(step)

            cargo_id = vehicle.take_step(step, self.cargo_id_to_cargo)
            if cargo_id:
                cargos_taken.add(cargo_id)

        return vehicle_id_to_steps

    def score_run(self, all_runs):
        scored_runs = []
        for vehicle_to_steps in all_runs:
            n_deliveries = 0
            for vehicle_id, steps in vehicle_to_steps.items():
                for step in steps:
                    cargo_id, action, travel_time = step
                    if action == "dropoff":
                        n_deliveries += 1
                        cargo = self.cargo_id_to_cargo[cargo_id]
                        vehicle = self.vehicle_id_to_vehicle[vehicle_id]
                        logging.info(f"cost_matrix: {vehicle.cost_matrix}")
                        cost = vehicle.cost_matrix[self.port_to_ind[cargo.origin]
                                                   ][self.port_to_ind[cargo.destination]]
                        logging.info(f"cost: {cost}")
                        logging.info(f"cargo.revenue: {cargo.revenue}")
                        profit = cargo.revenue - cost

            scored_runs.append((vehicle_to_steps, n_deliveries, cost, profit))

        sorted_scored_runs = sorted(
            scored_runs, key=lambda x: (x[1], x[3]), reverse=True)

        return sorted_scored_runs

    def solve(self):

        all_runs = []

        for i in range(self.n_iterations):
            run_result = self.one_run()
            all_runs.append(run_result)

        sorted_scored_run = self.score_run(all_runs)

        return sorted_scored_run


class Vehicle:
    def __init__(
        self,
        id,
        speed,
        weight_capacity,
        volume_capacity,
        draft_capacity,
        current_weight,
        current_volume,
        current_draft,
        distance_matrix,
        cost_matrix,
        current_location,
        current_time,
        port_to_ind,
        immersion_summer=None,
        cargo_on_board={},
        deliveries=[]
    ):
        self.id = id
        self.speed = speed
        self.weight_capacity = weight_capacity
        self.volume_capacity = volume_capacity
        self.draft_capacity = draft_capacity
        self.current_weight = current_weight
        self.current_volume = current_volume
        self.current_draft = current_draft
        self.distance_matrix = distance_matrix
        self.cost_matrix = cost_matrix
        self.current_location = current_location
        self.current_time = current_time
        self.port_to_ind = port_to_ind
        self.immersion_summer = immersion_summer
        self.cargo_on_board = cargo_on_board
        self.deliveries = deliveries

    def get_travel_time(self, location):
        distance = self.distance_matrix[self.port_to_ind[self.current_location]
                                        ][self.port_to_ind[location]]

        return distance / self.speed

    def weight_check_ok(self, cargo_weight):
        if self.current_weight + cargo_weight > self.weight_capacity:
            return False
        return True

    def volume_check_ok(self, cargo_volume):
        if self.current_volume + cargo_volume > self.volume_capacity:
            return False
        return True

    def draft_origin_check_ok(self, cargo_weight, max_draft):
        if self.current_draft + cargo_weight / self.immersion_summer > max_draft:
            return False
        return True

    def calc_possible_steps(self, cargos, cargos_taken, port_to_max_draft):

        possible_actions = []
        for cargo in self.cargo_on_board.values():
            travel_time = self.get_travel_time(cargo.destination)
            dest_draft_ok = self.current_draft <= port_to_max_draft[cargo.destination]
            if self.current_time + travel_time <= cargo.dischargeDateTo and dest_draft_ok:
                possible_actions.append((cargo.id, "dropoff", travel_time))

        for cargo in cargos:
            travel_time = self.get_travel_time(cargo.origin)

            travel_time_ok = self.current_time + travel_time <= cargo.dischargeDateTo
            cargo_not_taken = cargo.id not in cargos_taken
            weight_ok = self.weight_check_ok(cargo.weight)
            volume_ok = self.volume_check_ok(cargo.volume)
            origin_draft_ok = self.draft_origin_check_ok(
                cargo.weight, port_to_max_draft[cargo.origin])
            # allowed_ok = self.id in cargo.allowed_vehicles
            allowed_ok = True  # till we get to use allowed vehicles
            # if cargo.id not in cargos_taken:
            #     if self.current_time + travel_time <= cargo.dischargeDateTo and self.weight_check_ok(cargo.weight):

            if all([travel_time_ok, cargo_not_taken, weight_ok, volume_ok, origin_draft_ok, allowed_ok]):
                possible_actions.append((cargo.id, "pickup", travel_time))

        return possible_actions

    def take_step(self, step, cargo_id_to_cargo):
        cargo_id, action, travel_time = step
        cargo = cargo_id_to_cargo[cargo_id]
        if action == "dropoff":
            self.current_weight -= cargo.weight
            self.current_time += travel_time
            self.current_location = cargo.destination
            self.deliveries.append(cargo)
            self.cargo_on_board.pop(cargo_id)
        elif action == "pickup":
            self.current_weight += cargo.weight
            self.current_time += travel_time
            self.current_location = cargo.origin
            self.cargo_on_board[cargo_id] = cargo
            return cargo_id

    def choose_step(self, possible_actions):
        random_step = rn.choice(possible_actions)
        return random_step


def make_vehicles(vehicle_json, distance_matrix, cost_matrices, port_to_ind, start_time=0):
    vehicles = []
    for v_js, cost_matrix in zip(vehicle_json, cost_matrices):

        id = v_js["id"]
        speed = v_js["vehicleSpeed"]["value"]
        weight_capacity = v_js["weightCapacity"]["value"]
        volume_capacity = v_js["volumeCapacity"]["value"]
        md = v_js["vehicleDimensions"]["depth"]["max"]
        mw = weight_capacity
        s = v_js["vehicleDimensions"]["depth"]["massMultiplier"]
        current_draft = md - (mw / s)
        current_location = v_js["startingLocation"]["id"]
        distance_matrix = distance_matrix
        cost_matrix = cost_matrix
        port_to_ind = port_to_ind

        vehicle = Vehicle(id=id,
                          speed=speed,
                          weight_capacity=weight_capacity,
                          volume_capacity=volume_capacity,
                          draft_capacity=md,
                          current_weight=0,
                          current_volume=0,
                          current_draft=current_draft,
                          distance_matrix=distance_matrix,
                          cost_matrix=cost_matrix,
                          current_location=current_location,
                          current_time=0,
                          port_to_ind=port_to_ind,
                          immersion_summer=s
                          )

        vehicles.append(vehicle)

    return vehicles


def make_port_to_ind(distance_matrix_json):

    print(f"distance_matrix_json_1: {distance_matrix_json}")

    port_to_ind = {}
    for ind, row in enumerate(distance_matrix_json["rows"]):
        port = row["id"].split("::")[0]
        port_to_ind[row["id"]] = ind

    return port_to_ind


def make_distance_matrix(distance_matrix_json):
    distance_matrix = []
    print(f"distance_matrix_json_2: {distance_matrix_json}")
    for row in distance_matrix_json["rows"]:
        distance_matrix.append(row["values"])
    return distance_matrix


def make_cost_matrices(cost_matrices_json):
    cost_matrices = []
    for cost_matrix_json in cost_matrices_json["costMatrices"]:
        cost_matrix = []
        for row in cost_matrix_json["rows"]:
            cost_matrix.append(row["values"])
        cost_matrices.append(cost_matrix)
    return cost_matrices


def convert_cargo(input_cargos):

    cargos = []

    for input_cargo in input_cargos:
        cargo = Cargo()

        cargo.id = input_cargo["id"]
        cargo.volume = input_cargo["volume"]
        cargo.weight = input_cargo["weight"]
        cargo.origin = input_cargo["routePair"]["origin"]["id"].split("::")[0]
        cargo.destination = input_cargo["routePair"]["destination"]["id"].split("::")[
            0]
        cargo.laycanFrom = input_cargo["loadWindow"]["timeWindow"]["start"]
        cargo.laycanTo = input_cargo["loadWindow"]["timeWindow"]["end"]
        cargo.dischargeDateFrom = input_cargo["unloadWindow"]["timeWindow"]["start"]
        cargo.dischargeDateTo = input_cargo["unloadWindow"]["timeWindow"]["end"]
        cargo.revenue = input_cargo["revenue"]

        cargos.append(cargo)

    return cargos


def make_port_to_max_draft(cargo_json):

    port_to_max_draft = {}
    for cargo in cargo_json:
        origin_port = cargo["routePair"]["origin"]["id"].split("::")[0]
        port_to_max_draft[origin_port] = cargo["routePair"]["origin"]["dimension"]["depth"]["max"]
        destination_port = cargo["routePair"]["destination"]["id"].split("::")[
            0]
        port_to_max_draft[destination_port] = cargo["routePair"]["destination"]["dimension"]["depth"]["max"]

    return port_to_max_draft


def random_optimizer_wrapper(cargos_json, vehicle_json, cost_matrices_json, distance_matrix_json):

    cargos = convert_cargo(cargos_json)
    port_to_ind = make_port_to_ind(distance_matrix_json)
    logging.info(f"port_to_ind: {port_to_ind}")
    distance_matrix = make_distance_matrix(distance_matrix_json)
    cost_matrices = make_cost_matrices(cost_matrices_json)
    logging.info(f"cost_matrices: {cost_matrices}")
    vehicles = make_vehicles(
        vehicle_json, distance_matrix, cost_matrices, port_to_ind, start_time=0)
    port_to_max_draft = make_port_to_max_draft(cargos_json)

    simulation = RandomOptimizer(
        vehicles, cargos, port_to_max_draft, port_to_ind, n_iterations=5)
    result = simulation.solve()

    return result[0]


if __name__ == "__main__":

    distance_matrix = [[0, 5, 6, 8],
                       [5, 0, 7, 9],
                       [6, 7, 0, 3],
                       [6, 9, 3, 0]]

    port_to_ind = {"port_a": 0, "port_b": 1, "port_c": 2, "port_d": 3}

    vehicles = []

    cost_matrix_1 = [[0, 9, 7, 7],
                     [9, 0, 6, 9],
                     [7, 6, 0, 8],
                     [7, 9, 8, 0]]

    vehicle = Vehicle(id=1,
                      speed=1,
                      weight_capacity=10,
                      volume_capacity=10,
                      draft_capacity=None,
                      current_weight=0,
                      current_volume=0,
                      current_draft=0,
                      distance_matrix=distance_matrix,
                      cost_matrix=cost_matrix_1,
                      current_location="port_a",
                      current_time=0,
                      port_to_ind=port_to_ind,
                      immersion_summer=1,
                      )

    vehicles.append(vehicle)

    cost_matrix_2 = [[0, 5, 4, 2],
                     [5, 0, 6, 2],
                     [4, 6, 0, 3],
                     [2, 2, 3, 0]
                     ]

    vehicle_2 = Vehicle(id=2,
                        speed=1,
                        weight_capacity=15,
                        volume_capacity=15,
                        draft_capacity=None,
                        current_weight=0,
                        current_volume=0,
                        current_draft=0,
                        distance_matrix=distance_matrix,
                        cost_matrix=cost_matrix_2,
                        current_location="port_a",
                        current_time=0,
                        port_to_ind=port_to_ind,
                        immersion_summer=1,
                        )

    vehicles.append(vehicle_2)

    cargos = []

    cargo_1 = Cargo(id="cargo_1",
                    origin="port_a",
                    dest="port_b",
                    volume=2,
                    weight=2,
                    laycanFrom=3,
                    laycanTo=5,
                    dischargeDateFrom=12,
                    dischargeDateTo=15,
                    revenue=6.5,
                    # allowed_vehicles=[1, 2]
                    )
    cargos.append(cargo_1)

    cargo_2 = Cargo(id="cargo_2",
                    origin="port_c",
                    dest="port_d",
                    volume=2,
                    weight=2,
                    laycanFrom=3,
                    laycanTo=5,
                    dischargeDateFrom=35,
                    dischargeDateTo=38,
                    revenue=7.5,
                    # allowed_vehicles=[1, 2]
                    )
    cargos.append(cargo_2)

    cargo_3 = Cargo(id="cargo_3",
                    origin="port_b",
                    dest="port_c",
                    volume=2,
                    weight=13,
                    laycanFrom=3,
                    laycanTo=5,
                    dischargeDateFrom=35,
                    dischargeDateTo=38,
                    revenue=7.5,
                    # allowed_vehicles=[1, 2]
                    )
    cargos.append(cargo_3)

    cargo_4 = Cargo(id="cargo_4",
                    origin="port_d",
                    dest="port_c",
                    volume=2,
                    weight=13,
                    laycanFrom=3,
                    laycanTo=5,
                    dischargeDateFrom=35,
                    dischargeDateTo=38,
                    revenue=7.5,
                    # allowed_vehicles=[1, 2]
                    )

    cargos.append(cargo_4)

    port_to_max_draft = {"port_a": 100,
                         "port_b": 200, "port_c": 250, "port_d": 150}

    simulation = RandomOptimizer(
        vehicles, cargos, port_to_max_draft, port_to_ind, n_iterations=5)
    result = simulation.solve()

    import ipdb
    ipdb.set_trace()

    # cargo_id_to_cargo = {c.id: c for c in cargos}
    # cargos_taken = set()

    # steps = []

    # while True:

    #     possible_steps = vehicle.calc_possible_steps(cargos, cargos_taken)
    #     if not possible_steps:
    #         break
    #     step = vehicle.choose_step(possible_steps)
    #     steps.append(step)

    #     cargo_id = vehicle.take_step(step, cargo_id_to_cargo)
    #     if cargo_id:
    #         cargos_taken.add(cargo_id)

    # print(f"steps: {steps}")
