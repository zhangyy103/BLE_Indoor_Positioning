/*
 * Copyright (c) 2020 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_BLUETOOTH_DF_H_
#define ZEPHYR_INCLUDE_BLUETOOTH_DF_H_

#include <stdint.h>

enum bt_df_cte_type {
        BT_DF_CTE_TYPE_NONE = 0,
        BT_DF_CTE_TYPE_AOA = BIT(0),
        BT_DF_CTE_TYPE_AOD_1US = BIT(1),
        BT_DF_CTE_TYPE_AOD_2US = BIT(2),
        BT_DF_CTE_TYPE_ALL = (BT_DF_CTE_TYPE_AOA | BT_DF_CTE_TYPE_AOD_1US | BT_DF_CTE_TYPE_AOD_2US)
};

enum bt_df_antenna_switching_slot {
        BT_DF_ANTENNA_SWITCHING_SLOT_1US = 0x1,
        BT_DF_ANTENNA_SWITCHING_SLOT_2US = 0x2
};

enum bt_df_packet_status {
        BT_DF_CTE_CRC_OK = 0x0,
        BT_DF_CTE_CRC_ERR_CTE_BASED_TIME = 0x1,
        BT_DF_CTE_CRC_ERR_CTE_BASED_OTHER = 0x2,
        BT_DF_CTE_INSUFFICIENT_RESOURCES = 0xFF
};

struct bt_df_adv_cte_tx_param {
        uint8_t  cte_len;
        uint8_t  cte_type;
        uint8_t  cte_count;
        uint8_t  num_ant_ids;
        uint8_t  *ant_ids;
};

struct bt_df_per_adv_sync_cte_rx_param {
        uint8_t cte_types;
        uint8_t slot_durations;
        uint8_t max_cte_count;
        uint8_t num_ant_ids;
        const uint8_t *ant_ids;
};

enum bt_df_iq_sample {
        BT_DF_IQ_SAMPLE_8_BITS_INT,
        BT_DF_IQ_SAMPLE_16_BITS_INT,
};

struct bt_df_per_adv_sync_iq_samples_report {
        uint8_t chan_idx;
        int16_t rssi;
        uint8_t rssi_ant_id;
        uint8_t cte_type;
        uint8_t slot_durations;
        uint8_t packet_status;
        uint16_t per_evt_counter;
        uint8_t sample_count;
        enum bt_df_iq_sample sample_type;
        union {
                struct bt_hci_le_iq_sample const *sample;
                struct bt_hci_le_iq_sample16 const *sample16;
        };
};

struct bt_df_conn_cte_rx_param {
        uint8_t cte_types;
        uint8_t slot_durations;
        uint8_t num_ant_ids;
        const uint8_t *ant_ids;
};

enum bt_df_conn_iq_report_err {
        BT_DF_IQ_REPORT_ERR_SUCCESS,
        BT_DF_IQ_REPORT_ERR_NO_CTE,
        BT_DF_IQ_REPORT_ERR_PEER_REJECTED,
};

struct bt_df_conn_iq_samples_report {
        enum bt_df_conn_iq_report_err err;
        uint8_t rx_phy;
        uint8_t chan_idx;
        int16_t rssi;
        uint8_t rssi_ant_id;
        uint8_t cte_type;
        uint8_t slot_durations;
        uint8_t packet_status;
        uint16_t conn_evt_counter;
        enum bt_df_iq_sample sample_type;
        uint8_t sample_count;
        union {
                struct bt_hci_le_iq_sample const *sample;
                struct bt_hci_le_iq_sample16 const *sample16;
        };
};

struct bt_df_conn_cte_tx_param {
        uint8_t cte_types;
        uint8_t num_ant_ids;
        const uint8_t *ant_ids;
};

struct bt_df_conn_cte_req_params {
        uint16_t interval;
        uint8_t cte_length;
        uint8_t cte_type;
};

int bt_df_set_adv_cte_tx_param(struct bt_le_ext_adv *adv,
                               const struct bt_df_adv_cte_tx_param *params);

int bt_df_adv_cte_tx_enable(struct bt_le_ext_adv *adv);

int bt_df_adv_cte_tx_disable(struct bt_le_ext_adv *adv);

int bt_df_per_adv_sync_cte_rx_enable(struct bt_le_per_adv_sync *sync,
                                     const struct bt_df_per_adv_sync_cte_rx_param *params);

int bt_df_per_adv_sync_cte_rx_disable(struct bt_le_per_adv_sync *sync);

int bt_df_conn_cte_rx_enable(struct bt_conn *conn, const struct bt_df_conn_cte_rx_param *params);

int bt_df_conn_cte_rx_disable(struct bt_conn *conn);

int bt_df_set_conn_cte_tx_param(struct bt_conn *conn, const struct bt_df_conn_cte_tx_param *params);

int bt_df_conn_cte_req_enable(struct bt_conn *conn, const struct bt_df_conn_cte_req_params *params);

int bt_df_conn_cte_req_disable(struct bt_conn *conn);

int bt_df_conn_cte_rsp_enable(struct bt_conn *conn);

int bt_df_conn_cte_rsp_disable(struct bt_conn *conn);

#endif /* ZEPHYR_INCLUDE_BLUETOOTH_DF_H_ */