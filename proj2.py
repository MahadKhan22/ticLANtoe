import socket
import threading
import sys
import re


# choose server or player: begin relavent procedure. else recur
def main():
    role = input("Enter role: SERVER or PLAYER? (s/p): ").strip().lower()

    if role == "p":
        try: # if "target machine actively refused it", no server found, error
            CLIENT()
            return "client"
        except ConnectionRefusedError:
            print("\nNo server found\nEnsure a server is up before choosing player\n")
            main()

    elif role == "s":
        try: # if other server is up on this machine, error
            print("attempting server initiation...")
            serverInit()
            start()
            ticMain()
        except OSError:
            print("\nA server has already been initiated on this machine\nPlease choose player or exit program\n")
            main()

    else:
        print("\nInvalid role\nChoose (s/p)\n")
        main()

def CLIENT():
    keywords = ['input', 'again', 'move', 'format', 'continue']

    HEADER = 64
    PORT = 9150
    FORMAT = 'utf-8'
    SERVER = socket.gethostbyname(socket.gethostname())
    DISCONNECT_MESSAGE = "disconnect"
    ADDR = (SERVER, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("\nmade by MahadKhan22 and BaihusReal")
    print("- inputs: <column> SPACE <row>, eg: '2 3'")
    print("- input 'f f' to forfeit a match.")
    print("have fun! :D\n")



    def send_message(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).ljust(HEADER).encode(FORMAT)
        client.send(send_length)
        client.send(message)
        receive_message()  # Continue to receive messages after sending

    def receive_message():
        full_msg = ''
        while True:
            msg = client.recv(HEADER).decode(FORMAT)
            full_msg += msg
            if len(msg) < HEADER:  # Break when the complete message has been received
                break
        full_msg = full_msg.strip()
        print(f"{full_msg}\n")


        # Check if any of the keywords appear in the message sent by the server
        if any(keyword in full_msg.lower() for keyword in keywords):
            move = input()
            send_message(move)
        elif DISCONNECT_MESSAGE in full_msg:
            print("Disconnected by server.")
            client.close()
            sys.exit()
        elif "final" in full_msg:
            client.close()
            sys.exit()

    # Start listening for incoming messages
    while True:
        receive_message()






#Use 1 for player 1, 2 for player 2

#TIC TAC TOE IMPLEMENTATION
######################################################################################################################

######################################################################################################################

def announce(msg):
    global client_list
    if len(client_list) == 2:
        client_list[0].send(msg.encode(FORMAT))
        client_list[1].send(msg.encode(FORMAT))



def prompter(prompt, mark): # return answer, mark is who it prompts
    #Send the prompt to the mark received as parameter
    prompt = prompt.encode(FORMAT)
    if mark == "x":
        client_list[0].send(prompt)
        msg_length = int(client_list[0].recv(HEADER).decode(FORMAT).strip())
        return client_list[0].recv(msg_length).decode(FORMAT).strip()
    else:
        client_list[1].send(prompt)
        msg_length = int(client_list[1].recv(HEADER).decode(FORMAT).strip())
        return client_list[1].recv(msg_length).decode(FORMAT).strip()


def show(msg, mark): # mark is who it shows
    msg = msg.encode(FORMAT)
    if mark == "x":
        client_list[0].send(msg)
    else:
        client_list[1].send(msg)
    

def showBoard(mark):
    board_view = "\n".join([" ".join(row) for row in board])
    show(f"\n{board_view}\n\n", mark)


def announceBoard():
    board_view = "\n".join([" ".join(row) for row in board])
    announce(f"\n{board_view}\n\n")

def resetBoard():
    global board
    board = [["-"] *3 for i in range(3)]

def ticMain(): # iters games until players discontinue them. keeps score and calls dicontinue()
    global score
    
    # score[0] is for x, score[1] is for o
    score = [0,0]

    # keep running games (until cont comes back as false)
    while True:
        if (winner:=game()) == "x":
            score[0] += 1
        elif winner == "o":
            score[1] += 1
        #Asks user to end game or continue for another round
        if not cont():
            #end the game
            discontinue()


def cont():
    if (inpX:=prompter("continue? (y/n): ", "x").strip()) == "n"  or (inpO:=prompter("continue? (y/n): ", "o").strip()) == "n":
        return False
    elif inpX == "y" and inpO == "y":
        return True
    return cont()


def discontinue():
    xScore = score[0]
    oScore = score[1]
    announce(f"final score:\nx: {xScore}\no: {oScore}\n")
    sys.exit("games ended")


def checkWin(): #Checks if there is a win on the board, returns True if someone won, False if no one won

    global board
    for i in range(3):

        letter = board[i][0]
        if letter == "x" or letter ==  "o":
            if board[i][1] == letter and board[i][2] == letter:
                return True # win occured on horizontals
            
        letter = board[0][i]
        if letter == "x" or letter == "o":
            if board[1][i] == letter and board[2][i] == letter:
                return True # win occured on verticals

    letter = board[1][1]
    if letter == "x" or letter == "o":
        if board[0][0] == letter and board[2][2] == letter:
            return True # win occured on -ve diag

        if board[0][2] == letter and board[2][0] == letter:
            return True # win occured on +ve diag

    return False

#Cleanses user input to check for col, row or if they forfeit
def inputValidate(mark):
    inp = prompter("input move: ", mark)
    
    pattern = r"^(?P<column>[1-3]|f) (?P<row>[1-3]|f)$"
    if (matches:=re.search(pattern, inp)):
        col = matches.group("column")
        row = matches.group("row")
        try:
            col, row = int(col)-1, int(row)-1
            return [col, row]
        except:
            if col == "f" and row == "f":
                return "f"
        
    else:
        return False


def inputMove(mark): # returns True if move valid, False if forfeit. else recurs
    global board
    move = inputValidate(mark)

    if not move:
        show("\nposition invalid!\ntry again:\n", mark) 
        showBoard(mark)
        return(inputMove(mark))
    
    elif move == "f": # forfeit
        return False  
    
    else:
        col, row = move[0], move[1]
        if board[row][col] != "-": # if pos filled: retry
            show("position filled!\ntry again:\n", mark) 
            showBoard(mark)
            return(inputMove(mark))
        
        else:
            #ideal case: inputs player move to board
            board[row][col] = mark
            return True


board = [["-"] *3 for i in range(3)]

def game(): # runs 1 match, returns winner's mark, returns None if tie
    global board
    resetBoard()

    announce("new game: \n")
    announceBoard()
    Xmoves = 0
    while True:

        if (move:=inputMove("x")) == True: # x's move
            announceBoard()

            if checkWin():
                announce("x wins!")
                return "x"
        else:
            announce("o wins by forfeit!\n")
            return "o"
        
        Xmoves += 1
        if Xmoves == 5:
            announce("\ntie!\n")
            return
    
        if (move:=inputMove("o")) == True: # o's move
            announceBoard()

            if checkWin():
                announce("o wins!\n")
                return "o"
        else:
            announce("x wins by forfeit!\n")
            return "x"


#SERVER IMPLEMENTATION
######################################################################################################################

######################################################################################################################



def serverInit():

    #CREATE A LIST OF THE CLIENTS
    global client_list, current_turn
    client_list = []
    current_turn = 1
    global MAX_CONNECTIONS, CURRENT_CONNECTIONS
    MAX_CONNECTIONS = 2
    CURRENT_CONNECTIONS = 0

    global HEADER, FORMAT, SERVER, DISCONNECT_MESSAGE, server
    HEADER = 64
    FORMAT = 'utf-8'
    #Setting the port, and getting my local IP adress using the SERVER = ... line <- ignore this
    PORT = 9150
    #ENTER THE HOSTER"S PUBLIC IP BELOW IN THE SERVER variable
    SERVER = socket.gethostbyname(socket.gethostname())

    ADDR = (SERVER,PORT)
    DISCONNECT_MESSAGE = "disconnect"

    #creating a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)


def decode_message(msg_length, conn):
    msg_length = conn.recv(HEADER).decode(FORMAT).strip()
    
    #This if condition exists if a "Nonetype is send somehow", an empty string is NOT NONETYPE
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT).strip()
        return msg

def decodeMsg(conn):
    msg_len = conn.recv(HEADER).decode(FORMAT).strip()
    msg = conn.recv(int(msg_len)).decode(FORMAT).strip()
    return msg


def handle_client(conn, addr, playerID):
    global client_list
    global current_turn
    if playerID == 0:
        mark = "x"
    else:
        mark = "o"
    print(f"[NEW CONNECTION] {addr} connected using {mark}")
    client_list.append(conn)



#allow server to listen to connections and pass those connections to handle_client()
def start():
    global CURRENT_CONNECTIONS, MAX_CONNECTIONS
    #listening to the server
    server.listen()
    print(f"[HOST SERVER] is running on : {SERVER}")
    playerID = 0
    while playerID<2:
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

######################################################################################################################


if __name__ == "__main__":
    main()