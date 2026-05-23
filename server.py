import socket
import os

from protocol import send_json, receive_json, receive_file

HOST = "127.0.0.1"
PORT = 5000

SHARED_FOLDER = "shared_files"

# Create shared folder if missing
os.makedirs(SHARED_FOLDER, exist_ok=True)

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket
server_socket.bind((HOST, PORT))

# Listen for clients
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:

    # Accept client
    client_socket, client_address = server_socket.accept()

    print(f"\nConnected to {client_address}")

    try:

        # Receive JSON request
        request = receive_json(client_socket)

        print(f"Request: {request}")

        action = request.get("action")

        # -----------------------------------
        # LIST COMMAND
        # -----------------------------------
        if action == "LIST":

            files = os.listdir(SHARED_FOLDER)

            response = {
                "status": "OK",
                "files": files
            }

            send_json(client_socket, response)

        # -----------------------------------
        # UPLOAD COMMAND
        # -----------------------------------
        elif action == "UPLOAD":

            filename = request.get("filename")
            filesize = request.get("filesize")

            filepath = os.path.join(SHARED_FOLDER, filename)

            print(f"Receiving file: {filename}")
            print(f"File size: {filesize} bytes")

            # Tell client server is ready
            ready_response = {
                "status": "READY"
            }

            send_json(client_socket, ready_response)

            # Receive file bytes
            receive_file(client_socket, filepath, filesize)

            print("Upload complete.")

            # Final success response
            success_response = {
                "status": "OK",
                "message": "File uploaded successfully."
            }

            send_json(client_socket, success_response)

        # -----------------------------------
        # UNKNOWN COMMAND
        # -----------------------------------
        else:

            response = {
                "status": "ERROR",
                "message": "Unknown command."
            }

            send_json(client_socket, response)

    except Exception as error:

        error_response = {
            "status": "ERROR",
            "message": str(error)
        }

        send_json(client_socket, error_response)

    # Close client
    client_socket.close()

    print("Client disconnected.")