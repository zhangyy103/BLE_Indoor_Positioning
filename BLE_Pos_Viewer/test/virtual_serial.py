# Python 示例（需安装 pyserial）
import serial

ser = serial.Serial('COM5', 115200)
ser.write(b"Hello World")  # 发送字节数据
ser.write("你好".encode('utf-8'))  # 发送中文
ser.close()