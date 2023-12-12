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


import functools
import socket
import sys
import signal
import time
from datetime import datetime


import ctypes
import stdwp
stdchatf = ctypes.CDLL('./stdchatf.so')

def sigint_handler(conn, signal, frame):
    try:
        global s
        print('Server will shut down in five seconds.')

        x = 5
        sending = stdwp.create_word_packet('Server will shut down in five seconds.', 'm')
        conn.sendall(sending)
        while x != 0:
            conn.sendall(stdwp.create_word_packet(str(x), 'm'))
            x = x-1
            time.sleep(1)

        conn.close()
        sys.exit(0)
    except Exception as e:
        print(f'Error in sigint_handler: {e}')


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
#            signal.signal(signal.SIGINT, sigint_handler)
            s.bind(("",portNum))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                with conn:
#                    signal.signal(signal.SIGINT, sigint_handler)
                    #custom_param_value = 5  # Set your desired parameter value here
                    sigint_handler_with_param = functools.partial(sigint_handler, conn)
                    signal.signal(signal.SIGINT, sigint_handler_with_param)
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
                        nickname = readPackets(conn, int.from_bytes(length, byteorder='big'))
                        print(nickname)
                        isUnique = stdchatf.isNicknameUnique(b"nicknames.txt", nickname)
                        print("GOT HERE 1")
                        if isUnique == 0:
                            retry = stdwp.create_word_packet("RETRY", 'm')
                            print("Sent RETRY")
                            conn.sendall(retry)
                        else:
                            print("GOTHERE2")
                            #zaynin's code to put nickname stuff in
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            stdchatf.storeNickname(b"nicknames.txt", current_time.encode('utf-8'), clientIP.encode('utf-8'), nickname)


                            ready = stdwp.create_word_packet("READY", 'm')
                            print("SENDING READY")
                            conn.sendall(ready)
                            print("Past")

                    chat = " "
                    type = " "
                    while(chat != 'BYE' and type != 'c'):
#                        print("GOTHERE3")
                        length = readPackets(conn, 2)
                        wordPacket = length + readPackets(conn, int.from_bytes(length, byteorder='big') + 1)
                        print(wordPacket)
                        chat = stdwp.extract_word_packet_message(wordPacket)
#                        print(chat.encode())
                        #print(type.encode())
                        type = stdwp.get_word_packet_type(wordPacket)
#                        print(type.encode())
#                        print("GOTHERE5")
                        if length == 0:
                            break

                        if type == 'c':
                            command_parts = chat.split()
                            if command_parts[0] == "nick":
                                nickname = command_parts[1].encode('utf-8')
                                isUnique = stdchatf.isNicknameUnique(b'nicknames.txt', nickname)
                                while isUnique == 0:
                                    stdchatf.storeNickname(b"nicknames.txt", datetime.now().encode('utf-8'), clientIP.encode('utp+8'), nickname)
                                    conn.sendall(ready)
                                else:
                                    retry = stdwp.create_word_packet("RETRY", 'm')
                                    conn.sendall(retry)
                    #zaynin's code for putting into log file
                        else:
                            print("Made it to log file stuff.")
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            stdchatf.writeToLogFile(b"logfile.txt", current_time.encode('utf+8'), nickname, chat.encode())

                            # Zaynin's code:
                            # EVERY TIME YOU GET A CHAT MESSAGE FROM A CLIENT AND STORE IT IN THE LOG FILE, SEND THAT MESSAGE TO ALL CLIENTS
                            # send back to client as a formatted log file message
                            with open("logfile.txt", "r") as file:
                                # Read all lines into a list
                                lines = file.readlines()

                                # Get the last line
                                last_line = lines[-1]
                                # Send most recent chat message to all clients
                            formatted_sendback_wp = stdwp.format_logfile_entry(last_line)
                            sendback_wp = stdwp.create_word_packet(formatted_sendback_wp, "l")
                            conn.sendall(sendback_wp)
                    conn.sendall(stdwp.create_word_packet("BYE", "m"))
                    conn.close()
    except OSError as e:
        exit(f'{e}')
    except KeyboardInterrupt:
        print("DONE")
