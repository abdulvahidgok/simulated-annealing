

# Simulated Annealing
<div align="center">
  <img style="max-width: 50%" src="https://github.com/abdulvahidgok/simulated-annealing/blob/master/tests/example.gif?raw=true"
><br><br>
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
from solvers import TSPSolver
from algorithm.cooling_schedule import CoolingScheduleType
solver = TSPSolver(
    data=data,
    initial_temperature=7000,
    temperature_min=65,
    cooling_speed=0.0001,
    cooling_schedule_type=CoolingScheduleType.EXPONENTIAL
)
solver.solve()
```

## Plot Accepted Routes

```console
from tests.plot import PlotTSPSolver
PlotTSPSolver(
    data=data,
    initial_temperature=7000,
    temperature_min=65,
    cooling_speed=0.001,
    random_solutions=False,
    plot_coords=True,  # for live simulated annealing process
    save_last_frame=True,  # will save last state /tests/frames folder
    cooling_schedule_type=CoolingScheduleType.EXPONENTIAL
)
solver.solve()
```

## Test

```console
$ python test.py
```
