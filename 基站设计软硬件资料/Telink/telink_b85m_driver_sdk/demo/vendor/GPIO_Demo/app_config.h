/********************************************************************************************************
 * @file    app_config.h
 *
 * @brief   This is the header file for B85m
 *
 * @author  Driver Group
 * @date    2018
 *
 * @par     Copyright (c) 2018, Telink Semiconductor (Shanghai) Co., Ltd. ("TELINK")
 *
 *          Licensed under the Apache License, Version 2.0 (the "License");
 *          you may not use this file except in compliance with the License.
 *          You may obtain a copy of the License at
 *
 *              http://www.apache.org/licenses/LICENSE-2.0
 *
 *          Unless required by applicable law or agreed to in writing, software
 *          distributed under the License is distributed on an "AS IS" BASIS,
 *          WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *          See the License for the specific language governing permissions and
 *          limitations under the License.
 *
 *******************************************************************************************************/
#pragma once
#include "driver.h"
/* Enable C linkage for C++ Compilers: */
#if defined(__cplusplus)
extern "C" {
#endif


#if (MCU_CORE_B89)
#define LED1     		        GPIO_PD0
#define LED2     		        GPIO_PD1
#define LED3     		        GPIO_PD2
#define LED4     		        GPIO_PD3
/*
 * Button matrix table:
 * 			KEY3	KEY4
 * 	KEY1	SW2		SW3
 * 	KEY2	SW4		SW5
 */
#define KEY1           			GPIO_PD4
#define KEY2           			GPIO_PD5
#define KEY3           			GPIO_PD6
#define KEY4           			GPIO_PD7
#define IRQ_PIN           		KEY1

#elif (MCU_CORE_B87)
#define LED1     		        GPIO_PD2
#define LED2     		        GPIO_PD3
#define LED3     		        GPIO_PD4
#define LED4     		        GPIO_PD5
/*
 * Button matrix table:
 * 			KEY3	KEY4
 * 	KEY1	SW2		SW3
 * 	KEY2	SW4		SW5
 */
#define KEY1           			GPIO_PB2
#define KEY2           			GPIO_PB3
#define KEY3           			GPIO_PB4
#define KEY4           			GPIO_PB5
#define IRQ_PIN           		KEY1

#elif (MCU_CORE_B85)
#define LED1     		        GPIO_PD2
#define LED2     		        GPIO_PD3
#define LED3     		        GPIO_PD4
#define LED4     		        GPIO_PD5
/*
 * Button matrix table:
 * 			KEY3	KEY4
 * 	KEY1	SW2		SW3
 * 	KEY2	SW4		SW5
 */
#define KEY1           			GPIO_PB2
#define KEY2           			GPIO_PB3
#define KEY3           			GPIO_PB4
#define KEY4           			GPIO_PB5
#define IRQ_PIN           		KEY1

#elif (MCU_CORE_B80)
#define LED1     		        GPIO_PA4
#define LED2     		        GPIO_PA5
#define LED3     		        GPIO_PA6
#define LED4     		        GPIO_PA7
/*
 * Button matrix table:
 * 			KEY3	KEY4
 * 	KEY1	SW2		SW3
 * 	KEY2	SW4		SW5
 */
#define KEY1           			GPIO_PA0
#define KEY2           			GPIO_PD4
#define KEY3           			GPIO_PF0
#define KEY4           			GPIO_PF1
#define IRQ_PIN           		KEY1
#elif (MCU_CORE_B80B)
#define LED1                    GPIO_PA4
#define LED2                    GPIO_PA5
#define LED3                    GPIO_PA6
#define LED4                    GPIO_PA7
/*
 * Button matrix table:
 *          KEY3    KEY4
 *  KEY1    SW2     SW3
 *  KEY2    SW4     SW5
 */
#define KEY1                    GPIO_PA0
#define KEY2                    GPIO_PD4
#define KEY3                    GPIO_PF0
#define KEY4                    GPIO_PF1
#define IRQ_PIN                 KEY1
#endif

#define GPIO_DEMO_KEY			1	 //Short press SW2 intermittent trigger interrupts,short press KEY3 to generate an edge signal.
#define GPIO_DEMO_SQUARE_WAVE	2	 //long presses SW2 to continuously trigger interrupts,IRQ_PIN connects to KEY3, toggle KEY3 to generate a square wave signal.
#define GPIO_DEMO_MODE 			GPIO_DEMO_KEY

#define GPIO_HIGH_RESISTOR		   1
#define GPIO_IRQ				   2
#define GPIO_IRQ_RSIC0			   3
#define GPIO_IRQ_RSIC1			   4

#if(MCU_CORE_B80 || MCU_CORE_B80B)
#define GPIO_IRQ_RSIC2             5//only B80_A and B80_B support
#if (MCU_CORE_B80)
#define GPIO_SEL_IRQ_GROUP         6//only  B80_A support
#elif (MCU_CORE_B80B)
#define GPIO_SEL_IRQ_NEW_RISC      6//only  B80_B support
#define GPIO_IRQ_NEW_RISC_NUM      RISC3
#endif
#endif

#define AUTO_TEST_MODE 			   7 // For internal testing, users need not care

#define GPIO_MODE 				GPIO_IRQ

#define GPIO_DEMO_KEY			1	 //Short press SW2 intermittent trigger interrupts,short press KEY3 to generate an edge signal.
#define GPIO_DEMO_SQUARE_WAVE	2	 //long presses SW2 to continuously trigger interrupts,IRQ_PIN connects to KEY3, toggle KEY3 to generate a square wave signal.
#define GPIO_DEMO_MODE 			GPIO_DEMO_KEY



/* Define system clock */
#define CLOCK_SYS_CLOCK_HZ  	24000000

#if(MCU_CORE_B89)
#if(CLOCK_SYS_CLOCK_HZ==12000000)
	#define SYS_CLK  	SYS_CLK_12M_Crystal
#elif (CLOCK_SYS_CLOCK_HZ==16000000)
	#define SYS_CLK  	SYS_CLK_16M_Crystal
#elif (CLOCK_SYS_CLOCK_HZ==24000000)
	#define SYS_CLK  	SYS_CLK_24M_Crystal
#endif
#else
#if(CLOCK_SYS_CLOCK_HZ==12000000)
	#define SYS_CLK  	SYS_CLK_12M_Crystal
#elif (CLOCK_SYS_CLOCK_HZ==16000000)
	#define SYS_CLK  	SYS_CLK_16M_Crystal
#elif (CLOCK_SYS_CLOCK_HZ==24000000)
	#define SYS_CLK  	SYS_CLK_24M_Crystal
#elif (CLOCK_SYS_CLOCK_HZ==32000000)
	#define SYS_CLK  	SYS_CLK_32M_Crystal
#elif (CLOCK_SYS_CLOCK_HZ==48000000)
	#define SYS_CLK  	SYS_CLK_48M_Crystal
#endif
#endif
/* List tick per second/millisecond/microsecond */
enum{
	CLOCK_SYS_CLOCK_1S = CLOCK_SYS_CLOCK_HZ,				///< system tick per 1 second
	CLOCK_SYS_CLOCK_1MS = (CLOCK_SYS_CLOCK_1S / 1000),		///< system tick per 1 millisecond
	CLOCK_SYS_CLOCK_1US = (CLOCK_SYS_CLOCK_1S / 1000000),   ///< system tick per 1 microsecond
};



/* Disable C linkage for C++ Compilers: */
#if defined(__cplusplus)
}
#endif
