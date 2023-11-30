##############################################################
#
#   Names: Anthony Nelson, Zaynin Henthorn, Adam Wisnewski
#   Course: CSC 328 (Network Programming)
#   Semester/Year: Fall 2023
#   Assignment #7: Final Project
#   Short Description: This is the makefile for the client & server
#   executables. It also handles the shared library. It will also
#   submit the project to Dr. Schwesinger.
#
#############################################################

CFLAGS = -fPIC -Wall -Werror -Wextra -shared
CC = gcc #c compiler

all: server client stdchat.so

server: server.py
    cp server.py server
    chmod u+x server

client: client.py
    cp client.py client
    chmod u+x client

stdwp: stdwp.py
    cp stdwp.py
    chmod u+x stdwp


stdchatf.so: stdchatf.o
    $(CC) $(CFLAGS) -o stdchatf.so stdchatf.o

stdchat.o: stdchatf.c
    $(CC) -c -Wall -Werror -fpic stdchatf.c

.PHONY: submit clean
submit:
    ~schwesin/bin/submit csc328 project7

clean:
    rm -f server
    rm -f client
    rm -f stdwp
    rm -f *.o
    rm -f stdchatf.so


