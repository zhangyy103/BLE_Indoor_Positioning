"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import re

file_path = "C:\\Users\\32285\\OneDrive\\Desktop\\single_iq_sample.txt"

# 修正数据解析函数，处理文件中的IQ数据
def extract_iq_samples(file_path):

    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # 使用正则表达式匹配括号内的内容
        pattern = r'\((-?\d+),(-?\d+)\)'
        matches = re.findall(pattern, content)
        # 将匹配结果转换为整数元组
        iq_values = [[int(i), int(q)] for i, q in matches]
        return np.array(iq_values)
    except FileNotFoundError:
        print(f"未找到文件: {file_path}")
        return []
    except Exception as e:
        print(f"发生错误: {e}")
        return []

IQ_samples = extract_iq_samples(file_path)

# 采样率 1 MHz
fs = 1e6
N = len(IQ_samples)  # 采样点数
t = np.arange(N) / fs  # 时间轴

# 分离 I/Q 分量
I_samples = IQ_samples[:, 0]
Q_samples = IQ_samples[:, 1]

# 计算复数信号
IQ_complex = I_samples + 1j * Q_samples

# 计算 FFT
fft_result = fft(IQ_complex)
frequencies = np.fft.fftfreq(N, d=1/fs)  # 频率轴

# 取正频部分
pos_mask = frequencies > 0
frequencies = frequencies[pos_mask]
fft_magnitude = np.abs(fft_result[:len(frequencies)])

# 找到最大频率分量
dominant_freq = frequencies[np.argmax(fft_magnitude)]

print(f"主要频率分量: {dominant_freq / 1e3} kHz")

# 绘制时域波形
plt.figure(figsize=(12, 5))
plt.subplot(2, 1, 1)
plt.plot(t * 1e6, I_samples, label="I", alpha=0.7)
plt.plot(t * 1e6, Q_samples, label="Q", alpha=0.7)
plt.xlabel("Time (µs)")
plt.ylabel("Amplitude")
plt.title("I/Q Time-Domain Signal")
plt.legend()
plt.grid()

# 绘制频谱
plt.subplot(2, 1, 2)
plt.plot(frequencies / 1e3, fft_magnitude)
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude")
plt.title("FFT Spectrum of IQ Signal")
plt.grid()

plt.tight_layout()
plt.show()

# 还原原始正弦波
reconstructed_signal = np.real(IQ_complex * np.exp(1j * 2 * np.pi * fs * t))

# 绘制原始信号与重建的正弦波
plt.figure(figsize=(12, 5))
plt.plot(t * 1e6, I_samples, label="Original I", alpha=0.7, linestyle='dashed')
plt.plot(t * 1e6, Q_samples, label="Original Q", alpha=0.7, linestyle='dashed')
plt.plot(t * 1e6, reconstructed_signal, label="Reconstructed Signal", linewidth=2)

plt.xlabel("Time (µs)")
plt.ylabel("Amplitude")
plt.title("Original IQ Signal vs. Reconstructed Signal")
plt.legend()
plt.grid()
plt.show()

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift

# -------------------------------
# 1. 数据准备与基本参数设置
# -------------------------------

# 采样率：1 MHz
fs = 1e6  # 单位 Hz

# IQ采样数据（每个元组为 (I, Q)），共82个采样点
iq_data = np.array([
    (-103, -47), (48, -102), (97, 54), (-56, 97), (-97, -55), (64, -93), (88, 69), (-65, 90),
    (75, -82), (-77, 80), (85, -74), (-92, 67), (92, -64), (-94, 59), (98, -54), (-102, 45),
    (104, -43), (-106, 35), (109, -23), (-110, 15), (111, -12), (-113, 4), (112, 4), (-113, -12),
    (111, 16), (-110, -22), (107, 32), (-105, -37), (104, 40), (-105, -44), (97, 58), (-95, -61),
    (91, 66), (-91, -66), (79, 77), (-80, -80), (73, 85), (-68, -89), (57, 96), (-56, -96),
    (48, 100), (-45, -103), (37, 106), (-24, -108), (19, 110), (-17, -111), (3, 110), (1, -113),
    (-6, 111), (10, -112), (-23, 108), (20, -109), (-37, 106), (39, -103), (-48, 102), (49, -102),
    (-61, 94), (58, -95), (-75, 84), (71, -87), (-80, 78), (80, -76), (-88, 69), (93, -60),
    (-96, 56), (99, -50), (-105, 43), (101, -46), (-107, 30), (110, -27), (-111, 19), (111, -10),
    (-112, 5), (110, -1), (-113, -8), (110, 17), (-110, -23), (107, 32), (-106, -35), (106, 42),
    (-103, -47), (95, 55)
], dtype=np.float64)

# 将 IQ 数据转换为复数形式：I + j*Q
I = iq_data[:, 0]
Q = iq_data[:, 1]
iq_complex = I + 1j * Q

# 计算采样点数与时间轴（单位：秒）
N = len(iq_complex)         # 样本数量：82
t = np.arange(N) / fs       # 时间序列，步长为 1/fs

# --------------------------------------
# 2. “还原”原始信号（上变频到 RF 频段）
# --------------------------------------
# 对于蓝牙 5.1 的 CTE 信号，理论上导频部分为一个恒定正弦波。
# 如果你的采集是经过下变频后的基带 IQ 信号，
# 则可以假设本振（LO）频率为 250 kHz（即 CTE 信号的频率），
# 利用 IQ 数据上变频恢复原始 RF 信号。
#
# 原理：已知 IQ = A * exp(-j*2π*f_LO*t) * exp(j*2π*f_sig*t)（f_sig 为信号频率），
# 则乘以 exp(j*2π*f_LO*t) 后取实部，即可恢复出一个实数正弦波。
#
# 注意：这里假设 IQ 信号中并未对称双边带或其它处理，
# 若实际情况更复杂，需根据具体接收机结构调整。
f_cte = 250e3  # 250 kHz，CTE 信号频率

# 上变频：将基带 IQ 信号移回到 RF 频段
rf_signal = np.real(iq_complex * np.exp(1j * 2 * np.pi * f_cte * t))

# 绘制重构的原始 RF 信号（时域波形）
plt.figure(figsize=(12, 4))
plt.plot(t * 1e6, rf_signal, marker='o', linestyle='-', color='b')
plt.xlabel("时间 (μs)")
plt.ylabel("幅度")
plt.title("重构的原始 RF 信号 (假设 LO = 250 kHz)")
plt.grid()
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# 3. 对 IQ 数据进行频谱分析，并解释异常现象
# -----------------------------------------------------
#
# 注意到你观察到的现象：
#   - 频谱在 0～275 kHz 区间上升，
#   - 275～400 kHz 区间下降，
#   - 然后在高频部分急剧升高。
#
# 理想情况下，一个纯正弦波（CTE）在频域上应为一个窄峰（理想情况下是 Dirac 脉冲）。
#
# 出现这种“上升-下降-急剧升高”的现象，可能原因包括：
#
# 1. **有限采样长度 & FFT 窗口效应**
#    由于你只有 82 个采样点，使用矩形窗（隐式窗口，即没有额外加窗）时，
#    对于频率不精确落在 FFT 离散点上的正弦波，会出现 sinc 型的主瓣和旁瓣，
#    导致能量分布出现“波动”现象。主瓣的形状可能使得频谱从低频逐渐上升，
#    在接近信号中心频率处达到峰值后，再下降。
#
# 2. **零填充与 FFT 分辨率不足**
#    原始数据点较少导致 FFT 分辨率较低（约 fs/N ≈ 12.2 kHz），
#    能量泄露后显示的幅度曲线可能不够平滑，特别是在 dB 坐标下表现为“急剧上升”或“下降”。
#
# 3. **FFT 输出顺序（正负频率混合）**
#    如果不使用 fftshift，则 FFT 结果的负频率部分会排在正频率之后，
#    显示出来会出现不连续的跳变。建议采用 fftshift 后查看全频谱分布。
#
# 4. **接收机频率响应**
#    如果采集硬件的频率响应不平坦，也会导致不同频段幅度变化异常。
#
# 为了验证以上分析，这里我们使用 Hamming 窗口并零填充到 1024 点，
# 同时采用 fftshift 得到完整、中心化的频谱进行观察。

# -------------------------------
# 3.1 应用 Hamming 窗口
# -------------------------------
window = np.hamming(N)           # 生成 Hamming 窗口
iq_windowed = iq_complex * window  # 对 IQ 数据加窗

# -------------------------------
# 3.2 FFT 零填充处理
# -------------------------------
N_fft = 1024                     # 零填充到 1024 点，获得更平滑的频谱曲线
fft_result = fft(iq_windowed, n=N_fft)
# 计算对应的频率轴，注意频率步长为 d=1/fs
freq_axis = fftshift(fftfreq(N_fft, d=1/fs))  # 使用 fftshift 使零频居中

# 计算 FFT 幅值并中心化
fft_magnitude = fftshift(np.abs(fft_result))

# 转换为 dB 单位显示（加上一个小值以避免 log(0)）
fft_db = 20 * np.log10(fft_magnitude + 1e-12)

# 绘制频谱图
plt.figure(figsize=(12, 6))
plt.plot(freq_axis / 1e3, fft_db, 'b-', lw=1.5)
plt.xlabel("频率 (kHz)")
plt.ylabel("幅值 (dB)")
plt.title("加 Hamming 窗口和零填充后的 FFT 幅度谱")
plt.grid()
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# 4. 解释频谱异常现象
# -----------------------------------------------------
#
# 通过上述 FFT 分析可见：
#
# - 如果直接使用有限长度的矩形窗进行 FFT，纯正弦波信号的频谱会呈现 sinc 型分布，
#   即在主瓣内先上升后下降，同时伴有旁瓣。在你观察到的 0～275 kHz 上升和 275～400 kHz 下降，
#   很可能正是 sinc 主瓣的形状所致，因为信号频率（理论 250 kHz）并不精确落在 FFT 离散频点上，
#   能量就会扩散到相邻频点，形成这种非平坦的曲线。
#
# - “急剧升高”部分可能来源于：
#     a. 负频率部分的镜像（如果未正确使用 fftshift 进行中心化，会出现频谱不连续），
#     b. 或是硬件滤波器（或接收机增益）的频率响应曲线导致的增益突变。
#
# 实际上，对于理想的 CTE 信号（250 kHz 的单一正弦波），在理想情况下经过无限长数据采样后，
# 它的频谱应当是一个极窄的尖峰。但由于数据有限、窗函数效应以及采样系统的实际响应，
# 导致你观察到的频谱存在上述波动现象。
#
# 建议：
#   - 如果需要更精确的频率分析，可以适当增加采样点数或进行连续采样，
#   - 同时采用合适的窗函数（如 Hamming、Blackman）可以降低旁瓣泄露，
#   - 注意观察 fftshift 后的完整频谱，以避免正负频率混排带来的误解。

# -------------------------------
# 补充说明：如何直接观察基带 IQ 信号的时域波形
# -------------------------------
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t * 1e6, I, 'r-o', label='I 分量')
plt.xlabel("时间 (μs)")
plt.ylabel("I 幅值")
plt.title("基带 IQ 信号 - I 分量")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t * 1e6, Q, 'g-o', label='Q 分量')
plt.xlabel("时间 (μs)")
plt.ylabel("Q 幅值")
plt.title("基带 IQ 信号 - Q 分量")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
