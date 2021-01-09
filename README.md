

# Simulated Annealing Optimization

<div align="center">
  <img style="max-width: 50%" src="https://github.com/abdulvahidgok/simulated_annealing/blob/master/example2.gif"><br><br>
</div>

## Usage

```console
from optimization_problems import TSPSolver

solver = TSPSolver(
    data=data,
    steps=2000,  # maximum step for each thermal equilibrium loop, without steps program will calculate number of neighbour combinations.
    initial_temperature=1000,
    temperature_min=5,  # when system temperature reaches minimum temperature, cooling loop stops.
    cooling_speed=0.9999,  # The system cools slower as the cooling speed approaches 1.
    random_solution=True,  # will generate neighbour solutions randomly
    distance_calculator=geopy.distance,  # calculates distance between two coordinates.
)
solver.solve()
```

## Test

```console
$ python test.py
```
