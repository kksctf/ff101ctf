CC=gcc
CFLAGS=-Wall -Werror -pedantic -Ofast -march=native

BIN=gen

all: $(BIN)

gen: SimpleHashAlgorithm.o gen.o
	$(CC) $(CFLAGS) SimpleHashAlgorithm.o gen.o -o $@

%.o:%.c
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	@rm -v $(BIN) *.o
