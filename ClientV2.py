import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
DISCONNECT_MESSAGE = "Disconnect"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send_message(msg):
    #print("SEND MESSAGE WORKS")
    message = msg.encode(FORMAT)
    msg_length = len(message)
    #ADD PADDING TO MAKE SURE IT MATCHES THE HEADER SIZE
    send_length = str(msg_length).ljust(HEADER)
    send_length = send_length.encode(FORMAT)
    client.send(send_length)
    client.send(message)
    #Check if you can receive messages from the server
    #Works properly, use this to send the updated tic tac toe board to the players
    receive_message()


def receive_message():
    #print("RECEIVE MESSAGE WORKS")
    full_msg = ''
    while True:
        msg = client.recv(HEADER).decode(FORMAT)
        full_msg += msg
        if len(msg) < HEADER:  #Break when message is fully received on client's end
            break
    full_msg = full_msg.strip()
    print(full_msg)

    # Check if the message is prompting for input
    # == wasnt working for some reason
    if "Your turn to make a move Player" in full_msg:
        move = input("Enter your move (col row): ")
        send_message(move)
    elif DISCONNECT_MESSAGE in full_msg:
        print("Disconnected by server.")
        client.close()


# Initiate connection to the server
send_message("REQUEST TO CONNECT")

# Start listening for incoming messages
while True:
    receive_message()
