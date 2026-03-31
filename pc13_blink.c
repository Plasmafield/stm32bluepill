#include <stdint.h>
#include "stm32f1xx.h"       // from CMSIS-Device

static void delay(volatile uint32_t t) { while (t--) __asm__("nop"); }

int main(void)
{
  /* Enable GPIOC clock (APB2) */
  RCC->APB2ENR |= RCC_APB2ENR_IOPCEN;

  /* PC13 as general-purpose push-pull output, 2 MHz
     PC13 is in CRH (pins 8..15). */
  GPIOC->CRH &= ~(GPIO_CRH_MODE13_Msk | GPIO_CRH_CNF13_Msk);
  GPIOC->CRH |=  (0x2 << GPIO_CRH_MODE13_Pos);  // 10: Output 2 MHz, CNF=00

  while (1) {
    /* On Blue Pill the LED is wired to PC13 and is ACTIVE-LOW */
    GPIOC->BSRR = GPIO_BSRR_BR13;  // LED ON
    delay(800000);
    GPIOC->BSRR = GPIO_BSRR_BS13;  // LED OFF
    delay(800000);
  }
}
