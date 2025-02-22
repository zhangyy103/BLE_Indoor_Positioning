import numpy as np
import matplotlib.pyplot as plt

# ========== 参数 ==========
FREQ = 250e3  # CTE 信号频率 (Hz)
C = 3e8  # 光速 (m/s)
LAMBDA = C / FREQ  # 波长 (m)
D = LAMBDA / 4  # 单位间距 (天线间距，a = λ/4)
SAMPLING_RATE = 2e6  # 采样率 2 MHz
SAMPLE_PERIOD = 1 / SAMPLING_RATE  # 采样周期 (0.5 μs)
NUM_SAMPLES_PER_ANTENNA = 4  # 每个天线采样 2 μs 对应 4 个采样点
NUM_SWITCH_GAP_SAMPLES = 4  # 天线切换间隙 2 μs，丢弃 4 个采样点
TOTAL_SAMPLES_PER_CYCLE = NUM_SAMPLES_PER_ANTENNA + NUM_SWITCH_GAP_SAMPLES  # 每个天线周期总采样点数 = 8

# ========== 天线与目标位置 ==========
# 目标位置 (注：注释写 (10a, 10a, 0)，代码中可以根据需要设为 (10*D, 10*D, 0))
target_position = np.array([10 * D, 10 * D, 10 * D])

# 天线阵列位置 (单位: a = λ/4)
antenna_positions = np.array([
    [-3 * D, 3 * D, 0], [-1 * D, 3 * D, 0], [1 * D, 3 * D, 0], [3 * D, 3 * D, 0],
    [-3 * D, 1 * D, 0], [3 * D, 1 * D, 0],
    [-3 * D, -1 * D, 0], [3 * D, -1 * D, 0],
    [-3 * D, -3 * D, 0], [-1 * D, -3 * D, 0], [1 * D, -3 * D, 0], [3 * D, -3 * D, 0]
])

# 计算每个天线到目标的距离（欧几里得距离）
distances = np.linalg.norm(antenna_positions - target_position, axis=1)

# 计算每个天线的初始相位 (根据传播延时，公式：2π * distance / λ) 并取模 2π
# 注意：如果按严格的延时模型，接收信号应为 A*exp(-j*2π*FREQ*(distance/C))，而 2π*FREQ*(distance/C) = 2π*distance/λ，
# 这里只是取模 2π，不考虑负号，目的是模拟各天线间的相位差。
phases = (2 * np.pi * distances / LAMBDA) % (2 * np.pi)
# ========== IQ 数据序列生成 ==========

# 生成每个天线采样时的相对时间轴（每个天线采 4 个样点，时刻分别为 0, 0.5, 1, 1.5 μs）
time_axis = np.arange(NUM_SAMPLES_PER_ANTENNA) * SAMPLE_PERIOD  # 单位：秒

# 初始化存储所有 IQ 数据的列表
iq_data_sequence = []

# 发送信号功率 (dB)
TX_POWER_DB = -1  # 发送信号功率 (dB)

# fspl_const 为 FSPL 中不变的常数部分：20 * log10(4π/C)
fspl_const = 20 * np.log10(4 * np.pi / C)

# 遍历每个天线生成其 IQ 采样数据
for i in range(len(antenna_positions)):
    # 获取当前天线的距离和初始相位
    distance = distances[i]
    init_phase = phases[i]

    # 计算当前天线的自由空间路径损耗 (FSPL, 单位 dB)
    # FSPL(dB) = 20*log10(distance) + 20*log10(FREQ) + 20*log10(4π/C)
    fspl_db = 20 * np.log10(distance) + 20 * np.log10(FREQ) + fspl_const

    # 计算接收功率 (dB)：发送功率减去路径损耗
    rx_power_db = TX_POWER_DB - fspl_db

    # 将 dB 换算为线性幅度：幅度 = 10^(RxPower_dB/20)
    amplitude = 10 ** (rx_power_db / 20)

    # 为了模拟各天线采样时的不同时隙，我们为每个天线设置一个全局时间偏移
    # 每个天线的采样周期（含切换间隔）的时长为 TOTAL_SAMPLES_PER_CYCLE * SAMPLE_PERIOD
    antenna_time_offset = i * TOTAL_SAMPLES_PER_CYCLE * SAMPLE_PERIOD

    # 当前天线的全局采样时刻 = 本天线的采样时刻 + 对应的时间偏移
    t_samples = time_axis + antenna_time_offset

    # 生成当前天线的 IQ 数据
    # 模型：IQ = A * exp{ j [ 初始相位 + 2π * FREQ * (全局采样时刻) ] }
    iq_samples = amplitude * np.exp(1j * (init_phase + 2 * np.pi * FREQ * t_samples))

    # 将当前天线的 4 个采样点加入总体 IQ 数据序列
    iq_data_sequence.extend(iq_samples)

    # 模拟天线切换间隙：在两个天线采样周期间插入 NUM_SWITCH_GAP_SAMPLES 个空白采样（用 0 填充）
    gap_samples = np.zeros(NUM_SWITCH_GAP_SAMPLES, dtype=complex)
    iq_data_sequence.extend(gap_samples)

if __name__ == "__main__":
    # 将 IQ 数据序列转换为 numpy 数组
    iq_data_sequence = np.array(iq_data_sequence)

    # 构造整个采样序列的全局时间轴
    total_samples = len(iq_data_sequence)
    global_time_axis = np.arange(total_samples) * SAMPLE_PERIOD  # 单位：秒

    # ========== 绘图展示 ==========

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(global_time_axis * 1e6, np.real(iq_data_sequence), 'b-o')
    plt.xlabel("时间 (μs)")
    plt.ylabel("实部")
    plt.title("IQ 数据序列 - 实部")
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(global_time_axis * 1e6, np.imag(iq_data_sequence), 'r-o')
    plt.xlabel("时间 (μs)")
    plt.ylabel("虚部")
    plt.title("IQ 数据序列 - 虚部")
    plt.grid()

    plt.tight_layout()
    plt.show()
