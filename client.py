# Namra Chaklashiya
# 030698185
# CECS 327 - Introduction to Networks and Distributed Computing
# Assignment 8

import socket      

def start_client():
    # Prompt user for server IP and port
    server_ip = input("Enter server IP address: ")
    server_port = int(input("Enter server port number: "))

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Connected to {server_ip} on port {server_port}")

        while True:
            # Get user input
            message = input("Enter message to send (type 'exit' to quit): ")
            
            if message.lower() == 'exit':
                break  # Exit loop

            # Send message to the server
            client_socket.send(message.encode('utf-8'))

            # Receive response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally: 
        client_socket.close()
        print("Connection closed.")

# Run the client
if __name__ == "__main__":
    start_client()
