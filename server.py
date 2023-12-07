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
            s.bind('', portNum)
            s.listen(1)
            while True:
                clientIP = s.gethostbyname(s.gethostbyname())
                conn, addr = s.accept()
                with conn:
                    hello = create_word_packet("HELLO", 'm')
                    conn.sendall(hello)

                    #loop for asking for nickname and checking if nickname is unique
                    while isUnique == 0:
                        length = readPackets(s, 2)
                        if length == 0:
                            break
                        skip = readPackets(s, 1)
                        nickname = readPackets(s, length)

                        isUnique = isNicknameUnique('nicknames.txt", nickname)
                        if isUnique == 0:
                            retry = create_word_packet("RETRY", 'm')
                            conn.sendall(retry)

                    #zaynin's code to put nickname stuff in
                    storeNickname("nicknames.txt", datetime.now().encode('utf+8'), clientIP.encode('utp+8'), nickname)
                    ready = create_word_packet("READY", 'm')
                    conn.sendall(ready)

                    while(chat != "quit" and type != c):
                        length = readPackets(s, 2)
                        wordPacket = length+readPackets(s, length+1)
                        chat = extract_word_packet_message(wordPacket)
                        type = get_word_packet_type(wordPacket)
                        
                        if length == 0:
                            break

                        if type == c:
                            command_parts = chat.split()
                            if command_parts[0] == "nick":
                                nickname = command_parts[1].encode('utf+8')
                                isUnique = isNicknameUnique('nicknames.txt", nickname)
                                while isUnique == 0:
                                    storeNickname("nicknames.txt", datetime.now().encode('utf+8'), clientIP.encode('utp+8'), nickname)
                                    conn.sendall(ready)
                                else:
                                    retry = create_word_packet("RETRY", 'm')
                                    conn.sendall(retry)
                    #zaynin's code for putting into log file
                        else:
                         #   writeToLogFile(logfile, datetime.now().encode('utf+8'), nickname, chat)
        except OSError as e:
        exit(f'{e}')
    except KeyboardInterrupt:
        print("DONE")
