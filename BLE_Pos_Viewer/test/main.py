import sys
import serial
from serial.tools import list_ports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# 配色方案（现代蓝白主题）
COLOR_SCHEME = {
    "background": "#F0F5FF",
    "foreground": "#2C3E50",
    "accent_blue": "#3498DB",
    "accent_light": "#5DADE2",
    "grid_color": "#D6EAF8",
    "warning_red": "#E74C3C"
}


class SerialWorker(QThread):
    data_received = pyqtSignal(str)  # 数据接收信号

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True
        self.ser = None

    def run(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            while self.running:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if data:
                        self.data_received.emit(data)
        except Exception as e:
            print(f"Serial error: {str(e)}")
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()

    def stop(self):
        self.running = False


class RealTimePlot(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=6, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor(COLOR_SCHEME["background"])
        self.fig.patch.set_facecolor(COLOR_SCHEME["background"])

        # 初始化绘图元素
        self.current_point = self.axes.plot([], [], 'o',
                                            markersize=12, color=COLOR_SCHEME["accent_blue"], zorder=3)[0]
        self.trajectory_line = self.axes.plot([], [], '-',
                                              linewidth=2, color=COLOR_SCHEME["accent_light"], alpha=0.7)[0]

        # 设置坐标轴
        self.axes.set_xlim(0, 50)
        self.axes.set_ylim(0, 50)
        self.axes.grid(True, color=COLOR_SCHEME["grid_color"], linestyle=':')
        self.axes.set_xlabel('X Position (m)', color=COLOR_SCHEME["foreground"])
        self.axes.set_ylabel('Y Position (m)', color=COLOR_SCHEME["foreground"])

        self.trajectory_x = []
        self.trajectory_y = []

    def update_plot(self, x, y):
        # 更新轨迹数据
        self.trajectory_x.append(x)
        self.trajectory_y.append(y)

        # 保持最近100个轨迹点
        if len(self.trajectory_x) > 100:
            self.trajectory_x.pop(0)
            self.trajectory_y.pop(0)

        # 更新绘图
        self.current_point.set_data(x, y)
        self.trajectory_line.set_data(self.trajectory_x, self.trajectory_y)
        self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 窗口设置
        self.setWindowTitle("蓝牙AOA实时定位系统")
        self.setGeometry(100, 100, 1200, 800)

        # 串口相关变量
        self.serial_worker = None
        self.raw_data_buffer = ""

        # 初始化UI
        self.init_ui()
        self.apply_stylesheet()
        self.refresh_ports()

    def init_ui(self):
        # 主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # 左侧绘图区域
        self.plot_canvas = RealTimePlot(self)
        layout.addWidget(self.plot_canvas, 3)

        # 右侧控制面板
        control_panel = QFrame()
        control_layout = QVBoxLayout(control_panel)

        # 状态显示
        self.status_label = QLabel("系统状态: 未连接")
        self.coord_label = QLabel("当前坐标: (0.00, 0.00)")
        control_layout.addWidget(self.status_label)
        control_layout.addWidget(self.coord_label)

        # 串口设置
        serial_group = QGroupBox("串口设置")
        serial_layout = QFormLayout(serial_group)

        self.port_combo = QComboBox()
        self.refresh_btn = QPushButton("刷新端口")
        self.refresh_btn.clicked.connect(self.refresh_ports)
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["115200", "9600", "460800"])
        self.connect_btn = QPushButton("连接")
        self.connect_btn.clicked.connect(self.toggle_serial)

        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_btn)

        serial_layout.addRow("端口:", port_layout)
        serial_layout.addRow("波特率:", self.baud_combo)
        serial_layout.addRow(self.connect_btn)
        control_layout.addWidget(serial_group)

        # 系统控制
        self.start_btn = QPushButton("开始定位")
        self.start_btn.clicked.connect(self.toggle_positioning)
        self.clear_btn = QPushButton("清除轨迹")
        self.clear_btn.clicked.connect(self.clear_trajectory)
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.clear_btn)

        layout.addWidget(control_panel, 1)

    def apply_stylesheet(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_SCHEME["background"]};
                color: {COLOR_SCHEME["foreground"]};
                font-family: Segoe UI;
                font-size: 12px;
            }}
            QPushButton {{
                background-color: {COLOR_SCHEME["accent_blue"]};
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_SCHEME["accent_light"]};
            }}
            QGroupBox {{
                border: 2px solid {COLOR_SCHEME["accent_blue"]};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QLabel {{
                font-size: 12pt;
                color: {COLOR_SCHEME["foreground"]};
            }}
            QComboBox {{
                padding: 5px;
                border: 1px solid {COLOR_SCHEME["accent_blue"]};
                border-radius: 3px;
            }}
        """)

    def refresh_ports(self):
        """刷新可用串口列表"""
        self.port_combo.clear()
        ports = list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}")

    def toggle_serial(self):
        """切换串口连接状态"""
        if self.connect_btn.text() == "连接":
            # 获取选择的端口和波特率
            port_info = self.port_combo.currentText().split(" - ")[0]
            baudrate = int(self.baud_combo.currentText())

            try:
                # 创建串口工作线程
                self.serial_worker = SerialWorker(port_info, baudrate)
                self.serial_worker.data_received.connect(self.handle_data)
                self.serial_worker.start()

                self.connect_btn.setText("断开")
                self.status_label.setText("系统状态: 已连接")
                self.status_label.setStyleSheet(f"color: {COLOR_SCHEME['accent_blue']};")
            except Exception as e:
                QMessageBox.critical(self, "连接错误", f"无法打开串口:\n{str(e)}")
        else:
            if self.serial_worker:
                self.serial_worker.stop()
                self.serial_worker = None
            self.connect_btn.setText("连接")
            self.status_label.setText("系统状态: 未连接")
            self.status_label.setStyleSheet(f"color: {COLOR_SCHEME['foreground']};")

    def parse_data(self, data):
        """解析定位数据（示例格式：$POS,12.34,56.78#）"""
        try:
            if data.startswith("$POS") and data.endswith("#"):
                parts = data.strip("$#").split(",")
                if len(parts) == 3 and parts[0] == "POS":
                    return float(parts[1]), float(parts[2])
            return None
        except Exception as e:
            print(f"数据解析错误: {str(e)}")
            return None

    def handle_data(self, data):
        """处理接收到的数据"""
        # 示例数据协议：$POS,x,y#
        self.raw_data_buffer += data

        # 查找完整数据帧
        while True:
            start = self.raw_data_buffer.find("$")
            end = self.raw_data_buffer.find("#")

            if start != -1 and end != -1 and start < end:
                frame = self.raw_data_buffer[start:end + 1]
                self.raw_data_buffer = self.raw_data_buffer[end + 1:]

                # 解析数据
                coordinates = self.parse_data(frame)
                if coordinates:
                    x, y = coordinates
                    print(f"接收到数据: X={x}, Y={y}")
                    self.plot_canvas.update_plot(x, y)
                    self.coord_label.setText(f"当前坐标: ({x:.2f}, {y:.2f})")
            else:
                break

    def toggle_positioning(self):
        """切换定位状态"""
        if self.start_btn.text() == "开始定位":
            self.start_btn.setText("停止定位")
            # 这里可以添加实际开始定位的代码
        else:
            self.start_btn.setText("开始定位")
            # 这里可以添加实际停止定位的代码

    def clear_trajectory(self):
        """清除轨迹"""
        self.plot_canvas.trajectory_x.clear()
        self.plot_canvas.trajectory_y.clear()
        self.plot_canvas.update_plot(0, 0)
        self.coord_label.setText("当前坐标: (0.00, 0.00)")

    def closeEvent(self, event):
        """窗口关闭事件处理"""
        if self.serial_worker:
            self.serial_worker.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())