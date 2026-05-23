import socket

from protocol import send_json, receive_json

HOST = "127.0.0.1"
PORT = 5000

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((HOST, PORT))

print("Connected to server.")

# Create LIST request
request = {
    "action": "LIST"
}

# Send request
send_json(client_socket, request)

print("Requested file list.")

# Receive server response
response = receive_json(client_socket)

# Display files
if response["status"] == "OK":

    print("\nAvailable Files:")

    files = response["files"]

    if len(files) == 0:
        print("No files available.")

    else:
        for file_name in files:
            print(f"- {file_name}")

else:
    print("Error:", response["message"])

# Close connection
client_socket.close()

print("\nConnection closed.")