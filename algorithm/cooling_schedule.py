import math
from collections import OrderedDict
from enum import Enum


class Temperature(float):
    def __new__(cls, value):
        return super().__new__(cls, value)

    def __init__(self, value):
        float.__init__(value)


class CoolingScheduleType(Enum):
    LOGARITHMIC = 1  # T(k) = α*To / ln (1 + k)
    GEOMETRIC = 2  # T(k) = α^k * To
    EXPONENTIAL = 3  # T(k) = To*exp(−α*k^(1/N))


class CoolingStatusType(Enum):
    STOPPED = 1
    CONTINUE = 2


class CoolingSchedule:
    cooling_schedule_type = CoolingScheduleType.GEOMETRIC.value  # type: int
    cooling_status = CoolingStatusType.CONTINUE

    def __init__(self,
                 temperature,  # type: float
                 temperature_min,  # type: float
                 cooling_speed,  # type: float
                 temperature_max=0,  # type: float
                 k=0,  # type: float
                 n=1,  # type: float
                 cooling_schedule_type=cooling_schedule_type,  # type: int
                 ):
        """
        :param temperature: temperature is the current temperature
        :param cooling_speed: cooling_speed is the cooling speed parameter
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
        self.cooling_schedule_type = cooling_schedule_type

        self.temperature = temperature
        self.cooling_speed = cooling_speed
        self.k = k
        self.n = n
        self.cooling_schedule_type = cooling_schedule_type
        super(CoolingSchedule, self).__init__()

    def cool(self) -> bool:
        self.k += 1
        new_temperature = self.CoolingScheduleChoices[self.cooling_schedule_type]()
        if new_temperature >= self.temperature_min:
            self.temperature = new_temperature
            self.cooling_status = CoolingStatusType.CONTINUE
            return True
        else:
            self.cooling_status = CoolingStatusType.STOPPED
            return False

    def logarithmic(self):
        temperature = self.cooling_speed * self.temperature / math.exp(1 + self.k)
        return temperature

    def geometric(self):
        temperature = (self.cooling_speed ** self.k) * self.temperature
        return temperature

    def exponential(self):
        temperature = self.temperature * math.exp(-self.cooling_speed * (self.k ** (1 / self.n)))
        return temperature
