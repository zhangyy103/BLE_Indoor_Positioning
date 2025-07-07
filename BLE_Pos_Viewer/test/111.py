import numpy as np
amplitude = 255  # 幅度量化值
samples = 256   # 采样点数
# 生成正弦波数据
x = np.linspace(0, 2 * np.pi, samples)
y = amplitude * (np.sin(x) + 1) / 2  # 将正弦波映射到0-255范围
# 将数据量化为整数
quantized_data = np.round(y).astype(int)
# 将量化后的数值转换为二进制形式
binary_data = [bin(value)[2:].zfill(8) for value in quantized_data]
#binary_data = [hex(value)[2:].zfill(2) for value in quantized_data]
# 创建输出文件
with open("sine_wave_data.txt", "w") as f:
    for i in range(samples):
        # 计算当前地址的十六进制表示
        address_hex = format(i, '03x')  # 3位十六进制地址
        # 写入格式：@地址 二进制数据
        f.write(f"@{address_hex} {binary_data[i]} \t//{quantized_data[i]}\n")
print(f"已成功生成包含{samples}个点的正弦波数据文件：sine_wave_data.txt")
