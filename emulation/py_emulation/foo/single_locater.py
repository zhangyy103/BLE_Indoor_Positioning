import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin

# 基站位置 (x, y, z)，假设所有基站位于天花板上，z = 1000
stations = np.array([
    [0.0, 0.0, 3000.0],
])

stations_with_antennas = np.array([
    stations[0] + [1, 0, 0],
    stations[0] + [-1, 0, 0],
])

# 目标设备的真实位置（随机生成在1000x1000x1000空间内）
true_position = np.random.uniform(0, 1000, 3)

# 加入噪声的标准差，可以调整噪声的强度
noise_std = np.radians(0.0020)  # 水平角度噪声的标准差（单位：弧度）
vertical_noise_std = np.radians(0.0008)  # 垂直角度噪声的标准差（单位：弧度）

# 模拟反射路径的数量
num_reflections = 3  # 每个基站模拟3条反射路径

# 计算目标设备在每个基站的接收AOA角度
def calculate_aoa(station, target_position):
    dx = target_position[0] - station[0]
    dy = target_position[1] - station[1]
    dz = target_position[2] - station[2]

    # 计算AOA角度
    horizontal_distance = np.sqrt(dx ** 2 + dy ** 2)
    horizontal_aoa = np.arctan2(dy, dx)  # 水平角度 (azimuth)
    vertical_aoa = np.arctan2(dz, horizontal_distance)  # 垂直角度 (elevation)

    # 加入噪声（正态分布噪声）
    horizontal_aoa += np.random.normal(0, noise_std)  # 水平角度噪声
    vertical_aoa += np.random.normal(0, vertical_noise_std)  # 垂直角度噪声

    return horizontal_aoa, vertical_aoa

# 获取每个基站的AOA
def get_aoas(stations, true_position):
    aoas = []
    for station in stations:
        horizontal_aoa, vertical_aoa = calculate_aoa(station, true_position)
        for i in range(num_reflections):
            horizontal_aoa += np.random.normal(0, noise_std)
            vertical_aoa += np.random.normal(0, vertical_noise_std)
        aoas.append((horizontal_aoa, vertical_aoa))
    return aoas

# 计算两条射线的交点
def get_intersection(station1, aoa1, station2, aoa2):
    # 计算基站1的方向向量
    dx1 = cos(aoa1[1]) * cos(aoa1[0])  # x方向
    dy1 = cos(aoa1[1]) * sin(aoa1[0])  # y方向
    dz1 = sin(aoa1[1])  # z方向

    # 计算基站2的方向向量
    dx2 = cos(aoa2[1]) * cos(aoa2[0])
    dy2 = cos(aoa2[1]) * sin(aoa2[0])
    dz2 = sin(aoa2[1])

    # 射线方向向量
    v1 = np.array([dx1, dy1, dz1])
    v2 = np.array([dx2, dy2, dz2])

    # 计算基站之间的向量差
    station_diff = np.array([station2[0] - station1[0], station2[1] - station1[1], station2[2] - station1[2]])

    # 计算两射线交点
    A = np.array([v1, -v2]).T  # 构造线性方程组 A * t = station_diff
    t = np.linalg.lstsq(A, station_diff, rcond=None)[0]  # 解方程，得到t和s

    # 计算交点
    intersection = station1 + t[0] * v1  # 用t[0]来计算交点

    return intersection

# 使用多个基站的AOA信息来推算目标位置
def triangulate_position(stations, aoas):
    estimated_position = np.zeros(3)
    num_stations = len(stations)
    each_station = []

    # 计算每两个基站的交点
    for i in range(0, num_stations, 2):
        intersection = get_intersection(stations[i], aoas[i], stations[i+1], aoas[i+1])
        each_station.append(intersection)

    # 计算所有交点的平均值
    for station in each_station:
        estimated_position += station
    estimated_position /= len(each_station)
    return estimated_position

# 计算AOA角度
aoas = get_aoas(stations_with_antennas, true_position)

# 使用AOA来进行目标位置计算
estimated_position = triangulate_position(stations_with_antennas, aoas)

# 输出结果
print(f"真实位置: {true_position}")
print(f"估算位置: {estimated_position}")

# 计算估算误差
error = np.linalg.norm(true_position - estimated_position)
print(f"位置估算误差: {error} 米")

# 可视化结果
plt.figure(dpi=600)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制基站位置
ax.scatter(stations[:, 0], stations[:, 1], stations[:, 2], c='r', label='Stations')

# 绘制真实位置
ax.scatter(true_position[0], true_position[1], true_position[2], c='g', label='True Position')

# 绘制估算位置
ax.scatter(estimated_position[0], estimated_position[1], estimated_position[2], c='b', label='Estimated Position')

# 设置图形标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

# save
plt.savefig('../assets/single_antenna_with_errors.png')
#plt.show()

plt.close()

errors = []
positions = []

# 假设这个循环中进行位置估算并计算误差
for _ in range(1000):
    aoas = get_aoas(stations_with_antennas, true_position)
    estimated_position = triangulate_position(stations_with_antennas, aoas)
    positions.append(estimated_position)
    error = np.linalg.norm(true_position - estimated_position)
    errors.append(error)

# 计算平均误差
mean_error = np.mean(errors)
print(f"平均位置估算误差: {mean_error} 米")

# 绘制位置点的三维分布 减小点的大小
plt.figure(dpi=600)
positions = np.array(positions)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# 绘制真实位置
ax.scatter(true_position[0], true_position[1], true_position[2], c='r', label='True Position')
ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], s=0.5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Position Estimation Distribution')

plt.savefig('../assets/single_antenna_with_errors_distribution.png')
#plt.show()

plt.close()



# 绘制误差与真实值的关系，拉长图像呈曲线

plt.figure(dpi=600)
plt.figure(figsize=(24, 6))  # 拉长图像，增加图像宽度
plt.plot(errors, 'r-', linewidth=1.5)  # 设置红色折线，增加线宽
plt.xlabel('Simulation Iteration')
plt.ylabel('Position Error (m)')
plt.title('Position Estimation Error')
plt.grid(True)

# 自动调整布局以避免内容重叠
plt.tight_layout()
plt.savefig('../assets/single_antenna_with_errors_curve.png')
#plt.show()

plt.close()
