import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 创建一个图形对象
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 设置平面方程：ax + by + cz = d
# 平面1：x + y + z = 6
# 平面2：x - y + z = 2
# 平面3：2x + y - z = 3

# 创建网格数据
x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)
X, Y = np.meshgrid(x, y)

# 根据平面方程计算Z值
Z1 = 6 - X - Y        # 平面1：x + y + z = 6  ==>  z = 6 - x - y
Z2 = 2 - 1.5*X + Y        # 平面2：x - y + z = 2  ==>  z = 2 - x + y
Z3 = 3 - 2*X - Y      # 平面3：2x + y - z = 3 ==>  z = 3 - 2x - y

# 绘制平面
ax.plot_surface(X, Y, Z1, alpha=0.5, rstride=100, cstride=100, color='r', edgecolors='r', label="Plane 1")
ax.plot_surface(X, Y, Z2, alpha=0.5, rstride=100, cstride=100, color='g', edgecolors='g', label="Plane 2")
ax.plot_surface(X, Y, Z3, alpha=0.5, rstride=100, cstride=100, color='b', edgecolors='b', label="Plane 3")

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 设置图形显示范围
ax.set_xlim([-15, 15])
ax.set_ylim([-15, 15])
ax.set_zlim([-15, 15])

# 添加图例
ax.legend()

# 显示图形
plt.show()
