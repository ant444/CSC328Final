# stdwp library: Standard Word Packet

import socket


# Parameter 1: message: a string
# Parameter 2: type: a char
def create_word_packet(message, type):
    if isinstance(message, str) and isinstance(type, str) and len(type) == 1:      # Ensure that you have two strings, and the type has length of 1.
        msg_length_be = len(message).to_bytes(2, 'big')                            # Get the message length in big endian, in two bytes.
        bytes_msg = message.encode('utf+8')
        bytes_type = type.encode('utf+8')
        word_packet = (msg_length_be + bytes_type + bytes_msg)                        # Construct word packet
    else:
        raise TypeError("Invalid usage of create_word_packet Arguments must be a string and a char (str of len 1).")
    return word_packet


# Parameter 1: a word packet, which is a byte array.
# Converts a byte array word packet into a python string of just the message contained inside the word packet.
def extract_word_packet_message(word_packet):
    # Word packet format: 00 05 t h e l l o
    if len(word_packet) >= 3:                                       # Make sure that the word packet has at least the two bytes for size and the type
        word_packet_length = len(word_packet)                       # Get the word packet length
        byte_msg = word_packet[3:word_packet_length]                # Extract the message from the word packet. This will be a byte string.
        py_msg = byte_msg.decode('utf+8')                           # Convert our byte string to a python string
    else:
        raise TypeError("Invalid word packet parameter.")
    return py_msg

# Parameter 1: a word packet, which is a byte array
# Returns the type from the word packet. Example: Word Packet: 00 05 t h e l l o, returns 't'.
def get_word_packet_type(word_packet):
    if len(word_packet) >= 3:                                       # Make sure that the word packet has at least the two bytes for size and the type
        byte_type = word_packet[2]                                  # Gets the type from the word packet, as a byte char. Is received as ASCII code
        type = chr(byte_type)                                       # Converts ascii value (ex: 116) to char value (ex: t)
        if isinstance(type, str) and len(type) == 1:                # Makes sure that the type format is valid
            return type
        else:
            raise TypeError("Invalid type extracted from word packet.")

# Takes in a string (a chat from the user) as input. If their chat starts with "/", then they are attempting to send a command.
# Otherwise, they are not attempting to send a command.
# This is useful to determine what 'type' to create a word packet with.        
def is_command(userChatMsg):
    if isinstance(userChatMsg, str) and len(userChatMsg) >= 1:      # Ensure that userChatMsg is a string of at least length 1
        if userChatMsg[0] == "/":
            return True
        else:
            return False
    else:
        raise TypeError("Invalid parameter type passed into is_command(). Type required: string of length >= 1")

