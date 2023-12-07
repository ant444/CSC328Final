// Library C to Python

#include "stdchatf.h"
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>		// for htons()
#include <stdlib.h>


// Takes a file (nicknames storage file) and a IP and determines if that client's IP exists in the nickname file and has a nickname associated with it.
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



// Notes: 1. 
// Maximum dateAndTime length: 100
// Maximum clientNickname: 100
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
				for (size_t i = 0; i < strlen(dateTime); i++)
				{ putc(dateTime[i], tempfp); }
			
				putc(',', tempfp);         							// Add comma separation
			
				// Write clientIP to the new file
				for (size_t i = 0; i < strlen(clientIPAddress); i++)
				{ putc(clientIPAddress[i], tempfp); }
			
				putc(',', tempfp);         							// Add comma separation
			
				// Write client nickname to the new file
				for (size_t i = 0; i < strlen(clientNickname); i++)
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
	for (size_t i = 0; i < strlen(dateAndTime); i++)   // Write the date and time to the file
	{ putc(dateAndTime[i], tempfp); }
	
	putc(',', tempfp);									// Add comma separation
	
	for (size_t i = 0; i < strlen(clientIP); i++)      // Write the client IP to the file
	{ putc(clientIP[i], tempfp); }
	
	putc(',', tempfp);									// Add comma separation
	
	for (size_t i = 0; i < strlen(nickname); i++)		// Write the nickname to the file
	{ putc(nickname[i], tempfp); }
	
	putc('\n', tempfp);									// Add newLine - this will separate nickname entries.
	
	
	
	// Close both files
	fclose(fp);
	fclose(tempfp);
	
	
	// Now, replace the original file with the temporary file
	remove(filename);
	rename("temp.txt", filename);
}


// function to write: writeToLogFile
// Parameters: filename  (byte string) - the log file, ex: logfile.txt
//             timestamp (byte string)
//             nickname  (byte string)
//             msg       (byte string)
void writeToLogFile(char filename[], char timestamp[], char nick[], char msg[])
{
	// Open the current log file. We will be appending to this file to store chat logs.
	FILE* fp = fopen(filename, "a");                // Open the current log file for writing
	
	for (size_t i = 0; i < strlen(timestamp); i++)		// Write the timestamp to the log file
	{ putc(timestamp[i], fp); }
	
	putc(',', fp);									// Comma separation
	
	for (size_t i = 0; i < strlen(nick); i++)			// Write the nickname to the log file
	{ putc(nick[i], fp); }
	
	putc(',', fp);									// Comma separation
	
	for (size_t i = 0; i < strlen(msg); i++)			// Write the message to the log file
	{ putc(msg[i], fp); }
	
	putc('\n', fp);									// Add newLine - this will separate log file entrires
}



// function to write: outputLogFile


