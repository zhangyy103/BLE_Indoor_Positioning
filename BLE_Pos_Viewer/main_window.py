from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QGroupBox, QComboBox, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from serial.tools import list_ports

from serial_worker import SerialWorker, get_available_ports
from plot_canvas import RealTimePlot
from config import COLOR_SCHEME, RENDER_INTERVAL

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial_worker = None
        self.raw_buffer = bytearray()
        self.data_queue = []
        self._setup_ui()
        self._setup_timers()
        self.refresh_ports()

    def _setup_ui(self):
        """初始化界面"""
        self.setWindowTitle("蓝牙AOA高精度定位系统")
        self.setGeometry(100, 100, 1280, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # 绘图区域
        self.plot_canvas = RealTimePlot()
        layout.addWidget(self.plot_canvas, 3)

        # 右侧控制面板
        control_panel = self._create_control_panel()
        layout.addWidget(control_panel, 1)

        # 应用样式
        self._apply_stylesheet()

    def _create_control_panel(self):
        """创建右侧控制面板"""
        panel = QFrame()
        layout = QVBoxLayout(panel)

        # 状态显示
        self.status_label = QLabel("🟡 系统状态: 未连接")
        self.coord_label = QLabel("当前位置: (---, ---)")
        layout.addWidget(self.status_label)
        layout.addWidget(self.coord_label)

        # 串口设置
        serial_group = QGroupBox("串口配置")
        serial_layout = QVBoxLayout(serial_group)

        self.port_combo = QComboBox()
        self.refresh_btn = QPushButton("刷新端口")
        self.refresh_btn.clicked.connect(self.refresh_ports)
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "115200", "460800"])
        self.connect_btn = QPushButton("连接设备")
        self.connect_btn.clicked.connect(self.toggle_serial)

        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_btn)

        serial_layout.addWidget(QLabel("通信端口:"))
        serial_layout.addLayout(port_layout)
        serial_layout.addWidget(QLabel("波特率:"))
        serial_layout.addWidget(self.baud_combo)
        serial_layout.addWidget(self.connect_btn)
        layout.addWidget(serial_group)

        # 系统控制
        control_group = QGroupBox("系统控制")
        control_layout = QVBoxLayout(control_group)
        self.start_btn = QPushButton("▶ 开始定位")
        self.start_btn.clicked.connect(self.toggle_positioning)
        self.clear_btn = QPushButton("🗑 清除轨迹")
        self.clear_btn.clicked.connect(self.clear_trajectory)
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.clear_btn)
        layout.addWidget(control_group)

        return panel

    def _apply_stylesheet(self):
        """应用样式表"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_SCHEME["background"]};
                color: {COLOR_SCHEME["foreground"]};
                font-family: "微软雅黑";
                font-size: 12px;
            }}
            QPushButton {{
                background-color: {COLOR_SCHEME["accent_blue"]};
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_SCHEME["accent_light"]};
            }}
            QGroupBox {{
                border: 2px solid {COLOR_SCHEME["accent_blue"]};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QLabel#status_label {{
                font-size: 14px;
                color: {COLOR_SCHEME["foreground"]};
            }}
            QComboBox {{
                padding: 6px;
                border: 1px solid {COLOR_SCHEME["accent_blue"]};
                border-radius: 4px;
            }}
        """)

    def _setup_timers(self):
        """初始化定时器"""
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self._process_data)
        self.render_timer.start(RENDER_INTERVAL)

    def refresh_ports(self):
        """刷新可用串口列表"""
        self.port_combo.clear()
        ports = list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}")

    def toggle_serial(self):
        """切换串口连接状态"""
        if self.connect_btn.text().startswith("连接"):
            port_info = self.port_combo.currentText().split(" - ")[0]
            baudrate = int(self.baud_combo.currentText())

            try:
                self.serial_worker = SerialWorker(port_info, baudrate)
                self.serial_worker.data_ready.connect(self._receive_raw_data)
                self.serial_worker.start()

                self.connect_btn.setText("断开连接")
                self.status_label.setText("🟢 系统状态: 已连接")
            except Exception as e:
                QMessageBox.critical(self, "连接错误", f"无法打开串口:\n{str(e)}")
        else:
            if self.serial_worker:
                self.serial_worker.stop()
                self.serial_worker = None
            self.connect_btn.setText("连接设备")
            self.status_label.setText("🔴 系统状态: 已断开")

    def _receive_raw_data(self, data):
        """接收原始数据"""
        if data.startswith(b"ERROR"):
            QMessageBox.critical(self, "串口错误", data.decode())
            return

        self.raw_buffer.extend(data)
        while b'#' in self.raw_buffer:
            start = self.raw_buffer.find(b'$')
            end = self.raw_buffer.find(b'#')

            if start != -1 and end != -1 and start < end:
                frame = self.raw_buffer[start:end + 1]
                self.raw_buffer = self.raw_buffer[end + 1:]
                self._parse_frame(frame)
            else:
                break

    def _parse_frame(self, frame):
        """解析数据帧"""
        try:
            # 示例协议：$POS,12.34,56.78#
            if frame.startswith(b'$POS') and frame.endswith(b'#'):
                parts = frame[1:-1].split(b',')
                if len(parts) == 3:
                    x = float(parts[1].decode())
                    y = float(parts[2].decode())
                    self.data_queue.append((x, y))
        except Exception as e:
            print(f"解析错误: {str(e)}")

    def _process_data(self):
        """处理并渲染数据"""
        if not self.data_queue:
            return

        # 批量处理数据
        x_list, y_list = zip(*self.data_queue)
        self.data_queue.clear()

        # 更新界面
        self.plot_canvas.batch_update(x_list, y_list)
        self.plot_canvas.draw_idle()
        self.coord_label.setText(f"当前位置: ({x_list[-1]:.2f}, {y_list[-1]:.2f})")

    def toggle_positioning(self):
        if self.start_btn.text().startswith("▶"):
            # 发送开始定位指令
            if self.serial_worker and self.serial_worker.ser:
                self.serial_worker.ser.write(b'$START#')
            self.start_btn.setText("⏹ 停止定位")
        else:
            # 发送停止定位指令
            if self.serial_worker and self.serial_worker.ser:
                self.serial_worker.ser.write(b'$STOP#')
            self.start_btn.setText("▶ 开始定位")

    def clear_trajectory(self):
        """清除轨迹"""
        self.plot_canvas.trajectory_x.clear()
        self.plot_canvas.trajectory_y.clear()
        self.plot_canvas.current_point.set_data([], [])
        self.plot_canvas.trajectory_line.set_data([], [])
        self.plot_canvas.draw_idle()
        self.coord_label.setText("当前位置: (---, ---)")

    def closeEvent(self, event):
        """关闭事件处理"""
        if self.serial_worker:
            self.serial_worker.stop()
            self.serial_worker.wait(1000)
        event.accept()