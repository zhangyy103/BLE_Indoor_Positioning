## 蓝牙：方向寻找无连接信标  
##################################################  

**目录**  
.. contents::  
   :local:  
   :depth: 2  

### 概述  
方向寻找无连接信标示例演示了蓝牙®低功耗方向寻找传输。  

### 要求  
.. bt_dir_finding_tx_req_start  

该示例支持以下开发套件：  

.. table-from-sample-yaml::  

该示例在以“离开角（Angle of Departure，AoD）”模式运行时需要一个天线矩阵。  
这个天线矩阵可以是 Nordic Semiconductor 设计的 12 补丁天线矩阵，或者其他任意天线矩阵。  

.. bt_dir_finding_tx_req_end  

### 概览  
方向寻找无连接信标示例应用使用与周期性广告 PDU 一同传输的恒定音调扩展（CTE）。  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_ov_start  
   :end-before: bt_dir_finding_central_ov_end  

### 配置  
.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_conf_start  
   :end-before: bt_dir_finding_central_conf_end  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_5340_conf_start  
   :end-before: bt_dir_finding_central_5340_conf_end  

#### 到达角（AoA）模式  
.. bt_dir_finding_tx_aoa_mode_start  

该示例默认构建为到达角（AoA）模式。  

.. bt_dir_finding_tx_aoa_mode_end  

#### 离开角（AoD）模式  
.. bt_dir_finding_tx_aod_mode_start  

要以离开角（AoD）模式构建该示例，请将 :makevar:`EXTRA_CONF_FILE` 设置为 ``overlay-aod.conf;overlay-bt_ll_sw_split.conf``，  
并使用相应的 :ref:`CMake 选项 <cmake_options>` 将 :makevar:`SNIPPET` 设置为 ``bt-ll-sw-split``。  

有关 |NCS| 中配置文件的更多信息，请参阅 :ref:`app_build_system`。  

.. bt_dir_finding_tx_aod_mode_end  

#### 离开角模式下的天线矩阵配置  
.. bt_dir_finding_tx_ant_aod_start  

在启用 AoD 模式时使用该示例，需要额外配置用于控制天线阵列的 GPIO。  
一个这样的配置示例在设备树叠加文件 :file:`nrf52833dk_nrf52833.overlay` 中提供。  

该叠加文件提供了由无线电外设在 CTE 传输期间用于切换天线补丁的 GPIO 的信息。  
必须至少提供两个 GPIO 以启用天线切换。  

这些 GPIO 将按照 ``dfegpio#-gpios`` 属性中提供的顺序由无线电外设使用。  
顺序非常重要，因为它会影响天线切换模式与 GPIO 的映射（参见 `Antenna patterns`_）。  

为了在启用 AoD 模式时成功使用方向寻找信标，请提供与天线矩阵设计相关的以下数据：  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_conf_list_start  
   :end-before: bt_dir_finding_central_conf_list_end  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_ant_pat_start  
   :end-before: bt_dir_finding_central_ant_pat_end  

.. bt_dir_finding_tx_ant_aod_end  

### 编译与运行  
.. |sample path| replace:: :file:`samples/bluetooth/direction_finding_connectionless_tx`  

.. include:: /includes/build_and_run.txt  

### 测试  
=======  

|test_sample|  

1. |connect_terminal_specific|  
#. 在终端窗口中，检查类似如下的信息：  

      Starting Connectionless Beacon Demo  
      Bluetooth initialization...success  
      Advertising set create...success  
      Update CTE params...success  
      Periodic advertising params set...success  
      Enable CTE...success  
      Periodic advertising enable...success  
      Extended advertising enable...success  
      Started extended advertising as XX:XX:XX:XX:XX:XX (random)  

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
  * :file:`include/bluetooth/gatt.h`  