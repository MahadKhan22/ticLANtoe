import socket
import threading
import sys
import re

#CREATE A LIST OF THE CLIENTS
client_list = []
current_turn = 1

MAX_CONNECTIONS = 2
CURRENT_CONNECTIONS = 0
#Use 1 for player 1, 2 for player 2
#TIC TAC TOE IMPLEMENTATION
######################################################################################################################


#SERVER IMPLEMENTATION
######################################################################################################################

HEADER = 64
FORMAT = 'utf-8'
#Setting the port, and getting my local IP adress using the SERVER = ... line <- ignore this
PORT = 5050
#ENTER THE HOSTER"S PUBLIC IP BELOW IN THE SERVER variable
SERVER = socket.gethostbyname(socket.gethostname())

print(SERVER)
ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE = "Disconnect"

#creating a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr, playerID):
    global client_list
    global current_turn
    print(f"[NEW CONNECTION] {addr} connected and is player {playerID}.")
    client_list.append(conn)

    connected = True
    while connected:
        #msg is immediately sent for some reason, it is a blank string, so we use the if statement to only convert it to int if it exists
        #Test sending messages to the client
        for item in client_list:
            #interesting manuever you've made here
            if item != conn:
                item.send(f"Your turn to make a move Player {playerID}".encode(FORMAT))
                print(f"sent to {playerID}")

        #Prevent any of the players from spamming moves while it's the other player's turn
        while current_turn != playerID:
            continue


        msg_length = conn.recv(HEADER).decode(FORMAT).strip()
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT).strip()
            print(f"[Player {playerID}] : {msg}")

            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                # Use the player's input to place his X or O on the board
                    #insert relavent function for the game
                # Switch turns if a player makes a valid move
                current_turn = (current_turn + 1) % 3
                if current_turn == 0:
                    current_turn = 1
                conn.send("Your mark has been placed\n".encode(FORMAT))


    #execute the disconnection
    print("Disconnected successfully")
    conn.close()


#allow server to listen to connections and pass those connections to handle_client()
def start():
    #listening to the server
    server.listen()
    print(f"[HOST SERVER] is running on : {SERVER}")
    playerID = 1
    while True:
        global CURRENT_CONNECTIONS, MAX_CONNECTIONS
        #conn is an object of type socket and address is the address on the other end of the socket
        if CURRENT_CONNECTIONS < MAX_CONNECTIONS:
            conn, addr = server.accept()
            CURRENT_CONNECTIONS += 1
            #Use threading to simultaneously (sort of) run another function at the same time

            #syntax is threading.Thread(target=function_name, args = (arguments_to_function,...))
            thread = threading.Thread(target=handle_client, args= (conn,addr,playerID))
            playerID += 1
            #begin the thread
            thread.start()
            #Use this to view how many active connections there are, subtracting 1 because start function's thread is always running
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def game_announcements(msg):
    for client in client_list:
        client.send(msg.encode(FORMAT))

print("The server is initiating...")

start()

######################################################################################################################



#Okay what do i need to do
#REPLACE any mentions of print with conn.send, use a function for this, display game
#I need to send the output of the tic tac toe game to both clients
#First one to connect gets to choose username and whether they want to be X or O
#X goes first for some reason
#Take alternative inputs, first with X, then O. Use a dictionary to print Player Names along with scores
#Replace end = ' ' in any of the game_announcements() thingy