CC := arm-none-eabi-gcc
LD := arm-none-eabi-ld

CFLAGS :=
LDFLAGS :=
DEFINES :=

CFLAGS += -I"./STM32CubeF1/Drivers/CMSIS/Core/Include"
CFLAGS += -I"./STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Include"

DEFINES += -DSTM32F103xB

all: pc13_blink.elf

pc13_blink.o:
	$(CC) $(CFLAGS) $(DEFINES) -c pc13_blink.c

boot.o:
	$(CC) $(CFLAGS) $(DEFINES) -c boot.c

pc13_blink.elf: pc13_blink.o boot.o
	$(LD) $(LDFLAGS) $< -o $@

clean:
	rm *.o *.elf
