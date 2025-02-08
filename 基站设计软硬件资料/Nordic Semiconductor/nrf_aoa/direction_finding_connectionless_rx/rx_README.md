## 蓝牙：方向寻找无连接定位器  
###################################################  

**目录**  
.. contents::  
   :local:  
   :depth: 2  

### 概述  
方向寻找无连接定位器示例应用演示了蓝牙®低功耗方向寻找接收。  
该应用使用周期性广告 PDU 中的恒定音调扩展（CTE），对其进行接收与采样。  

### 要求  
************  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_req_start  
   :end-before: bt_dir_finding_central_req_end  

### 概览  
方向寻找无连接定位器示例应用使用周期性广告 PDU 中的 CTE 进行接收和采样。  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_ov_start  
   :end-before: bt_dir_finding_central_ov_end  

### 配置  
*************  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_conf_start  
   :end-before: bt_dir_finding_central_conf_end  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_5340_conf_start  
   :end-before: bt_dir_finding_central_5340_conf_end  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_aod_start  
   :end-before: bt_dir_finding_central_aod_end  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_ant_aoa_start  
   :end-before: bt_dir_finding_central_ant_aoa_end  

为在启用到达角（AoA）模式时成功使用方向寻找定位器，请提供与天线矩阵设计相关的以下数据：  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_conf_list_start  
   :end-before: bt_dir_finding_central_conf_list_end  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_ant_pat_start  
   :end-before: bt_dir_finding_central_ant_pat_end  

.. include:: /samples/bluetooth/direction_finding_central/README.rst  
   :start-after: bt_dir_finding_central_cte_start  
   :end-before: bt_dir_finding_central_cte_end  

### 编译与运行  
********************  
.. |sample path| replace:: :file:`samples/bluetooth/direction_finding_connectionless_rx`  

.. include:: /includes/build_and_run.txt  

### 测试  
=======  

|test_sample|  

1. |connect_terminal_specific|  
#. 在终端窗口中，检查类似如下的信息：  

      Starting Connectionless Locator Demo  
      Bluetooth initialization...success  
      Scan callbacks register...success.  
      Periodic Advertising callbacks register...success.  
      Start scanning...success  
      Waiting for periodic advertising...  
      [DEVICE]: XX:XX:XX:XX:XX:XX, AD evt type X, Tx Pwr: XXX, RSSI XXX C:X S:X D:X SR:X E:1 Prim: XXX, Secn: XXX, Interval: XXX (XXX ms), SID: X  
      success. Found periodic advertising.  
      Creating Periodic Advertising Sync...success.  
      Waiting for periodic sync...  
      PER_ADV_SYNC[0]: [DEVICE]: XX:XX:XX:XX:XX:XX synced, Interval XXX (XXX ms), PHY XXX  
      success. Periodic sync established.  
      Enable receiving of CTE...  
      success. CTE receive enabled.  
      Scan disable...Success.  
      Waiting for periodic sync lost...  
      PER_ADV_SYNC[X]: [DEVICE]: XX:XX:XX:XX:XX:XX, tx_power XXX, RSSI XX, CTE XXX, data length X, data: XXX  
      CTE[X]: samples count XX, cte type XXX, slot durations: X [us], packet status XXX, RSSI XXX  

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
  * :file:`include/bluetooth/direction.h`  