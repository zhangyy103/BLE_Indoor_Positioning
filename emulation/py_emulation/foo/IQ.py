import numpy as np
import matplotlib.pyplot as plt

file_path = "C:\\Users\\32285\\OneDrive\\Desktop\\single_iq_sample.txt"

# 修正数据解析函数，处理文件中的IQ数据
def extract_iq_samples(file_path):
    iq_data = []
    with open(file_path, 'r') as file:
        for line in file:
            if "IQ samples (AoA):" in line:
                # 提取括号内的IQ数据并分割
                raw_samples = line.split(":")[1].strip()
                raw_samples = raw_samples.replace(")(", "|").replace("(", "").replace(")", "").split("|")
                for sample in raw_samples:
                    try:
                        iq_pair = tuple(map(int, sample.split(',')))
                        iq_data.append(iq_pair)
                    except ValueError:
                        # 跳过无法解析的IQ数据
                        continue
    return np.array(iq_data)

# 计算幅度和相位
def calculate_amplitude_and_phase(iq_samples):
    amplitudes = np.sqrt(np.sum(iq_samples**2, axis=1))
    phases = np.arctan2(iq_samples[:, 1], iq_samples[:, 0])  # Q在前，I在后
    return amplitudes, phases


# 数据解析
iq_samples = extract_iq_samples(file_path)

# 检查数据是否成功解析
if iq_samples.size == 0:
    raise ValueError("No valid IQ samples were extracted from the file.")

# 数据归一化（幅度归一化）
amplitudes, phases = calculate_amplitude_and_phase(iq_samples)
normalized_iq_samples = iq_samples / amplitudes[:, None]

# 可视化：归一化后的散点图
plt.figure(figsize=(10, 6))
plt.scatter(normalized_iq_samples[:, 0], normalized_iq_samples[:, 1], alpha=0.6, label="Normalized IQ Points")
plt.title("Normalized IQ Samples Scatter Plot")
plt.xlabel("I (In-phase)")
plt.ylabel("Q (Quadrature)")
plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.7)
plt.grid(alpha=0.5)
plt.legend()
plt.show()

# 可视化：时间序列图
plt.figure(figsize=(12, 6))
time = np.arange(len(iq_samples))  # 假设每个点的时间间隔相等
plt.plot(time, iq_samples[:, 0], label="I (In-phase)", alpha=0.8)
plt.plot(time, iq_samples[:, 1], label="Q (Quadrature)", alpha=0.8)
plt.title("Time Series of I and Q Samples")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(alpha=0.5)
plt.show()

# 可视化：幅度和相位随时间变化
plt.figure(figsize=(12, 6))
plt.plot(time, amplitudes, label="Amplitude", alpha=0.8)
plt.plot(time, phases, label="Phase", alpha=0.8)
plt.title("Amplitude and Phase over Time")
plt.xlabel("Sample Index")
plt.ylabel("Value")
plt.legend()
plt.grid(alpha=0.5)
plt.show()

# 假设采样频率 fs
fs = 1e6  # 1 MHz 采样率，你需要根据实际情况调整
Ts = 1 / fs  # 采样周期
time = np.arange(len(iq_samples)) * Ts  # 生成时间轴

# 还原原始正弦波
reconstructed_signal = iq_samples[:, 0] * np.cos(2 * np.pi * fs * time) + iq_samples[:, 1] * np.sin(2 * np.pi * fs * time)

# 绘制波形
plt.figure(figsize=(12, 6))
plt.plot(time[:500], reconstructed_signal[:500], label="Reconstructed Signal", alpha=0.8)
plt.title("Reconstructed Time-Domain Signal from IQ Data")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(alpha=0.5)
plt.show()

# 数据处理结果保存
output_file = "../assets/processed_iq_data.npz"
np.savez(output_file, iq_samples=iq_samples, amplitudes=amplitudes, phases=phases)
print(f"Processed data saved to {output_file}")
