#!/usr/bin/env python3

###################################################################
#       Names: Anthony Nelson, Zaynin Henthorn, Adam Wisnewski
#       Course: CSC328 (Network Programming)
#       Semester/Year: Fall 2023
#       Assignment #7: Final Project
#       Short Description: Accept the server's hostname, and
#       optionally, port number as command line arguments.
#       If no port number command line argument is given,
#       should include a default port number.
#       The user enters a message in the client, and it is
#       sent to the server.
#       Client sends BYE to server upon client disconnect.
#       Client can send NICK to server, and contains user's
#       selected nickname.
#       The client should have a way to receive chat messages
#       from the server.
#       You have the choice to make this push-based or pull-based.
#
####################################################################
import socket
import sys
import ctypes
import os
import stdwp
from multiprocessing import Process, Pipe
stdchatf = ctypes.CDLL('./stdchatf.so')



def receive_word_packet(s):
    word_length = int.from_bytes(s.recv(2), byteorder='big')  # Receive the word length
    skip = s.recv(1)
    word_packet = s.recv(word_length)  # Receive the word packet based on the length received
    decodedwordpacket = word_packet.decode('utf-8')
    #print(decodedwordpacket)
    return decodedwordpacket



def recv_chat_msg(s):
    while True:
        chat_packet = s.recv(1024)
        if not chat_packet:
            break
        chat_message = chat_packet.decode('utf-8')
        print(f'Received: {chat_message}')



def send_nickname(s):
    while True:
        nickname = input("Please enter a nickname: ")
        if 2 < len(nickname) < 17:
            nick_length = len(nickname)
            typemessage = b'c'
            bytenick = nick_length.to_bytes(2, byteorder = 'big')
            nickname_bytes = bytes(nickname, 'utf-8')
            nicknamewordpacket = bytenick + typemessage + nickname_bytes
            s.sendall(nicknamewordpacket)
            return nickname
        else:
            print("Nickname should be 3-16 characters long. Retry:")

def ready_or_retry(s,nickname):
    while True:
        ready_or_not = receive_word_packet(s)
        if ready_or_not == "READY":
            print(f'Welcome, {nickname} ')
            chat = input(f'Please enter a chat message, {nickname}: ')
            chatlength = len(chat)
            typechat = b't'
            bytechat = chatlength.to_bytes(2, byteorder = 'big')
            chatbytes = bytes(chat, 'utf-8')
            chatwordpacket = bytechat + typechat + chatbytes
            s.sendall(chatwordpacket)
            break
        elif ready_or_not == "RETRY":
            while True:
                newnick = input("This nickname is in use. Please Retry: ")
                #Send it over to the client, type is t
                if 2 < len(newnick) < 17 and newnick != nickname:
                    print("Welcome, ", newnick)
                    send_nickname(s, newnick)
                    nickname = newnick
                    break
                else:
                    print("Nickname can only be 3-17 characters long. Retry:")
                    newnicklen = len(newnick)
                    type = b'c'
                    bytenewnick = newnicklen.to_bytes(2, byteorder = 'big')
                    newnickbytes = bytes(newnick, 'utf-8')
                    newnickwordpacket = bytenewnick + type + newnickbytes
                    s.sendall(newnickwordpacket)

def main():
    if len(sys.argv) < 2:
        print('Usage: python script.py <host> <port>')
        return

    host = sys.argv[1]


    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Port has to be an integer!!!!!")
            return
    else:
	port = 18008 #Defaulting the port
    try:
        with socket.socket() as s:
            s.connect((host, port))
#            pid = os.fork()
            nickname_sent = False
            word_data = receive_word_packet(s)
            if not nickname_sent:
                nickname = send_nickname(s)
                nickname_sent = True

            ready_or_retry(s,nickname)

            # Zaynin's Code: forking
            child_pid = os.fork()
            #parent_conn, child_conn = Pipe()          # create pipes to communicate between parent and child

            if child_pid == 0:
                # This code is in the child process

                # RECEIVE WORD PACKETS FROM SERVER - updates chats from all clients in real time
                while True:
                    word_data = receive_word_packet(s)
                    print(word_data)

            else:
                # This code is in the parent process

                # RECEIVE CHAT MESSAGES FROM USER
                while True:
                    #print("To quit the chat server, type '/quit'")
                    newchatmsg = input() #(f"{nickname}'s chat message: ") - weird output when this is uncommented
                    if newchatmsg.lower() == '/quit':
                        print("Sending BYE to the server...")
                        bye = stdwp.create_word_packet("BYE", 'm')
                        s.sendall(bye)
                        s.close()
                        exit()
                    else:
                        chatwrdpacket = stdwp.create_word_packet(newchatmsg, 't')
                        s.sendall(chatwrdpacket)


    except KeyboardInterrupt:
        print("Keyboard Interrupt:Program Terminated")
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()




