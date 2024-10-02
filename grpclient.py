import socket
import sys
import threading

def receive_messages(server):
    while True:
        try:
            message = server.recv(2048)#.decode('utf-8')
            if message:
                print(message)
            else:
                # Server closed connection
                print("Connection closed by the server.")
                server.close()
                break
        except:
            print("An error occurred while receiving message.")
            server.close()
            break

def send_messages(server):
    while True:
        message = sys.stdin.readline().strip()  # Take input from stdin (without using select)
        server.send(message.encode('utf-8'))
        sys.stdout.write("<You> " + message + "\n")
        sys.stdout.flush()

# Set up the client socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# Connect to the server
server.connect((IP_address, Port))

# Use separate threads for receiving and sending messages
receive_thread = threading.Thread(target=receive_messages, args=(server,))
receive_thread.start()

send_thread = threading.Thread(target=send_messages, args=(server,))
send_thread.start()