
/*
 * Copyright (c) 2017 Nordic Semiconductor ASA
 * Copyright (c) 2015-2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#ifndef ZEPHYR_INCLUDE_BLUETOOTH_BLUETOOTH_H_
#define ZEPHYR_INCLUDE_BLUETOOTH_BLUETOOTH_H_

#include <stdbool.h>
#include <string.h>

#include <zephyr/sys/util.h>
#include <zephyr/net_buf.h>
#include <zephyr/bluetooth/gap.h>
#include <zephyr/bluetooth/addr.h>
#include <zephyr/bluetooth/crypto.h>
#include <zephyr/bluetooth/classic/classic.h>

#ifdef __cplusplus
extern "C" {
#endif

#define BT_ID_DEFAULT 0

struct bt_le_ext_adv;

struct bt_le_per_adv_sync;

/* Don't require everyone to include conn.h */
struct bt_conn;

/* Don't require everyone to include iso.h */
struct bt_iso_biginfo;

/* Don't require everyone to include direction.h */
struct bt_df_per_adv_sync_iq_samples_report;

struct bt_le_ext_adv_sent_info {
        uint8_t num_sent;
};

struct bt_le_ext_adv_connected_info {
        struct bt_conn *conn;
};

struct bt_le_ext_adv_scanned_info {
        bt_addr_le_t *addr;
};

struct bt_le_per_adv_data_request {
        uint8_t start;

        uint8_t count;
};

struct bt_le_per_adv_response_info {
        uint8_t subevent;

        uint8_t tx_status;

        int8_t tx_power;

        int8_t rssi;

        uint8_t cte_type;

        uint8_t response_slot;
};

struct bt_le_ext_adv_cb {
        void (*sent)(struct bt_le_ext_adv *adv,
                     struct bt_le_ext_adv_sent_info *info);

        void (*connected)(struct bt_le_ext_adv *adv,
                          struct bt_le_ext_adv_connected_info *info);

        void (*scanned)(struct bt_le_ext_adv *adv,
                        struct bt_le_ext_adv_scanned_info *info);

#if defined(CONFIG_BT_PRIVACY)
        bool (*rpa_expired)(struct bt_le_ext_adv *adv);
#endif /* defined(CONFIG_BT_PRIVACY) */

#if defined(CONFIG_BT_PER_ADV_RSP)
        void (*pawr_data_request)(struct bt_le_ext_adv *adv,
                                  const struct bt_le_per_adv_data_request *request);
        void (*pawr_response)(struct bt_le_ext_adv *adv, struct bt_le_per_adv_response_info *info,
                              struct net_buf_simple *buf);

#endif /* defined(CONFIG_BT_PER_ADV_RSP) */
};

typedef void (*bt_ready_cb_t)(int err);

int bt_enable(bt_ready_cb_t cb);

int bt_disable(void);

bool bt_is_ready(void);

int bt_set_name(const char *name);

const char *bt_get_name(void);

uint16_t bt_get_appearance(void);

int bt_set_appearance(uint16_t new_appearance);

void bt_id_get(bt_addr_le_t *addrs, size_t *count);

int bt_id_create(bt_addr_le_t *addr, uint8_t *irk);

int bt_id_reset(uint8_t id, bt_addr_le_t *addr, uint8_t *irk);

int bt_id_delete(uint8_t id);

#define BT_DATA_SERIALIZED_SIZE(data_len) ((data_len) + 2)

struct bt_data {
        uint8_t type;
        uint8_t data_len;
        const uint8_t *data;
};

#define BT_DATA(_type, _data, _data_len) \
        { \
                .type = (_type), \
                .data_len = (_data_len), \
                .data = (const uint8_t *)(_data), \
        }

#define BT_DATA_BYTES(_type, _bytes...) \
        BT_DATA(_type, ((uint8_t []) { _bytes }), \
                sizeof((uint8_t []) { _bytes }))

size_t bt_data_get_len(const struct bt_data data[], size_t data_count);

size_t bt_data_serialize(const struct bt_data *input, uint8_t *output);

enum {
        BT_LE_ADV_OPT_NONE = 0,

        BT_LE_ADV_OPT_CONNECTABLE __deprecated = BIT(0),

        _BT_LE_ADV_OPT_CONNECTABLE = BIT(0),

        BT_LE_ADV_OPT_ONE_TIME __deprecated = BIT(1),

        _BT_LE_ADV_OPT_ONE_TIME = BIT(1),

        BT_LE_ADV_OPT_CONN = BIT(0) | BIT(1),

        BT_LE_ADV_OPT_USE_IDENTITY = BIT(2),

        BT_LE_ADV_OPT_USE_NAME = BIT(3),

        BT_LE_ADV_OPT_DIR_MODE_LOW_DUTY = BIT(4),

        BT_LE_ADV_OPT_DIR_ADDR_RPA = BIT(5),

        BT_LE_ADV_OPT_FILTER_SCAN_REQ = BIT(6),

        BT_LE_ADV_OPT_FILTER_CONN = BIT(7),

        BT_LE_ADV_OPT_NOTIFY_SCAN_REQ = BIT(8),

        BT_LE_ADV_OPT_SCANNABLE = BIT(9),

        BT_LE_ADV_OPT_EXT_ADV = BIT(10),

        BT_LE_ADV_OPT_NO_2M = BIT(11),

        BT_LE_ADV_OPT_CODED = BIT(12),

        BT_LE_ADV_OPT_ANONYMOUS = BIT(13),

        BT_LE_ADV_OPT_USE_TX_POWER = BIT(14),

        BT_LE_ADV_OPT_DISABLE_CHAN_37 = BIT(15),

        BT_LE_ADV_OPT_DISABLE_CHAN_38 = BIT(16),

        BT_LE_ADV_OPT_DISABLE_CHAN_39 = BIT(17),

        BT_LE_ADV_OPT_FORCE_NAME_IN_AD = BIT(18),

        BT_LE_ADV_OPT_USE_NRPA = BIT(19),
};

struct bt_le_adv_param {
        uint8_t  id;

        uint8_t  sid;

        uint8_t  secondary_max_skip;

        uint32_t options;

        uint32_t interval_min;

        uint32_t interval_max;

        const bt_addr_le_t *peer;
};

enum {
        BT_LE_PER_ADV_OPT_NONE = 0,

        BT_LE_PER_ADV_OPT_USE_TX_POWER = BIT(1),

        BT_LE_PER_ADV_OPT_INCLUDE_ADI = BIT(2),
};

struct bt_le_per_adv_param {
        uint16_t interval_min;

        uint16_t interval_max;

        uint32_t options;

#if defined(CONFIG_BT_PER_ADV_RSP)
        uint8_t num_subevents;

        uint8_t subevent_interval;

        uint8_t response_slot_delay;

        uint8_t response_slot_spacing;

        uint8_t num_response_slots;
#endif /* CONFIG_BT_PER_ADV_RSP */
};

#define BT_LE_ADV_PARAM_INIT(_options, _int_min, _int_max, _peer) \
{ \
        .id = BT_ID_DEFAULT, \
        .sid = 0, \
        .secondary_max_skip = 0, \
        .options = (_options), \
        .interval_min = (_int_min), \
        .interval_max = (_int_max), \
        .peer = (_peer), \
}

#define BT_LE_ADV_PARAM(_options, _int_min, _int_max, _peer) \
        ((const struct bt_le_adv_param[]) { \
                BT_LE_ADV_PARAM_INIT(_options, _int_min, _int_max, _peer) \
         })

#define BT_LE_ADV_CONN_DIR(_peer) BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONN, 0, 0, _peer)

#define BT_LE_ADV_CONN                                                                             \
        BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONNECTABLE, BT_GAP_ADV_FAST_INT_MIN_2,                      \
                        BT_GAP_ADV_FAST_INT_MAX_2, NULL)                                           \
        __DEPRECATED_MACRO

#define BT_LE_ADV_CONN_FAST_1                                                                      \
        BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONN, BT_GAP_ADV_FAST_INT_MIN_1, BT_GAP_ADV_FAST_INT_MAX_1,  \
                        NULL)

#define BT_LE_ADV_CONN_FAST_2                                                                      \
        BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONN, BT_GAP_ADV_FAST_INT_MIN_2, BT_GAP_ADV_FAST_INT_MAX_2,  \
                        NULL)

#define BT_LE_ADV_CONN_ONE_TIME BT_LE_ADV_CONN_FAST_2 __DEPRECATED_MACRO

#define BT_LE_ADV_CONN_NAME BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONNECTABLE | \
                                            BT_LE_ADV_OPT_USE_NAME, \
                                            BT_GAP_ADV_FAST_INT_MIN_2, \
                                            BT_GAP_ADV_FAST_INT_MAX_2, NULL) \
                                            __DEPRECATED_MACRO

#define BT_LE_ADV_CONN_NAME_AD BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONNECTABLE | \
                                            BT_LE_ADV_OPT_USE_NAME | \
                                            BT_LE_ADV_OPT_FORCE_NAME_IN_AD, \
                                            BT_GAP_ADV_FAST_INT_MIN_2, \
                                            BT_GAP_ADV_FAST_INT_MAX_2, NULL) \
                                            __DEPRECATED_MACRO

#define BT_LE_ADV_CONN_DIR_LOW_DUTY(_peer)                                                         \
        BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONN | BT_LE_ADV_OPT_DIR_MODE_LOW_DUTY,                      \
                        BT_GAP_ADV_FAST_INT_MIN_2, BT_GAP_ADV_FAST_INT_MAX_2, _peer)

#define BT_LE_ADV_NCONN BT_LE_ADV_PARAM(0, BT_GAP_ADV_FAST_INT_MIN_2, \
                                        BT_GAP_ADV_FAST_INT_MAX_2, NULL)

#define BT_LE_ADV_NCONN_NAME BT_LE_ADV_PARAM(BT_LE_ADV_OPT_USE_NAME, \
                                             BT_GAP_ADV_FAST_INT_MIN_2, \
                                             BT_GAP_ADV_FAST_INT_MAX_2, NULL) \
                                             __DEPRECATED_MACRO

#define BT_LE_ADV_NCONN_IDENTITY BT_LE_ADV_PARAM(BT_LE_ADV_OPT_USE_IDENTITY, \
                                                 BT_GAP_ADV_FAST_INT_MIN_2, \
                                                 BT_GAP_ADV_FAST_INT_MAX_2, \
                                                 NULL)

#define BT_LE_EXT_ADV_CONN                                                                         \
        BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | BT_LE_ADV_OPT_CONN, BT_GAP_ADV_FAST_INT_MIN_2,     \
                        BT_GAP_ADV_FAST_INT_MAX_2, NULL)

#define BT_LE_EXT_ADV_CONN_NAME BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | \
                                                BT_LE_ADV_OPT_CONNECTABLE | \
                                                BT_LE_ADV_OPT_USE_NAME, \
                                                BT_GAP_ADV_FAST_INT_MIN_2, \
                                                BT_GAP_ADV_FAST_INT_MAX_2, \
                                                NULL) \
                                                __DEPRECATED_MACRO

#define BT_LE_EXT_ADV_SCAN BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | \
                                           BT_LE_ADV_OPT_SCANNABLE, \
                                           BT_GAP_ADV_FAST_INT_MIN_2, \
                                           BT_GAP_ADV_FAST_INT_MAX_2, \
                                           NULL)

#define BT_LE_EXT_ADV_SCAN_NAME BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | \
                                                BT_LE_ADV_OPT_SCANNABLE | \
                                                BT_LE_ADV_OPT_USE_NAME, \
                                                BT_GAP_ADV_FAST_INT_MIN_2, \
                                                BT_GAP_ADV_FAST_INT_MAX_2, \
                                                NULL) \
                                                __DEPRECATED_MACRO

#define BT_LE_EXT_ADV_NCONN BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV, \
                                            BT_GAP_ADV_FAST_INT_MIN_2, \
                                            BT_GAP_ADV_FAST_INT_MAX_2, NULL)

#define BT_LE_EXT_ADV_NCONN_NAME BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | \
                                                 BT_LE_ADV_OPT_USE_NAME, \
                                                 BT_GAP_ADV_FAST_INT_MIN_2, \
                                                 BT_GAP_ADV_FAST_INT_MAX_2, \
                                                 NULL) \
                                                 __DEPRECATED_MACRO

#define BT_LE_EXT_ADV_NCONN_IDENTITY \
                BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | \
                                BT_LE_ADV_OPT_USE_IDENTITY, \
                                BT_GAP_ADV_FAST_INT_MIN_2, \
                                BT_GAP_ADV_FAST_INT_MAX_2, NULL)

#define BT_LE_EXT_ADV_CODED_NCONN BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | \
                                                  BT_LE_ADV_OPT_CODED, \
                                                  BT_GAP_ADV_FAST_INT_MIN_2, \
                                                  BT_GAP_ADV_FAST_INT_MAX_2, \
                                                  NULL)

#define BT_LE_EXT_ADV_CODED_NCONN_NAME \
                BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | BT_LE_ADV_OPT_CODED | \
                                BT_LE_ADV_OPT_USE_NAME, \
                                BT_GAP_ADV_FAST_INT_MIN_2, \
                                BT_GAP_ADV_FAST_INT_MAX_2, NULL) \
                                __DEPRECATED_MACRO

#define BT_LE_EXT_ADV_CODED_NCONN_IDENTITY \
                BT_LE_ADV_PARAM(BT_LE_ADV_OPT_EXT_ADV | BT_LE_ADV_OPT_CODED | \
                                BT_LE_ADV_OPT_USE_IDENTITY, \
                                BT_GAP_ADV_FAST_INT_MIN_2, \
                                BT_GAP_ADV_FAST_INT_MAX_2, NULL)

#define BT_LE_EXT_ADV_START_PARAM_INIT(_timeout, _n_evts) \
{ \
        .timeout = (_timeout), \
        .num_events = (_n_evts), \
}

#define BT_LE_EXT_ADV_START_PARAM(_timeout, _n_evts) \
        ((const struct bt_le_ext_adv_start_param[]) { \
                BT_LE_EXT_ADV_START_PARAM_INIT((_timeout), (_n_evts)) \
        })

#define BT_LE_EXT_ADV_START_DEFAULT BT_LE_EXT_ADV_START_PARAM(0, 0)

#define BT_LE_PER_ADV_PARAM_INIT(_int_min, _int_max, _options) \
{ \
        .interval_min = (_int_min), \
        .interval_max = (_int_max), \
        .options = (_options), \
}

#define BT_LE_PER_ADV_PARAM(_int_min, _int_max, _options) \
        ((struct bt_le_per_adv_param[]) { \
                BT_LE_PER_ADV_PARAM_INIT(_int_min, _int_max, _options) \
        })

#define BT_LE_PER_ADV_DEFAULT BT_LE_PER_ADV_PARAM(BT_GAP_PER_ADV_SLOW_INT_MIN, \
                                                  BT_GAP_PER_ADV_SLOW_INT_MAX, \
                                                  BT_LE_PER_ADV_OPT_NONE)

int bt_le_adv_start(const struct bt_le_adv_param *param,
                    const struct bt_data *ad, size_t ad_len,
                    const struct bt_data *sd, size_t sd_len);

int bt_le_adv_update_data(const struct bt_data *ad, size_t ad_len,
                          const struct bt_data *sd, size_t sd_len);

int bt_le_adv_stop(void);

int bt_le_ext_adv_create(const struct bt_le_adv_param *param,
                         const struct bt_le_ext_adv_cb *cb,
                         struct bt_le_ext_adv **adv);

struct bt_le_ext_adv_start_param {
        uint16_t timeout;
        uint8_t  num_events;
};

int bt_le_ext_adv_start(struct bt_le_ext_adv *adv,
                        const struct bt_le_ext_adv_start_param *param);

int bt_le_ext_adv_stop(struct bt_le_ext_adv *adv);

int bt_le_ext_adv_set_data(struct bt_le_ext_adv *adv,
                           const struct bt_data *ad, size_t ad_len,
                           const struct bt_data *sd, size_t sd_len);

int bt_le_ext_adv_update_param(struct bt_le_ext_adv *adv,
                               const struct bt_le_adv_param *param);

int bt_le_ext_adv_delete(struct bt_le_ext_adv *adv);

uint8_t bt_le_ext_adv_get_index(struct bt_le_ext_adv *adv);

struct bt_le_ext_adv_info {
        /* Local identity */
        uint8_t                    id;

        int8_t                     tx_power;

        const bt_addr_le_t         *addr;
};

int bt_le_ext_adv_get_info(const struct bt_le_ext_adv *adv,
                           struct bt_le_ext_adv_info *info);

typedef void bt_le_scan_cb_t(const bt_addr_le_t *addr, int8_t rssi,
                             uint8_t adv_type, struct net_buf_simple *buf);

int bt_le_per_adv_set_param(struct bt_le_ext_adv *adv,
                            const struct bt_le_per_adv_param *param);

int bt_le_per_adv_set_data(const struct bt_le_ext_adv *adv,
                           const struct bt_data *ad, size_t ad_len);

struct bt_le_per_adv_subevent_data_params {
        uint8_t subevent;

        uint8_t response_slot_start;

        uint8_t response_slot_count;

        const struct net_buf_simple *data;
};

int bt_le_per_adv_set_subevent_data(const struct bt_le_ext_adv *adv, uint8_t num_subevents,
                                    const struct bt_le_per_adv_subevent_data_params *params);

int bt_le_per_adv_start(struct bt_le_ext_adv *adv);

int bt_le_per_adv_stop(struct bt_le_ext_adv *adv);

struct bt_le_per_adv_sync_synced_info {
        const bt_addr_le_t *addr;

        uint8_t sid;

        uint16_t interval;

        uint8_t phy;

        bool recv_enabled;

        uint16_t service_data;

        struct bt_conn *conn;
#if defined(CONFIG_BT_PER_ADV_SYNC_RSP)
        uint8_t num_subevents;

        uint8_t subevent_interval;

        uint8_t response_slot_delay;

        uint8_t response_slot_spacing;

#endif /* CONFIG_BT_PER_ADV_SYNC_RSP */
};

struct bt_le_per_adv_sync_term_info {
        const bt_addr_le_t *addr;

        uint8_t sid;

        uint8_t reason;
};

struct bt_le_per_adv_sync_recv_info {
        const bt_addr_le_t *addr;

        uint8_t sid;

        int8_t tx_power;

        int8_t rssi;

        uint8_t cte_type;
#if defined(CONFIG_BT_PER_ADV_SYNC_RSP)
        uint16_t periodic_event_counter;

        uint8_t subevent;
#endif /* CONFIG_BT_PER_ADV_SYNC_RSP */
};

struct bt_le_per_adv_sync_state_info {
        bool recv_enabled;
};

struct bt_le_per_adv_sync_cb {
        void (*synced)(struct bt_le_per_adv_sync *sync,
                       struct bt_le_per_adv_sync_synced_info *info);

        void (*term)(struct bt_le_per_adv_sync *sync,
                     const struct bt_le_per_adv_sync_term_info *info);

        void (*recv)(struct bt_le_per_adv_sync *sync,
                     const struct bt_le_per_adv_sync_recv_info *info,
                     struct net_buf_simple *buf);

        void (*state_changed)(struct bt_le_per_adv_sync *sync,
                              const struct bt_le_per_adv_sync_state_info *info);

        void (*biginfo)(struct bt_le_per_adv_sync *sync, const struct bt_iso_biginfo *biginfo);

        void (*cte_report_cb)(struct bt_le_per_adv_sync *sync,
                              struct bt_df_per_adv_sync_iq_samples_report const *info);

        sys_snode_t node;
};

enum {
        BT_LE_PER_ADV_SYNC_OPT_NONE = 0,

        BT_LE_PER_ADV_SYNC_OPT_USE_PER_ADV_LIST = BIT(0),

        BT_LE_PER_ADV_SYNC_OPT_REPORTING_INITIALLY_DISABLED = BIT(1),

        BT_LE_PER_ADV_SYNC_OPT_FILTER_DUPLICATE = BIT(2),

        BT_LE_PER_ADV_SYNC_OPT_DONT_SYNC_AOA = BIT(3),

        BT_LE_PER_ADV_SYNC_OPT_DONT_SYNC_AOD_1US = BIT(4),

        BT_LE_PER_ADV_SYNC_OPT_DONT_SYNC_AOD_2US = BIT(5),

        BT_LE_PER_ADV_SYNC_OPT_SYNC_ONLY_CONST_TONE_EXT = BIT(6),
};

struct bt_le_per_adv_sync_param {
        bt_addr_le_t addr;

        uint8_t sid;

        uint32_t options;

        uint16_t skip;

        uint16_t timeout;
};

uint8_t bt_le_per_adv_sync_get_index(struct bt_le_per_adv_sync *per_adv_sync);

struct bt_le_per_adv_sync *bt_le_per_adv_sync_lookup_index(uint8_t index);

struct bt_le_per_adv_sync_info {
        bt_addr_le_t addr;

        uint8_t sid;

        uint16_t interval;

        uint8_t phy;
};

int bt_le_per_adv_sync_get_info(struct bt_le_per_adv_sync *per_adv_sync,
                                struct bt_le_per_adv_sync_info *info);

struct bt_le_per_adv_sync *bt_le_per_adv_sync_lookup_addr(const bt_addr_le_t *adv_addr,
                                                          uint8_t sid);

int bt_le_per_adv_sync_create(const struct bt_le_per_adv_sync_param *param,
                              struct bt_le_per_adv_sync **out_sync);

int bt_le_per_adv_sync_delete(struct bt_le_per_adv_sync *per_adv_sync);

int bt_le_per_adv_sync_cb_register(struct bt_le_per_adv_sync_cb *cb);

int bt_le_per_adv_sync_recv_enable(struct bt_le_per_adv_sync *per_adv_sync);

int bt_le_per_adv_sync_recv_disable(struct bt_le_per_adv_sync *per_adv_sync);

enum {
        BT_LE_PER_ADV_SYNC_TRANSFER_OPT_NONE = 0,

        BT_LE_PER_ADV_SYNC_TRANSFER_OPT_SYNC_NO_AOA = BIT(0),

        BT_LE_PER_ADV_SYNC_TRANSFER_OPT_SYNC_NO_AOD_1US = BIT(1),

        BT_LE_PER_ADV_SYNC_TRANSFER_OPT_SYNC_NO_AOD_2US = BIT(2),

        BT_LE_PER_ADV_SYNC_TRANSFER_OPT_SYNC_ONLY_CTE = BIT(3),

        BT_LE_PER_ADV_SYNC_TRANSFER_OPT_REPORTING_INITIALLY_DISABLED = BIT(4),

        BT_LE_PER_ADV_SYNC_TRANSFER_OPT_FILTER_DUPLICATES = BIT(5),
};

struct bt_le_per_adv_sync_transfer_param {
        uint16_t skip;

        uint16_t timeout;

        uint32_t options;
};

int bt_le_per_adv_sync_transfer(const struct bt_le_per_adv_sync *per_adv_sync,
                                const struct bt_conn *conn,
                                uint16_t service_data);

int bt_le_per_adv_set_info_transfer(const struct bt_le_ext_adv *adv,
                                    const struct bt_conn *conn,
                                    uint16_t service_data);

int bt_le_per_adv_sync_transfer_subscribe(
        const struct bt_conn *conn,
        const struct bt_le_per_adv_sync_transfer_param *param);

int bt_le_per_adv_sync_transfer_unsubscribe(const struct bt_conn *conn);

int bt_le_per_adv_list_add(const bt_addr_le_t *addr, uint8_t sid);

int bt_le_per_adv_list_remove(const bt_addr_le_t *addr, uint8_t sid);

int bt_le_per_adv_list_clear(void);

enum {
        BT_LE_SCAN_OPT_NONE = 0,

        BT_LE_SCAN_OPT_FILTER_DUPLICATE = BIT(0),

        BT_LE_SCAN_OPT_FILTER_ACCEPT_LIST = BIT(1),

        BT_LE_SCAN_OPT_CODED = BIT(2),

        BT_LE_SCAN_OPT_NO_1M = BIT(3),
};

#define BT_LE_SCAN_OPT_FILTER_WHITELIST __DEPRECATED_MACRO BT_LE_SCAN_OPT_FILTER_ACCEPT_LIST

enum {
        BT_LE_SCAN_TYPE_PASSIVE = 0x00,

        BT_LE_SCAN_TYPE_ACTIVE = 0x01,
};

struct bt_le_scan_param {
        uint8_t  type;

        uint8_t options;

        uint16_t interval;

        uint16_t window;

        uint16_t timeout;

        uint16_t interval_coded;

        uint16_t window_coded;
};

struct bt_le_scan_recv_info {
        const bt_addr_le_t *addr;

        uint8_t sid;

        int8_t rssi;

        int8_t tx_power;

        uint8_t adv_type;

        uint16_t adv_props;

        uint16_t interval;

        uint8_t primary_phy;

        uint8_t secondary_phy;
};

struct bt_le_scan_cb {

        void (*recv)(const struct bt_le_scan_recv_info *info,
                     struct net_buf_simple *buf);

        void (*timeout)(void);

        sys_snode_t node;
};

#define BT_LE_SCAN_PARAM_INIT(_type, _options, _interval, _window) \
{ \
        .type = (_type), \
        .options = (_options), \
        .interval = (_interval), \
        .window = (_window), \
        .timeout = 0, \
        .interval_coded = 0, \
        .window_coded = 0, \
}

#define BT_LE_SCAN_PARAM(_type, _options, _interval, _window) \
        ((struct bt_le_scan_param[]) { \
                BT_LE_SCAN_PARAM_INIT(_type, _options, _interval, _window) \
         })

#define BT_LE_SCAN_ACTIVE BT_LE_SCAN_PARAM(BT_LE_SCAN_TYPE_ACTIVE, \
                                           BT_LE_SCAN_OPT_FILTER_DUPLICATE, \
                                           BT_GAP_SCAN_FAST_INTERVAL, \
                                           BT_GAP_SCAN_FAST_WINDOW)

#define BT_LE_SCAN_ACTIVE_CONTINUOUS BT_LE_SCAN_PARAM(BT_LE_SCAN_TYPE_ACTIVE, \
                                                      BT_LE_SCAN_OPT_FILTER_DUPLICATE, \
                                                      BT_GAP_SCAN_FAST_INTERVAL_MIN, \
                                                      BT_GAP_SCAN_FAST_WINDOW)

BUILD_ASSERT(BT_GAP_SCAN_FAST_WINDOW == BT_GAP_SCAN_FAST_INTERVAL_MIN,
             "Continuous scanning is requested by setting window and interval equal.");

#define BT_LE_SCAN_PASSIVE BT_LE_SCAN_PARAM(BT_LE_SCAN_TYPE_PASSIVE, \
                                            BT_LE_SCAN_OPT_FILTER_DUPLICATE, \
                                            BT_GAP_SCAN_FAST_INTERVAL, \
                                            BT_GAP_SCAN_FAST_WINDOW)

#define BT_LE_SCAN_PASSIVE_CONTINUOUS BT_LE_SCAN_PARAM(BT_LE_SCAN_TYPE_PASSIVE, \
                                                       BT_LE_SCAN_OPT_FILTER_DUPLICATE, \
                                                       BT_GAP_SCAN_FAST_INTERVAL_MIN, \
                                                       BT_GAP_SCAN_FAST_WINDOW)

BUILD_ASSERT(BT_GAP_SCAN_FAST_WINDOW == BT_GAP_SCAN_FAST_INTERVAL_MIN,
             "Continuous scanning is requested by setting window and interval equal.");

#define BT_LE_SCAN_CODED_ACTIVE \
                BT_LE_SCAN_PARAM(BT_LE_SCAN_TYPE_ACTIVE, \
                                 BT_LE_SCAN_OPT_CODED | \
                                 BT_LE_SCAN_OPT_FILTER_DUPLICATE, \
                                 BT_GAP_SCAN_FAST_INTERVAL, \
                                 BT_GAP_SCAN_FAST_WINDOW)

#define BT_LE_SCAN_CODED_PASSIVE \
                BT_LE_SCAN_PARAM(BT_LE_SCAN_TYPE_PASSIVE, \
                                 BT_LE_SCAN_OPT_CODED | \
                                 BT_LE_SCAN_OPT_FILTER_DUPLICATE, \
                                 BT_GAP_SCAN_FAST_INTERVAL, \
                                 BT_GAP_SCAN_FAST_WINDOW)

int bt_le_scan_start(const struct bt_le_scan_param *param, bt_le_scan_cb_t cb);

int bt_le_scan_stop(void);

int bt_le_scan_cb_register(struct bt_le_scan_cb *cb);

void bt_le_scan_cb_unregister(struct bt_le_scan_cb *cb);

int bt_le_filter_accept_list_add(const bt_addr_le_t *addr);

int bt_le_filter_accept_list_remove(const bt_addr_le_t *addr);

int bt_le_filter_accept_list_clear(void);

int bt_le_set_chan_map(uint8_t chan_map[5]);

int bt_le_set_rpa_timeout(uint16_t new_rpa_timeout);

void bt_data_parse(struct net_buf_simple *ad,
                   bool (*func)(struct bt_data *data, void *user_data),
                   void *user_data);

struct bt_le_oob_sc_data {
        uint8_t r[16];

        uint8_t c[16];
};

struct bt_le_oob {
        bt_addr_le_t addr;

        struct bt_le_oob_sc_data le_sc_data;
};

int bt_le_oob_get_local(uint8_t id, struct bt_le_oob *oob);

int bt_le_ext_adv_oob_get_local(struct bt_le_ext_adv *adv,
                                struct bt_le_oob *oob);

int bt_unpair(uint8_t id, const bt_addr_le_t *addr);

struct bt_bond_info {
        bt_addr_le_t addr;
};

void bt_foreach_bond(uint8_t id, void (*func)(const struct bt_bond_info *info,
                                           void *user_data),
                     void *user_data);

int bt_configure_data_path(uint8_t dir, uint8_t id, uint8_t vs_config_len,
                           const uint8_t *vs_config);

struct bt_le_per_adv_sync_subevent_params {
        uint16_t properties;

        uint8_t num_subevents;

        uint8_t *subevents;
};

int bt_le_per_adv_sync_subevent(struct bt_le_per_adv_sync *per_adv_sync,
                                struct bt_le_per_adv_sync_subevent_params *params);

struct bt_le_per_adv_response_params {
        uint16_t request_event;

        uint8_t request_subevent;

        uint8_t response_subevent;

        uint8_t response_slot;
};

int bt_le_per_adv_set_response_data(struct bt_le_per_adv_sync *per_adv_sync,
                                    const struct bt_le_per_adv_response_params *params,
                                    const struct net_buf_simple *data);

#ifdef __cplusplus
}
#endif
#endif /* ZEPHYR_INCLUDE_BLUETOOTH_BLUETOOTH_H_ */