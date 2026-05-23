import json


def send_json(socket_object, data):
    """
    Convert dictionary to JSON and send it.
    """

    json_data = json.dumps(data)

    socket_object.send(json_data.encode())


def receive_json(socket_object):
    """
    Receive JSON data and convert it to dictionary.
    """

    json_data = socket_object.recv(1024).decode()

    return json.loads(json_data)