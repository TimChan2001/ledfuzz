CC = gcc
CFLAGS = -Wall -O2

all: target_program

target_program: target_program.c distance.c
	$(CC) $(CFLAGS) -o target_program target_program.c distance.c
