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

stdchatf = ctypes.CDLL('./stdchatf.so')
#import stdcomm.so
#def receive_word(s, word_length):
#    received = b''
#    while len(received) < word_length:
#        chunk = s.recv(word_length - len(received))
#        if not chunk:
#            # Handle error or break loop
#            break
#        received += chunk
#    return received


stdchatf.recv_word_packet.argtypes = [ctypes.c_int]
stdchatf.recv_word_packet.restype = ctypes.c_char_p

def receive_word_packet(s):
    word_packet = stdchatf.recv_word_packet(s.fileno())
    print(f'Word Packet: {word_packet}')
    return word_packet


def main():
    if len(sys.argv) != 3:
        print('Usage: python script.py <host> <port>')
        return

    host = sys.argv[1]
    port = int(sys.argv[2])

    try:
        with socket.socket() as s:
            s.connect((host, port))
            while True:
                word_data = receive_word_packet(s)
                print(word_data)

    except OSError as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
