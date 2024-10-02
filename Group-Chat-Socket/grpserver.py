import socket
import sys
from _thread import *

# Set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Check for correct number of command-line arguments
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# Bind and listen
server.bind((IP_address, Port))
server.listen(100)
print("Listening...")

list_of_clients = []

def clientthread(conn, addr):
    global list_of_clients  # Declare global
    conn.send("Welcome to this chatroom!".encode('utf-8'))

    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print(f"<{addr[0]}> {message}")
                message_to_send = f"<{addr[0]}> {message}"
                broadcast(message_to_send, conn)
            else:
                print(f"Disconnected: {addr[0]}")
                remove(conn)
                break
        except Exception as e:
            print(f"Error: {e}")
            remove(conn)
            break

def broadcast(message, connection):
    global list_of_clients  # Declare global
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")
                client.close()
                remove(client)

def remove(connection):
    global list_of_clients  # Declare global
    if connection in list_of_clients:
        list_of_clients.remove(connection)
        print(f"Client removed: {connection}")

while True:
    try:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print(f"{addr[0]} connected")
        start_new_thread(clientthread, (conn, addr))
    except KeyboardInterrupt:
        print("Server is shutting down.")
        break
    except Exception as e:
        print(f"Error: {e}")

# Close all connections
for client in list_of_clients:
    client.close()
server.close()
