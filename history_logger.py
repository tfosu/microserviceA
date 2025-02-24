"""
Microservice A - Maintenance History Logger
Author: Trevor Foote
For Tyler Knudson-Forrest's Program

This microservice is responsible for logging the car's maintenance history. It will receive messages (written to a file)
from the main program and log the maintenance history. It will also be able to receive requests for the
maintenance history and send it back to the main program.

NOTE:
- Run this microservice first before running the main program.
- Main program should have
"""

import zmq


class MaintenanceEntry:

    def __init__(self, date: str, part: str, description: str):
        self.date = date
        self.description = description
        self.part = part

    def get_dict(self) -> dict[str, str]:
        return {
            "date": self.date,
            "part": self.part,
            "description": self.description
        }


def receive_message(socket: zmq.Socket, history: list[MaintenanceEntry]):
    """
    Receive a message from the main program
    """
    message = socket.recv_json()
    print(f"Received message: {message}")

    if message["type"] == "write":
        history.append(MaintenanceEntry(
            message["date"],
            message["part"],
            message["description"]
        ))
        print(f"Logged maintenance history: {message}")
        socket.send_string("Logged Successfully")
        return

    if message["type"] == "read":
        socket.send_json([entry.get_dict() for entry in history])
        return

    socket.send_string("Error: Invalid message type")


def main():
    context = zmq.Context()

    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    # Create the maintenance history
    history: list[MaintenanceEntry] = []

    while True:
        receive_message(socket, history)


if __name__ == "__main__":
    main()
