# Namra Chaklashiya
# 030698185
# CECS 327 - Assignment 8

import socket

def start_client():
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port number: "))

    valid_queries = [
        "What is the average moisture inside my fridge in the past three hours?",
        "What is the average water consumption per cycle in my smart dishwasher?",
        "Which device consumed more electricity among my three IoT devices?"
    ]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((server_ip, server_port))
        except Exception as e:
            print("Error connecting to server:", e)
            return

        while True:
            print("\nAvailable Queries:")
            for i, q in enumerate(valid_queries, 1):
                print(f"{i}. {q}")
            print("Type 'exit' to quit.")

            message = input("\nEnter your query exactly as listed above: ")
            if message.lower() == "exit":
                break
            if message not in valid_queries:
                print("Sorry, this particular query cannot be processed.")
                print("Please try one of the listed queries.")
                continue

            client_socket.sendall(message.encode())
            response = client_socket.recv(4096)
            print("Server Response:", response.decode())

if __name__ == "__main__":
    start_client()
