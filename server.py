# Namra Chaklashiya
# 030698185
# CECS 327 - Introduction to Networks and Distributed Computing
# Assignment 8

import socket

def start_server():
    # Define server parameters
    host = input("Enter IP Address: ")
    port = int(input("Enter the port number: "))

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind the socket to the given IP and port
        server_socket.bind((host, port))
        server_socket.listen(5)  # Listen for incoming connections
        print(f"Server started on port {port}, waiting for connections...")

        while True:
            # Accept incoming client connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            while True:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                
                if not data:
                    break  # Client disconnected
                
                print(f"Received from client: {data}")

                # Convert to uppercase and send response
                response = data.upper()
                client_socket.send(response.encode('utf-8'))

            client_socket.close()  # Close client connection

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()

# Run the server
if __name__ == "__main__":
    start_server()
