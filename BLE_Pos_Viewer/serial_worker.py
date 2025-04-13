import serial
from config import SERIAL_TIMEOUT
from serial.tools import list_ports
from PyQt5.QtCore import QThread, pyqtSignal, QMutex

class SerialWorker(QThread):
    data_ready = pyqtSignal(bytes)  # 原始数据信号

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self._mutex = QMutex()
        self._is_running = True
        self.ser = None

    def run(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=SERIAL_TIMEOUT
            )
            while self._is_running:
                if self.ser.in_waiting > 0:
                    data = self.ser.read(self.ser.in_waiting)
                    self.data_ready.emit(data)
        except Exception as e:
            self.data_ready.emit(f"ERROR:{str(e)}".encode())
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()

    def stop(self):
        self._mutex.lock()
        self._is_running = False
        self._mutex.unlock()

def get_available_ports():
    """获取可用串口列表"""
    return [f"{port.device} - {port.description}" for port in list_ports.comports()]