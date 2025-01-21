# 关于蓝牙AOA定位中对CTE信号的解析

## 项目配置
- SoC -- nrf5340
  nRF5340 是全球首款配备两个 Arm® Cortex-M33® 处理器的无线 SoC(发售时间2019年11月)

## 前言
我是先看的ti的代码再看的nrf的, 刚开始看Nordic的代码的时候看不到一点常见单片机外设的使用(ti是使用TIM+DMA+GPIO)来完成天线切换的  
然后我逐渐发现自己被ti带偏了 Nordic才是真正的BLE MCU 供应商!  

nRF5340 是双核MCU在学习时要先了解蓝牙协议栈, 特别注重对hci层的理解  
(stm32wb5x 也是双核MCU)

## 项目基于Zephyr开发
Zephyr 是一个开源的实时操作系统(RTOS), 具有原生的`BLE` `Wi-Fi` `TCP/IP` 等协议栈, 特别适用于物联网平台. 具有良好的开发生态以及个人比较喜欢的代码风格. 是学习ble协议栈的不二选择!  
Zephyr 对Nordic的SoC具有良好的支持

## 关于BLE AOA定位的代码解读  

### 1. first
德州仪器对于AOA天线切换的时间控制是通过定时器中断的方式来实现的  
与ti不同 nRF 的 AoA 天线切换基于硬件射频模块, 无需软件控制中断, 完全由寄存器完成天线切换和时序管理. 其核心在于:

- 射频硬件直接控制: nRF 的射频模块支持 CTE 的硬件处理, 包括天线切换和 IQ 采样, 开发者只需配置寄存器即可完成. 
- DFE 天线切换逻辑: 寄存器 RADIO->DFECTRL1 和 RADIO->SWITCHPATTERN 定义了天线切换时隙和序列.
- 硬件自动化: CTE 信号接收开始后, 硬件按配置的切换时序切换天线, 并按规定时间采样 IQ 数据.  

配置寄存器的方式才是正确的! 高效的! 现代的! 蓝牙应用开发方式! 包括stm32wb0也采取这一方法(我在看完ti的代码之后看st的demo一头雾水, 就是被ti误导了!)

### 2. host层
打开SDK中的`direction_finding_central`工程, 从`main.c`开始, 明显能看出来
```c
#if defined(CONFIG_BT_DF_CTE_RX_AOA)
/* Example sequence of antenna switch patterns for antenna matrix designed by
 * Nordic. For more information about antenna switch patterns see README.rst.
 */
static const uint8_t ant_patterns[] = { 0x2, 0x0, 0x5, 0x6, 0x1, 0x4,
					0xC, 0x9, 0xE, 0xD, 0x8, 0xA };
#endif /* CONFIG_BT_DF_CTE_RX_AOA */
```
是我们需要的, 接着, `ant_patterns`被封装到`cte_rx_params`中, 作为参数传入
```c
bt_df_conn_cte_rx_enable(default_conn, &cte_rx_params);
```
以及旁边的
```c
bt_df_conn_cte_req_enable(default_conn, &cte_req_params);
```
一看就很重要  
经过层层调用来到了
```c
type func(type a, ...){
    bt_hci_cmd_send_sync(ABC_DEF, buf, &rsp)
}
```
你会发现很多重要的参数都被传入到`bt_hci_cmd_send_sync`这个函数中. 
下面我们详解这个作为`hci`和`controller`之间的桥梁函数

### 3. host to controller
`bt_hci_cmd_send_sync` 是 Zephyr 蓝牙协议栈中一个非常重要的 API, 用于同步地向蓝牙控制器发送 HCI 命令并等待其响应. 

##### 1. **函数原型**
```c
int bt_hci_cmd_send_sync(uint16_t opcode, struct net_buf *buf, struct net_buf **rsp);
```

###### 参数解释: 

- **opcode (`uint16_t`)**:  
  这个参数是 HCI 命令的操作码, 它指定了我们要发送的具体 HCI 命令. 每个蓝牙 HCI 命令都有一个独特的操作码. 例如, `HCI_OP_READ_BD_ADDR` 是读取设备蓝牙地址的命令. 

- **buf (`struct net_buf *`)**:  
  这是一个指向 `net_buf` 结构体的指针, 它包含了 HCI 命令的具体参数. HCI 命令的参数会打包到这个 `net_buf` 中. 在调用 `bt_hci_cmd_send_sync` 时, 应用需要提供一个已填充的 `net_buf`, 其中存储了 HCI 命令所需的所有参数.   
  [关于net_buf的解析](./bt_hci_cmd_create.md)

- **rsp (`struct net_buf **`)**:  
  这是一个指向 `net_buf *` 的指针, 它用于接收控制器的响应. 当命令完成时, 控制器会返回一个响应数据包, 这个响应数据包会存储在 `rsp` 指向的内存中. 应用程序可以通过 `rsp` 获取控制器的响应. 

###### 返回值: 
- 返回 **0** 表示命令发送并执行成功, 且 `rsp` 已经填充了控制器返回的响应数据. 
- 如果返回负值, 表示命令发送或执行失败, 具体的错误码可以参考 Zephyr 的错误定义. 

---

##### 2. **工作原理**

`bt_hci_cmd_send_sync` 函数是 HCI 和控制器之间的桥梁. 其工作流程如下: 

1. **发送 HCI 命令**:   
   `bt_hci_cmd_send_sync` 会向蓝牙控制器发送一个 HCI 命令. 发送命令时, 会传递一个操作码 (`opcode`) 和一个包含命令参数的缓冲区 (`buf`) . 

2. **控制器处理命令**:   
   蓝牙控制器 (通常是硬件蓝牙芯片) 接收到 HCI 命令后, 会根据操作码解析并执行相应的操作. 控制器处理过程可能包括硬件交互 (如设置蓝牙设备地址、启动扫描等) . 

3. **控制器返回响应**:   
   执行完命令后, 控制器会返回一个响应数据包, 通常是一个 `net_buf` 结构体, 包含了执行结果或错误信息. 这个响应数据包通过 `rsp` 参数传递回应用程序. 

4. **同步等待响应**:   
   因为这是一个同步函数调用, `bt_hci_cmd_send_sync` 会阻塞当前线程, 直到控制器完成命令执行并将响应数据填充到 `rsp` 中, 只有当命令执行完成并且响应数据可用时, 函数才会返回. 

通过这一函数, 我们实现了`host` 对 `controller` 的控制, 实现了两个`Arm® Cortex-M33®`处理器的通信

### 4. controller
- code path`zephyr-3.7.0\subsys\bluetooth\controller\ll_sw\nordic\hal\nrf5\radio`
基于硬件射频模块, 无需软件控制中断, 完全由寄存器完成天线切换和时序管理
[controller](./controller.md)