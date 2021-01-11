import time
from math import radians, cos, sin, asin, sqrt

from data import example_data
from tests import plot


def distance(origin, destination):
    r = 6371  # radius of the earth in km
    lat1 = radians(origin[0])
    lat2 = radians(destination[0])
    lat_dif = lat2 - lat1
    lng_dif = radians(destination[1] - origin[1])
    a = sin(lat_dif / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(lng_dif / 2.0) ** 2
    d = 2 * r * asin(sqrt(a))
    return d * 0.621371  # return miles


def test(data=example_data.LOCATIONS_59, steps=1000, initial_temperature=2000, temperature_min=1,
         cooling_speed=0.999999, random_solutions=True, *args, **kwargs):
    start = time.time()
    solver = plot.PlotTSPSolver(
        data=data,
        steps=steps,
        initial_temperature=initial_temperature,
        temperature_min=temperature_min,
        cooling_speed=cooling_speed,
        random_solutions=random_solutions,
        distance_calculator=distance,
        *args, **kwargs
    )

    solver.solve()

    end = time.time()
    print("energy: %s" % solver.energy)
    print("solution plan: %s" % solver.solution.plan)
    print("time: %s" % (end - start))
    print("generated solutions: %s" % solver.total_generated_solution)


def main():
    """
    other examples:
        test(data=example_data.LOCATIONS_22, steps=1000, initial_temperature=900, temperature_min=1,
         cooling_speed=0.9999, random_solutions=True, plot_coords=True, )

    """
    test(data=example_data.LOCATIONS_22, initial_temperature=900, temperature_min=1,
         cooling_speed=0.9999, random_solutions=False, plot_coords=True, )


if __name__ == '__main__':
    main()
