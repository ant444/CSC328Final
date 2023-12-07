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



def receive_word_packet(s):
    word_length = int.from_bytes(s.recv(2), byteorder='big')  # Receive the word length
    skip = s.recv(1)
    word_packet = s.recv(word_length)  # Receive the word packet based on the length received
    decodedwordpacket = word_packet.decode('utf-8')
    print(decodedwordpacket)
    return decodedwordpacket



def send_nickname(s):
    nickname = input("Please enter a nickname: ")
    print("Welcome,", nickname)
    #Get length of nickname
    nick_length = len(nickname)
    typemessage = b'c'
    bytenick = nick_length.to_bytes(2, byteorder = 'big')
    nickname_bytes = bytes(nickname, 'utf-8')
    nicknamewordpacket = bytenick + typemessage + nickname_bytes
    s.sendall(nicknamewordpacket)

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
            while True:
                word_data = receive_word_packet(s)
                send_nickname(s)
                #try:
                #    decoded_data = word_data.decode('utf-8')  # Decode the received data
                #    print(f'Word Packet: {decoded_data}')
                #except UnicodeDecodeError:
                #    print('Unable to decode the received data')

    except KeyboardInterrupt:
        print("Keyboard Interrupt:Program Terminated")


if __name__ == '__main__':
    main()




