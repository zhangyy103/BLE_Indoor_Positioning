import numpy as np

# ========== 物理参数 ==========
FREQ = 2.4e9  # CTE 频率 (Hz)
C = 3e8  # 光速 (m/s)
LAMBDA = C / FREQ  # 波长 (m)
D = LAMBDA / 4  # 天线间距
NUM_ANTENNAS = 12  # 天线数量
NUM_SAMPLES_PER_ANTENNA = 4  # 每个天线采 4 个 IQ 样点

# ========== 目标位置 ==========
target_position = np.array([50 * D, 50 * D, 50 * D])

# ========== 天线阵列布局 ==========
antenna_positions = np.array([
    [-3 * D, 3 * D, 0], [-1 * D, 3 * D, 0], [1 * D, 3 * D, 0], [3 * D, 3 * D, 0],
    [-3 * D, 1 * D, 0], [3 * D, 1 * D, 0],
    [-3 * D, -1 * D, 0], [3 * D, -1 * D, 0],
    [-3 * D, -3 * D, 0], [-1 * D, -3 * D, 0], [1 * D, -3 * D, 0], [3 * D, -3 * D, 0]
])


# ========== 计算 IQ 数据 ==========
def generate_iq_data():
    distances = np.linalg.norm(antenna_positions - target_position, axis=1)
    phases = (2 * np.pi * distances / LAMBDA) % (2 * np.pi)

    iq_matrix = np.zeros((NUM_ANTENNAS, NUM_SAMPLES_PER_ANTENNA), dtype=complex)

    for i in range(NUM_ANTENNAS):
        phase_shift = phases[i]
        iq_matrix[i, :] = np.exp(1j * phase_shift)

    return iq_matrix


# ========== MUSIC 算法 ==========
def music_aoa_estimation(iq_matrix):
    # 计算协方差矩阵
    R = iq_matrix @ iq_matrix.conj().T / NUM_SAMPLES_PER_ANTENNA

    # 特征分解
    eigvals, eigvecs = np.linalg.eigh(R)
    noise_space = eigvecs[:, :-2]  # 选取噪声子空间（假设有 2 个信号源）

    # 角度扫描
    theta_scan = np.linspace(-90, 90, 181)  # AOA 角度范围
    phi_scan = np.linspace(-90, 90, 181)
    Pmusic = np.zeros((len(theta_scan), len(phi_scan)))

    for i, theta in enumerate(theta_scan):
        for j, phi in enumerate(phi_scan):
            sv = steering_vector(theta, phi)  # 计算导向矢量
            Pmusic[i, j] = 1 / np.abs(sv.conj().T @ noise_space @ noise_space.conj().T @ sv)

    # 找最大值点（即估计出的 AOA）
    max_idx = np.unravel_index(np.argmax(Pmusic), Pmusic.shape)
    aoa_theta = theta_scan[max_idx[0]]
    aoa_phi = phi_scan[max_idx[1]]

    return aoa_theta, aoa_phi


# ========== 计算导向矢量 ==========
def steering_vector(theta, phi):
    theta_rad = np.deg2rad(theta)
    phi_rad = np.deg2rad(phi)

    k = 2 * np.pi / LAMBDA
    wave_vector = k * np.array([np.sin(theta_rad) * np.cos(phi_rad),
                                np.sin(theta_rad) * np.sin(phi_rad),
                                np.cos(theta_rad)])

    sv = np.exp(1j * (antenna_positions @ wave_vector))  # 阵列响应向量
    return sv[:, np.newaxis]  # 变为列向量


# ========== 三角测量法计算坐标 ==========
def triangulate_position(aoa_theta, aoa_phi):
    aoa_theta_rad = np.deg2rad(aoa_theta)
    aoa_phi_rad = np.deg2rad(aoa_phi)

    # 设定已知基站位置 (0,0,0)，计算目标坐标
    r = 10 * D  # 目标估计距离
    x = r * np.sin(aoa_theta_rad) * np.cos(aoa_phi_rad)
    y = r * np.sin(aoa_theta_rad) * np.sin(aoa_phi_rad)
    z = r * np.cos(aoa_theta_rad)

    return np.array([x, y, z])


# ========== 主函数 ==========
if __name__ == "__main__":
    iq_data = generate_iq_data()
    aoa_theta, aoa_phi = music_aoa_estimation(iq_data)
    estimated_position = triangulate_position(aoa_theta, aoa_phi)

    print(f"目标真实坐标: {target_position}")
    print(f"估计的 AOA 角度: θ = {aoa_theta:.2f}°, φ = {aoa_phi:.2f}°")
    print(f"估计的目标坐标: {estimated_position}")
