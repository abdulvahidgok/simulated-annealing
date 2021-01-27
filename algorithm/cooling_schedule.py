import math
from collections import OrderedDict
from enum import Enum
from functools import cached_property
from typing import Union


class CoolingScheduleType(Enum):
    LOGARITHMIC = 1  # T(k) = α*To / ln (1 + k)
    GEOMETRIC = 2  # T(k) = α^k * To
    EXPONENTIAL = 3  # T(k) = To*exp(−α*k^(1/N))


class CoolingStatusType(Enum):
    STOPPED = 1
    CONTINUE = 2


class CoolingSchedule:
    cooling_status = CoolingStatusType.CONTINUE

    def __init__(self,
                 temperature,  # type: float
                 temperature_min,  # type: float
                 cooling_speed,  # type: float
                 temperature_max=0,  # type: float
                 k=0,  # type: float
                 n=1,  # type: float
                 cooling_schedule_type=CoolingScheduleType.GEOMETRIC,  # type: Union[int, None, CoolingScheduleType]
                 ):
        """
        :param temperature: temperature is the current temperature
        :param cooling_speed: cooling_speed is the cooling speed parameter.
        :param k: k is the iteration
        :param n: N is the dimensionality of the model space
        """
        self.CoolingScheduleChoices = OrderedDict(
            [
                (CoolingScheduleType.LOGARITHMIC.value, self.logarithmic),
                (CoolingScheduleType.GEOMETRIC.value, self.geometric),
                (CoolingScheduleType.EXPONENTIAL.value, self.exponential),
            ]
        )
        self.temperature = temperature
        self.temperature_max = temperature_max if temperature_max else temperature
        self.temperature_min = temperature_min
        self.cooling_speed = cooling_speed
        self.k = k
        self.n = n
        self.cooling_schedule_type = cooling_schedule_type
        super(CoolingSchedule, self).__init__()

    @cached_property
    def initial_temperature(self):
        return self.temperature

    def cool(self) -> bool:
        self.k += 1
        new_temperature = self.CoolingScheduleChoices[self.cooling_schedule_type.value]()
        if new_temperature >= self.temperature_min:
            self.temperature = new_temperature
            self.cooling_status = CoolingStatusType.CONTINUE
            return True
        else:
            self.cooling_status = CoolingStatusType.STOPPED
            return False

    def logarithmic(self):
        temperature = (self.cooling_speed * self.initial_temperature) / \
                      math.log1p(self.k)  # logarithm of 1+self.k (base e)
        return temperature

    def geometric(self):
        """
        The system cools slowly as cooling_speed approaches 1. cooling_speed must be in range 0 to 1.
        """
        temperature = (self.cooling_speed ** self.k) * self.initial_temperature
        return temperature

    def exponential(self):
        temperature = self.initial_temperature * math.exp(-self.cooling_speed * (self.k ** (1 / self.n)))
        return temperature
