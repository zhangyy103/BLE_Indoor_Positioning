/*
 * 版权所有 (c) 2020 Nordic Semiconductor ASA
 *
 * SPDX 许可证标识符：Apache-2.0
 */

#include <stdint.h>
#include <errno.h>
#include <soc.h>
#include <zephyr/devicetree.h>
#include <zephyr/sys/util_macro.h>
#include <hal/nrf_radio.h>
#include <hal/nrf_gpio.h>
#include <hal/ccm.h>

#include "pdu_df.h"
#include "lll/pdu_vendor.h"
#include "pdu.h"

#include "radio_nrf5.h"
#include "radio.h"
#include "radio_df.h"
#include "radio_internal.h"

/* Devicetree 节点标识符，用于无线电节点 */
#define RADIO_NODE DT_NODELABEL(radio)

/* 未连接天线 GPIO 引脚时要设置的值 */
#define DFE_PSEL_NOT_SET 0xFF
/* 无线电外设中 PSEL_DFEGPIO[n] 寄存器的数量 */
#define MAX_DFE_GPIO 8
/* 对每个可用的 DFE GPIO 索引运行宏 'fn'，从 0 到 MAX_DFE_GPIO-1，使用给定的括号分隔符 */
#define FOR_EACH_DFE_GPIO(fn, sep) \
	FOR_EACH(fn, sep, 0, 1, 2, 3, 4, 5, 6, 7)

/* 在天线切换模式中用于 GUARD 和 REFERENCE 周期的天线索引 */
#define GUARD_REF_ANTENNA_PATTERN_IDX 0U

/* 方向定位天线矩阵配置 */
struct df_ant_cfg {
	uint8_t ant_num;
	/* 选择由无线电用于切换天线的 GPIO */
	uint8_t dfe_gpio[MAX_DFE_GPIO];
};

#define DFE_GPIO_PSEL(idx)					  \
	NRF_DT_GPIOS_TO_PSEL_OR(RADIO_NODE, dfegpio##idx##_gpios, \
				DFE_PSEL_NOT_SET)

#define DFE_GPIO_PIN_DISCONNECT (RADIO_PSEL_DFEGPIO_CONNECT_Disconnected << \
				 RADIO_PSEL_DFEGPIO_CONNECT_Pos)

#define HAS_DFE_GPIO(idx) DT_NODE_HAS_PROP(RADIO_NODE, dfegpio##idx##_gpios)

/* 已设置的 dfegpio[n]-gpios 属性的数量 */
#define DFE_GPIO_NUM (FOR_EACH_DFE_GPIO(HAS_DFE_GPIO, (+)))

/* 启用天线切换所需的最小天线数量 */
#define MIN_ANTENNA_NUM 2

/* 根据已设置的 dfegpio[n]-gpios 属性数量支持的最大天线数量 */
#if (DFE_GPIO_NUM > 0)
#define MAX_ANTENNA_NUM BIT(DFE_GPIO_NUM)
#else
#define MAX_ANTENNA_NUM 0
#endif

uint8_t radio_df_pdu_antenna_switch_pattern_get(void)
{
	return PDU_ANTENNA;
}

#if defined(CONFIG_BT_CTLR_DF_ANT_SWITCH_TX) || \
	defined(CONFIG_BT_CTLR_DF_ANT_SWITCH_RX)

/*
 * 检查我们是否有一个用于 DFE 空闲状态的天线切换模式。
 * （在 DFE 空闲状态时，无线电外设传输或接收 PDUs。）
 */

#define HAS_PDU_ANTENNA DT_NODE_HAS_PROP(RADIO_NODE, dfe_pdu_antenna)

BUILD_ASSERT(HAS_PDU_ANTENNA,
	     "缺少用于选择 PDU 传输期间空闲状态天线的天线模式。"
	     "请设置 devicetree 属性 dfe-pdu-antenna。");

void radio_df_ant_switch_pattern_set(const uint8_t *patterns, uint8_t len)
{
	/* SWITCHPATTERN 像是一个指向底层缓冲区的移动指针。
	 * 每次写入都会存储一个值并将指针移动到新的空闲位置。
	 * 当读取时，它会返回自上次写入 CLEARPATTERN 以来存储的元素数量。
	 * 需要 不使用下标操作符。
	 *
	 * SWITCHPATTER 缓冲区的一些存储条目对于 DFE 扩展在无线电中有特殊用途：
	 * - SWITCHPATTERN[0] 用于空闲周期（PDU 传输/接收），
	 * - SWITCHPATTERN[1] 用于保护和参考周期，
	 * - SWITCHPATTERN[2] 及后续用于切换采样槽。
	 * 因此，在 SWITCHPATTERN[0] 中存储了由 DTS 属性 dfe_pdu_antenna 提供的模式。
	 * 这限制了支持的天线切换模式数量为一个。
	 */
	NRF_RADIO->SWITCHPATTERN = PDU_ANTENNA;
	for (uint8_t idx = 0; idx < len; ++idx) {
		NRF_RADIO->SWITCHPATTERN = patterns[idx];
	}

	/* 在 SWITCHPATTERN 缓冲区的末尾存储用于 GUARD 和 REFERENCE 周期的天线 ID。
	 * 当用户提供的切换模式耗尽时，需要应用参考天线 ID。
	 * 提供给此函数的最大切换模式长度最多比 SWITCHPATTERN 缓冲区的容量少一个。
	 * 因此，总会有空间在切换模式的末尾存储参考天线 ID。
	 */
	NRF_RADIO->SWITCHPATTERN = patterns[GUARD_REF_ANTENNA_PATTERN_IDX];
}

/*
 * 检查是否已设置天线数量，并且配置了足够的引脚以表示给定天线数量的每个模式。
 */

#define HAS_ANTENNA_NUM DT_NODE_HAS_PROP(RADIO_NODE, dfe_antenna_num)

BUILD_ASSERT(HAS_ANTENNA_NUM,
	     "您必须在无线电节点中设置 dfe-antenna-num 属性以启用天线切换。");

#define ANTENNA_NUM DT_PROP_OR(RADIO_NODE, dfe_antenna_num, 0)

BUILD_ASSERT(!HAS_ANTENNA_NUM || (ANTENNA_NUM <= MAX_ANTENNA_NUM),
	     "配置的 GPIO 引脚数量不足。"
	     "请设置更多 dfegpio[n]-gpios 属性。");
BUILD_ASSERT(!HAS_ANTENNA_NUM || (ANTENNA_NUM >= MIN_ANTENNA_NUM),
	     "提供的天线数量不足。"
	     "请增加 dfe-antenna-num 属性。");

/*
 * 检查每个 dfegpio[n]-gpios 属性的标志单元是否为零。
 */

#define ASSERT_DFE_GPIO_FLAGS_ARE_ZERO(idx)				   \
	BUILD_ASSERT(DT_GPIO_FLAGS(RADIO_NODE, dfegpio##idx##_gpios) == 0, \
		     "每个 dfegpio[n]-gpios 属性的标志单元必须为零。")

FOR_EACH_DFE_GPIO(ASSERT_DFE_GPIO_FLAGS_ARE_ZERO, (;));

/* 存储 dfegpio[n]-gpios 属性的值 */
const static struct df_ant_cfg ant_cfg = {
	.ant_num = ANTENNA_NUM,
	.dfe_gpio = { FOR_EACH_DFE_GPIO(DFE_GPIO_PSEL, (,)) }
};

/* @brief 配置无线电以获取可用于 CTE 传输/接收期间驱动天线切换的 GPIO 引脚信息。
 *
 * 设置 DF 相关的 PSEL.DFEGPIO 寄存器，以便无线电能够驱动天线切换。
 *
 */
void radio_df_ant_switching_pin_sel_cfg(void)
{
	uint8_t pin_sel;

	for (uint8_t idx = 0; idx < MAX_DFE_GPIO; ++idx) {
		pin_sel = ant_cfg.dfe_gpio[idx];

		if (pin_sel != DFE_PSEL_NOT_SET) {
			nrf_radio_dfe_pattern_pin_set(NRF_RADIO,
						      pin_sel,
						      idx);
		} else {
			nrf_radio_dfe_pattern_pin_set(NRF_RADIO,
						      DFE_GPIO_PIN_DISCONNECT,
						      idx);
		}
	}
}

#if defined(CONFIG_BT_CTLR_DF_INIT_ANT_SEL_GPIOS)
/* @brief 配置将由方向定位扩展用于天线切换的 GPIO 引脚。
 *
 * 配置 GPIO 外设中用于天线选择的 GPIO 引脚。
 * 还将引脚输出设置为匹配 SWITCHPATTERN[0] 中的状态，该状态用于启用 PDU 接收/传输的天线。
 * 这可以防止在 DFE 关闭后出现毛刺。
 *
 * @return	成功时返回零，失败时返回其他值。
 */
void radio_df_ant_switching_gpios_cfg(void)
{
	uint8_t pin_sel;

	for (uint8_t idx = 0; idx < MAX_DFE_GPIO; ++idx) {
		pin_sel = ant_cfg.dfe_gpio[idx];
		if (pin_sel != DFE_PSEL_NOT_SET) {
			nrf_gpio_cfg_output(pin_sel);

			if (BIT(idx) & PDU_ANTENNA) {
				nrf_gpio_pin_set(pin_sel);
			} else {
				nrf_gpio_pin_clear(pin_sel);
			}
		}
	}
}
#endif /* CONFIG_BT_CTLR_DF_INIT_ANT_SEL_GPIOS */
#endif /* CONFIG_BT_CTLR_DF_ANT_SWITCH_TX || CONFIG_BT_CTLR_DF_ANT_SWITCH_RX */

/* @brief 提供方向定位可用的天线数量。
 *
 * 天线数量是硬件定义的，通过 devicetree 提供。
 *
 * 如果未启用天线切换，则必须有一个天线负责 PDU 接收和传输。
 *
 * @return	可用天线的数量。
 */
uint8_t radio_df_ant_num_get(void)
{
#if defined(CONFIG_BT_CTLR_DF_ANT_SWITCH_TX) || \
	defined(CONFIG_BT_CTLR_DF_ANT_SWITCH_RX)
	return ant_cfg.ant_num;
#else
	return 1U;
#endif
}

static inline void radio_df_mode_set(uint8_t mode)
{
	NRF_RADIO->DFEMODE &= ~RADIO_DFEMODE_DFEOPMODE_Msk;
	NRF_RADIO->DFEMODE |= ((mode << RADIO_DFEMODE_DFEOPMODE_Pos)
			       & RADIO_DFEMODE_DFEOPMODE_Msk);
}

void radio_df_mode_set_aoa(void)
{
	radio_df_mode_set(NRF_RADIO_DFE_OP_MODE_AOA);
}

void radio_df_mode_set_aod(void)
{
	radio_df_mode_set(NRF_RADIO_DFE_OP_MODE_AOD);
}

static inline void radio_df_ctrl_set(uint8_t cte_len,
				     uint8_t switch_spacing,
				     uint8_t sample_spacing,
				     uint8_t phy)
{
	uint16_t sample_offset;
	uint32_t conf;

	/* 完整设置是有意为之，以确保寄存器中没有留下任何意外的状态。 */
	conf = ((((uint32_t)cte_len << RADIO_DFECTRL1_NUMBEROF8US_Pos) &
				       RADIO_DFECTRL1_NUMBEROF8US_Msk) |
		((uint32_t)RADIO_DFECTRL1_DFEINEXTENSION_CRC <<
		 RADIO_DFECTRL1_DFEINEXTENSION_Pos) |
		((uint32_t)switch_spacing << RADIO_DFECTRL1_TSWITCHSPACING_Pos) |
		((uint32_t)NRF_RADIO_DFECTRL_SAMPLE_SPACING_1US <<
		 RADIO_DFECTRL1_TSAMPLESPACINGREF_Pos) |
		((uint32_t)NRF_RADIO_DFECTRL_SAMPLE_TYPE_IQ <<
		 RADIO_DFECTRL1_SAMPLETYPE_Pos) |
		((uint32_t)sample_spacing << RADIO_DFECTRL1_TSAMPLESPACING_Pos) |
		(((uint32_t)0 << RADIO_DFECTRL1_AGCBACKOFFGAIN_Pos) &
				 RADIO_DFECTRL1_AGCBACKOFFGAIN_Msk));

	NRF_RADIO->DFECTRL1 = conf;

	switch (phy) {
	case PHY_1M:
		if (switch_spacing == RADIO_DFECTRL1_TSWITCHSPACING_2us) {
			sample_offset = CONFIG_BT_CTLR_DF_SAMPLE_OFFSET_PHY_1M_SAMPLING_1US;
		} else if (switch_spacing == RADIO_DFECTRL1_TSWITCHSPACING_4us) {
			sample_offset = CONFIG_BT_CTLR_DF_SAMPLE_OFFSET_PHY_1M_SAMPLING_2US;
		} else {
			sample_offset = 0;
		}
		break;
	case PHY_2M:
		if (switch_spacing == RADIO_DFECTRL1_TSWITCHSPACING_2us) {
			sample_offset = CONFIG_BT_CTLR_DF_SAMPLE_OFFSET_PHY_2M_SAMPLING_1US;
		} else if (switch_spacing == RADIO_DFECTRL1_TSWITCHSPACING_4us) {
			sample_offset = CONFIG_BT_CTLR_DF_SAMPLE_OFFSET_PHY_2M_SAMPLING_2US;
		} else {
			sample_offset = 0;
		}
		break;
	case PHY_LEGACY:
	default:
		/* 如果 phy 设置为 legacy，则该函数在 TX 上下文中被调用，实际值无关紧要，因此设置为默认零。 */
		sample_offset = 0;
	}

	conf = ((((uint32_t)sample_offset << RADIO_DFECTRL2_TSAMPLEOFFSET_Pos) &
				       RADIO_DFECTRL2_TSAMPLEOFFSET_Msk) |
		(((uint32_t)CONFIG_BT_CTLR_DF_SWITCH_OFFSET << RADIO_DFECTRL2_TSWITCHOFFSET_Pos) &
				       RADIO_DFECTRL2_TSWITCHOFFSET_Msk));

	NRF_RADIO->DFECTRL2 = conf;
}

void radio_df_cte_tx_aod_2us_set(uint8_t cte_len)
{
	/* 对于 AoD Tx，采样间隔无关紧要。它被设置为 DFECTRL1 寄存器复位后的值。
	 * 这是故意为之，而不是在存储配置之前对值添加条件或屏蔽字段。
	 * DFECTRL2 中的值取决于 PHY，在 AoD Tx 中无关紧要，因此这里使用 PHY_LEGACY。
	 */
	radio_df_ctrl_set(cte_len, RADIO_DFECTRL1_TSWITCHSPACING_2us,
			  RADIO_DFECTRL1_TSAMPLESPACING_2us, PHY_LEGACY);
}

void radio_df_cte_tx_aod_4us_set(uint8_t cte_len)
{
	/* 对于 AoD Tx，采样间隔无关紧要。它被设置为 DFECTRL1 寄存器复位后的值。
	 * 这是故意为之，而不是在存储配置之前对值添加条件或屏蔽字段。
	 * DFECTRL2 中的值取决于 PHY，在 AoD Tx 中无关紧要，因此这里使用 PHY_LEGACY。
	 */
	radio_df_ctrl_set(cte_len, RADIO_DFECTRL1_TSWITCHSPACING_4us,
			  RADIO_DFECTRL1_TSAMPLESPACING_2us, PHY_LEGACY);
}

void radio_df_cte_tx_aoa_set(uint8_t cte_len)
{
	/* 对于 AoA Tx，切换和采样间隔无关紧要。它被设置为 DFECTRL1 寄存器复位后的值。
	 * 这是故意为之，而不是在存储配置之前对值添加条件或屏蔽字段。
	 * DFECTRL2 中的值取决于 PHY，在 AoA Tx 中无关紧要，因此这里使用 PHY_LEGACY。
	 */
	radio_df_ctrl_set(cte_len, RADIO_DFECTRL1_TSWITCHSPACING_4us,
			  RADIO_DFECTRL1_TSAMPLESPACING_2us, PHY_LEGACY);
}

void radio_df_cte_rx_2us_switching(bool cte_info_in_s1, uint8_t phy)
{
	/* BT 规范要求每个切换槽只有一个采样，因此槽和采样的间隔相同。
	 * 只有在禁用 CTEINLINE 配置时才使用 CTE 持续时间。
	 */
	radio_df_ctrl_set(0, RADIO_DFECTRL1_TSWITCHSPACING_2us,
			  RADIO_DFECTRL1_TSAMPLESPACING_2us, phy);
	radio_df_cte_inline_set_enabled(cte_info_in_s1);
}

void radio_df_cte_rx_4us_switching(bool cte_info_in_s1, uint8_t phy)
{
	/* BT 规范要求每个切换槽只有一个采样，因此槽和采样的间隔相同。
	 * 只有在禁用 CTEINLINE 配置时才使用 CTE 持续时间。
	 */
	radio_df_ctrl_set(0, RADIO_DFECTRL1_TSWITCHSPACING_4us,
			  RADIO_DFECTRL1_TSAMPLESPACING_4us, phy);
	radio_df_cte_inline_set_enabled(cte_info_in_s1);
}

void radio_df_ant_switch_pattern_clear(void)
{
	NRF_RADIO->CLEARPATTERN = RADIO_CLEARPATTERN_CLEARPATTERN_Clear;
}

void radio_df_reset(void)
{
	/* 初始化为 NRF_RADIO 复位值
	 * 注意：只有关闭 DF 功能的寄存器和那些在函数中部分修改的寄存器被重新赋值为上电复位值。
	 */
	NRF_RADIO->DFEMODE = HAL_RADIO_RESET_VALUE_DFEMODE;
	NRF_RADIO->CTEINLINECONF = HAL_RADIO_RESET_VALUE_CTEINLINECONF;

	radio_df_ant_switch_pattern_clear();
}

void radio_switch_complete_and_phy_end_b2b_tx(uint8_t phy_curr, uint8_t flags_curr,
					      uint8_t phy_next, uint8_t flags_next)
{
#if defined(CONFIG_BT_CTLR_TIFS_HW)
	NRF_RADIO->SHORTS = RADIO_SHORTS_READY_START_Msk | RADIO_SHORTS_END_DISABLE_Msk |
			    RADIO_SHORTS_DISABLED_TXEN_Msk;
#else /* !CONFIG_BT_CTLR_TIFS_HW */
	NRF_RADIO->SHORTS = RADIO_SHORTS_READY_START_Msk | NRF_RADIO_SHORTS_TRX_END_DISABLE_Msk;
	sw_switch(SW_SWITCH_TX, SW_SWITCH_TX, phy_curr, flags_curr, phy_next, flags_next,
		  END_EVT_DELAY_DISABLED);
#endif /* !CONFIG_BT_CTLR_TIFS_HW */
}

void radio_df_iq_data_packet_set(uint8_t *buffer, size_t len)
{
	nrf_radio_dfe_buffer_set(NRF_RADIO, (uint32_t *)buffer, len);
}

uint32_t radio_df_iq_samples_amount_get(void)
{
	return nrf_radio_dfe_amount_get(NRF_RADIO);
}

uint8_t radio_df_cte_status_get(void)
{
	return NRF_RADIO->CTESTATUS;
}

bool radio_df_cte_ready(void)
{
	return (NRF_RADIO->EVENTS_CTEPRESENT != 0);
}