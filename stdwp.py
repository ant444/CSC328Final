#!/usr/bin/env python3
# stdwp library: Standard Word Packet

# Author: Zaynin Henthorn
# Major: Computer Science
# Course: CSC 328 Fall 2023
# Assignment: Final Group Project - Chat Server
# Purpose: The stdwp (standard word packet) library, contains functions pertaining to word packets
# and retreival from files.

import socket
import os

# Function name: create_word_packet
# Description: Creates a word packet in the following format:
#              - First two bytes are the size of the message, in hexadecimal, big endian
#              - Third byte is a char, representing the type of the word packet.
#              - Remaining bytes are each character of the message.
#              - The size stored in the first two bytes does not include the type.
# Parameters:  string message   : the message to be stored in the word packet - input
#              char/string type : the type of the word packet - input
# Return value: the created word packet, otherwise error
def create_word_packet(message, type):
    if isinstance(message, str) and isinstance(type, str) and len(type) == 1:      # Ensure that you have two strings, and the type has length of 1.
        msg_length_be = len(message).to_bytes(2, 'big')                            # Get the message length in big endian, in two bytes.
        
        if type == "c" and message[0] == "/":                                      # If the message is a command, do not put the "/" in the word packet.
            message = message[1:len(message)]
            bytes_msg = message.encode('utf+8')
        else:
            bytes_msg = message.encode('utf+8')
        
        bytes_msg = message.encode('utf+8')
        bytes_type = type.encode('utf+8')
        word_packet = (msg_length_be + bytes_type + bytes_msg)                        # Construct word packet
    else:
        raise TypeError("Invalid usage of create_word_packet Arguments must be a string and a char (str of len 1).")
    return word_packet



# Function name: extract_word_packet_message
# Description: Returns the message portion of a word packet. For example, if
#              you have a word packet: "00 05 t h e l l o", "hello" will be extracted.
# Parameters: word_packet, a byte array. - the word packet to extract the message from - input
# Return Value: string (python), extracted message. Otherwise error.
def extract_word_packet_message(word_packet):
    # Word packet format: 00 05 t h e l l o
    if len(word_packet) >= 3:                                       # Make sure that the word packet has at least the two bytes for size and the type
        word_packet_length = len(word_packet)                       # Get the word packet length
        byte_msg = word_packet[3:word_packet_length]                # Extract the message from the word packet. This will be a byte string.
        py_msg = byte_msg.decode('utf+8')                           # Convert our byte string to a python string
    else:
        raise TypeError("Invalid word packet parameter.")
    return py_msg


# Function name: get_word_packet_type
# Description: Returns the type from the word packet (as a char)
# Parameters: word_packet, a byte array - the word packet to extract the type from - input
# Return value: string/char (python), the type of the word packet (t, c, or m)
def get_word_packet_type(word_packet):
    if len(word_packet) >= 3:                                       # Make sure that the word packet has at least the two bytes for size and the type
        byte_type = word_packet[2]                                  # Gets the type from the word packet, as a byte char. Is received as ASCII code
        type = chr(byte_type)                                       # Converts ascii value (ex: 116) to char value (ex: t)
        if isinstance(type, str) and len(type) == 1:                # Makes sure that the type format is valid
            return type
        else:
            raise TypeError("Invalid type extracted from word packet.")


# Function name: is_command
# Description: Determines if a chat message is a command (if it starts with "/")
# Parameters: userChatMsg, a python string - the user's chat message. - input
# Return Value: True or False depending on whether or not the chat message is a command (starts with "/")
def is_command(userChatMsg):
    if isinstance(userChatMsg, str) and len(userChatMsg) >= 1:      # Ensure that userChatMsg is a string of at least length 1
        if userChatMsg[0] == "/":
            return True
        else:
            return False
    else:
        raise TypeError("Invalid parameter type passed into is_command(). Type required: string of length >= 1")
        
        

# Function Name: get_most_recent_chat_log
# Description: Returns the most recent chat log (bottom line from the log file)
# Parameters: string (python) filename, the name of the log file. - input
# Returns: String (python), the most recent chat log.
def get_most_recent_chat_log(filename):
    with open(filename, 'rb') as file:           # "with" will automatically close the file after this block is ended. opens as read in "b" for binary, so you can see newlines.
        try:
            file.seek(-2, os.SEEK_END)           # set the file cursor to the 2nd last byte of the file (starting from os.SEEK_END, byte -2)
            while file.read(1) != b'\n':         # keep reading 1 byte at a time, backwards, until you hit a newline.
                file.seek(-2, os.SEEK_CUR)          # Need to read backwards 2 bytes, since you read 1 forwards for every iteration of the while loop.
        except OSError:
            file.seek(0)
        last_line = file.readline().decode()        # now that you are at the start of the last line, read in the entire line.
    return last_line


# Takes in a log file entry as a parameter. A log file entry is one line from the log file, ideally obtained through calling readline().
# A log file entry is formatted as follows: <timestamp>~<nickname>~<message>
# The log file entry will be formatted to look prettier as follows:
# (Timestamp) nickname: message
# Example:
# (2023-12-09T22:23:00) Joe: hi 

# Function name: format_logfile_entry
# Desription: Formats a logfile entry (typically returned by get_most_recent_chat_log()
#             into a more attractive format, typically before printing to a client's screen.
#             A log file entry is formatted as follows: <timestamp>~<nickname>~<message>
#             The log file entry will be formatted to look prettier as follows:
#             (Timestamp) nickname: message
#             Example:
#             (2023-12-09T22:23:00) Joe: hi 
# Parameters: python string, the log file entry - input
# Return Value: python string, the formatted log file entry.
def format_logfile_entry(log_file_entry):
    formatted_log_file_entry = "("
    
    string_index = 0
    while (log_file_entry[string_index] != '~'):                        # Iterate through the log file entry until you reach the first "~"
        formatted_log_file_entry += log_file_entry[string_index]        # Append the timestamp to the formatted_log_file_entry
        string_index += 1
        
    string_index += 1                                                   # Skip the ","
    formatted_log_file_entry += ") "
        
    while (log_file_entry[string_index] != '~'):                        # Iterate through the log file entry until you reach the second "~"
        formatted_log_file_entry += log_file_entry[string_index]        # Append the nickname to the formatted_log_file_entry
        string_index += 1
        
    string_index += 1                                                   # Skip the "~"
    formatted_log_file_entry += ": "
    
    while (string_index < len(log_file_entry)):                         # Append the entire message
        formatted_log_file_entry += log_file_entry[string_index]
        string_index += 1
        
    return formatted_log_file_entry
    
    
