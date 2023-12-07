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
from datetime import datetime


import ctypes
import stdwp
stdchatf = ctypes.CDLL('./stdchatf.so')



def readPackets(s, num):
    bytes = b''
    while len(bytes) != num:
        read = s.recv(num - len(bytes))
        bytes += read
        if len(read) == 0: break
    print("READ")
    return bytes

if __name__ == "__main__":
    if len(sys.argv) > 2:
        exit("Too many arguments.")
    try:
        if len(sys.argv) == 1:
            portNum = 3001
        else:
            portNum = int(sys.argv[1])

        with socket.socket() as s:
            s.bind(("",portNum))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    clientIP = addr[0]
                    hello = stdwp.create_word_packet("HELLO", 'm')
                    conn.sendall(hello)

                    #loop for asking for nickname and checking if nickname is unique
                    isUnique = 0
                    while isUnique == 0:
                        print("CHECK")
                        length = readPackets(conn, 2)
                        if length == 0:
                            break
                        skip = readPackets(conn, 1)
                        nickname = readPackets(conn, length)

                        isUnique = stdchatf.isNicknameUnique(b"nicknames.txt", nickname)
                        if isUnique == 0:
                            retry = stdwp.create_word_packet("RETRY", 'm')
                            conn.sendall(retry)

                    #zaynin's code to put nickname stuff in
                    currtime = datetime.now()
                    isoformatted = currtime.isoformat()
                    isobytes = isoformatted.encode('utf-8')
                    stdchatf.storeNickname(b"nicknames.txt", b"ABC", clientIP.encode('utf-8'), nickname)
                    ready = stdwp.create_word_packet("READY", 'm')
                    conn.sendall(ready)

                    chat = ""
                    type = ""
                    while(chat != "quit" and type != 'c'):
                        length = readPackets(s, 2)
                        wordPacket = length+readPackets(s, length+1)
                        chat = stdwp.extract_word_packet_message(wordPacket)
                        type = stdwp.get_word_packet_type(wordPacket)

                        if length == 0:
                            break

                        if type == c:
                            command_parts = chat.split()
                            if command_parts[0] == "nick":
                                nickname = command_parts[1].encode('utf-8')
                                isUnique = stdchatf.isNicknameUnique(b'nicknames.txt', nickname)
                                while isUnique == 0:
                                    stdchat.storeNickname(b"nicknames.txt", b"ABC", clientIP.encode('utp+8'), nickname)
                                    conn.sendall(ready)
                                else:
                                    retry = stdwp.create_word_packet("RETRY", 'm')
                                    conn.sendall(retry)
                    #zaynin's code for putting into log file
#                        else:
                         #   writeToLogFile(logfile, datetime.now().encode('utf+8'), nickname, chat)
    except OSError as e:
        exit(f'{e}')
    except KeyboardInterrupt:
        print("DONE")



