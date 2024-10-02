import socket

def start_client():
    host = input("Enter server IP address: ")  # IP address of the server
    port = 12345                                 # Port to connect to

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))
        
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
