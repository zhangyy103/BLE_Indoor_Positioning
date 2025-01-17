"""
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

"""

import numpy as np
import antenna_arrays_with_errors as foo
import matplotlib.pyplot as plt

# 定义粒子滤波器类
class ParticleFilter:
    def __init__(self, num_particles, initial_state, state_transition_std, measurement_noise_std, vertical_noise_std, stations):
        self.num_particles = num_particles  # 粒子数量
        self.particles = np.repeat(initial_state[None, :], num_particles, axis=0)  # 初始粒子集合
        self.weights = np.ones(num_particles) / num_particles  # 初始权重
        self.state_transition_std = state_transition_std  # 状态转移模型的标准差
        self.measurement_noise_std = measurement_noise_std  # 水平方向测量噪声标准差
        self.vertical_noise_std = vertical_noise_std  # 垂直方向测量噪声标准差
        self.stations = stations  # 基站位置

    # 预测步骤
    def predict(self):
        # 状态转移模型，假设简单的随机游走模型
        noise = np.random.normal(0, self.state_transition_std, size=self.particles.shape)
        self.particles += noise

    # 更新步骤
    def update(self, measurements):
        weights = np.ones(self.num_particles)
        for i, station in enumerate(self.stations):
            dx = self.particles[:, 0] - station[0]
            dy = self.particles[:, 1] - station[1]
            dz = self.particles[:, 2] - station[2]
            horizontal_distance = np.sqrt(dx ** 2 + dy ** 2)
            horizontal_aoa = np.arctan2(dy, dx)
            vertical_aoa = np.arctan2(dz, horizontal_distance)

            # 计算测量值的似然（高斯分布）
            horizontal_measurement = measurements[2 * i]
            vertical_measurement = measurements[2 * i + 1]

            horizontal_error = horizontal_measurement - horizontal_aoa
            vertical_error = vertical_measurement - vertical_aoa

            # 确保角度误差在[-pi, pi]内
            horizontal_error = (horizontal_error + np.pi) % (2 * np.pi) - np.pi
            vertical_error = (vertical_error + np.pi) % (2 * np.pi) - np.pi

            # 计算概率密度
            horizontal_prob = (1 / (np.sqrt(2 * np.pi) * self.measurement_noise_std)) * \
                              np.exp(-0.5 * (horizontal_error / self.measurement_noise_std) ** 2)
            vertical_prob = (1 / (np.sqrt(2 * np.pi) * self.vertical_noise_std)) * \
                            np.exp(-0.5 * (vertical_error / self.vertical_noise_std) ** 2)

            # 更新权重
            weights *= horizontal_prob * vertical_prob

        # 处理数值问题，防止权重为零
        weights += 1.e-300
        self.weights = weights / np.sum(weights)

    # 重采样步骤
    def resample(self):
        cumulative_sum = np.cumsum(self.weights)
        cumulative_sum[-1] = 1.  # 避免累积误差
        indexes = np.searchsorted(cumulative_sum, np.random.rand(self.num_particles))

        # 重置粒子和权重
        self.particles = self.particles[indexes]
        self.weights.fill(1.0 / self.num_particles)

    # 估计状态
    def estimate(self):
        # 使用粒子的加权平均作为估计值
        return np.average(self.particles, weights=self.weights, axis=0)

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

def particle_filter():
    # 粒子滤波器参数
    num_particles = 1000  # 粒子数量
    initial_position = foo.triangulate_position(foo.stations_with_antennas, foo.get_aoas(foo.stations_with_antennas, foo.true_position))
    initial_state = initial_position  # 初始状态，只包含位置，不考虑速度

    state_transition_std = np.array([1.0, 1.0, 1.0])  # 状态转移标准差（过程噪声）
    measurement_noise_std = np.radians(0.0010)  # 水平测量噪声标准差
    vertical_noise_std = np.radians(0.01)  # 垂直测量噪声标准差

    # 初始化粒子滤波器
    pf = ParticleFilter(num_particles, initial_state, state_transition_std, measurement_noise_std, vertical_noise_std, foo.stations_with_antennas)

    num_iterations = 10  # 迭代次数

    for _ in range(num_iterations):
        # 预测步骤
        pf.predict()

        # 获取测量值（模拟真实测量）
        measurements = simulate_measurements(foo.stations_with_antennas, foo.true_position, measurement_noise_std, vertical_noise_std)

        # 更新步骤
        pf.update(measurements)

        # 重采样步骤
        pf.resample()

    # 估计状态
    estimated_position = pf.estimate()

    return estimated_position

if __name__ == '__main__':

    estimated_position = particle_filter()

    print("Estimated Position:", estimated_position)
    print("True Position:", foo.true_position)
    # 计算误差
    error = np.linalg.norm(estimated_position - foo.true_position)
    print("Error:", error)

    # 可视化结果
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制基站位置
    ax.scatter(foo.stations[:, 0], foo.stations[:, 1], foo.stations[:, 2], c='r', label='Stations')

    # 绘制真实位置
    ax.scatter(foo.true_position[0], foo.true_position[1], foo.true_position[2], c='g', label='True Position')

    # 绘制估算位置
    ax.scatter(estimated_position[0], estimated_position[1], estimated_position[2], c='b', label='Estimated Position')

    # 设置图形标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    plt.savefig('../assets/particle_antenna_arrays.png')
    plt.close()

    errors = []
    positions = []

    # 假设这个循环中进行位置估算并计算误差
    for _ in range(1000):
        estimated_position = particle_filter()
        positions.append(estimated_position)
        error = np.linalg.norm(estimated_position - foo.true_position)
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

    plt.savefig('../assets/particle_antenna_arrays_distribution.png')
    plt.close()

    # 绘制误差与真实值的关系，拉长图像呈曲线
    plt.figure(dpi=600)
    plt.figure(figsize=(24, 6))  # 拉长图像，增加图像宽度
    plt.plot(errors, 'r-', linewidth=1.5)  # 设置红色折线，增加线宽
    plt.xlabel('Simulation Iteration')
    plt.ylabel('Position Error (m)')
    plt.title('Position Estimation Error')

    # 自动调整布局以避免内容重叠
    plt.tight_layout()
    plt.savefig('../assets/particle_antenna_arrays_curve.png')

    plt.close()
