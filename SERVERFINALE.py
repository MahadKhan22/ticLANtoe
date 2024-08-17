import socket
import threading

HEADER = 64
FORMAT = 'utf-8'
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "disconnect"

MAX_CONNECTIONS = 2
clients = []
lock = threading.Lock()
current_turn = 0  # 0 for player using X, 1 for player using O
scores = [0,0] #USE FIRST INDEX FOR PLAYER 1 WINS AND 2nd INDEX FOR PLAYER @ WINS!
#create the emtpy board
board = [["-" for _ in range(3)] for _ in range(3)]

def announce(message):
    for client in clients:
        client.send(message.encode(FORMAT))

def prompter(client, message):
    client.send(message.encode(FORMAT))

def handle_client(client, player_id):
    global current_turn
    global scores
    mark = "x" if player_id == 0 else "o"
    last_notified_turn = -1 
    
    try:
        while True:
            if current_turn == player_id:
                prompter(client, f"Your move (format: col row) as {mark}: ")
                
                msg_length = int(client.recv(HEADER).decode(FORMAT).strip())
                move = client.recv(msg_length).decode(FORMAT).strip()
                
                if move == DISCONNECT_MESSAGE:
                    break
                
                #IMPLEMENTING OF FORFEITS using "f f"
                if move == "f f":
                    announce(f"\n{mark.upper()} forfeits the match! The other player wins!\n")
                    reset_game()
                    continue


                # Validate and make the move, else the func wremports
                if validate_move(move, mark):
                    current_turn = (current_turn + 1) % 2  # Switch turns of p1 and p2
                    last_notified_turn = -1 
                    broadcast_board()
                    
                    if check_win(mark):
                        announce(f"{mark.upper()} wins!\n The current score is f{scores[0]} for player 1 and f{scores[1]} for player 2\n")
                        reset_game()
                else:
                    prompter(client, "Invalid move. Try again.")
            else:
                if last_notified_turn != current_turn:  # Notify only once when the turn changes, do not flood other terminals
                    prompter(client, "Waiting for the other player...")
                    last_notified_turn = current_turn
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        with lock:
            clients.remove(client)
        client.close()
        if len(clients) < 2:
            announce("The other player has disconnected. Ending game.")
            reset_game()

# Validates the move input and checks if it's a valid board position
def validate_move(move, mark):
    global board
    try:
        col, row = map(int, move.split())
        col -= 1
        row -= 1
        if board[row][col] == "-":
            board[row][col] = mark
            return True
    except (ValueError, IndexError):
        return False
    return False

def broadcast_board():
    board_view = "\n".join([" ".join(row) for row in board])
    announce(f"\n{board_view}\n")

# Checks if there is a win condition on the board
def check_win(mark):
    global board
    global scores #i dont remmeber if i needed to globalize these
    # Check stragihts in rows and columns
    for i in range(3):
        if all([board[i][j] == mark for j in range(3)]) or all([board[j][i] == mark for j in range(3)]):
            scores[current_turn] += 1
            return True

    # Check diagonals for Xs or Os
    if board[0][0] == board[1][1] == board[2][2] == mark or board[0][2] == board[1][1] == board[2][0] == mark:
        scores[current_turn] += 1
        return True

    return False

def reset_game():
    global board, current_turn
    board = [["-" for _ in range(3)] for _ in range(3)]
    current_turn = 0
    announce("New game starting...")

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server started on {SERVER}")

    while True:
        if len(clients) < MAX_CONNECTIONS:
            client, addr = server.accept()
            with lock:
                clients.append(client)
            player_id = len(clients) - 1
            threading.Thread(target=handle_client, args=(client, player_id)).start()
            print(f"Player {player_id + 1} connected from {addr}")

        #dislpay credits and how to forfeit once both the players are connected to servertictactoe
        #THIS IS BREAKING IT FOR SOME REASON??!??!?!?!?!?!?
        """
        if len(clients) == 2:
            announce("\nGame created by MahadKhan22 and BaihusReal")
            announce("- Inputs: <column> SPACE <row>, e.g., '2 3'")
            announce("- Input 'f f' to forfeit a match.")
            announce("Have fun! :D\n")
            #I didnt break this so it kept prompting these messages, woops
            break
        """


if __name__ == "__main__":
    start()
