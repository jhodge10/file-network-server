import json


def send_json(socket_object, data):
    """
    Send dictionary as JSON.
    """

    json_data = json.dumps(data)

    socket_object.send(json_data.encode())


def receive_json(socket_object):
    """
    Receive JSON and convert to dictionary.
    """

    json_data = socket_object.recv(1024).decode()

    return json.loads(json_data)


def receive_file(socket_object, filename, filesize):
    """
    Receive file bytes and save file.
    """

    with open(filename, "wb") as file:

        bytes_received = 0

        while bytes_received < filesize:

            chunk = socket_object.recv(1024)

            if not chunk:
                break

            file.write(chunk)

            bytes_received += len(chunk)