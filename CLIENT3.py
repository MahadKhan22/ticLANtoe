import socket

# Define the keywords that indicate the client should provide input
keywords = ['input', 'again', 'move', 'format']

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
DISCONNECT_MESSAGE = "Disconnect"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

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
        if len(msg) < HEADER:  # Break when the complete message has beene received
            break
    full_msg = full_msg.strip()
    print(full_msg)

    # Check if any of the keywords appear in the message sent by the server
    if any(keyword in full_msg.lower() for keyword in keywords):
        move = input()
        send_message(move)
    elif DISCONNECT_MESSAGE in full_msg:
        print("Disconnected by server.")
        client.close()

# Start listening for incoming messages
while True:
    receive_message()
