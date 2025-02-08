## 蓝牙：方向寻找中心  
####################################  

**目录**  
.. contents::  
   :local:  
   :depth: 2  

### 概述  
方向寻找中心示例应用演示了蓝牙®低功耗方向寻找功能，其中中心设备从连接的外设设备收到响应时提取 CTE 信息。  

该示例支持两种方向寻找模式：  

* 到达角（Angle of Arrival，AoA）  
* 离开角（Angle of Departure，AoD）  

默认情况下，示例中同时提供了这两种模式。  

.. bt_dir_finding_central_ov_start  

.. bt_dir_finding_central_ov_end  

### 配置  
*************  

.. bt_dir_finding_central_conf_start  

|config|  

该示例的配置分为以下两个文件：  

* 通用配置：在 :file:`prj.conf` 文件中  
* 针对具体开发板的配置：在 :file:`boards/<BOARD>.conf` 文件中  

.. bt_dir_finding_central_conf_end  

.. bt_dir_finding_central_5340_conf_start  

nRF5340 配置文件  
===========================  

以下是针对 :ref:`nRF5340 DK <ug_nrf5340>` 的附加配置文件：  

* 蓝牙低功耗控制器作为子镜像运行在网络核心上。  
  子镜像的配置存储在 :file:`child_image/` 子目录中。  
* 应用核心使用的 DTS 叠加文件为 :file:`boards/nrf5340dk_nrf5340_cpuapp.overlay`。  
  该文件将对 GPIO 的控制转发给网络核心，由网络核心向无线电外设传递控制信号以执行天线切换。  

.. bt_dir_finding_central_5340_conf_end  

#### 离开角（AoD）模式  
.. bt_dir_finding_central_aod_start  

要仅构建离开角（AoD）模式的示例，请将 :makevar:`EXTRA_CONF_FILE` 设置为 :file:`overlay-aod.conf` 文件，使用相应的 :ref:`CMake 选项 <cmake_options>`。  

有关 |NCS| 中配置文件的更多信息，请参阅 :ref:`app_build_system`。  

要为 :ref:`nRF5340 DK <ug_nrf5340>` 构建仅离开角模式的示例，请将 :file:`overlay-aod.conf` 文件的内容添加到 :file:`child_image/hci_ipc.conf` 文件中。  

.. bt_dir_finding_central_aod_end  

#### 到达角（AoA）模式下的天线矩阵配置  
.. bt_dir_finding_central_ant_aoa_start  

要在启用到达角（AoA）模式时使用该示例，需要额外配置用于控制天线阵列的 GPIO。  
一个这样的配置示例在设备树叠加文件 :file:`nrf52833dk_nrf52833.overlay` 中提供。  

该叠加文件提供了由无线电外设在 AoA 模式下接收 CTE 时用于切换天线补丁的 GPIO 信息。  
必须至少提供两个 GPIO 以启用天线切换。  

这些 GPIO 将按照 ``dfegpio#-gpios`` 属性中提供的顺序使用。  
顺序非常重要，因为它会影响天线切换模式与 GPIO 的映射（参见 `Antenna patterns`_）。  

为在启用 AoA 模式时成功使用方向寻找中心，请提供与天线矩阵设计相关的以下数据：  

.. bt_dir_finding_central_conf_list_start  

* 将要用于 ``dfegpio#-gpios`` 属性的 GPIO 引脚，配置在设备树叠加文件 :file:`nrf52833dk_nrf52833.overlay` 中。  
* 将作为接收 PDU 时使用的默认天线，即 :c:member:`dfe-pdu-antenna` 属性，在同一叠加文件中配置。  
* 更新 :file:`main.c` 文件中 :c:member:`ant_patterns` 数组的天线切换模式。  

.. bt_dir_finding_central_conf_list_end  

#### 天线切换模式  
.. bt_dir_finding_central_ant_pat_start  

天线切换模式是一个二进制数字，每一位对应一个特定的天线 GPIO 引脚。  
例如，模式 ``0x3`` 表示索引为 0、1 的天线 GPIO 将被置位，而其他引脚保持不置位。  

这也意味着，例如使用四个 GPIO 时，模式数不能超过 16，最大允许值为 15。  

如果切换采样周期数大于存储的切换模式数，无线电将循环回第一个模式。  

天线切换模式的长度受 :kconfig:option:`CONFIG_BT_CTLR_DF_MAX_ANT_SW_PATTERN_LEN` 选项的限制。  
如果所需天线切换模式的长度大于该选项的默认值，请在开发板配置文件中将其设置为所需值。  
例如，对于 :ref:`nRF52833 DK <ug_nrf52>`，请在 :file:`nrf52833dk_nrf52833.conf` 文件中设置该选项。  

下表展示了可用于切换 Nordic 设计天线矩阵上天线的模式：  

+--------+--------------+  
|天线    | PATTERN[3:0] |  
+========+==============+  
| ANT_12 |  0 (0b0000)  |  
+--------+--------------+  
| ANT_10 |  1 (0b0001)  |  
+--------+--------------+  
| ANT_11 |  2 (0b0010)  |  
+--------+--------------+  
| 保留   |  3 (0b0011)  |  
+--------+--------------+  
| ANT_3  |  4 (0b0100)  |  
+--------+--------------+  
| ANT_1  |  5 (0b0101)  |  
+--------+--------------+  
| ANT_2  |  6 (0b0110)  |  
+--------+--------------+  
| 保留   |  7 (0b0111)  |  
+--------+--------------+  
| ANT_6  |  8 (0b1000)  |  
+--------+--------------+  
| ANT_4  |  9 (0b1001)  |  
+--------+--------------+  
| ANT_5  | 10 (0b1010)  |  
+--------+--------------+  
| 保留   | 11 (0b1011)  |  
+--------+--------------+  
| ANT_9  | 12 (0b1100)  |  
+--------+--------------+  
| ANT_7  | 13 (0b1101)  |  
+--------+--------------+  
| ANT_8  | 14 (0b1110)  |  
+--------+--------------+  
| 保留   | 15 (0b1111)  |  
+--------+--------------+  

.. bt_dir_finding_central_ant_pat_end  

#### 恒定音调扩展（CTE）传输与接收参数  
.. bt_dir_finding_central_cte_start  

恒定音调扩展可在 AoA 或 AoD 模式下工作。  
发送端配置的操作模式用于 CTE 传输；  
接收端的工作模式取决于配置。  
默认情况下，两种模式均在示例中启用，接收端在 PDU 的扩展广告头中的 ``CTEInfo`` 字段中接收 CTE 类型。  
根据接收时选择的操作模式，接收端的无线电外设要么同时执行天线切换与 CTE 采样（AoA），  
要么只进行 CTE 采样（AoD）。  

允许的天线切换槽长度为 1 µs 或 2 µs。  
发送端使用天线切换槽长度来配置纯 AoD 模式下的无线电外设。  
接收端在纯 AoA 模式下使用本地设置的天线切换槽长度。  
当接收到的 PDU 中的 CTE 类型为 AoD 时，接收端的无线电外设将使用适用于 AoD 类型的天线切换槽长度（1 或 2 µs）。  
天线切换槽长度会影响 IQ 采样报告中提供的样本数。  

CTE 长度限定在 16 µs 到 160 µs 之间。  
该值以 8 µs 为单位提供，例如 12 表示 96 µs。  
发送端负责设置 CTE 长度。  
该值在 PDU 的扩展广告头中作为 CTEInfo 字段发送给接收端。  
接收端的无线电外设使用周期性广告 PDU 中提供的 CTE 长度来执行：  
- 在 AoA 模式下的天线切换和 CTE 采样  
- 或在 AoD 模式下仅进行 CTE 采样。  

CTE 长度会影响 IQ 采样报告中提供的样本数。  

CTE 包含以下三个阶段：  

* **保护期**：4 µs，在实际 CTE 接收和相邻 PDU 传输之前存在一个间隔，以避免干扰。  
* **参考期**：在此期间使用单一天线进行采样，采样间隔为 1 µs，周期持续 8 µs。  
* **切换采样期**：分为切换槽和采样槽。每个槽的长度可为 1 或 2 µs。  

由 IQ 采样报告提供的 IQ 样本总数是变化的。  
它取决于 CTE 长度和天线切换槽长度。  
参考期始终提供 8 个样本；  
对于 2 µs 天线切换槽，切换采样期会提供 1 到 37 个样本；  
对于 1 µs 天线切换槽，则提供 2 到 74 个样本；  
总计 9 到 82 个样本。  

例如，CTE 长度为 120 µs，天线切换槽为 1 µs，则结果为：  

* 参考期提供 8 个样本；  
* 切换采样期的持续时间为 ``120 µs - 12 µs = 108 µs``。  
  对于 1 µs 天线切换槽，采样间隔为 2 µs（1 µs 切换槽 + 1 µs 采样槽），  
  因此切换采样期提供的样本数为 ``108 µs / 2 µs = 54``。  

总样本数为 62。  

.. bt_dir_finding_central_cte_end  

### 编译与运行  
********************  
.. |sample path| replace:: :file:`samples/bluetooth/direction_finding_central`  

.. include:: /includes/build_and_run.txt  

### 测试  
=======  

|test_sample|  

1. |connect_terminal_specific|  
#. 在终端窗口中，检查类似如下的信息：  

      Bluetooth initialized  
      <inf> bt_hci_core: HW Platform: Nordic Semiconductor (XxXXXX)  
      <inf> bt_hci_core: HW Variant: nRF52x (XxXXXX)  
      <inf> bt_hci_core: Firmware: Standard Bluetooth controller (0xXX) Version 3.0 Build X  
      <inf> bt_hci_core: Identity: XX:XX:XX:XX:XX:XX (random)  
      <inf> bt_hci_core: HCI: version 5.3 (XxXX) revision XxXXXX, manufacturer XxXXXX  
      <inf> bt_hci_core: LMP: version 5.3 (XxXX) subver XxXXXX  
      Scanning successfully started  
      [DEVICE]: XX:XX:XX:XX:XX:XX (public), AD evt type 0, AD data len XX, RSSI XXX  
      [AD]: X data_len X  
      [AD]: X data_len X  
      Connected: XX:XX:XX:XX:XX:XX (random)  
      Enable receiving of CTE...  
      success. CTE receive enabled.  
      Request CTE from peer device...  
      success. CTE request enabled.  
      CTE[XX:XX:XX:XX:XX:XX (random)]: samples count XX, cte type XXX, slot durations: X [us], packet status XXX , RSSI XXX  

### 依赖项  
************  

该示例使用了以下 Zephyr 库：  

* :file:`include/zephyr/types.h`  
* :file:`lib/libc/minimal/include/errno.h`  
* :file:`include/sys/printk.h`  
* :file:`include/sys/byteorder.h`  
* :file:`include/sys/util.h`  
* :ref:`zephyr:bluetooth_api`:  

  * :file:`include/bluetooth/bluetooth.h`  
  * :file:`include/bluetooth/hci.h`  
  * :file:`include/bluetooth/direction.h`  
  * :file:`include/bluetooth/conn.h`  