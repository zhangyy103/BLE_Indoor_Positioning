.. _ncs_release_notes_changelog:

Changelog for |NCS| v2.9.99
###########################

.. contents::
   :local:
   :depth: 2

The most relevant changes that are present on the main branch of the |NCS|, as compared to the latest official release, are tracked in this file.

.. note::
   This file is a work in progress and might not cover all relevant changes.

.. HOWTO

   When adding a new PR, decide whether it needs an entry in the changelog.
   If it does, update this page.
   Add the sections you need, as only a handful of sections are kept when the changelog is cleaned.
   The "Protocols" section serves as a highlight section for all protocol-related changes, including those made to samples, libraries, and so on.

Known issues
************

Known issues are only tracked for the latest official release.
See `known issues for nRF Connect SDK v2.9.0-nRF54H20-rc1`_ for the list of issues valid for the latest release.

Changelog
*********

The following sections provide detailed lists of changes by component.

IDE, OS, and tool support
=========================

* Updated:

  * The required `SEGGER J-Link`_ version to v8.10f.
  * The :ref:`installing_vsc` section on the :ref:`installation` page with the Windows-only requirement to install SEGGER USB Driver for J-Link.

Board support
=============

|no_changes_yet_note|

Build and configuration system
==============================

|no_changes_yet_note|

Bootloaders and DFU
===================

|no_changes_yet_note|

Developing with nRF91 Series
============================

|no_changes_yet_note|

Developing with nRF70 Series
============================

|no_changes_yet_note|

Working with nRF54H Series
==========================

* Removed the note on installing SEGGER USB Driver for J-Link on Windows from the :ref:`ug_nrf54h20_gs` page and moved its contents to the `nRF Util prerequisites`_ documentation.
  The Windows-only requirement to install the SEGGER USB Driver for J-Link is now mentioned in the :ref:`installing_vsc` section on the :ref:`installation` page.

Developing with nRF54L Series
=============================

* Added HMAC SHA-256 with a 128-bit key type to KMU, as detailed in the :ref:`ug_nrf54l_crypto_kmu_supported_key_types` documentation section.

Developing with nRF53 Series
============================

|no_changes_yet_note|

Developing with nRF52 Series
============================

|no_changes_yet_note|

Developing with Front-End Modules
=================================

|no_changes_yet_note|

Developing with PMICs
=====================

|no_changes_yet_note|

Security
========

  * Added support for HKDF-Expand and HKDF-Extract in CRACEN.
  * Added support for Ed25519ph(HashEdDSA) to CRACEN

Protocols
=========

|no_changes_yet_note|

Amazon Sidewalk
---------------

|no_changes_yet_note|

Bluetooth® LE
-------------

* Fixed an issue where a flash operation executed on the system workqueue might result in ``-ETIMEDOUT``, if there is an active Bluetooth LE connection.

Bluetooth Mesh
--------------

|no_changes_yet_note|

DECT NR+
--------

|no_changes_yet_note|

Enhanced ShockBurst (ESB)
-------------------------

* Added loading of radio trims and a fix of a hardware errata for the nRF54H20 SoC to improve the RF performance.

Gazell
------

|no_changes_yet_note|

Matter
------

* Added a new documentation page :ref:`ug_matter_group_communication` in the :ref:`ug_matter_intro_overview`.

* Disabled the :ref:`mpsl` before performing factory reset to speed up the process.

Matter fork
+++++++++++

|no_changes_yet_note|

nRF IEEE 802.15.4 radio driver
------------------------------

|no_changes_yet_note|

Thread
------

|no_changes_yet_note|

Zigbee
------

|no_changes_yet_note|

Wi-Fi
-----

|no_changes_yet_note|

Applications
============

This section provides detailed lists of changes by :ref:`application <applications>`.

Machine learning
----------------

|no_changes_yet_note|

Asset Tracker v2
----------------

* Updated the application to use the :ref:`lib_downloader` library instead of the deprecated :ref:`lib_download_client` library.

Connectivity Bridge
-------------------

|no_changes_yet_note|

IPC radio firmware
------------------

|no_changes_yet_note|

Matter Bridge
-------------

* Enabled SUIT DFU support for the :ref:`matter_bridge_app` application.
  Currently, only the Matter OTA protocol is fully supported for SUIT DFU purposes.

nRF5340 Audio
-------------

|no_changes_yet_note|

nRF Desktop
-----------

* Updated:

  * The :ref:`nrf_desktop_failsafe` to use the Zephyr :ref:`zephyr:hwinfo_api` driver for getting and clearing the reset reason information (see the :c:func:`hwinfo_get_reset_cause` and :c:func:`hwinfo_clear_reset_cause` functions).
    The Zephyr :ref:`zephyr:hwinfo_api` driver replaces the dependency on the nrfx reset reason helper (see the :c:func:`nrfx_reset_reason_get` and :c:func:`nrfx_reset_reason_clear` functions).
  * The release configuration for the :ref:`zephyr:nrf54h20dk_nrf54h20` board target to enable the :ref:`nrf_desktop_failsafe` (see the :ref:`CONFIG_DESKTOP_FAILSAFE_ENABLE <config_desktop_app_options>` Kconfig option).

* Added:

  * System Power Management for the :ref:`zephyr:nrf54h20dk_nrf54h20` board target on the application and radio cores.
    The application still has high power consumption as the Bluetooth LE controller running on the radio core requires disabling MRAM latency (:kconfig:option:`CONFIG_MRAM_LATENCY_AUTO_REQ`).
    Enabling MRAM latency makes the Bluetooth LE controller unstable.

nRF Machine Learning (Edge Impulse)
-----------------------------------

|no_changes_yet_note|

Serial LTE modem
----------------

* Updated the application to use the :ref:`lib_downloader` library instead of the deprecated :ref:`lib_download_client` library.

Thingy:53: Matter weather station
---------------------------------

|no_changes_yet_note|

Samples
=======

This section provides detailed lists of changes by :ref:`sample <samples>`.

Amazon Sidewalk samples
-----------------------

|no_changes_yet_note|

Bluetooth samples
-----------------

* :ref:`direct_test_mode` sample:

  * Added loading of radio trims and a fix of a hardware errata for the nRF54H20 SoC to improve the RF performance.

Bluetooth Fast Pair samples
---------------------------

* :ref:`fast_pair_locator_tag` sample:

  * Added support for the :ref:`zephyr:nrf54h20dk_nrf54h20` board target.

Bluetooth Mesh samples
----------------------

* Added:

  * Support for nRF54L10 in the following samples:

    * :ref:`bluetooth_mesh_sensor_client`
    * :ref:`bluetooth_mesh_sensor_server`
    * :ref:`bluetooth_ble_peripheral_lbs_coex`
    * :ref:`bt_mesh_chat`
    * :ref:`bluetooth_mesh_light_switch`
    * :ref:`bluetooth_mesh_silvair_enocean`
    * :ref:`bluetooth_mesh_light_dim`
    * :ref:`bluetooth_mesh_light`
    * :ref:`ble_mesh_dfu_target`
    * :ref:`bluetooth_mesh_light_lc`
    * :ref:`ble_mesh_dfu_distributor`

  * Support for nRF54L05 in the following samples:

    * :ref:`bluetooth_mesh_sensor_client`
    * :ref:`bluetooth_mesh_sensor_server`
    * :ref:`bluetooth_ble_peripheral_lbs_coex`
    * :ref:`bt_mesh_chat`
    * :ref:`bluetooth_mesh_light_switch`
    * :ref:`bluetooth_mesh_silvair_enocean`
    * :ref:`bluetooth_mesh_light_dim`
    * :ref:`bluetooth_mesh_light`
    * :ref:`bluetooth_mesh_light_lc`

Cellular samples
----------------

* Updated the following samples to use the :ref:`lib_downloader` library instead of the :ref:`lib_download_client` library:

  * :ref:`http_application_update_sample`
  * :ref:`http_modem_delta_update_sample`
  * :ref:`http_modem_full_update_sample`
  * :ref:`location_sample`
  * :ref:`lwm2m_carrier`
  * :ref:`lwm2m_client`
  * :ref:`modem_shell_application`
  * :ref:`nrf_cloud_multi_service`
  * :ref:`nrf_cloud_rest_fota`

* :ref:`modem_shell_application` sample:

  * Removed the ``CONFIG_MOSH_LINK`` Kconfig option.
    The link control functionality is now always enabled and cannot be disabled.

* :ref:`nrf_cloud_multi_service` sample:

  * Fixed:

    * An issue with an uninitialized variable in the :c:func:`handle_at_cmd_requests` function.
    * An issue with the too small :kconfig:option:`CONFIG_COAP_EXTENDED_OPTIONS_LEN_VALUE` Kconfig value
      in the :file:`overlay-coap_nrf_provisioning.conf` file.

* :ref:`lte_sensor_gateway` sample:

   * Fixed an issue with devicetree configuration after HCI updates in `sdk-zephyr`_.

Cryptography samples
--------------------

|no_changes_yet_note|

Debug samples
-------------

|no_changes_yet_note|

DECT NR+ samples
----------------

|no_changes_yet_note|

Edge Impulse samples
--------------------

|no_changes_yet_note|

Enhanced ShockBurst samples
---------------------------

|no_changes_yet_note|

Gazell samples
--------------

|no_changes_yet_note|

Keys samples
------------

|no_changes_yet_note|

Matter samples
--------------

* Updated the :ref:`matter_template_sample` sample document with the instructions on how to build the sample on the nRF54L15 DK with support for Matter OTA DFU and DFU over Bluetooth SMP, and using internal MRAM only.
* Enabled SUIT DFU support for the :ref:`matter_lock_sample`, and :ref:`matter_template_sample` samples.
  Currently, only the Matter OTA protocol is fully supported for SUIT DFU purposes.

Networking samples
------------------

* Updated the following samples to use the :ref:`lib_downloader` library instead of the :ref:`lib_download_client` library:

  * :ref:`aws_iot`
  * :ref:`azure_iot_hub`
  * :ref:`download_sample`

NFC samples
-----------

|no_changes_yet_note|

nRF5340 samples
---------------

* Removed the ``nRF5340: Multiprotocol RPMsg`` sample.
  Use the :ref:`ipc_radio` application instead.

Peripheral samples
------------------

* :ref:`radio_test` sample:

  * Added loading of radio trims and a fix of a hardware errata for the nRF54H20 SoC to improve the RF performance.

PMIC samples
------------

|no_changes_yet_note|

Protocol serialization samples
------------------------------

|no_changes_yet_note|

SDFW samples
------------

|no_changes_yet_note|

Sensor samples
--------------

|no_changes_yet_note|

SUIT samples
------------

|no_changes_yet_note|

Trusted Firmware-M (TF-M) samples
---------------------------------

|no_changes_yet_note|


Thread samples
--------------

|no_changes_yet_note|

Zigbee samples
--------------

|no_changes_yet_note|

Wi-Fi samples
-------------

|no_changes_yet_note|

Other samples
-------------

* :ref:`coremark_sample` sample:

  * Added support for the nRF54L05 and nRF54L10 SoCs (emulated on nRF54L15 DK).

Drivers
=======

This section provides detailed lists of changes by :ref:`driver <drivers>`.

|no_changes_yet_note|

Wi-Fi drivers
-------------

|no_changes_yet_note|

Libraries
=========

This section provides detailed lists of changes by :ref:`library <libraries>`.

Binary libraries
----------------

* :ref:`liblwm2m_carrier_readme` library:

  * Updated the glue to use the :ref:`lib_downloader` library instead of the deprecated :ref:`lib_download_client` library.

Bluetooth libraries and services
--------------------------------

* :ref:`bt_mesh` library:

  * Fixed an issue in the :ref:`bt_mesh_light_ctrl_srv_readme` model to automatically resume the Lightness Controller after recalling a scene (``NCSDK-30033`` known issue).

Common Application Framework
----------------------------

|no_changes_yet_note|

Debug libraries
---------------

|no_changes_yet_note|

DFU libraries
-------------

|no_changes_yet_note|

* :ref:`lib_fmfu_fdev`:

  * Regenerated the zcbor-generated code files using v0.9.0.

Gazell libraries
----------------

|no_changes_yet_note|

Security libraries
------------------

|no_changes_yet_note|

Modem libraries
---------------

* :ref:`pdn_readme` library:

  * Deprecated the :c:func:`pdn_dynamic_params_get` function.
    Use the new function :c:func:`pdn_dynamic_info_get` instead.

* :ref:`lte_lc_readme` library:

  * Fixed handling of ``%NCELLMEAS`` notification with status 2 (measurement interrupted) and no cells.
  * Added sending of ``LTE_LC_EVT_NEIGHBOR_CELL_MEAS`` event with ``current_cell`` set to ``LTE_LC_CELL_EUTRAN_ID_INVALID`` in case an error occurs while parsing the ``%NCELLMEAS`` notification.

* :ref:`modem_key_mgmt` library:

  * Fixed an issue with the :c:func:`modem_key_mgmt_clear` function where it returned ``-ENOENT`` when the credential was cleared.

Multiprotocol Service Layer libraries
-------------------------------------

|no_changes_yet_note|

Libraries for networking
------------------------

* Added the :ref:`lib_downloader` library.
* Deprecated the :ref:`lib_download_client` library.
  See the :ref:`migration guide <migration_3.0_recommended>` for recommended changes.

* Updated the following libraries to use the :ref:`lib_downloader` library instead of the :ref:`lib_download_client` library:

  * :ref:`lib_nrf_cloud`
  * :ref:`lib_aws_fota`
  * :ref:`lib_azure_fota`
  * :ref:`lib_fota_download`

* :ref:`lib_nrf_cloud_pgps` library:

  * Fixed the warning due to missing ``https`` download protocol.

Libraries for NFC
-----------------

|no_changes_yet_note|

nRF RPC libraries
-----------------

|no_changes_yet_note|

Other libraries
---------------

|no_changes_yet_note|

Security libraries
------------------

|no_changes_yet_note|

Shell libraries
---------------

|no_changes_yet_note|

Libraries for Zigbee
--------------------

|no_changes_yet_note|

sdk-nrfxlib
-----------

See the changelog for each library in the :doc:`nrfxlib documentation <nrfxlib:README>` for additional information.

Scripts
=======

This section provides detailed lists of changes by :ref:`script <scripts>`.

|no_changes_yet_note|

Integrations
============

This section provides detailed lists of changes by :ref:`integration <integrations>`.

Google Fast Pair integration
----------------------------

|no_changes_yet_note|

Edge Impulse integration
------------------------

|no_changes_yet_note|

Memfault integration
--------------------

|no_changes_yet_note|

AVSystem integration
--------------------

|no_changes_yet_note|

nRF Cloud integration
---------------------

|no_changes_yet_note|

CoreMark integration
--------------------

|no_changes_yet_note|

DULT integration
----------------

|no_changes_yet_note|

MCUboot
=======

The MCUboot fork in |NCS| (``sdk-mcuboot``) contains all commits from the upstream MCUboot repository up to and including ``a4eda30f5b0cfd0cf15512be9dcd559239dbfc91``, with some |NCS| specific additions.

The code for integrating MCUboot into |NCS| is located in the :file:`ncs/nrf/modules/mcuboot` folder.

The following list summarizes both the main changes inherited from upstream MCUboot and the main changes applied to the |NCS| specific additions:

|no_changes_yet_note|

Zephyr
======

.. NOTE TO MAINTAINERS: All the Zephyr commits in the below git commands must be handled specially after each upmerge and each nRF Connect SDK release.

The Zephyr fork in |NCS| (``sdk-zephyr``) contains all commits from the upstream Zephyr repository up to and including ``beb733919d8d64a778a11bd5e7d5cbe5ae27b8ee``, with some |NCS| specific additions.

For the list of upstream Zephyr commits (not including cherry-picked commits) incorporated into nRF Connect SDK since the most recent release, run the following command from the :file:`ncs/zephyr` repository (after running ``west update``):

.. code-block:: none

   git log --oneline beb733919d ^ea02b93eea

For the list of |NCS| specific commits, including commits cherry-picked from upstream, run:

.. code-block:: none

   git log --oneline manifest-rev ^beb733919d

The current |NCS| main branch is based on revision ``beb733919d`` of Zephyr.

.. note::
   For possible breaking changes and changes between the latest Zephyr release and the current Zephyr version, refer to the :ref:`Zephyr release notes <zephyr_release_notes>`.

Additions specific to |NCS|
---------------------------

|no_changes_yet_note|

zcbor
=====

|no_changes_yet_note|

Trusted Firmware-M
==================

|no_changes_yet_note|

cJSON
=====

|no_changes_yet_note|

Documentation
=============

* Added:

  * New section :ref:`ug_custom_board`.
    This section includes the following pages:

    * :ref:`defining_custom_board` - Previously located under :ref:`app_boards`.
    * :ref:`programming_custom_board` - New page.

  * New page :ref:`thingy53_precompiled` under :ref:`ug_thingy53`.
    This page includes some of the information previously located on the standalone page for getting started with Nordic Thingy:53.
  * New page :ref:`add_new_led_example` under :ref:`configuring_devicetree`.
    This page includes information previously located in the |nRFVSC| documentation.

* Updated the :ref:`create_application` page with the :ref:`creating_add_on_index` section.
* Removed the standalone page for getting started with Nordic Thingy:53.
  The contents of this page have been moved to the :ref:`thingy53_precompiled` page and to the `Programmer app <Programming Nordic Thingy:53_>`_ documentation.
