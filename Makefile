CC := arm-none-eabi-gcc
LD := arm-none-eabi-ld
OBJCOPY := arm-none-eabi-objcopy

CFLAGS :=
LDFLAGS := -T stm32f103RCTb.ld
DEFINES :=

CFLAGS += -I"./STM32CubeF1/Drivers/CMSIS/Core/Include"
CFLAGS += -I"./STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Include"

DEFINES += -DSTM32F103xE

all: firmware.bin

pc13_blink.o: pc13_blink.c
	$(CC) $(CFLAGS) $(DEFINES) -c $^

boot.o: boot.c
	$(CC) $(CFLAGS) $(DEFINES) -c $^

firmware.elf: pc13_blink.o boot.o
	$(LD) $(LDFLAGS) $^ -o $@

firmware.bin: firmware.elf
	$(OBJCOPY) -O binary $^ $@

clean:
	rm *.o *.elf *.bin
