import socket
import os
import threading

from protocol import (
    send_json,
    receive_json,
    receive_file,
    send_file
)

HOST = "0.0.0.0"
PORT = 5000

SHARED_FOLDER = "shared_files"

# Create shared folder if missing
os.makedirs(SHARED_FOLDER, exist_ok=True)

# -----------------------------------
# HANDLE CLIENT FUNCTION
# -----------------------------------
def handle_client(client_socket, client_address):

    print(f"\nConnected to {client_address}")

    try:

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

            ready_response = {
                "status": "READY"
            }

            send_json(client_socket, ready_response)

            receive_file(client_socket, filepath, filesize)

            print("Upload complete.")

            success_response = {
                "status": "OK",
                "message": "File uploaded successfully."
            }

            send_json(client_socket, success_response)

        # -----------------------------------
        # DOWNLOAD COMMAND
        # -----------------------------------
        elif action == "DOWNLOAD":

            filename = request.get("filename")

            filepath = os.path.join(SHARED_FOLDER, filename)

            if not os.path.exists(filepath):

                response = {
                    "status": "ERROR",
                    "message": "File does not exist."
                }

                send_json(client_socket, response)

            else:

                filesize = os.path.getsize(filepath)

                response = {
                    "status": "OK",
                    "filename": filename,
                    "filesize": filesize
                }

                send_json(client_socket, response)

                ready_message = receive_json(client_socket)

                if ready_message["status"] == "READY":

                    print(f"Sending file: {filename}")

                    send_file(client_socket, filepath)

                    print("Download complete.")

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

        print(f"Error: {error}")

        error_response = {
            "status": "ERROR",
            "message": str(error)
        }

        try:
            send_json(client_socket, error_response)
        except:
            pass

    finally:

        client_socket.close()

        print(f"Disconnected from {client_address}")


# -----------------------------------
# SERVER SETUP
# -----------------------------------

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reuse port immediately after restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket
server_socket.bind((HOST, PORT))

# Listen for connections
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# -----------------------------------
# MAIN SERVER LOOP
# -----------------------------------
while True:

    # Accept new client
    client_socket, client_address = server_socket.accept()

    # Create thread for client
    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    # Start thread
    client_thread.start()

    print(f"Active connections: {threading.active_count() - 1}")