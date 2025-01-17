"""
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
plt.savefig('../assets/antenna_with_errors.png')
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

plt.savefig('../assets/antenna_with_errors_distribution.png')
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
plt.savefig('../assets/antenna_with_errors_curve.png')
#plt.show()

plt.close()

"""

import antenna_arrays_with_errors as foo
import numpy as np
import matplotlib.pyplot as plt

# 初始化EKF
def initialize_kalman_filter(initial_state, process_noise_cov, measurement_noise_cov):
    x = np.array(initial_state)  # 状态向量：[x, y, z, vx, vy, vz]
    P = np.eye(6) * 1000  # 初始协方差矩阵
    Q = process_noise_cov  # 过程噪声协方差矩阵
    R = measurement_noise_cov  # 测量噪声协方差矩阵
    return x, P, Q, R

# 预测步骤
def predict(x, P, Q, dt):
    # 状态转移矩阵
    F = np.eye(6)
    F[0, 3] = dt
    F[1, 4] = dt
    F[2, 5] = dt

    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    return x_pred, P_pred

# 更新步骤（EKF）
def update(x_pred, P_pred, z, stations, R):
    # 组合所有测量
    def h(x):
        hx = []
        for station in stations:
            dx = x[0] - station[0]
            dy = x[1] - station[1]
            dz = x[2] - station[2]
            horizontal_distance = np.sqrt(dx ** 2 + dy ** 2)
            horizontal_aoa = np.arctan2(dy, dx)
            vertical_aoa = np.arctan2(dz, horizontal_distance)
            hx.extend([horizontal_aoa, vertical_aoa])
        return np.array(hx)

    # 计算雅可比矩阵
    def jacobian(x):
        H = []
        for station in stations:
            dx = x[0] - station[0]
            dy = x[1] - station[1]
            dz = x[2] - station[2]

            r_squared = dx**2 + dy**2 + dz**2
            horizontal_distance_sq = dx**2 + dy**2
            horizontal_distance = np.sqrt(horizontal_distance_sq)

            # 避免除以零
            epsilon = 1e-6
            if horizontal_distance_sq < epsilon:
                horizontal_distance_sq = epsilon
            if r_squared < epsilon:
                r_squared = epsilon
            if horizontal_distance < epsilon:
                horizontal_distance = epsilon

            # 水平AOA对状态的偏导数
            dh_dxh = -dy / horizontal_distance_sq
            dh_dyh = dx / horizontal_distance_sq
            dh_dzh = 0

            # 垂直AOA对状态的偏导数
            dv_dxh = -(dx * dz) / (r_squared * horizontal_distance)
            dv_dyh = -(dy * dz) / (r_squared * horizontal_distance)
            dv_dzh = horizontal_distance / r_squared

            H_row_h = [dh_dxh, dh_dyh, dh_dzh, 0, 0, 0]
            H_row_v = [dv_dxh, dv_dyh, dv_dzh, 0, 0, 0]
            H.extend([H_row_h, H_row_v])
        return np.array(H)

    hx = h(x_pred)
    H = jacobian(x_pred)

    # 计算测量残差
    y = z - hx
    # 角度归一化到[-pi, pi]
    y = (y + np.pi) % (2 * np.pi) - np.pi

    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ np.linalg.inv(S)

    x_upd = x_pred + K @ y
    P_upd = (np.eye(len(x_pred)) - K @ H) @ P_pred
    return x_upd, P_upd

# 模拟测量值
def simulate_measurements(stations, true_position, noise_std, vertical_noise_std):
    measurements = []
    for station in stations:
        dx = true_position[0] - station[0]
        dy = true_position[1] - station[1]
        dz = true_position[2] - station[2]
        horizontal_distance = np.sqrt(dx ** 2 + dy ** 2)
        horizontal_aoa = np.arctan2(dy, dx)
        vertical_aoa = np.arctan2(dz, horizontal_distance)

        # 加入噪声
        horizontal_aoa += np.random.normal(0, noise_std)
        vertical_aoa += np.random.normal(0, vertical_noise_std)

        measurements.extend([horizontal_aoa, vertical_aoa])
    return np.array(measurements)

def kalman_filter():
    # 初始状态：[位置，速度]
    initial_position = foo.triangulate_position(foo.stations_with_antennas, foo.get_aoas(foo.stations_with_antennas, foo.true_position))
    initial_velocity = np.array([0, 0, 0])  # 假设初始速度为0
    initial_state = np.hstack((initial_position, initial_velocity))

    # 增大过程噪声协方差矩阵Q
    process_noise_cov = np.diag([1, 1, 1, 1, 1, 1]) * 1.0

    # 调整测量噪声协方差矩阵R
    noise_std = np.radians(0.0010)  # 水平角度噪声标准差
    vertical_noise_std = np.radians(0.01)   # 增大垂直角度噪声标准差
    R_elements = []
    for _ in range(len(foo.stations_with_antennas)):
        R_elements.extend([noise_std**2, vertical_noise_std**2])
    measurement_noise_cov = np.diag(R_elements)

    # 时间步长
    dt = 1.0

    x, P, Q, R = initialize_kalman_filter(initial_state, process_noise_cov, measurement_noise_cov)

    num_iterations = 10

    for _ in range(num_iterations):
        # 预测步骤
        x_pred, P_pred = predict(x, P, Q, dt)

        # 获取测量值（模拟真实测量）
        z = simulate_measurements(foo.stations_with_antennas, foo.true_position, noise_std, vertical_noise_std)

        # 更新步骤
        x, P = update(x_pred, P_pred, z, foo.stations_with_antennas, R)

    return x


if __name__ == '__main__':
    x = kalman_filter()

    print("Estimated Position:", x[:3])
    print("True Position:", foo.true_position)
    print("Error:", np.linalg.norm(foo.true_position - x[:3]))

    # 可视化结果
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制基站位置
    ax.scatter(foo.stations[:, 0], foo.stations[:, 1], foo.stations[:, 2], c='r', label='Stations')

    # 绘制真实位置
    ax.scatter(foo.true_position[0], foo.true_position[1], foo.true_position[2], c='g', label='True Position')

    # 绘制估算位置
    ax.scatter(x[0], x[1], x[2], c='b', label='Estimated Position')

    # 设置图形标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    plt.savefig('../assets/kalman_antenna_arrays.png')
    plt.close()

    errors = []
    positions = []

    # 假设这个循环中进行位置估算并计算误差
    for _ in range(1000):
        x = kalman_filter()
        positions.append(x[:3])
        error = np.linalg.norm(foo.true_position - x[:3])
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
    ax.scatter(foo.true_position[0], foo.true_position[1], foo.true_position[2], c='r', label='True Position')
    ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], s=0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Position Estimation Distribution')

    plt.savefig('../assets/kalman_antenna_arrays_distribution.png')
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
    plt.savefig('../assets/kalman_antenna_arrays_curve.png')

    plt.close()
