import numpy as np
import matplotlib.pyplot as plt
plt.rc("font", family='Microsoft YaHei')

# 信号传播速度和频率设置
speed = 3e8  # 信号传播速度 (米/秒)
frequency = 2.4e9  # 信号频率 (赫兹)
wavelength = speed / frequency  # 波长
pre_phase = 0  # 信号初始相位

# 基站和标签位置
base_station1_position = np.array([500, 500])  # 基站1位置 (x, y)
base_station2_position = np.array([-500, 835])  # 基站2位置 (x, y)
tag_position = np.array([2999, -500])  # 标签位置 (x, y)

# 打印基站和标签的位置
print(f"基站1位置: {base_station1_position}")
print(f"基站2位置: {base_station2_position}")
print(f"标签位置: {tag_position}")

# 基站天线设置
antenna_distance = 0.5  # 两个天线之间的距离
antenna1r_position = base_station1_position + np.array([-antenna_distance / 2, 0])
antenna1l_position = base_station1_position + np.array([antenna_distance / 2, 0])

antenna2r_position = base_station2_position + np.array([-antenna_distance / 2, 0])
antenna2l_position = base_station2_position + np.array([antenna_distance / 2, 0])

# 计算到达基站天线的距离和相位
tag_to_antenna1r_distance = np.linalg.norm(tag_position - antenna1r_position)
tag_to_antenna1l_distance = np.linalg.norm(tag_position - antenna1l_position)
tag_to_antenna2r_distance = np.linalg.norm(tag_position - antenna2r_position)
tag_to_antenna2l_distance = np.linalg.norm(tag_position - antenna2l_position)

# 计算传播时间
tag_to_antenna1r_time = tag_to_antenna1r_distance / speed
tag_to_antenna1l_time = tag_to_antenna1l_distance / speed
tag_to_antenna2r_time = tag_to_antenna2r_distance / speed
tag_to_antenna2l_time = tag_to_antenna2l_distance / speed

# 计算相位
tag_to_antenna1r_phase = 2 * np.pi * frequency * tag_to_antenna1r_time + pre_phase
tag_to_antenna1l_phase = 2 * np.pi * frequency * tag_to_antenna1l_time + pre_phase
tag_to_antenna2r_phase = 2 * np.pi * frequency * tag_to_antenna2r_time + pre_phase
tag_to_antenna2l_phase = 2 * np.pi * frequency * tag_to_antenna2l_time + pre_phase

# 计算相位差
phase_diff1 = tag_to_antenna1l_phase - tag_to_antenna1r_phase
phase_diff2 = tag_to_antenna2l_phase - tag_to_antenna2r_phase

# 计算 AOA
aoa1 = np.degrees(np.arcsin((phase_diff1 * wavelength) / (2 * np.pi * antenna_distance)))
aoa2 = np.degrees(np.arcsin((phase_diff2 * wavelength) / (2 * np.pi * antenna_distance)))

"""
aoa1 = (90 + aoa1) % 360 - 180
aoa2 = (90 + aoa2) % 360 - 180
"""
# 调整坐标系的角度
aoa1 = (90 - aoa1)  # 将AOA调整为从北方顺时针方向
aoa2 = (90 - aoa2)  # 将AOA调整为从北方顺时针方向

# 输出 AOA
print(f"基站1 AOA: {aoa1:.2f} 度")
print(f"基站2 AOA: {aoa2:.2f} 度")

# 通过 AOA 计算交点位置
def calculate_intersection(aoa1, aoa2, base_station1_pos, base_station2_pos):
    # 将角度转化为弧度
    theta1 = np.radians(aoa1)
    theta2 = np.radians(aoa2)

    # 基站1到交点的方向向量
    dir_vector1 = np.array([np.cos(theta1), np.sin(theta1)])
    # 基站2到交点的方向向量
    dir_vector2 = np.array([np.cos(theta2), np.sin(theta2)])

    # 计算交点
    A = np.array([dir_vector1, -dir_vector2]).T
    b = base_station2_pos - base_station1_pos
    t_vals = np.linalg.solve(A, b)

    # 根据t值计算交点
    intersection_point = base_station1_pos + t_vals[0] * dir_vector1

    return intersection_point, dir_vector1, dir_vector2

# 计算交点及方向向量
intersection, dir_vector1, dir_vector2 = calculate_intersection(aoa1, aoa2, base_station1_position, base_station2_position)
print(f"标签估计位置: {intersection}")

# 绘制结果
plt.figure(figsize=(6, 6))
plt.plot(base_station1_position[0], base_station1_position[1], 'bo', label="基站1")
plt.plot(base_station2_position[0], base_station2_position[1], 'go', label="基站2")
plt.plot(tag_position[0], tag_position[1], 'rx', label="实际标签位置")
plt.plot(intersection[0], intersection[1], 'kx', label="估计标签位置")

# 绘制基站1和基站2的方向射线
line_range = 1500  # 射线延伸的长度
plt.plot([base_station1_position[0], base_station1_position[0] + dir_vector1[0] * line_range],
         [base_station1_position[1], base_station1_position[1] + dir_vector1[1] * line_range],
         'b--', label="基站1方向射线")

plt.plot([base_station2_position[0], base_station2_position[0] + dir_vector2[0] * line_range],
         [base_station2_position[1], base_station2_position[1] + dir_vector2[1] * line_range],
         'g--', label="基站2方向射线")

plt.xlim(-3000, 3000)
plt.ylim(-3000, 3000)
plt.grid(True)
plt.legend()
plt.title("标签位置估计与基站方向射线")
plt.show()

