#ifndef stdcomm_h
#define stdcomm_h

// Function Prototypes
int add(int, int);
//void send_all(int, char[]);
void send_all(int, char[], char);
int hasNickname(char[], char[]);
int isNicknameUnique(char[], char[]);
void storeNickname(char[], char[], char[], char[]);
void createWordPacket(char[], char, char[]);
char* recv_word_packet(int);
char* extract_word_packet_message(char*);

#endif
