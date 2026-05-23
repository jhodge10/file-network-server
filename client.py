import socket
import os

from protocol import (
    send_json,
    receive_json,
    receive_file
)

HOST = "127.0.0.1"
PORT = 5000

DOWNLOAD_FOLDER = "downloads"

# Create downloads folder if needed
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# -----------------------------------
# LIST FILES
# -----------------------------------
def list_files():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((HOST, PORT))

    request = {
        "action": "LIST"
    }

    send_json(client_socket, request)

    response = receive_json(client_socket)

    print("\n--- Available Files ---")

    if response["status"] == "OK":

        files = response["files"]

        if len(files) == 0:
            print("No files available.")

        else:
            for file_name in files:
                print(f"- {file_name}")

    else:
        print("Error:", response["message"])

    client_socket.close()


# -----------------------------------
# UPLOAD FILE
# -----------------------------------
def upload_file():

    filename = input("Enter file path to upload: ")

    # Check file exists
    if not os.path.exists(filename):

        print("File does not exist.")

        return

    filesize = os.path.getsize(filename)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((HOST, PORT))

    request = {
        "action": "UPLOAD",
        "filename": os.path.basename(filename),
        "filesize": filesize
    }

    send_json(client_socket, request)

    response = receive_json(client_socket)

    if response["status"] == "READY":

        print("Uploading file...")

        with open(filename, "rb") as file:

            while True:

                chunk = file.read(1024)

                if not chunk:
                    break

                client_socket.send(chunk)

        final_response = receive_json(client_socket)

        print(final_response["message"])

    else:

        print("Upload failed.")

    client_socket.close()


# -----------------------------------
# DOWNLOAD FILE
# -----------------------------------
def download_file():

    filename = input("Enter filename to download: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((HOST, PORT))

    request = {
        "action": "DOWNLOAD",
        "filename": filename
    }

    send_json(client_socket, request)

    response = receive_json(client_socket)

    if response["status"] == "OK":

        filename = response["filename"]
        filesize = response["filesize"]

        print(f"Downloading {filename}...")

        ready_message = {
            "status": "READY"
        }

        send_json(client_socket, ready_message)

        save_path = os.path.join(DOWNLOAD_FOLDER, filename)

        receive_file(client_socket, save_path, filesize)

        print("Download complete.")

    else:

        print("Error:", response["message"])

    client_socket.close()


# -----------------------------------
# MAIN MENU LOOP
# -----------------------------------
while True:

    print("\n========================")
    print(" File Sharing Client")
    print("========================")
    print("1. List files")
    print("2. Upload file")
    print("3. Download file")
    print("4. Quit")

    choice = input("Select an option: ")

    # LIST
    if choice == "1":
        list_files()

    # UPLOAD
    elif choice == "2":
        upload_file()

    # DOWNLOAD
    elif choice == "3":
        download_file()

    # QUIT
    elif choice == "4":

        print("Goodbye.")

        break

    # INVALID INPUT
    else:
        print("Invalid option.")