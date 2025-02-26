import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)  # To indicate it's a REQuest socket (as opposed to a REPly socket)
socket.connect("tcp://localhost:5555")  # Connect to the server

# To send a maintenance log entry to the microservice:
def send():
    # REQUEST:
    message = {  # make sure all 4 keys are present
        "type": "write",   # type will always be 'write' or 'read'
        "date": "2025-02-24",
        "part": "Engine",
        "description": "Replaced spark plugs",
    }
    socket.send_json(message)     # Send the request
    # RECEIVE:
    reply = socket.recv_string()  # Receive the response (if successful, it will be 'Logged Successfully')
    print(reply)

# To read all maintenance log entries from the microservice:

def read():
    # REQUEST:
    message = {
        "type": "read",
    }
    socket.send_json(message)     # Send the request
    # RECEIVE:
    reply = socket.recv_json()    # Receive the response (if successful, it will be a list of dictionaries)
    print(reply)
