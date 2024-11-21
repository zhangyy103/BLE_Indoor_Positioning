/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    radio.c
  * @brief   This file provides code for the configuration
  *          of the RADIO instances.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "radio.h"

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/* RADIO init function */
void MX_RADIO_Init(void)
{

  /* USER CODE BEGIN RADIO_Init 0 */

  /* USER CODE END RADIO_Init 0 */

  RADIO_HandleTypeDef hradio = {0};

  /* USER CODE BEGIN RADIO_Init 1 */

  /* USER CODE END RADIO_Init 1 */

  if (__HAL_RCC_RADIO_IS_CLK_DISABLED())
  {
    /* Radio Peripheral reset */
    __HAL_RCC_RADIO_FORCE_RESET();
    __HAL_RCC_RADIO_RELEASE_RESET();

    /* Enable Radio peripheral clock */
    __HAL_RCC_RADIO_CLK_ENABLE();
  }
  hradio.Instance = RADIO;
  HAL_RADIO_Init(&hradio);
  /* USER CODE BEGIN RADIO_Init 2 */

  /* USER CODE END RADIO_Init 2 */

}

void HAL_RADIO_MspInit(RADIO_HandleTypeDef* radioHandle)
{

  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};
  if(radioHandle->Instance==RADIO)
  {
  /* USER CODE BEGIN RADIO_MspInit 0 */

  /* USER CODE END RADIO_MspInit 0 */

  /** Initializes the peripherals clock
  */
    PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_RF;
    PeriphClkInitStruct.RFClockSelection = RCC_RF_CLK_32M;
    if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
    {
      Error_Handler();
    }

    /* RADIO clock enable */
    __HAL_RCC_RADIO_CLK_ENABLE();

    /**RADIO GPIO Configuration
    RF1     ------> RADIO_RF1
    */
    RT_DEBUG_GPIO_Init();

    /* RADIO interrupt Init */
    HAL_NVIC_SetPriority(RADIO_TXRX_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(RADIO_TXRX_IRQn);
    HAL_NVIC_SetPriority(RADIO_TXRX_SEQ_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(RADIO_TXRX_SEQ_IRQn);
  /* USER CODE BEGIN RADIO_MspInit 1 */

  /* USER CODE END RADIO_MspInit 1 */
  }
}

void HAL_RADIO_MspDeInit(RADIO_HandleTypeDef* radioHandle)
{

  if(radioHandle->Instance==RADIO)
  {
  /* USER CODE BEGIN RADIO_MspDeInit 0 */

  /* USER CODE END RADIO_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_RADIO_CLK_DISABLE();

    /* RADIO interrupt Deinit */
    HAL_NVIC_DisableIRQ(RADIO_TXRX_IRQn);
    HAL_NVIC_DisableIRQ(RADIO_TXRX_SEQ_IRQn);
  /* USER CODE BEGIN RADIO_MspDeInit 1 */

  /* USER CODE END RADIO_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */

/* USER CODE END 1 */
