import numpy as np
import matplotlib.pyplot as plt

file_path = "C:\\Users\\32285\\OneDrive\\Desktop\\singleant.txt"

# 修正数据解析函数，处理文件中的IQ数据
def extract_iq_samples(file_path):
    iq_data = []
    with open(file_path, 'r') as file:
        for line in file:
            if "IQ samples:" in line:
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

#iq_samples = iq_samples[:328]
iq_samples = iq_samples[:82]

# 检查数据是否成功解析
if iq_samples.size == 0:
    raise ValueError("No valid IQ samples were extracted from the file.")

# 数据归一化（幅度归一化）
amplitudes, phases = calculate_amplitude_and_phase(iq_samples)
print(amplitudes)
print(phases)
normalized_iq_samples = iq_samples

import numpy as np
import matplotlib.pyplot as plt

# Assuming normalized_iq_samples is defined
N = len(normalized_iq_samples)

# Create color array for all points
point_colors = ['black'] * 8  # First 8 points black

# For remaining points, process in groups of 4
remaining_points = N - 8
num_groups = (remaining_points + 3) // 4  # Ceiling division

# Generate distinct colors for the last 2 points of each group
group_colors = plt.cm.tab20(np.linspace(0, 1, num_groups))  # Using tab20 for more colors

for i in range(num_groups):
    start_idx = 8 + i * 4
    end_idx = min(8 + (i + 1) * 4, N)

    # First 2 points in group are blue
    point_colors.extend(['blue'] * min(2, end_idx - start_idx))

    # Last 2 points get unique color (converted from RGBA to hex)
    if end_idx - start_idx > 2:
        color = group_colors[i]
        hex_color = '#%02x%02x%02x' % (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        point_colors.extend([hex_color] * (end_idx - start_idx - 2))

plt.figure(figsize=(10, 10))

# Draw scatter plot with colored points
plt.scatter(normalized_iq_samples[:, 0], normalized_iq_samples[:, 1],
            s=10,
            alpha=1,
            color=point_colors,  # Use our custom color array
            label="IQ Points")

# Draw connecting lines (keeping your original line drawing code)
num_line_groups = (N + 81) // 82
line_colors = plt.cm.tab10(np.linspace(0, 1, num_line_groups))

for i in range(num_line_groups):
    start_idx = i * 82
    end_idx = min((i + 1) * 82, N)
    group_data = normalized_iq_samples[start_idx:end_idx]

    #plt.plot(group_data[:, 0], group_data[:, 1],
    #         color=line_colors[i],
     #        alpha=0.6,
     #        linewidth=1,
      #       label=f'Group {i + 1} (Points {start_idx}-{end_idx - 1})')

plt.title("Normalized IQ Samples with Custom Coloring")
plt.xlabel("I (In-phase)")
plt.ylabel("Q (Quadrature)")
plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.7)
plt.grid(alpha=0.5)
plt.legend()

plt.savefig("../assets/iq_samples_custom_colored.png", dpi=300, bbox_inches='tight')
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
# 保存图片
plt.savefig("../assets/iq_samples_time_series.png", dpi=300, bbox_inches='tight')
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
# 保存图片
plt.savefig("../assets/amplitude_phase_time_series.png", dpi=300, bbox_inches='tight')
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
