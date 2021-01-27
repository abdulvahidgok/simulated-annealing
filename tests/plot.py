import pathlib
import time

import matplotlib
import matplotlib.pyplot as plt

from solvers import tsp

matplotlib.use("TkAgg")


class PlotTSPSolver(tsp.TSPSolver):
    def __init__(self, plot_coords=True, save_last_frame=True, *args, **kwargs):
        if plot_coords:
            plt.ion()
        if save_last_frame and not plot_coords:
            plt.ioff()
        self.plot_coords = plot_coords
        self.save_last_frame = save_last_frame
        self.figure, self.ax, self.lines = None, None, None
        self.time = 0
        super(PlotTSPSolver, self).__init__(*args, **kwargs)

    def start_plot(self):
        if self.plot_coords or self.save_last_frame:
            self.figure, self.ax = plt.subplots(figsize=(17, 11), )
            self.lines, = self.ax.plot([], [])
            self.ax.set_autoscaley_on(True)
            self.ax.set_xlim(-500, 500)
            self.ax.grid()

    def thermal_equilibrium_achievement(self):
        super(PlotTSPSolver, self).thermal_equilibrium_achievement()
        if self.plot_coords:
            if self.state_list[0].solution_list[0].accepted:
                self.run_plot()

    def solve(self):
        start_time = time.time()
        self.start_plot()
        super(PlotTSPSolver, self).solve()
        end_time = time.time()
        self.time = end_time - start_time
        if self.save_last_frame:
            self.save_last_state()

    def set_coords(self, coords):
        self.lines.set_xdata(i[0] for i in coords)
        self.lines.set_ydata(i[1] for i in coords)

    def run_plot(self):
        plt.cla()
        solution = self.state_list[0].solution_list[0]
        plan = solution.plan
        energy = solution.energy
        plt.legend("energy" + str(energy))
        self.ax.label = "energy" + str(energy)
        coords = [self.data[i] for i in plan]
        coords.append(self.data[plan[0]])
        self.set_coords(coords)
        self.ax.set_title(
            "%s Cooling Schedule \n initial temperature: %.2f, cooling_speed: %.2f, minimum temperature: %.2f" %
            (self.cooling_schedule_type.name, self.initial_temperature, self.cooling_speed, self.temperature_min),
            color="b"
        )
        self.ax.set_xlabel('Latitude', color="r")
        self.ax.set_ylabel('Longitude', color="r")
        self.ax.scatter(*zip(*coords), color="r")
        self.ax.plot(*zip(*coords))
        self.ax.legend(['Temperature: %.4f - Energy: %.2f' % (round(self.temperature, 7), round(energy, 3))])
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def save_last_state(self):
        plt.cla()
        plt.legend("energy" + str(self.energy))
        self.ax.label = "energy" + str(self.energy)
        coords = [self.data[i] for i in self.solution.plan]
        coords.append(self.data[self.solution.plan[0]])
        self.set_coords(coords)
        self.ax.scatter(*zip(*coords))
        self.ax.plot(*zip(*coords))
        self.ax.legend(['Initial Temp: %.4f - '
                        'Cooling Speed: %f - '
                        'Energy: %.2f - '
                        'Elapsed time: %.5f - '
                        'Total Generated Solutions: %d' %
                        (round(self.initial_temperature, 7),
                         self.cooling_speed,
                         round(self.energy, 3),
                         self.time,
                         self.total_generated_solution)])
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        base_dir = pathlib.Path(__file__).parent.parent.absolute()
        self.figure.savefig(
            base_dir.joinpath("tests").joinpath("frames").joinpath(
                "%s-%s-%s-%s-%s.png" % (
                    str(len(self.solution.plan)),
                    str(self.cooling_schedule_type.name),
                    str(self.initial_temperature),
                    str(self.temperature_min),
                    str(self.cooling_speed)
                )
            )
        )
        plt.close()
