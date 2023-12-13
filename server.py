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



import multiprocessing
import functools
import os
import socket
import sys
import signal
import time
import fcntl
from datetime import datetime


import ctypes
import stdwp
stdchatf = ctypes.CDLL('./stdchatf.so')

global sisterPid

def sigint_handler(conn, pid, child_receive, parent_receive, child_send, parent_send, signal, frame):
    try:
        global s

        if pid == 0 and sisterPid == 1:
            x = 5
            sending = stdwp.create_word_packet('Server will shut down in five seconds.', 'm')
            conn.sendall(sending)
            while x != 0:
                conn.sendall(stdwp.create_word_packet(str(x), 'm'))
                x = x-1
                time.sleep(1)

        if pid != 0:
            print("Server is shutting down")
            pid, status = os.wait()
            if os.WIFEXITED(status) == False:
                print("Error given when exiting")

        if pid == 0:
            conn.close()
        child_receive.close()
        parent_receive.close()
        child_send.close()
        parent_send.close()
        sys.exit(0)
    except Exception as e:
       print(f'Error in sigint_handler: {e}')


def readPackets(s, num):
    bytes = b''
    while len(bytes) != num:
        read = s.recv(num - len(bytes))
        bytes += read
        if len(read) == 0: break
#    print("READ")
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
            s.listen(5)

            #makes pipes for communication, also how many connections there are
#            parent_receive, child_send = multiprocessing.Pipe()
#            parent_send, child_receive = multiprocessing.Pipe()
            connections_send, connections_receive = multiprocessing.Pipe()

#            fatherPid = os.getpid()
            sisterPid = 0
            procNumber = 0
            processes = []
            
            #forks into different processes and makes pipes for each child, putting them into a list.
            for x in range(1,6):
                try:
                    parent_receive, child_send = multiprocessing.Pipe()
                    parent_send, child_receive = multiprocessing.Pipe()
                    processes.append((child_receive, child_send, parent_receive, parent_send))
                    procNumber += 1
                    pid = os.fork()
                except OSError as err:
                    print("Error with creating a new process: ", err.strerror)
                    sys.exit(-1)

                if pid == 0:
                    procNumber -= 1
                    break

            connected = 0
            
            while True:
                #child process
                if pid == 0:
                    conn, addr = s.accept()
                    #checks the number of connections
                    if connected == 0:
                        connections_send.send(b'1')
                        connected = 1
                    with conn:

                        #checks for keyboard interrupt
                        sigint_handler_with_param = functools.partial(sigint_handler, conn, pid, child_receive, parent_receive, child_send, parent_send)
                        signal.signal(signal.SIGINT, sigint_handler_with_param)


                        clientIP = addr[0]
                        #says hello to client to confirm connection
                        hello = stdwp.create_word_packet("HELLO", 'm')
                        conn.sendall(hello)
                        
                        #loop for asking for nickname and checking if nickname is unique
                        isUnique = 0
                        #while the nickname is not unique, keep sending retry, once it is leave loop.
                        while isUnique == 0:
                            length = readPackets(conn, 2)
                            if length == 0:
                                break
                            skip = readPackets(conn, 1)
                            nickname = readPackets(conn, int.from_bytes(length, byteorder='big'))
                            print(nickname)
                            isUnique = stdchatf.isNicknameUnique(b"nicknames.txt", nickname)
                            if isUnique == 0:
                                retry = stdwp.create_word_packet("RETRY", 'm')
                                print("Sent RETRY")
                                conn.sendall(retry)
                            else:
                                #puts nickname into file
                                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                stdchatf.storeNickname(b"nicknames.txt", current_time.encode('utf-8'), clientIP.encode('utf-8'), nickname)


                                ready = stdwp.create_word_packet("READY", 'm')
                                print("SENDING READY")
                                conn.sendall(ready)

                        chat = " "
                        type = " "

                        #creates another process, one that checks for input from user and one that sends input to user
                        pid2 = os.fork()
#                        check = 2
                        #child that sends input
                        if pid2 == 0:
                            while(chat != 'BYE' and type != 'c'):

#                                if check == 2:
#                                    print("act: "+str(os.getpid()))
#                                    print("pid2: "+str(pid2))
#                                    print("pid: "+str(pid))

     #                           check += 1

                                #child2 receives data from client

                                sisterPid = 1
                                length = readPackets(conn, 2)

                                wordPacket = length + readPackets(conn, int.from_bytes(length, byteorder='big') + 1)
                                #print(wordPacket)
                                chat = stdwp.extract_word_packet_message(wordPacket)
                                print("chat sent: "+str(chat))
                                type = stdwp.get_word_packet_type(wordPacket)

                                if length == 0:
                                    break
                                    
                                #changes nickname if requested (not implemented in client yet)
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
                                #if not a command, is a chat
                                else:
                                    #sends chats to parent proc
                                    try:
                                        print("sending chats")
#                                        print("procNumber: "+str(procNumber))
                                        processes[procNumber][1].send(nickname)
                                        processes[procNumber][1].send(chat)
                                    except Exception as e:
                                        print(f'client sends wrong: {e}')

            #                        print(processes[procNumber][2].recv())

                            #parent2 receives data from parent 1
                        else:
                            while True:
                                sigint_handler_with_param = functools.partial(sigint_handler, conn, pid, child_receive, parent_receive, child_send, parent_send)
                                signal.signal(signal.SIGINT, sigint_handler_with_param)
                                #will receive chat that was sent from the parent after it is put into log file. Then it will broadcast to all clients.
                                try:
                                    if child_receive.poll(timeout=1000):
                                        print("detected data")
                                        print(os.getpid())
                                        data = processes[procNumber][0].recv()
                                        print("read data")
                                        conn.sendall(data)
                                except BrokenPipeError:
                                    print("Pipe is closed")
                                except EOFError:
                                    print("End of file error")
                                except Exception as e:
                                    print(f"exception reading data: {e}")

                            # MOVED TO PARENT
                            # Zaynin's code:
                            # EVERY TIME YOU GET A CHAT MESSAGE FROM A CLIENT AND STORE IT IN THE LOG FILE, SEND THAT MESSAGE TO ALL CLIENTS
                            # send back to client as a formatted log file message
#                                with open("logfile.txt", "r") as file:
                                # Read all lines into a list
#                                    lines = file.readlines()

                                # Get the last line
#                                last_line = lines[-1]
                            # Send most recent chat message to all clients
#                                formatted_sendback_wp = stdwp.format_logfile_entry(last_line)
#                                sendback_wp = stdwp.create_word_packet(formatted_sendback_wp, "l")
#                                conn.sendall(sendback_wp)


                        #if user sends bye, will close connection
                        conn.sendall(stdwp.create_word_packet("BYE", "m"))
                        conn.close()


                #parent process
                else:
                    #number of connections (plus 1)
                    conn = 1

                    try:
                        while(True):

                            if connections_receive.poll():
                                data = connections_receive.recv()
                                print(data)
#                                time.sleep(1)
                                conn = conn + 1

                            #if first client sends something, read it then send chat to all clients
                            if processes[0][2].poll():
                                print("in pipe")
                                nickname = processes[0][2].recv()
                                chat = processes[0][2].recv()
                                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                stdchatf.writeToLogFile(b"logfile.txt", current_time.encode('utf+8'), nickname, chat.encode())

                                with open("logfile.txt") as file:
                                    lines = file.readlines()

                                #used to test
#                                print(f"Received from the pipe: {data}")

                                last_line = lines[-1]
                                formatted_sendback_wp = stdwp.format_logfile_entry(last_line)
                                sendback_wp = stdwp.create_word_packet(formatted_sendback_wp, "l")

                                #sends recent chat to all clients
                                print("about to send")
                                print(sendback_wp)
                                for p in range(0, conn):
                                    processes[p][3].send(sendback_wp)
                                print("sent")

                            #if second client sends something
                            if processes[1][2].poll():
                                nickname = processes[1][2].recv()
                                chat = processes[1][2].recv()
                                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                stdchatf.writeToLogFile(b"logfile.txt", current_time.encode('utf+8'), nickname, chat.encode())
                                with open("logfile.txt") as file:
                                    lines = file.readlines()
                                last_line = lines[-1]
                                formatted_sendback_wp = stdwp.format_logfile_entry(last_line)
                                sendback_wp = stdwp.create_word_packet(formatted_sendback_wp, "l")
                                print("about to send")
                                print(sendback_wp)
                                for p in range(0, conn-1):
                                    processes[p][3].send(sendback_wp)
                                print("sent")

                   #must implement more. will do soon but it works with two clients, just need to either hardcode 3 more or do a for loop or something.

                            sigint_handler_with_param = functools.partial(sigint_handler, conn, pid, child_receive, parent_receive, child_send, parent_send)
                            signal.signal(signal.SIGINT, sigint_handler_with_param)

                    except Exception as e:
                        print(f"exception sending {e}")

    except OSError as e:
        exit(f'{e}')
    except KeyboardInterrupt:
        x = 0
