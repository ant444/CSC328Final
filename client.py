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



#####################################################################
#
#       Function Name: child_process
#
#       Description: This function handles the child process, where it
#       will send in the pipe to the parent process when to close
#
#       Parameters, s - socket
#                   pout - parent out
#
#       Return Value: N/A
#
#
#####################################################################
def child_process(s, pout):
    global child_process_finished
    while True:
        word_data = receive_word_packet(s) #recv worddata
        print(word_data)
        if word_data == "BYE" or word_data == "1":  #check if it is done
            child_process_finished = True           #if so close
            s.close()
            pout.write("f")
            pout.flush()
            exit()


######################################################################
#
#       Function Name: receive_word_packet
#
#       Description: This function receives the word packets of hello,
#       retry and ready
#
#       Parameters: s - socket
#
#       Return Value: The decoded word packet
#
#
#
#####################################################################
def receive_word_packet(s):
    word_length = int.from_bytes(s.recv(2), byteorder='big') #get the length
    skip = s.recv(1)                                         #dont care about the type
    word_packet = s.recv(word_length)                       #get actual word packet
    decodedwordpacket = word_packet.decode('utf-8')           #decode it
    return decodedwordpacket



####################################################################
#
#       Function Name: recv_chat_msg
#
#       Description: This function will actively receive chat messages
#               from the client via select.
#
#       Parameters: s - socket
#
#       Return Value: N/A
#
#
#
###################################################################
def recv_chat_msg(s):
    while True:
        chat_packet = s.recv(1024) #actively recieve
        if not chat_packet:
            break
        chat_message = chat_packet.decode('utf-8') #decode it
        if chat_message == "1":
            s.close()
            os._exit(0)
        print(f'Received: {chat_message}')




###################################################################
#
#       Function Name: send_nickname
#
#       Description: This function will send the nickname after it
#                   receives hello.It prompts for user input and
#                   handles if it contains any banned characters
#
#       Parameters: s - socket
#
#       Return Value: nickname - the nickname inputted
#
#
###################################################################
def send_nickname(s):
    while True:
        banned_chars = ['~', ',', ' ', '.', '\'', '\'', '/'] #banned words
        containsBannedChar = False
        nickname = input("Please enter a nickname: ")
        for char in banned_chars:
            if char in nickname:    #check if nickname contains banned char
                print("Your nickname contains a banned character. Banned characters: ~ , space, ., \', \". Retry:")
                containsBannedChar = True
                break
        if 2 < len(nickname) < 17 and containsBannedChar == False:  # make sure length is greater than2 and less than 16
            nick_length = len(nickname)
            typemessage = b'c'
            bytenick = nick_length.to_bytes(2, byteorder='big')
            nickname_bytes = bytes(nickname, 'utf-8')
            nicknamewordpacket = bytenick + typemessage + nickname_bytes
            s.sendall(nicknamewordpacket) #send the nickname
            return nickname
        else: #check for length
            print("Nickname should be 3-16 characters long. Retry:")

###################################################################
#
#       Function Name: ready_or_retry
#
#       Description: This function checks for ready or retry and handles
#       it accordingly. It also handles the banned characters in user input.
#
#       Parameters: s - socket
#                   nickname - the user's chosen nickname
#
#       Return Value: NA
#
#
##################################################################
def ready_or_retry(s, nickname):
    containsBannedChatChar = False
    while True:
        if containsBannedChatChar == False:
            ready_or_not = receive_word_packet(s) #recv word packet
        if ready_or_not == "READY": #check for ready, go as normal if so
            print(f'Welcome, {nickname} ')
            chat = input(f'Please enter a chat message, {nickname}: ')
            banned_chars = ['~']
            containsBannedChatChar = False
            for char in banned_chars: #check for banned chars
                if char in chat:
                    containsBannedChatChar = True
            if containsBannedChatChar == True:
                print("Your chat messsage contains a banned character. Banned characters: \"~\" Retry:")
                chat = input(f'Please enter a chat message, {nickname}: ')
            elif chat == '/quit': #quits the client
                print("Sending BYE to the server.")
                bye = stdwp.create_word_packet("BYE", 'm')
                s.sendall(bye)
                s.close()
                os._exit(0)
            else:
                chatlength = len(chat) #otherwise just send the chat
                typechat = b't'
                bytechat = chatlength.to_bytes(2, byteorder='big')
                chatbytes = bytes(chat, 'utf-8')
                chatwordpacket = bytechat + typechat + chatbytes
                s.sendall(chatwordpacket)
                break
        elif ready_or_not == "RETRY":
            print("This nickname is in use. Please retry.")
            nickname = send_nickname(s)

###############################################################
#
#       Function Name: main
#
#       Description: This function handles command line args
#       and calls all of the important functions in order to work
#
#       Parameters: NA
#
#       Return Value: Int - 0 or -1
#
#
###############################################################
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
            #call ready_or_retry
            ready_or_retry(s, nickname)

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
                    #implement select via this web, used as a reference: https://pymotw.com/2/select/
                    ready, _, _ = select.select([pin], [], [], 0.1)
                    if pin in ready:
                        data = pin.readline()
                        if data == "f":
                            print("Goodbye.")
                            exit()
                    if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                        newchatmsg = input(f"{nickname}'s chat message: ") #get user input
                        banned_chars = ['~']
                        containsBannedChatChar = False
                        for char in banned_chars:
                            if char in newchatmsg:
                                containsBannedChatChar = True
                        if containsBannedChatChar == True: #check banned chars
                            print("Your chat messsage contains a banned character. Banned characters: \"~\" Retry:")
                        elif child_process_finished.value == 1 or newchatmsg.lower() == '/quit':
                            print("Sending BYE to the server...") #sending bye
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



