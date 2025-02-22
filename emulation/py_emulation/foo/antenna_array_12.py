import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 已有仿真 IQ 数据代码（你已运行，下述变量已定义）
# ==============================
# 参数定义
FREQ = 250e3              # CTE 信号频率 (Hz)
C = 3e8                   # 光速 (m/s)
LAMBDA = C / FREQ         # 波长 (m)
D = LAMBDA / 4            # 单位间距 (天线间距, a = λ/4)
SAMPLING_RATE = 2e6       # 采样率 2 MHz
SAMPLE_PERIOD = 1 / SAMPLING_RATE  # 采样周期 (0.5 μs)
NUM_SAMPLES_PER_ANTENNA = 4        # 每个天线有效采样点数 (2 μs 对应 4 个点)
NUM_SWITCH_GAP_SAMPLES = 4         # 天线切换间隙丢弃的采样点数 (2 μs)
TOTAL_SAMPLES_PER_CYCLE = NUM_SAMPLES_PER_ANTENNA + NUM_SWITCH_GAP_SAMPLES  # 每个天线周期总采样点数 = 8

# 天线阵列位置（单位：m，注意：a = λ/4）
antenna_positions = np.array([
    [-3 * D,  3 * D, 0],
    [-1 * D,  3 * D, 0],
    [ 1 * D,  3 * D, 0],
    [ 3 * D,  3 * D, 0],
    [-3 * D,  1 * D, 0],
    [ 3 * D,  1 * D, 0],
    [-3 * D, -1 * D, 0],
    [ 3 * D, -1 * D, 0],
    [-3 * D, -3 * D, 0],
    [-1 * D, -3 * D, 0],
    [ 1 * D, -3 * D, 0],
    [ 3 * D, -3 * D, 0]
])
M = antenna_positions.shape[0]  # 天线数 = 12

# 目标位置（仿真时设定），例如：目标位于 (10a, 10a, 0)
target_position = np.array([10 * D, 10 * D, 0])
print("真实目标位置 (m):", target_position)

# 仿真 IQ 数据的生成代码（与之前一致）：
# 计算各天线到目标的欧几里得距离
distances = np.linalg.norm(antenna_positions - target_position, axis=1)
# 计算各天线初始相位（取模 2π，不考虑负号）
phases = (2 * np.pi * distances / LAMBDA) % (2 * np.pi)

# 显示各天线距离和初始相位
print("各天线到目标距离 (m):")
print(distances)
print("各天线初始相位 (rad):")
print(phases)

# 生成每个天线采样的相对时间轴（4 个采样点：0, 0.5, 1, 1.5 μs）
time_axis = np.arange(NUM_SAMPLES_PER_ANTENNA) * SAMPLE_PERIOD  # 单位：秒

# 初始化存储 IQ 数据序列的列表
iq_data_sequence = []

# 发送信号功率 (dB)
TX_POWER_DB = -1  # 发送信号功率 (dB)
# fspl_const 为 FSPL 中常数部分：20*log10(4π/C)
fspl_const = 20 * np.log10(4 * np.pi / C)

# 遍历每个天线生成其 IQ 数据
for i in range(len(antenna_positions)):
    distance = distances[i]
    init_phase = phases[i]
    # 计算自由空间路径损耗 FSPL (dB)
    fspl_db = 20 * np.log10(distance) + 20 * np.log10(FREQ) + fspl_const
    # 接收功率 (dB)
    rx_power_db = TX_POWER_DB - fspl_db
    # 换算为线性幅度
    amplitude = 10 ** (rx_power_db / 20)
    # 为模拟各天线采样时存在时隙，设置全局时间偏移
    antenna_time_offset = i * TOTAL_SAMPLES_PER_CYCLE * SAMPLE_PERIOD
    t_samples = time_axis + antenna_time_offset
    # 生成 IQ 数据：IQ = A * exp{j [ 初始相位 + 2π*FREQ*(全局采样时刻) ]}
    iq_samples = amplitude * np.exp(1j * (init_phase + 2 * np.pi * FREQ * t_samples))
    # 加入当前天线有效采样点（4 个点）
    iq_data_sequence.extend(iq_samples)
    # 模拟天线切换间隙：插入 4 个零值
    gap_samples = np.zeros(NUM_SWITCH_GAP_SAMPLES, dtype=complex)
    iq_data_sequence.extend(gap_samples)

# 将 IQ 数据序列转换为 numpy 数组
iq_data_sequence = np.array(iq_data_sequence)

# 可选：绘制 IQ 数据时域图（实部、虚部）
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(np.arange(len(iq_data_sequence))*SAMPLE_PERIOD*1e6, np.real(iq_data_sequence), 'b-o')
plt.xlabel("时间 (μs)")
plt.ylabel("实部")
plt.title("IQ 数据序列 - 实部")
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(np.arange(len(iq_data_sequence))*SAMPLE_PERIOD*1e6, np.imag(iq_data_sequence), 'r-o')
plt.xlabel("时间 (μs)")
plt.ylabel("虚部")
plt.title("IQ 数据序列 - 虚部")
plt.grid()
plt.tight_layout()
plt.show()


# =====================================================
# 以下部分使用 MUSIC 算法进行 3D 定位（AOA 联合定位）
# =====================================================

# --- 1. 构造快拍矩阵 ---
# 每个天线有效采样点为前 4 个采样点，排列成矩阵 X (M x N_snapshots)
N_snapshots = NUM_SAMPLES_PER_ANTENNA  # 快拍数（4个）
X = np.zeros((M, N_snapshots), dtype=complex)
for m in range(M):
    start_index = m * TOTAL_SAMPLES_PER_CYCLE
    X[m, :] = iq_data_sequence[start_index : start_index + NUM_SAMPLES_PER_ANTENNA]

# --- 2. 计算空间协方差矩阵 R ---
R = X @ X.conj().T / N_snapshots  # 形状为 (M, M)

# --- 3. 对 R 进行特征分解，构造噪声子空间 ---
eigvals, eigvecs = np.linalg.eig(R)
# 由于 R 为 Hermitian（对称矩阵），特征值均为实数；按从小到大排序
idx = np.argsort(eigvals.real)
eigvals_sorted = eigvals[idx].real
eigvecs_sorted = eigvecs[:, idx]

# 假设信号数 d = 1，则噪声子空间维数为 M - 1
d = 1
En = eigvecs_sorted[:, :M - d]  # 噪声子空间矩阵，尺寸 (M, M-d)

# --- 4. 定义近场 steering vector 函数 ---
def steering_vector(r, sensor_positions, wavelength):
    """
    计算候选目标位置 r 对应的近场 steering vector
    使用参考天线（第 0 个天线）去除共模相位影响

    参数：
      r: 候选目标位置，形状 (3,)
      sensor_positions: 天线位置数组，形状 (M, 3)
      wavelength: 信号波长
    返回：
      a: steering vector，形状 (M,)
    """
    # 计算每个天线到候选目标 r 的距离
    dists = np.linalg.norm(sensor_positions - r, axis=1)
    # 以第 0 个天线为参考，计算相对距离差
    d_ref = dists[0]
    a = np.exp(-1j * 2 * np.pi / wavelength * (dists - d_ref))
    return a

# --- 5. 在 3D 空间中进行网格搜索，计算 MUSIC 伪谱 ---
# 定义搜索区域：这里以真实目标附近为例，可根据实际情况调整搜索范围和步长
# 注意：由于天线均在 z=0 平面，z 方向分辨率较低；但本例目标 z=0
delta = 100  # 搜索范围扩展量（单位：m）
step = 50    # 网格步长（单位：m）
x_min = target_position[0] - delta
x_max = target_position[0] + delta
y_min = target_position[1] - delta
y_max = target_position[1] + delta
z_min = -delta
z_max = delta

x_range = np.arange(x_min, x_max + step, step)
y_range = np.arange(y_min, y_max + step, step)
z_range = np.arange(z_min, z_max + step, step)

# 初始化 MUSIC 谱值存储数组（3D 网格）
P_music = np.zeros((len(x_range), len(y_range), len(z_range)))

# 对每个候选位置 r=(x,y,z) 计算 steering vector 和 MUSIC 伪谱值
for ix, x in enumerate(x_range):
    for iy, y in enumerate(y_range):
        for iz, z in enumerate(z_range):
            r_candidate = np.array([x, y, z])
            a_candidate = steering_vector(r_candidate, antenna_positions, LAMBDA)
            # MUSIC 伪谱：P(r) = 1 / || En^H * a_candidate ||^2
            denom = np.linalg.norm(En.conj().T @ a_candidate)**2
            # 为防止除零，加上一个小值
            P_music[ix, iy, iz] = 1 / (denom + 1e-12)

# --- 6. 找到 MUSIC 伪谱的最大值，对应的候选位置即为目标位置的估计值 ---
max_idx = np.unravel_index(np.argmax(P_music), P_music.shape)
est_x = x_range[max_idx[0]]
est_y = y_range[max_idx[1]]
est_z = z_range[max_idx[2]]
estimated_position = np.array([est_x, est_y, est_z])
print("Estimated target position (m):", estimated_position)
print("True target position (m):     ", target_position)

# --- 7. 绘制某一截面（例如 z=0）上的 MUSIC 伪谱等高图 ---
# 选取 z=0 对应的层（若 z=0不在网格上，则选择离 0 最近的那一层）
z_idx = np.argmin(np.abs(z_range - 0))
plt.figure(figsize=(8,6))
# P_music 的第一个维度对应 x，第二维度对应 y
plt.contourf(x_range, y_range, P_music[:, :, z_idx].T, 50, cmap='jet')
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title("MUSIC Spectrum (z = {:.1f} m)".format(z_range[z_idx]))
plt.colorbar(label="Spectrum Value")
plt.scatter(target_position[0], target_position[1], c='w', marker='x', s=100, label="True Position")
plt.scatter(estimated_position[0], estimated_position[1], c='k', marker='o', s=100, label="Estimated Position")
plt.legend()
plt.show()
