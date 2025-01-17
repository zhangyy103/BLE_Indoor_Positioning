import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, atan2

# 基站位置 (x, y, z)，假设所有基站位于天花板上，z = 1000
# 3000 * 3000 * 3000 空间内的9个基站
stations = np.array([
    [   0.0,    0.0,  3000.0],  # 基站 1 (天花板左下角)
    [3000.0,    0.0,  3000.0],  # 基站 2 (天花板右下角)
    [   0.0, 3000.0,  3000.0],  # 基站 3 (天花板左上角)
    [3000.0, 3000.0,  3000.0],  # 基站 4 (天花板右上角)
    [1500.0,    0.0,  3000.0],  # 基站 5 (天花板下边中点)
    [1500.0, 3000.0,  3000.0],  # 基站 6 (天花板上边中点)
    [   0.0, 1500.0,  3000.0],  # 基站 7 (天花板左边中点)
    [3000.0, 1500.0,  3000.0]   # 基站 8 (天花板右边中点)
])

stations_with_antennas = np.array([
    stations[0] + [1, 0, 0],
    stations[0] + [-1, 0, 0],
    stations[1] + [1, 0, 0],
    stations[1] + [-1, 0, 0],
    stations[2] + [1, 0, 0],
    stations[2] + [-1, 0, 0],
    stations[3] + [1, 0, 0],
    stations[3] + [-1, 0, 0],
    stations[4] + [1, 0, 0],
    stations[4] + [-1, 0, 0],
    stations[5] + [1, 0, 0],
    stations[5] + [-1, 0, 0],
    stations[6] + [1, 0, 0],
    stations[6] + [-1, 0, 0],
    stations[7] + [1, 0, 0],
    stations[7] + [-1, 0, 0],
])

# 目标设备的真实位置（随机生成在1000x1000x1000空间内）
true_position = np.random.uniform(0, 1000, 3)


# 计算目标设备在每个基站的接收AOA角度
def calculate_aoa(station, target_position):
    dx = target_position[0] - station[0]
    dy = target_position[1] - station[1]
    dz = target_position[2] - station[2]

    # 计算AOA角度
    horizontal_distance = np.sqrt(dx ** 2 + dy ** 2)
    horizontal_aoa = np.arctan2(dy, dx)  # 水平角度 (azimuth)
    vertical_aoa = np.arctan2(dz, horizontal_distance)  # 垂直角度 (elevation)

    return horizontal_aoa, vertical_aoa


# 获取每个基站的AOA
def get_aoas(stations, true_position):
    aoas = []
    for station in stations:
        horizontal_aoa, vertical_aoa = calculate_aoa(station, true_position)
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
    # 我们通过求解两个向量的线性组合来计算交点。该方法需要解决一个线性方程组。
    # 使用numpy.linalg.lstsq来求解
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
plt.savefig('../assets/antenna_arrays.svg')
#plt.show()
