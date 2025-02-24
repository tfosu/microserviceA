# Microservice A

The microservice Python file should be run first, then the main program (in order for the sockets to bind/connect in the right order).

Main program should have:

```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)  # To indicate it's a REQuest socket (as opposed to a REPly socket)
socket.connect("tcp://localhost:5555")  # Connect to the server
```

To send a maintenance log entry to the microservice:

```Python
message = {  # make sure all 4 keys are present
    "type": "write",   # type will always be 'write' or 'read'
    "date": "2025-02-24", 
    "part": "Engine",
    "description": "Replaced spark plugs",
}
socket.send_json(message)     # Send the request
reply = socket.recv_string()  # Receive the response (if successful, it will be 'Logged Successfully')
```

To read all maintenance log entries from the microservice:

```Python
message = {
    "type": "read",
}
socket.send_json(message)     # Send the request
reply = socket.recv_json()    # Receive the response (if successful, it will be a list of dictionaries)
```
Note that the socket method used to get the reply is different for the two operations, as one returns a string and the other a list of dicts.

