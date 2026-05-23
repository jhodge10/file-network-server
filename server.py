import socket
import os

from protocol import send_json, receive_json

HOST = "127.0.0.1"
PORT = 5000

SHARED_FOLDER = "shared_files"

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket
server_socket.bind((HOST, PORT))

# Listen for clients
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:

    # Accept client connection
    client_socket, client_address = server_socket.accept()

    print(f"\nConnected to {client_address}")

    # Receive JSON request
    request = receive_json(client_socket)

    print(f"Request: {request}")

    action = request.get("action")

    # -----------------------------------
    # LIST COMMAND
    # -----------------------------------
    if action == "LIST":

        try:
            files = os.listdir(SHARED_FOLDER)

            response = {
                "status": "OK",
                "files": files
            }

        except Exception as error:

            response = {
                "status": "ERROR",
                "message": str(error)
            }

    # -----------------------------------
    # UNKNOWN COMMAND
    # -----------------------------------
    else:

        response = {
            "status": "ERROR",
            "message": "Unknown command."
        }

    # Send response
    send_json(client_socket, response)

    # Close client connection
    client_socket.close()

    print("Client disconnected.")