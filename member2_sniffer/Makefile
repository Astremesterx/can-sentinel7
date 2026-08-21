CC=gcc
CFLAGS=-Wall -Wextra -O2

all: output/sniffer

output/sniffer: src/sniffer.c
	mkdir -p output
	$(CC) $(CFLAGS) -o output/sniffer src/sniffer.c

clean:
	rm -rf output/sniffer
