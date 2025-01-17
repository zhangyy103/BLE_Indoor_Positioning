import numpy as np
import matplotlib.pyplot as plt
plt.rc("font", family='Microsoft YaHei')

# 定义仿真参数
frequency = 2.4e9  # 蓝牙频率 (2.4 GHz)
wavelength = 3e8 / frequency  # 波长 (m)
antenna_distance = wavelength / 2  # 天线间距 (一般设置为波长的一半)

# 天线阵列坐标（假设正方形排列）
antenna_positions = np.array([
    [0, 0],
    [antenna_distance, 0],
    [0, antenna_distance],
    [antenna_distance, antenna_distance]
])

# 定义信号源的真实位置
source_position = np.array([5, 3])  # 随机设定在(5,3)处

# 计算信号源到每个天线的距离
distances = np.linalg.norm(antenna_positions - source_position, axis=1)

# 计算每个天线接收到的相位 (与距离成正比)
phases = (2 * np.pi / wavelength) * distances
phases = phases - phases[0]  # 归一化相位差，以第一个天线为参考
phase_shifts = phases[1:]  # 获取与第一个天线的相位差


# 使用最小二乘法估计信号源方向
def estimate_aoa(antenna_positions, phase_shifts):
    # 将天线位置转换为相对矢量（相对于第一个天线）
    relative_positions = antenna_positions[1:] - antenna_positions[0]

    # 提取相对位置的x和y坐标
    A = relative_positions[:, 0]
    B = relative_positions[:, 1]

    # 求解方位角 theta
    theta_est = np.arctan2(
        np.sum(B * phase_shifts),
        np.sum(A * phase_shifts)
    )
    return np.degrees(theta_est)


# 计算到达角（AOA）
aoa_estimate = estimate_aoa(antenna_positions, phase_shifts)
print(f"估计的AOA（方位角）: {aoa_estimate:.2f}°")

# 可视化天线和信号源
plt.figure(figsize=(6, 6))
plt.scatter(antenna_positions[:, 0], antenna_positions[:, 1], c='b', marker='o', label='天线位置')
plt.scatter(source_position[0], source_position[1], c='r', marker='x', label='信号源位置')
plt.legend()
plt.xlabel('X 位置 (m)')
plt.ylabel('Y 位置 (m)')
plt.title(f"AOA仿真 - 估计角度: {aoa_estimate:.2f}°")
plt.grid(True)
plt.axis('equal')
plt.show()
