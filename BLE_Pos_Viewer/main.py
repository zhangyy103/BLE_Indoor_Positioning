import sys
import serial
import warnings
from PyQt5 import QtCore, QtWidgets
from ui_design import Ui_MainWindow
from serial_parser import DataParser
import numpy as np
from pyqtgraph import PlotWidget  # 新增导入

warnings.filterwarnings("ignore", category=DeprecationWarning)  # 屏蔽警告


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 替换绘图控件
        self.replace_plot_widget()

        # 初始化变量
        self.serial = None
        self.parser = DataParser()
        self.timer = QtCore.QTimer()

        # 初始化UI
        self.init_ui()

        # 连接信号槽
        self.connect_btn.clicked.connect(self.toggle_serial)
        self.timer.timeout.connect(self.read_serial)

    def replace_plot_widget(self):
        """动态替换为pyqtgraph控件"""
        # 删除原有控件
        old_widget = self.findChild(QtWidgets.QGraphicsView, "plot_widget")
        old_widget.deleteLater()

        # 创建新控件
        self.plot_widget = PlotWidget(self.centralwidget)
        self.plot_widget.setObjectName("plot_widget")

        # 插入到原有布局位置
        self.horizontalLayout_2.insertWidget(1, self.plot_widget)

    def init_ui(self):
        # 填充可用串口
        ports = [f"COM{i}" for i in range(1, 10)]
        self.com_port.addItems(ports)
        self.baud_rate.setCurrentText("115200")

        # 初始化绘图区域
        self.plot_widget.setBackground('w')
        self.plot_curve = self.plot_widget.plot(pen='b')

    def toggle_serial(self):
        if self.serial and self.serial.is_open:
            self.close_serial()
        else:
            self.open_serial()

    def open_serial(self):
        try:
            self.serial = serial.Serial(
                port=self.com_port.currentText(),
                baudrate=int(self.baud_rate.currentText()),
                timeout=0.1
            )
            self.timer.start(50)  # 每50ms读取一次
            self.connect_btn.setText("断开连接")
        except Exception as e:
            self.log_display.append(f"打开串口失败: {str(e)}")

    def close_serial(self):
        if self.serial:
            self.serial.close()
        self.timer.stop()
        self.connect_btn.setText("连接串口")

    def read_serial(self):
        if self.serial and self.serial.is_open:
            try:
                raw_bytes = self.serial.readline()
                data = raw_bytes.decode().strip()  # 去除首尾空白和换行符
                if data:
                    self.raw_display.append(data)
                    x, y = self.parser.parse(data)
                    self.update_position(x, y)
            except UnicodeDecodeError:
                self.log_display.append("编码错误: 非UTF-8数据")
            except Exception as e:
                self.log_display.append(f"串口读取错误: {str(e)}")

    def update_position(self, x, y):
        print(x, y)
        # 处理显示文本
        x_display = f"X: {x:.2f} m" if x is not None else "X: N/A"
        self.x_label.setText(x_display)
        y_display = f"Y: {y:.2f} m" if y is not None else "Y: N/A"
        self.y_label.setText(y_display)

        # 处理绘图数据（关键修改！）
        # 将 None 转换为 np.nan（数值类型的无效标记）
        plot_x = x if x is not None else np.nan
        plot_y = y if y is not None else np.nan

        # 更新绘图（确保传递数组）
        self.plot_curve.setData([plot_x], [plot_y])  # 单个点绘图


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())