import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from config import COLOR_SCHEME, BUFFER_SIZE

class RealTimePlot(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(8, 6), dpi=100)
        super().__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self._setup_plot()
        self.trajectory_x = []
        self.trajectory_y = []

    def _setup_plot(self):
        """初始化绘图参数"""
        self.axes.set_facecolor(COLOR_SCHEME["background"])
        self.fig.patch.set_facecolor(COLOR_SCHEME["background"])
        self.axes.set_xlim(0, 50)
        self.axes.set_ylim(0, 50)
        self.axes.grid(True, color=COLOR_SCHEME["grid_color"], linestyle=':')
        self.axes.set_xlabel('X Position (m)', color=COLOR_SCHEME["foreground"])
        self.axes.set_ylabel('Y Position (m)', color=COLOR_SCHEME["foreground"])

        # 创建绘图对象
        self.current_point = self.axes.plot([], [], 'o',
                                            markersize=12, color=COLOR_SCHEME["accent_blue"], zorder=3)[0]
        self.trajectory_line = self.axes.plot([], [], '-',
                                              linewidth=2, color=COLOR_SCHEME["accent_light"], alpha=0.7)[0]

    def batch_update(self, x_list, y_list):
        """批量更新轨迹数据"""
        self.trajectory_x.extend(x_list)
        self.trajectory_y.extend(y_list)

        if len(self.trajectory_x) > BUFFER_SIZE:
            del self.trajectory_x[:len(self.trajectory_x) - BUFFER_SIZE]
            del self.trajectory_y[:len(self.trajectory_y) - BUFFER_SIZE]

        if x_list and y_list:
            self.current_point.set_data(x_list[-1], y_list[-1])
            self.trajectory_line.set_data(self.trajectory_x, self.trajectory_y)
            self.axes.relim()
            self.axes.autoscale_view()