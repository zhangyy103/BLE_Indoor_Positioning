import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
plt.rc("font", family='Microsoft YaHei', size=12)

# 数据
techniques = ["WiFi", "蓝牙 AOA", "UWB", "RSSI"]
accuracy = [1/2, 1/0.33, 1/0.3, 1/1]   # 各技术的精度（米）
cost = [1/2.6, 1/2, 1/4, 1/2/5]          # 成本（相对）

# 创建柱状图的位置
x = np.arange(len(techniques))
width = 0.35  # 柱状图宽度

fig, ax1 = plt.subplots(figsize=(10, 6))

# 左侧y轴：精度
bar1 = ax1.bar(x - width/2, [0]*len(accuracy), width, label='Accuracy (1/m)', color='skyblue')
ax1.set_ylabel('Accuracy (1/meters)')
ax1.set_ylim(0, max(accuracy) + 1)
ax1.set_xticks(x)
ax1.set_xticklabels(techniques)

# 右侧y轴：成本
ax2 = ax1.twinx()
bar2 = ax2.bar(x + width/2, [0]*len(cost), width, label='Cost (relative)', color='salmon')
ax2.set_ylabel('Cost (relative)')
ax2.set_ylim(0, max(cost) + 0.2)

# 图例
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

# 标题
plt.title("Accuracy and Cost")

# 动画更新函数
def update(frame):
    # 计算当前帧的插值，模拟从慢到快的加速效果
    frame_ratio = (frame / 100) ** 2  # 使用平方函数使速度从慢到快
    for b1, a in zip(bar1, accuracy):
        b1.set_height(a * frame_ratio)
    for b2, c in zip(bar2, cost):
        b2.set_height(c * frame_ratio)
    return bar1 + bar2

# 创建动画，frames=100表示100帧，interval=10表示每帧10毫秒
ani = animation.FuncAnimation(fig, update, frames=100, interval=10, repeat=False)

# 保存动画
ani.save("indoor_positioning_comparison_slow_to_fast.gif", writer="pillow", fps=100)

# 保存图表
plt.savefig("../assets/indoor_positioning_comparison.png")
# 显示图表
plt.show()