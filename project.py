import socket
import threading
import sys
import re
import time
# Define the keywords that indicate the client should provide input
def main():
    role = input("Enter PC role as 'server' or 'client': ")
    if role == "client":
        CLIENT()
    elif role == "server":
        SERVER()
    else:
        sys.exit("Invalid role")


def CLIENT():
    keywords = ['input', 'again', 'move', 'format', 'continue']

    HEADER = 64
    PORT = 5050
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
        print(full_msg)
        print()

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



def SERVER():
    #CREATE A LIST OF THE CLIENTS
    global client_list, current_turn
    client_list = []
    current_turn = 1
    global MAX_CONNECTIONS, CURRENT_CONNECTIONS
    MAX_CONNECTIONS = 2
    CURRENT_CONNECTIONS = 0

    #Use 1 for player 1, 2 for player 2

    #TIC TAC TOE IMPLEMENTATION
    ######################################################################################################################

    ######################################################################################################################

    def announce(msg):
        global client_list
        if len(client_list) == 2:
            client_list[0].send(msg.encode(FORMAT))
            client_list[1].send(msg.encode(FORMAT))



    def prompter(prompt, mark): # return answer
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


    def show(msg, mark):
        if mark == "x":
            client_list[0].send(msg.encode(FORMAT))
        else:
            client_list[1].send(msg.encode(FORMAT))
        
        

    def ticMain():
        global score
        
        #saves scores, x o x o. Which mark won how many times
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
        time.sleep(3)
        sys.exit("games ended")

    def showBoard(mark):
        board_view = "\n".join([" ".join(row) for row in board])
        show(f"\n{board_view}\n\n", mark)


    def announceBoard():
        board_view = "\n".join([" ".join(row) for row in board])
        announce(f"\n{board_view}\n\n")

    #Checks if there is a win on the board, and returns the letter of who won, returns True if someone won
    def checkWin():
        global board
        for i in range(3):

            letter = board[i][0]
            if letter == "x" or letter ==  "o":
                if board[i][1] == letter and board[i][2] == letter:
                    announce(f"{letter} wins!\n")
                    return True
                
            letter = board[0][i]
            if letter == "x" or letter == "o":
                if board[1][i] == letter and board[2][i] == letter:
                    announce(f"{letter} wins!\n")
                    return True

        letter = board[1][1]
        if letter == "x" or letter == "o":
            if board[0][0] == letter and board[2][2] == letter:
                announce(f"{letter} wins!\n")
                return True

            if board[0][2] == letter and board[2][0] == letter:
                announce(f"{letter} wins!\n")
                return True

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

    #CAN RETURN X or O if forfeited, or TRUE
    def inputMove(mark):
        global board

        move = inputValidate(mark)
        if not move:
            show("\nposition invalid!\ntry again:\n", mark) # send to mark (para)

            showBoard(mark)

            return(inputMove(mark))
        elif move == "f":
            announce(f"\n{mark} forfeits")
            #Checking if x forfeited, meaning o wins
            if mark == "x":
                return "o"
            return "x"   
        else:
            
            col, row = move[0], move[1]
            if board[row][col] != "-":
                # if pos filled: retry
                show("\nposition filled!\ntry again:", mark) # send to mark (para)

                showBoard(mark)

                return(inputMove(mark))
            else:
                #ideal case: inputs player move to board
                board[row][col] = mark
                return True

    #returns winner's mark
    def game():
        global board
        board = [["-"] *3 for i in range(3)]
        announce("new game: \n")
        announceBoard()
        Xmoves = 0
        while True:

            if (move:=inputMove("x")) == True:
                pass
            else:
                announce("o wins by forfeit!\n")
                return move

            announceBoard()  
            if checkWin():
                return "x"
            
            Xmoves += 1
            if Xmoves == 5:
                announce("\ntie!\n")
                return
        
            if (move:=inputMove("o")) == True:
                pass
            else:
                announce("x wins by forfeit!\n")
                return move

            announceBoard()
            if checkWin():
                return "o"


    #SERVER IMPLEMENTATION
    ######################################################################################################################

    ######################################################################################################################

    def serverInit():
        global HEADER, FORMAT, SERVER, DISCONNECT_MESSAGE, server
        HEADER = 64
        FORMAT = 'utf-8'
        #Setting the port, and getting my local IP adress using the SERVER = ... line <- ignore this
        PORT = 5050
        #ENTER THE HOSTER"S PUBLIC IP BELOW IN THE SERVER variable
        SERVER = socket.gethostbyname(socket.gethostname())

        print(SERVER)
        ADDR = (SERVER,PORT)
        DISCONNECT_MESSAGE = "disconnect"

        #creating a socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(ADDR)
    serverInit()

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

    print("The server is initiating...")

    start()
    ticMain()

if __name__ == "__main__":
    main()