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
import select
import multiprocessing
stdchatf = ctypes.CDLL('./stdchatf.so')

def child_process(s, pout):
    global child_process_finished
    while True:
        word_data = receive_word_packet(s)
        print(word_data)
        if word_data == "BYE" or word_data == "1":
            child_process_finished = True
            s.close()
            pout.write("f")
            pout.flush()
            exit()

def receive_word_packet(s):
    word_length = int.from_bytes(s.recv(2), byteorder='big')
    skip = s.recv(1)
    word_packet = s.recv(word_length)
    decodedwordpacket = word_packet.decode('utf-8')
    return decodedwordpacket

def recv_chat_msg(s):
    while True:
        chat_packet = s.recv(1024)
        if not chat_packet:
            break
        chat_message = chat_packet.decode('utf-8')
        if chat_message == "1":
            s.close()
            os._exit(0)
        print(f'Received: {chat_message}')

def send_nickname(s):
    while True:
        banned_chars = ['~', ',', ' ', '.', '\'', '\'', '/']
        containsBannedChar = False
        nickname = input("Please enter a nickname: ")
        for char in banned_chars:
            if char in nickname:
                print("Your nickname contains a banned character. Banned characters: ~ , space, ., \', \". Retry:")
                containsBannedChar = True
                break
        if 2 < len(nickname) < 17 and containsBannedChar == False:
            nick_length = len(nickname)
            typemessage = b'c'
            bytenick = nick_length.to_bytes(2, byteorder='big')
            nickname_bytes = bytes(nickname, 'utf-8')
            nicknamewordpacket = bytenick + typemessage + nickname_bytes
            s.sendall(nicknamewordpacket)
            return nickname
        else:
            print("Nickname should be 3-16 characters long. Retry:")

def ready_or_retry(s, nickname):
    containsBannedChatChar = False
    while True:
        if containsBannedChatChar == False:
            ready_or_not = receive_word_packet(s)
        if ready_or_not == "READY":
            print(f'Welcome, {nickname} ')
            chat = input(f'Please enter a chat message, {nickname}: ')
            banned_chars = ['~']
            containsBannedChatChar = False
            for char in banned_chars:
                if char in chat:
                    containsBannedChatChar = True
            if containsBannedChatChar == True:
                print("Your chat messsage contains a banned character. Banned characters: \"~\" Retry:")
                chat = input(f'Please enter a chat message, {nickname}: ')
            elif chat == '/quit':
                print("Sending BYE to the server.")
                bye = stdwp.create_word_packet("BYE", 'm')
                s.sendall(bye)
                s.close()
                os._exit(0)
            else:
                chatlength = len(chat)
                typechat = b't'
                bytechat = chatlength.to_bytes(2, byteorder='big')
                chatbytes = bytes(chat, 'utf-8')
                chatwordpacket = bytechat + typechat + chatbytes
                s.sendall(chatwordpacket)
                break
        elif ready_or_not == "RETRY":
            #while True:
            print("This nickname is in use. Please retry.")
                #send_nickname(s)
                
                
                #newnick = input("This nickname is in use. Please Retry: ")
                #if 2 < len(newnick) < 17 and newnick != nickname:
                #    print("Welcome, ", newnick)
                #    #send_nickname(s, newnick)
            nickname = send_nickname(s)
                #    nickname = newnick
                #    break
                #else:
                #    print("Nickname can only be 3-17 characters long. Retry:")

def main():
    global child_process_finished

    child_process_finished = multiprocessing.Value('i', 0)
    if len(sys.argv) < 2:
        print('Usage: python script.py <host> <port>')
        return

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 18008

    try:
        with socket.socket() as s:
            s.connect((host, port))
            nickname_sent = False
            word_data = receive_word_packet(s)
            if not nickname_sent:
                nickname = send_nickname(s)
                nickname_sent = True

            ready_or_retry(s, nickname)

            #child_process_finished.value = 0
            #child_proc = multiprocessing.Process(target=child_process, args=(s, child_conn))
            #child_proc.start()

            ########
            #
            #Used Dr. Schwesinger's pipe code as a reference for this...
            #
            ############


            pr, cw = os.pipe()
            cr, pw = os.pipe()

            pid = os.fork()

            if pid == 0:
                os.close(pr)
                os.close(pw)
                child_process(s, os.fdopen(cw, 'w'))
            else:
                os.close(cr)
                os.close(cw)
                pin = os.fdopen(pr, 'r')
                pout = os.fdopen(pw, 'w')
                while True:
                    ready, _, _ = select.select([pin], [], [], 0.1)
                    if pin in ready:
                        data = pin.readline()
                        if data == "f":
                            print("Goodbye.")
                            exit()
                    if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                        newchatmsg = input(f"{nickname}'s chat message: ")
                        banned_chars = ['~']
                        containsBannedChatChar = False
                        for char in banned_chars:
                            if char in newchatmsg:
                                containsBannedChatChar = True
                        if containsBannedChatChar == True:
                            print("Your chat messsage contains a banned character. Banned characters: \"~\" Retry:")
                        elif child_process_finished.value == 1 or newchatmsg.lower() == '/quit':
                            print("Sending BYE to the server...")
                            bye = stdwp.create_word_packet("BYE", 'c')
                            s.sendall(bye)
                            s.close()
                            os._exit(0)
                        else:
                            chatwrdpacket = stdwp.create_word_packet(newchatmsg, 't')
                            s.sendall(chatwrdpacket)

    except KeyboardInterrupt:
        print("Keyboard Interrupt: Program Terminated")
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
