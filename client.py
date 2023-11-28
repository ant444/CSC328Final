#!/usr/bin/env python3

###################################################################
#
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
import json


def main():
    if len(sys.argv) != 3:
        exit('Usage: <host> <port>')
    try:
        with socket.socket() as s:
            s.connect((sys.argv[1], int(sys.argv[2])))
            while True:
                word_length = int.from_bytes # call read and 'big'
                if word_length == 0: break
                word = #read (parameters)
                print(word.decode())
    except OSError as e:
        exit(f'{e}')


if __name__ == '__main__':
    main()


##########################################################
#
#   Function Name: getAndSendNick
#
#   Description:
#
#
#   Parameters:
#
#
#
#
#
#
#   Return Values: 
#
##########################################################
