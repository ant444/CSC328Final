#!/usr/bin/env python3

###################################################################
#
#       Names: Anthony Nelson, Zaynin Henthorn, Adam Wisnewski
#       Course: CSC328 (Network Programming)
#       Semester/Year: Fall 2023
#       Assignment #7: Final Project
#       Short Description:
#
#
#
###################################################################


import socket 
import sys
import json

def readPackets(s, num):
    bytes = b''
    while len(bytes) != num:
        read = s.recv(num - len(bytes))
        bytes += read
        if len(read) == 0: break
    return bytes

if __name__ == "__main__":
   if len(sys.argv) > 2:
        exit("Too many arguments.")
   try:
        if len(sys.argv) == 1:
            portNum = 3001
        else:
            portNum = int(sys.argv[1]))

        with socket.socket() as s:
            s.bind(portNum)
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    conn.sendall("HELLO")

                    length = readPackets(s, 2)
                    if length == 0:
                        break
                    nickname = readPackets(s, length)
                    #zaynin's code to put nickname stuff in

                while(chat != "quit"):
                    length = readPackets(s, 2)
                    if length == 0:
                        break
                    chat = readPackets(s, length)
                    #zaynin's code for putting into log file
    except OSError as e:
        exit(f'{e}')
    except KeyboardInterrupt:
        print("DONE")

