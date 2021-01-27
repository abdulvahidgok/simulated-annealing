import copy
import itertools
import math
import random
import typing
from functools import cached_property

import geopy.distance as geopy_distance

from algorithm.annealing import SMA, Solution
from algorithm.cooling_schedule import CoolingScheduleType


class TSPSolver(SMA):
    def __init__(self,
                 data,  # type: typing.Dict[typing.Any, typing.Tuple[float, float]]
                 distance_matrix_result=None,  # type: typing.Dict[str, typing.Dict[str, float]]
                 cooling_schedule_type=CoolingScheduleType.GEOMETRIC.value,
                 random_solutions=True,  # type: bool
                 distance_calculator=geopy_distance.geodesic,  # type: typing.Type
                 *args, **kwargs):
        self.distance_matrix_result = distance_matrix_result
        self.distance_calculator = distance_calculator
        self.total_generated_solution = 0  # type: int
        super(TSPSolver, self).__init__(data, cooling_schedule_type=cooling_schedule_type, *args, **kwargs)
        if not self.steps:
            self.count_steps()
        self.neighbour_solution_generator = self.generate_random_neighbour_solution() if random_solutions \
            else self.generate_neighbour_solution()
        self.previous_swap = (0, 0)  # type: typing.Tuple[int, int]

    def stopping_criteria(self) -> bool:
        return self.temperature < self.temperature_min

    @cached_property
    def distance_matrix(self) -> typing.Dict[str, typing.Dict[str, float]]:
        return self.distance_matrix_result if self.distance_matrix_result else {
            location[0]: {location_inner[0]: self.distance_calculator(location[1], location_inner[1]) for location_inner
                          in self.data.items()}
            for location in self.data.items()}

    @cached_property
    def number_of_point(self) -> int:
        return len(self.data)

    def count_steps(self):
        """
        (n!/(n-k)!)/k! counts neighbour solutions, with data length choose 2
        """
        number_of_combinations = math.factorial(self.number_of_point) // math.factorial(2) // math.factorial(
            self.number_of_point - 2)
        self.steps = number_of_combinations * 2

    @staticmethod
    def swap_index(
            given_list,  # type: list
            index_1,  # type: int
            index_2  # type: int
    ):
        given_list[index_1], given_list[index_2] = given_list[index_2], given_list[index_1]

    def generate_neighbour_solution(self):
        index_combinations = itertools.combinations(range(self.number_of_point), 2)
        indexes = (0, 0)
        while indexes:
            indexes = next(index_combinations, None)
            if indexes:
                plan = copy.copy(self.solution.plan)
                self.swap_index(plan, *indexes)
                yield Solution(plan=plan)
        self.neighbour_solution_generator = self.generate_neighbour_solution()
        yield next(self.neighbour_solution_generator)

    def generate_random_neighbour_solution(self):
        while True:
            random_index_1, random_index_2 = random.sample(range(self.number_of_point), 2)
            new_plan = copy.deepcopy(self.solution.plan)
            self.swap_index(new_plan, random_index_1, random_index_2)
            self.total_generated_solution += 1
            yield Solution(plan=new_plan)

    def generate_solution(
            self,
            *args, **kwargs
    ):
        new_solution = next(self.neighbour_solution_generator)
        self.total_generated_solution += 1
        return new_solution

    def generate_initial_solution(
            self,
            *args, **kwargs
    ) -> Solution:
        data_key_list = [i for i in self.data.keys()]
        random.shuffle(data_key_list)
        return Solution(plan=data_key_list)

    def iterate_coords(self, plan):
        a, total_distance = 0, 0
        while self.number_of_point > a:
            location_0 = plan[a - 1]
            location_1 = plan[a]
            distance = self.distance_matrix[location_0][location_1]
            total_distance += distance
            yield total_distance
            a = a + 1

    def objective_function(
            self,
            solution,  # type: Solution
            *args, **kwargs
    ) -> float:
        """
        thread:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            sum_distance = executor.submit(lambda: sum(
                self.distance_matrix[p1][p2] for p1, p2 in zip(solution.plan, solution.plan[1:])))
            max_location_distance = executor.submit(
                lambda: max(zip(solution.plan, solution.plan[1:]),
                            key=lambda x: self.distance_matrix[x[0]][x[1]]))
        self.max_location_distance = max_location_distance.result()
        return sum_distance.result()
        """
        *_, total_distance = self.iterate_coords(plan=solution.plan)
        return total_distance
