CC = avr-gcc -mmcu=atmega1280
CFLAGS = -Wall -Wextra -std=c99 -O2
CPPFLAGS = -MMD

OBJCOPY = avr-objcopy

DEV ?= /dev/ttyACM0
AVRDUDE = avrdude
AFLAGS = -p m1280 -c arduino -P $(DEV) -D -b57600

SRC = galdumper.c
OBJ = $(SRC:.c=.o)
DEP = $(SRC:.c=.d)

all: galdumper.hex

program: galdumper.hex
	$(AVRDUDE) $(AFLAGS) -U "flash:w:$<"

galdumper: $(OBJ)

%.hex: %
	$(OBJCOPY) -O ihex $< $@

clean:
	$(RM) $(OBJ) $(DEP) galdumper

-include $(DEP)

.PHONY: all clean program
