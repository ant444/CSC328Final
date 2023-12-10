# (SERVER) GENERAL IDEA OF HOW TO SEND THE LOG FILE TO CLIENTS:
# Open the file in read mode
with open('your_file.txt', 'r') as file:
    # Read the first line from the file
    logfile_entry = file.readline()

    # Continue reading lines until the end of the file
    while logfile_entry:
        # You now have a logfile entry. Example: "2023-12-09T22:23:00,joe,hi there"
        formatted_logfile_entry = format_logfile_entry(logfile_entry)       # You now have a formatted logfile entry.
                                                                            # Example: "(2023-12-09T22:23:00) joe: hi there"
                                                                            
        wp_logfile_entry = create_word_packet(formatted_logfile_entry, "l") # You now have a word packet of your formatted logfile entry. (l = type, "logfile")
                                                                            # Example: 0x00 0x24 m ( 2 0 2 3 - 1 2 - 0 9 T 2 2 : 2 3 : 0 0 )   j o e :   h i   t h e r e
                                                                            
        # Send the word packet logfile entry to all clients (do that here)
    
    
        line = file.readline()                                              # Read the next log file entry
        
        

# (CLIENT) GENERAL IDEA OF HOW TO RECEIVE THE LOG FILE FROM SERVER

    # infinite while loop to receive from the server

        # read in an entire word packet, store it in variable "wp".       # Example: wp = 0x00 0x24 m ( 2 0 2 3 - 1 2 - 0 9 T 2 2 : 2 3 : 0 0 )   j o e :   h i   t h e r e
        
        # if wp's type is 'l' for "logfile":
        
            extracted_logfile_wp = extract_word_packet_message(wp)      # Extract the string from the word packet.
                                                                        # Example: extracted_logfile_wp = "(2023-12-09T22:23:00) joe: hi there"
                                                                        
            print(extracted_logfile_wp)                                 # Print the message so that the user can see it
