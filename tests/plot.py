import matplotlib
import matplotlib.pyplot as plt

from solvers import tsp

matplotlib.use("TkAgg")

plt.ion()


class PlotTSPSolver(tsp.TSPSolver):

    def __init__(self, plot_coords=True, *args, **kwargs):
        self.plot_coords = plot_coords
        self.figure, self.ax, self.lines = None, None, None
        super(PlotTSPSolver, self).__init__(*args, **kwargs)

    def start_plot(self):
        if self.plot_coords:
            self.figure, self.ax = plt.subplots(figsize=(17, 11))
            self.lines, = self.ax.plot([], [], marker='o', label="Temperature, Energy")
            self.ax.set_autoscaley_on(True)
            self.ax.set_xlim(-500, 500)
            self.ax.grid()

    def thermal_equilibrium_achievement(self):
        super(PlotTSPSolver, self).thermal_equilibrium_achievement()
        if self.plot_coords:
            if self.state_list[0].solution_list[0].accepted:
                self.run_plot()

    def solve(self):
        self.start_plot()
        super(PlotTSPSolver, self).solve()

    def run_plot(self):
        plt.cla()
        solution = self.state_list[0].solution_list[0]
        plan = solution.plan
        energy = solution.energy
        plt.legend("energy" + str(energy))
        self.ax.label = "energy" + str(energy)
        coords = [self.data[i] for i in plan]
        coords.append(self.data[plan[0]])
        self.lines.set_xdata(i[0] for i in coords)
        self.lines.set_ydata(i[1] for i in coords)
        self.ax.scatter(*zip(*coords))
        self.ax.plot(*zip(*coords))
        self.ax.legend(['Temperature: %.4f - Energy: %.2f' % (round(self.temperature, 7), round(energy, 3))])
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
