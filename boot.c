#include <stdint.h>

extern int main(void);

/* Symbols from linker script */
extern uint32_t _estack;
extern uint32_t _sdata, _edata;
extern uint32_t _etext;
extern uint32_t _sbss, _ebss;

void Reset_Handler(void);

void Default_Handler(void) { while(1) {} }

__attribute__((section(".isr_vector")))
void (* const vectors[])(void) = {
    (void (*)(void))&_estack, /* 0  Initial SP */
    Reset_Handler,            /* 1  Reset */
    Default_Handler,          /* 2  NMI */
    Default_Handler,          /* 3  HardFault */
    Default_Handler,          /* 4  MemManage */
    Default_Handler,          /* 5  BusFault */
    Default_Handler,          /* 6  UsageFault */
    0, 0, 0, 0,               /* 7-10 Reserved */
    Default_Handler,          /* 11 SVC */
    Default_Handler,          /* 12 DebugMon */
    0,                        /* 13 Reserved */
    Default_Handler,          /* 14 PendSV */
    Default_Handler,          /* 15 SysTick */
};

static void SystemInit(void)
{
  /* Optional: set clocks. For LED blink we can live with reset clock (8 MHz HSI). */
}

void Reset_Handler(void)
{
  /* Copy .data from Flash to RAM */
  uint32_t *src = (uint32_t *)&_etext;
  uint32_t *dst = &_sdata;
  while (dst < &_edata) { *dst++ = *src++; }

  /* Zero .bss */
  for (uint32_t *b = &_sbss; b < &_ebss; ++b) *b = 0;

  SystemInit();
  (void)main();

  /* If main returns, loop */
  for(;;){}
}
