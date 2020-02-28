# from app.resolvers.optimizer_types import Cargo


import random as rn
from copy import deepcopy


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
                 revenue=0):
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


class Simulation:
    def __init__(self, vehicles, cargos, n_iterations):
        self.vehicles = vehicles
        self.cargos = cargos
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
                self.cargos, cargos_taken)
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
            score = 0
            for steps in vehicle_to_steps.values():
                for step in steps:
                    if step[1] == "dropoff":
                        score += 1
            scored_runs.append((vehicle_to_steps, score))

        sorted_scored_runs = sorted(
            scored_runs, key=lambda x: x[1], reverse=True)

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
        distance = self.distance_matrix[port_to_ind[self.current_location]
                                        ][port_to_ind[location]]

        return distance / self.speed

    def weight_check_ok(self, cargo_weight):
        if self.current_weight + cargo_weight > self.weight_capacity:
            return False
        return True

    def calc_possible_steps(self, cargos, cargos_taken):

        possible_actions = []
        for cargo in self.cargo_on_board.values():
            travel_time = self.get_travel_time(cargo.destination)
            if self.current_time + travel_time <= cargo.dischargeDateTo:
                possible_actions.append((cargo.id, "dropoff", travel_time))

        for cargo in cargos:
            travel_time = self.get_travel_time(cargo.origin)
            if cargo.id not in cargos_taken:
                if self.current_time + travel_time <= cargo.dischargeDateTo and self.weight_check_ok(cargo.weight):
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


if __name__ == "__main__":

    distance_matrix = [[0, 5, 6, 8],
                       [5, 0, 7, 9],
                       [6, 7, 0, 3],
                       [6, 9, 3, 0]]

    port_to_ind = {"port_a": 0, "port_b": 1, "port_c": 2, "port_d": 3}

    vehicle = Vehicle(id=1,
                      speed=1,
                      weight_capacity=10,
                      volume_capacity=None,
                      draft_capacity=None,
                      current_weight=0,
                      current_volume=None,
                      current_draft=None,
                      distance_matrix=distance_matrix,
                      cost_matrix=None,
                      current_location="port_a",
                      current_time=0,
                      port_to_ind=port_to_ind,
                      immersion_summer=None,
                      )

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
                    revenue=6.5
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
                    revenue=7.5
                    )
    cargos.append(cargo_2)

    vehicles = []
    vehicles.append(vehicle)

    simulation = Simulation(vehicles, cargos, n_iterations=5)
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
