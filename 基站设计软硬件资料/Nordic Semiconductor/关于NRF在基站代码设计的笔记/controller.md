代码实现了蓝牙5.1 AoA（到达角）和AoD（离开角）功能中与方向定位相关的硬件配置和操作，主要是围绕 Nordic Semiconductor 的 nRF 系列芯片的 Radio 模块进行操作。这是 Nordic 官方方向定位（Direction Finding）支持的一部分。

以下是代码的主要功能总结和说明：

---

### 1. **宏定义和常量**
   - `DFE_PSEL_NOT_SET`：未设置的 GPIO 默认值。
   - `MAX_DFE_GPIO`：最大支持的 GPIO 数量为 8。
   - `MIN_ANTENNA_NUM`：最少需要 2 根天线。
   - `MAX_ANTENNA_NUM`：基于配置的 GPIO 数量计算可支持的最大天线数量。
   - `GUARD_REF_ANTENNA_PATTERN_IDX`：保护和参考期间的天线模式索引。
   - `PDU_ANTENNA`：通过天线发送或接收 PDU 数据包的天线模式。

---

### 2. **数据结构**
   - `struct df_ant_cfg`：定义了方向定位的天线矩阵配置，包括：
     - `ant_num`：天线数量。
     - `dfe_gpio[MAX_DFE_GPIO]`：用于切换天线的 GPIO 引脚。

---

### 3. **功能实现**

#### **(1) 天线切换模式与 GPIO 配置**
   - **`radio_df_ant_switching_pin_sel_cfg`**
     - 配置 Radio 的 PSEL.DFEGPIO 寄存器，指定用于切换天线的 GPIO。
     - 如果某个 GPIO 未设置，将其断开连接。

   - **`radio_df_ant_switching_gpios_cfg`**
     - 设置 GPIO 为输出模式，并根据 SWITCHPATTERN 配置 GPIO 的初始状态，防止 DFE 功能关闭后出现电平突变。

#### **(2) 天线切换模式设置**
   - **`radio_df_ant_switch_pattern_set`**
     - 配置 Radio 模块中 SWITCHPATTERN 寄存器的天线切换模式。
     - 支持保护（Guard）、参考（Reference）和采样期间的天线切换。

#### **(3) 模式设置**
   - **`radio_df_mode_set_aoa`** 和 **`radio_df_mode_set_aod`**
     - 配置方向定位模式为 AoA 或 AoD。

#### **(4) 方向定位控制**
   - **`radio_df_ctrl_set`**
     - 配置方向定位的参数，包括 CTE（连续导频）长度、切换间隔、采样间隔和物理层模式。
     - 使用 `DFECTRL1` 和 `DFECTRL2` 寄存器。

#### **(5) CTE 配置**
   - **`radio_df_cte_tx_aod_2us_set`** 和 **`radio_df_cte_tx_aod_4us_set`**
     - 配置 AoD 模式下的 CTE 参数（2 μs 和 4 μs 的切换间隔）。

---

### 4. **校验与断言**
   - 使用 `BUILD_ASSERT` 验证配置的有效性：
     - 是否设置了足够数量的 GPIO。
     - 配置的天线数量是否在有效范围内。
     - GPIO 配置中的标志位是否为零。

---

### 5. **实用函数**
   - **`radio_df_ant_num_get`**：返回支持的天线数量。
   - **`radio_df_pdu_antenna_switch_pattern_get`**：返回当前的天线切换模式。

---

### 6. **模块配置依赖**
   - `CONFIG_BT_CTLR_DF_ANT_SWITCH_TX` 和 `CONFIG_BT_CTLR_DF_ANT_SWITCH_RX`：启用 Tx 和 Rx 方向定位天线切换功能。
   - `CONFIG_BT_CTLR_DF_INIT_ANT_SEL_GPIOS`：初始化方向定位 GPIO。

---

### 代码应用场景
1. **硬件初始化**
   - 配置方向定位天线 GPIO 和模式。

2. **蓝牙定位系统**
   - 在 AoA 和 AoD 模式下实现精确的角度计算。

3. **多天线阵列**
   - 使用天线切换模式（Switching Pattern）在蓝牙 CTE 期间采集 IQ 数据。

