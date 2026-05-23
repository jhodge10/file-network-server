import socket
import os

from protocol import send_json, receive_json

HOST = "127.0.0.1"
PORT = 5000

FILE_TO_UPLOAD = "test_upload.txt"

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((HOST, PORT))

print("Connected to server.")

# Get file size
filesize = os.path.getsize(FILE_TO_UPLOAD)

# Create upload request
request = {
    "action": "UPLOAD",
    "filename": FILE_TO_UPLOAD,
    "filesize": filesize
}

# Send upload metadata
send_json(client_socket, request)

print("Upload request sent.")

# Wait for READY response
response = receive_json(client_socket)

if response["status"] == "READY":

    print("Server ready. Uploading file...")

    # Send file bytes
    with open(FILE_TO_UPLOAD, "rb") as file:

        while True:

            chunk = file.read(1024)

            if not chunk:
                break

            client_socket.send(chunk)

    print("File upload complete.")

    # Receive final response
    final_response = receive_json(client_socket)

    print(final_response["message"])

else:

    print("Upload failed.")

# Close connection
client_socket.close()

print("Connection closed.")