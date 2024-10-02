import socket

def start_server():
    host = '0.0.0.0'  # Listen on all interfaces
    port = 12345       # Port to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    while True:
        message = conn.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"Client: {message}")
        
        response = input("You: ")
        conn.send(response.encode('utf-8'))

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
