import itertools
import time
from math import radians, cos, sin, asin, sqrt

from algorithm import cooling_schedule
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


def test(data=example_data.LOCATIONS_58, steps=1000, initial_temperature=2000., temperature_min=1.,
         cooling_speed=0.999999, random_solutions=True, save_last_frame=True, *args, **kwargs):
    start = time.time()
    solver = plot.PlotTSPSolver(
        data=data,
        steps=steps,
        initial_temperature=initial_temperature,
        temperature_min=temperature_min,
        cooling_speed=cooling_speed,
        random_solutions=random_solutions,
        distance_calculator=distance,
        save_last_frame=save_last_frame,
        *args, **kwargs
    )
    red = '\033[91m'
    end_color = '\033[0m'
    bold = '\033[1m'
    blue = '\033[94m'
    divider = f"{bold}| {end_color}"
    g_b = f"{blue}{bold}"
    print(f"{red}{blue}Simulated Annealing Process{end_color}", )
    print(
        f"{g_b}cooling type: {end_color}", f"{red}{solver.cooling_schedule_type.name}{end_color}",
        f"{divider}{g_b}initial temperature: {end_color}", f"{red}{solver.initial_temperature}{end_color}",
        f"{divider}{g_b}min temperature: {end_color}", f"{red}{solver.temperature_min}{end_color}",
        f"{divider}{g_b}cooling speed: {end_color}", f"{red}{solver.cooling_speed}{end_color}"
    )
    solver.solve()

    end = time.time()
    elapsed_time = end - start
    print(f"{red}{blue}Result{end_color}", )
    print(
        f"{g_b}Data Length:  {end_color}", f"{red}{len(solver.solution.plan)}{end_color}",
        f"{divider}{g_b}Last energy:  {end_color}", f"{red}{solver.energy}{end_color}",
        f"{divider}{g_b}Total generated solutions:  {end_color}", f"{red}{solver.total_generated_solution}{end_color}",
        f"{divider}{g_b}Elapsed time:  {end_color}", f"{red}{elapsed_time}{end_color}",
        f"{divider}{g_b}Solution Plan:  {end_color}", f"{red}{solver.solution.plan}{end_color}",
    )


def main():
    """
    other examples:
        test(data=example_data.LOCATIONS_22, steps=1000, initial_temperature=900, temperature_min=1,
         cooling_speed=0.9999, random_solutions=True, plot_coords=True, )

    with thread, plot features disabled with plot_coords=False, save_last_frame=False:
        with ThreadPoolExecutor(max_workers=8) as executor:
        executor.submit(
            lambda: test(
                data=example_data.LOCATIONS_58, initial_temperature=100, temperature_min=1,
                cooling_speed=0.1, random_solutions=False, plot_coords=False, save_last_frame=False,
                cooling_schedule_type=cooling_schedule.CoolingScheduleType.GEOMETRIC
            )
        )
    geometric cooling:
        cooling_speed - between 0.8 and 1
    logarithmic cooling:
        cooling_speed - 1:
            1 will cause slow cooling. Choose smaller than 1 for fast cooling.
    exponential cooling:
        cooling_speed - 1:
            1 will cause fast cooling. Choose smaller than 1 for slow cooling.
    """

    schedules = [
        {
            "data": example_data.LOCATIONS_50,
            "cooling_schedule_types": [
                {
                    "cooling_schedule_type": cooling_schedule.CoolingScheduleType.GEOMETRIC,
                    "initial_temperature_list": [500, 1000, 2000, 3000, 4000],
                    "cooling_speed_list": [0.85, 0.9, 0.95, 0.99]
                },
                {
                    "cooling_schedule_type": cooling_schedule.CoolingScheduleType.EXPONENTIAL,
                    "initial_temperature_list": [7000],
                    "cooling_speed_list": [0.0001]
                },
                {
                    "cooling_schedule_type": cooling_schedule.CoolingScheduleType.LOGARITHMIC,
                    "initial_temperature_list": [500, 1000, 2000, 3000, 4000],
                    "cooling_speed_list": [0.85, 0.9, 0.95, 0.99]
                },
            ]
        },
    ]
    for schedule in schedules:
        for cooling_schedule_type in schedule.get("cooling_schedule_types"):
            for initial_temperature, cooling_speed in itertools.product(
                    cooling_schedule_type.get("initial_temperature_list"),
                    cooling_schedule_type.get("cooling_speed_list")):
                test(
                    data=schedule.get("data"), initial_temperature=initial_temperature, temperature_min=65,
                    cooling_speed=cooling_speed, random_solutions=False, plot_coords=False, save_last_frame=True,
                    cooling_schedule_type=cooling_schedule_type.get("cooling_schedule_type")
                )


if __name__ == '__main__':
    main()
