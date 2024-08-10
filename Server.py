import socket
import threading

HEADER = 64
FORMAT = 'utf-8'
#Setting the port, and getting my local IP adress using the SERVER = ... line <- ignore this
PORT = 5050
#ENTER THE HOSTER"S PUBLIC IP BELOW IN THE SERVER variable
SERVER = "58.65.198.124"

print(SERVER)
ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE = "Disconnect"

#creating a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        #msg is immediately sent for some reason, it is a blank string, so we use the if statement to only convert it to int if it exists
        msg_length = conn.recv(HEADER).decode(FORMAT).strip()
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT).strip()
            print(f"[{addr}], msg:{msg}")
        

        #implement disconnection requirement
        if msg == DISCONNECT_MESSAGE:
            connected = False


        #Test sending messages to the client
        conn.send("Message received butter boy".encode(FORMAT))



    #execute the disconnection
    print("Disconnected successfully")
    conn.close()


#allow server to listen to connections and pass those connections to handle_client()
def start():
    #listening to the server
    server.listen()
    print(f"[HOST SERVER] is running on : {SERVER}")
    while True:
        #conn is an object of type socket and address is the address on the other end of the socket
        conn, addr = server.accept()
        #Use threading to simultaneously (sort of) run another function at the same time

        #syntax is threading.Thread(target=function_name, argus = (arguments_to_function,...))
        thread = threading.Thread(target=handle_client, args= (conn,addr))
        #begin the thread
        thread.start()
        #Use this to view how many active connections there are, subtracting 1 because start thread is always running
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        

print("The server is initiating...")
start()

