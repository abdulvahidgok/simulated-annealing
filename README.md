

# Simulated Annealing

<div align="center">
  <img style="max-width: 50%" src="https://github.com/abdulvahidgok/simulated_annealing/blob/master/example.gif"><br><br>
</div>

## Usage

```console
from solvers import TSPSolver

solver = TSPSolver(
    data=data,
    steps=2000,  # maximum steps for each thermal equilibrium loop, without steps program will calculate number of neighbour combinations.
    initial_temperature=1000,
    temperature_min=5,  # when system temperature reaches minimum temperature, cooling loop stops.
    cooling_speed=0.9999,  # The system cools slower as the cooling speed approaches 1.
    random_solution=True,  # will generate neighbour solutions randomly ( default )
    distance_calculator=geopy.distance,  # calculates distance between two coordinates.
    distance_matrix_result=None  # optional
)
solver.solve()
```
## Cooling Schedule Types

```console
# from cooling schedule types:
# 1 is Logarithmic, 2 is Geometric, 3 is Exponential
from solvers import TSPSolver
from algorithm.cooling_schedule import CoolingScheduleType
solver = TSPSolver(
    data=data,
    temperature_min=5,
    cooling_speed=0.9999,
    cooling_schedule_type=CoolingScheduleType.EXPONENTIAL.value  # or directly 1, 2, 3 can assigned.
)
solver.solve()
```

## Plot Accepted Routes

```console
from tests.plot import PlotTSPSolver
solver = PlotTSPSolver(
    data=data,
    temperature_min=5,
    cooling_speed=0.9999,
    plot_coords=True  # default
)
solver.solve()
```

## Test

```console
$ python test.py
```
