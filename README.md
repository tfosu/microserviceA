# Microservice A

### Communication contract:

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
```

To read all maintenance log entries from the microservice:

```Python
# REQUEST:
message = {
    "type": "read",
}
socket.send_json(message)     # Send the request

# RECEIVE:
reply = socket.recv_json()    # Receive the response (if successful, it will be a list of dictionaries)
```
Note that the socket method used to get the reply is different for the two operations, as one returns a string and the other a list of dicts.

### How to Request and Receive Data from Microservice A

This section explains how to interact with Microservice A to send and receive maintenance log entries. The microservice uses ZeroMQ (zmq) for communication, and the main program must follow the steps below to request and receive data.

---

#### 1. **Setting Up the Connection**
Before sending or receiving data, the main program must establish a connection to the microservice. Use the following code to set up the connection:

```python
import zmq

# Create a ZeroMQ context and a REQ (request) socket
context = zmq.Context()
socket = context.socket(zmq.REQ)  # REQ socket is used to send requests
socket.connect("tcp://localhost:5555")  # Connect to the microservice running on localhost port 5555

#### 2. **Sending a Maintenance Log Entry (Write Operation)**
To send a maintenance log entry to the microservice, follow these steps:

1. Create a dictionary with the required keys: `type`, `date`, `part`, and `description`.
2. Send the dictionary as a JSON object using `socket.send_json()`.
3. Receive the response from the microservice using `socket.recv_string()`.

**Example Code:**
```python
# REQUEST:
message = {
    "type": "write",   # Type of operation (always 'write' for logging data)
    "date": "2025-02-24",  # Date of the maintenance log entry
    "part": "Engine",  # Part of the vehicle being maintained
    "description": "Replaced spark plugs",  # Description of the maintenance performed
}
socket.send_json(message)  # Send the request to the microservice

# RECEIVE:
reply = socket.recv_string()  # Receive the response (e.g., 'Logged Successfully')
print(reply)  # Output: 'Logged Successfully'

#### 3. **Reading All Maintenance Log Entries (Read Operation)**
To retrieve all maintenance log entries from the microservice, follow these steps:

1. Create a dictionary with the key `type` set to `"read"`.
2. Send the dictionary as a JSON object using `socket.send_json()`.
3. Receive the response from the microservice using `socket.recv_json()`. The response will be a list of dictionaries, where each dictionary represents a maintenance log entry.

**Example Code:**
```python
# REQUEST:
message = {
    "type": "read",  # Type of operation (always 'read' for retrieving data)
}
socket.send_json(message)  # Send the request to the microservice

# RECEIVE:
reply = socket.recv_json()  # Receive the response (a list of maintenance log entries)
print(reply)  # Output: [{"date": "2025-02-24", "part": "Engine", "description": "Replaced spark plugs"}, ...]
