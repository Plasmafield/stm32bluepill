CC := arm-none-eabi-gcc
LD := arm-none-eabi-ld
OBJCOPY := arm-none-eabi-objcopy

CFLAGS :=
LDFLAGS := -T stm32f103c8.ld
DEFINES :=

CFLAGS += -I"./STM32CubeF1/Drivers/CMSIS/Core/Include"
CFLAGS += -I"./STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Include"

DEFINES += -DSTM32F103xB

all: pc13_blink.bin

pc13_blink.o: pc13_blink.c
	$(CC) $(CFLAGS) $(DEFINES) -c pc13_blink.c

boot.o: boot.c
	$(CC) $(CFLAGS) $(DEFINES) -c boot.c

pc13_blink.elf: pc13_blink.o boot.o
	$(LD) $(LDFLAGS) $^ -o $@

pc13_blink.bin: pc13_blink.elf
	$(OBJCOPY) -O binary $^ $@

clean:
	rm *.o *.elf *.bin
