// Author: Zaynin Henthorn
// Major: Computer Science
// Course: CSC 328 Fall 2023
// Assignment: Final Group Project - Chat Server
// Purpose: The c file containing function definitions for the stdchatf library.

// Library C to Python

#include "stdchatf.h"
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>		// for htons()
#include <stdlib.h>

// CITATIONS:
// 1. https://support.sas.com/documentation/onlinedoc/ccompiler/doc700/html/lr1/z2055292.htm#:~:text=getc%20returns%20the%20next%20input,called%20to%20distinguish%20these%20cases.
//    Determines the difference between getc() returning EOF due to reaching the end of file versus being unsuccessful. ferror().



// Function Name: hasNickname()
// Description:  Takes a file (nicknames storage file) and an IP and determines if that
//               client's IP exists in the nicknames file and has a nickname associated with it.
// Parameters:   char filename[] : a char array (byte string) of the name of the file, example: "nicknames.txt" - input
//               char clientIP[] : a char array (byte string) of the client's IP you wish to determine if has a nickname or not - input
// Return Value: integer, 0 if false (the IP does not have a nickname)
//                        1 if true (the IP does have a nickname)
//                       -1 if error
int hasNickname(char filename[], char clientIP[])
{
	FILE* fp = fopen(filename, "r");													// Opens the nickname storage file
	if (fp == NULL)
	{
		perror("Error opening file in stdchatf.hasNickname().\n");
		return -1;
	}
	
	char charFromFile;																	// Will store each read-in char from file
	
	char ipFromFile[20];																// Where we will store each IP we read from the file
	int ipIndex = 0;
	
	// Read through the nicknames storage file. If an IP is found that matches the IP passed into this function, then the client already has a nickname. Return true (1)
	// Otherwise, if the passed-in IP is not found in the file, then that client does not yet have a nickname. Return false (0).
	while ((charFromFile = getc(fp)) != EOF)
	{
		while ((charFromFile = getc(fp)) != ',')										// Read in date and time
		{
			if (ferror(fp))
			{ 	perror("Error reading from file in stdchatf.storeNickname().\n");
				return -1; 
			}
		}

		while ((charFromFile = getc(fp)) != ',')										// Read in IP
		{
			if (ferror(fp))
			{ 	perror("Error reading from file in stdchatf.storeNickname().\n");
				return -1; 
			}
			ipFromFile[ipIndex] = charFromFile;
			ipIndex++;
		}

		while ((charFromFile = getc(fp)) != '\n')										// Read in nickname
		{
			if (ferror(fp))
			{ 	perror("Error reading from file in stdchatf.storeNickname().\n");
				return -1; 
			}
		}
		
		if (strcmp(ipFromFile, clientIP) == 0)											// If this specific IP is equal to the passed-in IP,
		{ return 1; }																	// then the client already has a nickname. Return true (1).
		
		ipIndex = 0;
		memset(ipFromFile, 0, sizeof(ipFromFile));										// Reset ipFromFile
		
		// Repeat this process until you go through every IP address in the nicknames storage file.
	}
	
	fclose(fp);												// close nicknames file
	return 0;												// if you got here, then the passed-in client IP was not found in the nicknames storage file,
															// meaning that the client does not already have a nickname. Return false (0).
}





// Function name: isNicknameUnique
// Description:  Determines if a nickname is unique in a nicknames storage file.
// Parameters:   char filename[] : a char array (byte string) of the name of the file, example: "nicknames.txt" - input
//               char nickname[] : a char array (byte s tring) of the nickname you wish to determine if is unique in the nicknames storage file. - input
// Return value: integer, 0 if false (the nickname is not unique)
//                        1 if true (the nickname is unique)
//                       -1 if error
int isNicknameUnique(char filename[], char nickname[])
{
	FILE* fp = fopen(filename, "r");						// Opens the nicknames storage file and error check
	if (fp == NULL)
	{ 
		perror("Error opening file in stdchatf.isNicknameUnique().\n");
		return -1;
	}
	
	char charFromFile;										// Will store each read-in char from file
	
	char nickFromFile[100];									// Where we will store each nickname we read to compare if it is unique or not.
	int nicknameIndex = 0;
	
	// Read through the nicknames storage file. If a nickname is found that matches the nickname passed into this function, then return false.
	// Otherwise, if the nickname is not found, then it is unique and return true.
	while ((charFromFile = getc(fp)) != EOF)
	{
		while ((charFromFile = getc(fp)) != ',') 					// Read in date and time
		{
			if (ferror(fp))
			{ 	perror("Error reading from file in stdchatf.storeNickname().\n");
				return -1; 
			}
		}					

		while ((charFromFile = getc(fp)) != ',')					// Read in IP
		{
			if (ferror(fp))
			{ 	perror("Error reading from file in stdchatf.storeNickname().\n");
				return -1; 
			}
		}
		
		while ((charFromFile = getc(fp)) != '\n')					// Read in nickname
		{
			if (ferror(fp))
			{ 	perror("Error reading from file in stdchatf.storeNickname().\n");
				return -1; 
			}
			nickFromFile[nicknameIndex] = charFromFile;
			nicknameIndex++;
		}
																	
		if (strcmp(nickFromFile, nickname) == 0)					// If this specific nickname entry is equal to the passed-in nickname,
		{ return 0; } 												// then the passed-in nickname is NOT unique. Return false
		
		nicknameIndex = 0; 											
		memset(nickFromFile, 0, sizeof(nickFromFile));				// Reset nickFromFile
		
		// Repeat the process until you go through every nickname entry in the nicknames storage file.
	}
	
	fclose(fp); // close nicknames file
	return 1;	// if you get here, then the passed-in nickname was not found in the nicknames storage file, meaning that the nickname is unique.
	
}





// Function Name: storeNickname
// Description:  Will store an entry into a nicknames storage file. The nickname entry will be
//               formatted as follows: <date and time>,<client IP>,<nickname>
//               If a client IP already has a nickname stored in this nicknames storage file, then
//               their previous entry will be overwritten with the new time and nickname.
// Parameters:   char filename[]    : a char array (byte string) of the name of the file, example: "nicknames.txt" - input
//               char dateAndTime[] : a char array (byte string) of the date and time - input
//               char clientIP[]    : a char array (byte string) of the client's IP - input
//               char nickname[]    : a char array (byte string) of the nickname - input
// Return value: integer, 0 if storeNickname() executed successfully
//                       -1 if storeNickname() was unsuccessful (error).
int storeNickname(char filename[], char dateAndTime[], char clientIP[], char nickname[])
{
	// Open the current nicknames file. We will be reading from this file to determine if the clientIP already has a nickname.
	FILE* fp = fopen(filename, "r");                // Open the current nicknames file and error check.
	if (fp == NULL)									// a: appends to the file (instead of overwriting)
	{   
		perror("Nicknames file failed to open in stdchatf.storeNickname().\n");
		return -1; 
	}

	char charFromFile;
	char dateTime[100];
	char clientIPAddress[strlen(clientIP) + 1];
		 clientIPAddress[strlen(clientIP)] = '\0';
	char clientNickname[20];
	
	if (strlen(nickname) < 3 || strlen(nickname) > 16)						// Ensure arbitrary length of nickname.
	{   perror("Invalid nickname length (stdchatf.storeNickname())\n");
		return -1; 
	}

	// If a client already has a nickname entry, remove it.
		// Open a temporary file - this is where we will write the new file with the removed nickname entry.
		FILE* tempfp = fopen("temp.txt", "w");
		if (tempfp == NULL)
		{
			perror("Temporary nickname file failed to open in stdchatf.storeNickname().\n");
			return -1;
		}
		
		// Read through the nicknames file, and if there is an entry with the same clientIP, don't write it to the new temporary file.
		while ((charFromFile = getc(fp)) != EOF)
		{
			dateTime[0] = charFromFile;   // store the first char in the dateTime
			// Read up until the first ",". Now we are at the clientIP.
			int dateAndTimeIndex = 1;
			while ((charFromFile = getc(fp)) != ',')
			{
				if (ferror(fp))
				{ perror("Error reading from file in stdchatf.storeNickname().\n");
				  return -1; }
				dateTime[dateAndTimeIndex] = charFromFile;
				dateAndTimeIndex++;
			}
			
			// Now, read in the clientIP.
			int clientIPAddressIndex = 0;
			while ((charFromFile = getc(fp)) != ',')
			{
				if (ferror(fp))
				{ perror("Error reading from file in stdchatf.storeNickname().\n");
				  return -1; }
				clientIPAddress[clientIPAddressIndex] = charFromFile;
				clientIPAddressIndex++;
			}
			
			// Now, read in client nickname.
			int clientNicknameIndex = 0;
			while ((charFromFile = getc(fp)) != '\n')
			{
				if (ferror(fp))
				{ perror("Error reading from file in stdchatf.storeNickname().\n");
				  return -1; }
				clientNickname[clientNicknameIndex] = charFromFile;
				clientNicknameIndex++;
			}
			
			// Now that we have the client IP from the file, compare it to the client IP passed into this function. If they are the same, do not write to new file.
			// Otherwise, write this entire nickname entry to the new file.
			if (strcmp(clientIPAddress, clientIP) != 0)
			{
				// Write dateTime to the new file
				for (size_t i = 0; i < strlen(dateTime); i++)
				{ 
					if (putc(dateTime[i], tempfp) == EOF)
					{ 
						perror("Error using putc() in strchatf.storeNickname().\n");
						return -1;
					}
				}
			
				if (putc(',', tempfp) == EOF)											// Add comma separation
				{
					perror("Error using putc() in strchatf.storeNickname().\n");
					return -1;
				}
			
				// Write clientIP to the new file
				for (size_t i = 0; i < strlen(clientIPAddress); i++)
				{ 
					if (putc(clientIPAddress[i], tempfp) == EOF)
					{
						perror("Error using putc() in strchatf.storeNickname().\n");
						return -1;
					}
				}
			
				if (putc(',', tempfp) == EOF)											// Add comma separation
				{
					perror("Error using putc() in strchatf.storeNickname().\n"); 
					return -1;
				}
			
				// Write client nickname to the new file
				for (size_t i = 0; i < strlen(clientNickname); i++)
				{ 
					if (putc(clientNickname[i], tempfp) == EOF)
					{
						perror("Error using putc() in strchatf.storeNickname().\n"); 
						return -1;
					}
				}
			
				if (putc('\n', tempfp) == EOF)
				{
					perror("Error using putc() in strchatf.storeNickname().\n"); 
					return -1;
				}
			}
			
			
			// Reset dateTime and clientIPAddress and clientNickname
			memset(dateTime, 0, sizeof(dateTime));
			memset(clientIPAddress, 0, sizeof(clientIPAddress));
			memset(clientNickname, 0, sizeof(clientNickname));
		}
		// Now, we have an updated nicknames file with the current clientIP's nickname entry removed.
		
	// Write the client's new nickname entry to the file.
	for (size_t i = 0; i < strlen(dateAndTime); i++)   // Write the date and time to the file
	{ 
		if (putc(dateAndTime[i], tempfp) == EOF) 
		{
			perror("Error using putc() in strchatf.storeNickname().\n");
			return -1;
		}
	}
	
	if (putc(',', tempfp) == EOF)									// Add comma separation
	{
		perror("Error using putc() in strchatf.storeNickname().\n");
		return -1;
	}
	
	for (size_t i = 0; i < strlen(clientIP); i++)      				// Write the client IP to the file
	{ 
		if (putc(clientIP[i], tempfp) == EOF)
		{
			perror("Error using putc() in strchatf.storeNickname().\n");
			return -1;
		}
	}
	
	if (putc(',', tempfp) == EOF)									// Add comma separation
	{
		perror("Error using putc() in strchatf.storeNickname().\n");
		return -1;
	}
	
	for (size_t i = 0; i < strlen(nickname); i++)					// Write the nickname to the file
	{ 
		if (putc(nickname[i], tempfp) == EOF)
		{
			perror("Error using putc() in strchatf.storeNickname().\n");
			return -1;
		}
	}
	
	if (putc('\n', tempfp) == EOF)									// Add newLine - this will separate nickname entries.
	{ 
		perror("Error using putc() in strchatf.storeNickname().\n");
		return -1;
	}
	
	
	
	// Close both files
	fclose(fp);
	fclose(tempfp);
	
	// Now, replace the original file with the temporary file
	remove(filename);
	rename("temp.txt", filename);
	
	return 0; // storeNickname() successful
}





// Function Name: writeToLogFile
// Description:  Will write a chat message log entry into a passed-in log file.
//               Log message chat entries are formatted as follows: <timestamp>,<nickname>,<msg>
// Parameters:   char filename[]  : a char array (byte string) of the name of the file, example: "logfile.txt" - input
//               char timestamp[] : a char array (byte string) of the timestamp associated with chat message - input
//               char nick[]      : a char array (byte string) of the nickname associated with chat message - input
//               char msg[]       : a char array (byte string) of the message associated with the chat message - input
// Return Value: integer, 0 if successful
//                       -1 if unsuccessful (error)
int writeToLogFile(char filename[], char timestamp[], char nick[], char msg[])
{
	// Open the current log file. We will be appending to this file to store chat logs.
	FILE* fp = fopen(filename, "a");               	 	// Open the current log file for writing & error check fopen()
	if (fp == NULL)
	{ return -1; }
	
	for (size_t i = 0; i < strlen(timestamp); i++)		// Write the timestamp to the log file
	{ 
		if (putc(timestamp[i], fp) == EOF)
		{ return -1; }
	}
	
	if (putc(',', fp) == EOF)							// Comma separation
	{ return -1; }
	
	for (size_t i = 0; i < strlen(nick); i++)			// Write the nickname to the log file
	{ 
		if (putc(nick[i], fp) == EOF)
		{ return -1; }
	}
	
	if (putc(',', fp) == EOF)							// Comma separation
	{ return -1; }
	
	for (size_t i = 0; i < strlen(msg); i++)			// Write the message to the log file
	{ 
		if (putc(msg[i], fp) == EOF)
		{ return -1; }
	}
	
	if (putc('\n', fp) == EOF)							// Add newLine - this will separate log file entrires
	{ return -1; }
	
	fclose(fp);											// Close the log file.

	return 0;											// writeToLogFile() succeeded.
}
