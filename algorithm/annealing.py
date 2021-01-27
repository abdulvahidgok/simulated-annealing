import functools
import math
import random
import typing
from abc import ABC, abstractmethod
from enum import Enum

from algorithm.cooling_schedule import CoolingSchedule, CoolingScheduleType, CoolingStatusType


class Solver(ABC):
    pass


class SolutionStatusType(Enum):
    CANDIDATE = 0
    ACCEPTED = 1
    REJECTED = 2


class Solution:
    """
    if solution is non-improver, status parameter will be SolutionStatusType.CANDIDATE
    """
    status = SolutionStatusType.CANDIDATE  # type: SolutionStatusType

    def __init__(self,
                 plan,
                 energy=None,  # type: float
                 *args, **kwargs):
        super(Solution, self).__init__(*args, **kwargs)
        self.plan = plan
        self.energy = energy
        self.status = SolutionStatusType.CANDIDATE

    def calculate_energy(self,
                         solver,  # type: ObjectiveFunction
                         ) -> float:
        if self.energy is None:
            self.energy = solver.objective_function(
                solution=self
            )
        return self.energy

    def accept(self):
        self.status = SolutionStatusType.ACCEPTED

    def reject(self):
        self.status = SolutionStatusType.CANDIDATE

    @property
    def accepted(self) -> bool:
        return self.status == SolutionStatusType.ACCEPTED

    @property
    def candidate(self) -> bool:
        return self.status == SolutionStatusType.CANDIDATE

    @property
    def rejected(self) -> bool:
        return self.status == SolutionStatusType.REJECTED


class ObjectiveFunction:
    @abstractmethod
    def objective_function(
            self,
            solution,  # type: Solution
            *args, **kwargs
    ) -> float:
        """
        :param solution: solution that is initial solution or new solution
        :return energy: energy that is the result of objective function which calculated with solution
        """
        pass


class SolutionGeneratorStatusType(Enum):
    STOPPED = 1
    CONTINUE = 2


class SolutionGenerator:
    solution_generator_status = SolutionGeneratorStatusType.CONTINUE  # type: SolutionGeneratorStatusType

    @abstractmethod
    def generate_initial_solution(
            self,
            data,
            *args, **kwargs
    ) -> Solution:
        """
        :param data: data
        :return solution: we could choose a initial solution randomly.
        """
        pass

    @abstractmethod
    def generate_solution(
            self,
            data,
            *args, **kwargs
    ) -> Solution:
        """
        :param data: data
        :return solution: we could choose a solution randomly. solution can be initial solution or new solution
        """
        pass


class State:
    def __init__(self,
                 temperature,  # type: float
                 old_solutions=False,  # type: bool
                 *args, **kwargs):
        super(State, self).__init__(*args, **kwargs)
        self.solution_list = list()  # type: typing.List[Solution]
        self.temperature = temperature
        self.old_solutions = old_solutions

    @property
    def thermal_equilibrium(self) -> bool:
        return next(iter(solution.accepted for solution in self.solution_list), None)

    @property
    def status(self) -> SolutionStatusType:
        return next(iter(solution.status for solution in self.solution_list), None)

    @property
    def solution(self) -> Solution:
        return next(iter(solution for solution in self.solution_list), None)

    def is_initial(self,
                   solver,  # type: SMA
                   ):
        return self == solver.initial_state

    def stopped(self,
                solver,  # type: SMA
                ):
        return self.temperature != solver.temperature or self.is_initial(solver=solver) or self.thermal_equilibrium

    def add_solution(self,
                     solution,  # type: Solution
                     ) -> bool:
        if not self.thermal_equilibrium:
            if self.old_solutions:
                self.solution_list.insert(0, solution)
            else:
                self.solution_list.insert(0, solution)
                self.solution_list = self.solution_list[0:2]
            return True
        else:
            return False


class SMA(Solver, ABC, ObjectiveFunction, SolutionGenerator, CoolingSchedule):

    def __init__(
            self,
            data,
            initial_temperature,  # type: float
            temperature_min,  # type: float
            cooling_speed,  # type: float
            cooling_schedule_type=CoolingScheduleType.GEOMETRIC.value,  # type: int
            steps=0,  # type: int
            initial_solution=None,  # type: Solution
            old_states=False,  # type: bool
            old_solutions=False,  # type: bool
            *args, **kwargs
    ):
        super(SMA, self).__init__(
            temperature=initial_temperature,
            temperature_min=temperature_min,
            cooling_speed=cooling_speed,
            cooling_schedule_type=cooling_schedule_type,
            *args, **kwargs)
        self.state_list = list()  # type: typing.List[State]
        self.data = data
        self.steps = steps
        self.old_states = old_states
        self.old_solutions = old_solutions
        initial_state = self.create_and_add_new_state()
        if not initial_solution:
            initial_solution = self.generate_initial_solution(data=self.data)
        initial_solution.calculate_energy(solver=self)
        initial_solution.accept()
        initial_state.add_solution(solution=initial_solution)

    @abstractmethod
    def stopping_criteria(self) -> bool:
        return self.temperature < self.temperature_min

    def add_state(self,
                  state,  # type: State
                  ) -> bool:

        state.old_solutions = self.old_solutions
        if not self.state_list or not self.incomplete_state:
            if self.old_states:
                self.state_list.insert(0, state)
            else:
                self.state_list = [state, self.state] if self.state_list else [state]
            return True
        else:
            return False

    def create_and_add_new_state(self):

        new_state = State(temperature=self.temperature, old_solutions=self.old_solutions)
        self.add_state(new_state)
        return new_state

    @functools.cached_property
    def initial_state(self) -> State:
        return self.state_list[-1]

    @property
    def incomplete_state(self) -> State:
        last_state = self.state_list[0]
        return last_state if not last_state.stopped(solver=self) else None

    @property
    def state(self):
        a = next(
            (state_i for state_i in self.state_list if state_i.thermal_equilibrium),
            self.initial_state)
        return a

    @property
    def solution(self):
        return self.state.solution

    @property
    def energy(self):
        return self.solution.energy

    def comparison_of_solutions(
            self,
            new_energy
    ):
        """
        Parameters:
        :param new_energy: energy that is the result of objective function which calculated with new solution
        :return energy_var: energy_variation=new_energy-self.energy
        if energy_variation ( ∆energy ) is positive or zero, we will use metropolis acceptance criterion
        """

        energy_variation = new_energy - self.energy
        return energy_variation

    def metropolis_acceptance_criterion(self, energy_variation):
        """
        calculate acceptance
        Parameters
        ----------
        :param energy_variation: energy_variation if energy_variation is positive or zero.
        if energy_variation is close to T, the probability of being accepted increases.
        :return acceptance: if true, we will accept new solution.
        test:
        ---------
        j = 0
        T = 10
        for i in range(10000):
            a = metropolis_acceptance_criterion(75)
            if a[2]:
                j+=1
                print(math.ceil(a[0]), math.ceil(a[1]), )
        print(j)
        """
        random_number = random.uniform(0, 1)
        acceptance = random_number <= math.exp(-energy_variation / self.temperature)
        return acceptance

    def thermal_equilibrium_achievement(self):
        new_solution = self.generate_solution(data=self.data)
        if self.solution_generator_status == SolutionGeneratorStatusType.CONTINUE:
            new_solution.calculate_energy(solver=self)
            energy_variation = self.comparison_of_solutions(new_energy=new_solution.energy)
            if energy_variation > 0:
                if self.metropolis_acceptance_criterion(energy_variation=energy_variation):
                    new_solution.accept()
                else:
                    new_solution.reject()
            else:
                new_solution.accept()
            self.incomplete_state.add_solution(new_solution)

    def reduce_system_temperature(self):
        self.cool()
        self.create_and_add_new_state()

    def solve(self):
        while not self.stopping_criteria():
            self.reduce_system_temperature()
            if self.cooling_status == CoolingStatusType.STOPPED:
                break
            step = 0
            while step <= self.steps and self.incomplete_state:
                self.thermal_equilibrium_achievement()
                if self.solution_generator_status == SolutionGeneratorStatusType.STOPPED:
                    break
                step += 1
        return self.solution.plan
