/////////////////////////////////////////////////////////////
//
//  Names: Zaynin Henthorn, Adam Wisnewski, Anthony Nelson
//  Course: CSC328 (Network Programming)
//  Semester/Year: Fall 2023
//  Assignment #7: Final Project
//  Short Description: 
//
//
//
//
//
/////////////////////////////////////////////////////////////

// Library C to Python

#include "stdcomm.h"
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>		// for htons()
#include <stdlib.h>

int add(int x, int y)
{
	return x + y;
}

// rename to send_word_packet
void send_all(int fd, char message[], char type)
{	
	char word_packet[3 + strlen(message)];								// Create word packet buffer
	createWordPacket(message, type, word_packet);						// Create the word packet
	
	int bytesSent;
	int bytesToSend = strlen(message) + 3;								// Sending <number of bytes in message> + 3 bytes (2 for size, 1 for type) 
	
	
	if ((bytesSent = send(fd, word_packet, bytesToSend, 0)) != bytesToSend)// Send message
	{
		if (bytesSent == -1)										// Error while sending
		{ perror("send"); }
		else if (bytesSent != bytesToSend)							// If the whole message was not sent, then recursively keep sending until the entire message is sent.
		{ 
			char remainingMessage[bytesToSend - bytesSent];			// Declare our new message to send, which is a smaller portion of the original message.
			
			for (int i = 0; i < bytesToSend - bytesSent; i++)       // Fill our new message buffer with the rest of the message that we have yet to send.
			{
				remainingMessage[i] = message[i + bytesSent];
			}
			
			send_all(fd, remainingMessage, type);				  	// Now that we have the rest our message, send it. Recursive call to send_all() to make sure that
																	// every byte is read.
		}
	}
}


int hasNickname(char filename[], char clientIP[])
{
	FILE* fp = fopen(filename, "r");						// Opens the nickname storage file
	
	char charFromFile;										// Will store each read-in char from file
	
	char ipFromFile[20];									// Where we will store each IP we read from the file
	int ipIndex = 0;
	
	// Read through the nicknames storage file. If an IP is found that matches the IP passed into this function, then the client already has a nickname. Return true (1)
	// Otherwise, if the passed-in IP is not found in the file, then that client does not yet have a nickname. Return false (0).
	while ((charFromFile = getc(fp)) != EOF)
	{
		while ((charFromFile = getc(fp)) != ',') {}			// Read in date and time

		while ((charFromFile = getc(fp)) != ',')			// Read in IP
		{
			ipFromFile[ipIndex] = charFromFile;
			ipIndex++;
		}

		while ((charFromFile = getc(fp)) != '\n') {}		// Read in nickname
		
		if (strcmp(ipFromFile, clientIP) == 0)				// If this specific IP is equal to the passed-in IP,
		{ return 1; }										// then the client already has a nickname. Return true (1).
		
		ipIndex = 0;
		memset(ipFromFile, 0, sizeof(ipFromFile));			// Reset ipFromFile
		
		// Repeat this process until you go through every IP address in the nicknames storage file.
	}
	
	return 0;												// if you got here, then the passed-in client IP was not found in the nicknames storage file,
															// meaning that the client does not already have a nickname. Return false (0).
}



// Parameter 1: The file name where the nicknames are stored (nicknames.txt)
// Parameter 2: The nickname you want to check if exists already in the nicknames storage file
int isNicknameUnique(char filename[], char nickname[])
{
	FILE* fp = fopen(filename, "r");						// Opens the nicknames storage file
	
	char charFromFile;										// Will store each read-in char from file
	
	char nickFromFile[100];									// Where we will store each nickname we read to compare if it is unique or not.
	int nicknameIndex = 0;
	
	// Read through the nicknames storage file. If a nickname is found that matches the nickname passed into this function, then return false.
	// Otherwise, if the nickname is not found, then it is unique and return true.
	while ((charFromFile = getc(fp)) != EOF)
	{
		while ((charFromFile = getc(fp)) != ',') {}					// Read in the date time

		while ((charFromFile = getc(fp)) != ',') {}					// Read in IP
		
		while ((charFromFile = getc(fp)) != '\n')					// Read in nickname
		{
			nickFromFile[nicknameIndex] = charFromFile;
			nicknameIndex++;
		}
																	
		if (strcmp(nickFromFile, nickname) == 0)					// If this specific nickname entry is equal to the passed-in nickname,
		{ return 0; } 												// then the passed-in nickname is NOT unique. Return false
		
		nicknameIndex = 0; 											
		memset(nickFromFile, 0, sizeof(nickFromFile));				// Reset nickFromFile
		
		// Repeat the process until you go through every nickname entry in the nicknames storage file.
	}
	
	return 1;	// if you get here, then the passed-in nickname was not found in the nicknames storage file, meaning that the nickname is unique.
	
}





// TO DO: if the nicknames.txt file is empty, it will segfault. account for if there is nothing in the file


// Notes: 1. 
void storeNickname(char filename[], char dateAndTime[], char clientIP[], char nickname[])
{
	// Open the current nicknames file. We will be reading from this file to determine if the clientIP already has a nickname.
	FILE* fp = fopen(filename, "r");                // Open the current nicknames file
													// a: appends to the file (instead of overwriting)
	char charFromFile;
	char dateTime[100];
	char clientIPAddress[strlen(clientIP) + 1];
		 clientIPAddress[strlen(clientIP)] = '\0';
	char clientNickname[100];

	// If a client already has a nickname entry, remove it.
		// Open a temporary file - this is where we will write the new file with the removed nickname entry.
		FILE* tempfp = fopen("temp.txt", "w");
		
		// Read through the nicknames file, and if there is an entry with the same clientIP, don't write it to the new temporary file.
		while ((charFromFile = getc(fp)) != EOF)
		{
			dateTime[0] = charFromFile;   // store the first char in the dateTime
			// Read up until the first ",". Now we are at the clientIP.
			int dateAndTimeIndex = 1;
			while ((charFromFile = getc(fp)) != ',')
			{
				dateTime[dateAndTimeIndex] = charFromFile;
				dateAndTimeIndex++;
			}
			
			// Now, read in the clientIP.
			int clientIPAddressIndex = 0;
			while ((charFromFile = getc(fp)) != ',')
			{
				clientIPAddress[clientIPAddressIndex] = charFromFile;
				clientIPAddressIndex++;
			}
			
			// Now, read in client nickname.
			int clientNicknameIndex = 0;
			while ((charFromFile = getc(fp)) != '\n')
			{
				clientNickname[clientNicknameIndex] = charFromFile;
				clientNicknameIndex++;
			}
			
			// Now that we have the client IP from the file, compare it to the client IP passed into this function. If they are the same, do not write to new file.
			// Otherwise, write this entire nickname entry to the new file.
			printf("client ip address: %s\n", clientIPAddress);
			printf("clientIP: %s\n", clientIP);
			//if (clientIPAddress != clientIP)
			if (strcmp(clientIPAddress, clientIP) != 0)
			{
				printf("Not equal.\n");
			}
			else
			{
				printf("Equal\n");
			}
			
			
			//if (clientIPAddress != clientIP)
			if (strcmp(clientIPAddress, clientIP) != 0)
			{
				// Write dateTime to the new file
				for (int i = 0; i < strlen(dateTime); i++)
				{ putc(dateTime[i], tempfp); }
			
				putc(',', tempfp);         							// Add comma separation
			
				// Write clientIP to the new file
				for (int i = 0; i < strlen(clientIPAddress); i++)
				{ putc(clientIPAddress[i], tempfp); }
			
				putc(',', tempfp);         							// Add comma separation
			
				// Write client nickname to the new file
				for (int i = 0; i < strlen(clientNickname); i++)
				{ putc(clientNickname[i], tempfp); }
			
				putc('\n', tempfp);									// Add newLine
			}
			
			
			// Reset dateTime and clientIPAddress and clientNickname
			memset(dateTime, 0, sizeof(dateTime));
			memset(clientIPAddress, 0, sizeof(clientIPAddress));
			memset(clientNickname, 0, sizeof(clientNickname));
		}
		// Now, we have an updated nicknames file with the current clientIP's nickname entry removed.
		
	// Write the client's new nickname entry to the file.
	for (int i = 0; i < strlen(dateAndTime); i++)   // Write the date and time to the file
	{ putc(dateAndTime[i], tempfp); }
	
	putc(',', tempfp);									// Add comma separation
	
	for (int i = 0; i < strlen(clientIP); i++)      // Write the client IP to the file
	{ putc(clientIP[i], tempfp); }
	
	putc(',', tempfp);									// Add comma separation
	
	for (int i = 0; i < strlen(nickname); i++)		// Write the nickname to the file
	{ putc(nickname[i], tempfp); }
	
	putc('\n', tempfp);									// Add newLine - this will separate nickname entries.
	
	
	
	// Close both files
	fclose(fp);
	fclose(tempfp);
	
	
	// Now, replace the original file with the temporary file
	remove(filename);
	rename("temp.txt", filename);
}


// parameter 1: the message you want to put in your word packet
// parameter 2: the type of message
// parameter 3: the buffer that the word packet will be stored in
void createWordPacket(char msg[], char type, char wordPacketBuffer[])
{
	unsigned short msg_length = strlen(msg);									// Get the length of the message
	unsigned short msg_length_be = htons(msg_length);							// Length of messsage in big endian
	
	//char word_packet[3 + msg_length];								// Initialize the word packet
	
	char* lengthOfMsgSeparatedByBytes = malloc(2);
	lengthOfMsgSeparatedByBytes = (char*)&msg_length_be;			// Store the length of our msg into a char array,
																	// where each byte in that char array is one byte
																	// of our 2-byte length. Big Endian.
																	
	wordPacketBuffer[0] = lengthOfMsgSeparatedByBytes[0];				// Store the length bytes in word packet
	wordPacketBuffer[1] = lengthOfMsgSeparatedByBytes[1];
	
	if (type == 'm')												// Put the message type into the word packet at index 2.
	{ wordPacketBuffer[2] = 'm'; }
	else if (type == 'c')
	{ wordPacketBuffer[2] = 'c'; }
	else if (type == 't')
	{ wordPacketBuffer[2] = 't'; }
	else
	{ // error, invalid type 
	}
	
	// Now, we have the word packet size and type. Now, put message into word packet.
	for (int i = 0; i < msg_length; i++)
	{
		wordPacketBuffer[i + 3] = msg[i];
	}
	
	//free(lengthOfMsgSeparatedByBytes);
}






// Receive an entire word packet. Will recieve all bytes (recv_all)
char* recv_word_packet(int fd)
{
	char* packetBuffer = (char*)malloc(65535);			// The packet buffer
	if (packetBuffer == NULL)
	{ perror("malloc"); }


	unsigned short wordSizeInHex;						// The size of each  word we will be printing - is the first two bytes read in from each word packet.
	int bytesReceived = 0;
	int bytesToReceive = 2;
	int moreBytesToReceive;
	
	// Read in the first two bytes of the word packet

	// BIG NOTE: "packetBuffer + bytesReceived" will APPEND when recv(). recv() alone will replace the entire buffer with the most recent recv().
	// Incrementing by the bytesReceived acts as an index into where I am going to store the next byte recv()ed. This took me approximately 2.5 hours to figure out...
	while (((moreBytesToReceive = recv(fd, packetBuffer + bytesReceived, 1, 0)) + bytesReceived) != 2)
	{
		if (moreBytesToReceive == -1)
		{ perror("recv"); }
		bytesReceived += moreBytesToReceive;
	}

	
	wordSizeInHex = htons(*((unsigned short*)packetBuffer));  				// Converts the buffer (which contains two hexidecimal bytes (ex: FF FF) into an unsigned short.
																			// ntohs() converts network byte order (Big Endian) to host byte order (typically little-endian). 
																			// However, ntohs() will work regardless of the host's endianness.

	char* wordPacket = (char*)malloc((int)wordSizeInHex + 3);				// Create the word packet you are going to read in
	char* lengthOfMsgSeparatedByBytes = malloc(2);
	lengthOfMsgSeparatedByBytes = (char*)&wordSizeInHex;					// Store the length of our msg into a char array,
																			// where each byte in that char array is one byte
																			// of our 2-byte length. Big Endian.
																	
	wordPacket[0] = lengthOfMsgSeparatedByBytes[0];							// Store the length bytes in word packet
	wordPacket[1] = lengthOfMsgSeparatedByBytes[1];

	memset(packetBuffer, 0, 65535);								 			// Clear the buffer. Allows a max size word to fit inside of buffer of size MAX_16BIT_INTEGER (65535).
	moreBytesToReceive = 0;
	bytesReceived = 0;
	bytesToReceive = 1;

	// Read in the third byte of the word packet, the type.
	while (((moreBytesToReceive = recv(fd, packetBuffer + bytesReceived, 1, 0)) + bytesReceived) != bytesToReceive)
	{
		if (moreBytesToReceive == -1)
		{ perror("recv"); }
		bytesReceived += moreBytesToReceive;
	}
	wordPacket[2] = packetBuffer[0];										// Store the type into the word packet

	memset(packetBuffer, 0, 65535);								 			// Clear the buffer. Allows a max size word to fit inside of buffer of size MAX_16BIT_INTEGER (65535).
	moreBytesToReceive = 0;
	bytesReceived = 0;
	bytesToReceive = (int)wordSizeInHex;
	
	// Read in the rest of the word
	while (((moreBytesToReceive = recv(fd, packetBuffer + bytesReceived, 1, 0)) + bytesReceived) != bytesToReceive)
	{
		if (moreBytesToReceive == -1)
		{ perror("recv"); }
		bytesReceived += moreBytesToReceive;
	}
	
	// Fill in the rest of the word packet with the read-in-word
	for (int i = 0; i < bytesToReceive; i++)
	{
		wordPacket[i + 3] = packetBuffer[i];
		//printf("wordPacket[%d + 3] = packetBuffer[%d] where is %c\n", i, i, packetBuffer[i]);
	}
	
	return wordPacket;
}


// Extracts the message from the word packet
char* extract_word_packet_message(char* wordPacket)
{
	char wordPacketSize[2];
	wordPacketSize[0] = wordPacket[0];														// Get the size of the message.
	wordPacketSize[1] = wordPacket[1];
	
	unsigned short wordSizeInHex;															// Get the size of the message in usable format.
	memcpy(&wordSizeInHex, wordPacketSize, sizeof(wordSizeInHex));
	
	char* wordPacketMessage = (char*)malloc((int)wordSizeInHex + 1);						// The message in the word packet. +1 for null terminator.
	
	// Fill the message from the word packet
	for (int i = 0; i < (int)wordSizeInHex; i++)
	{
		wordPacketMessage[i] = wordPacket[i + 3];
		//printf("wordPacketMessage[%d] = %c\n", i, wordPacket[i + 3]);
	}
	wordPacketMessage[wordSizeInHex] = '\0';												// Add null terminator
	
	return wordPacketMessage;
}


