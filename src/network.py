#!/usr/bin/env python3

"""network.py: The network file for the WebFile project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2020, Rhys Read"

import socket
import os
import logging

from threading import Thread

HOST = '0.0.0.0'
SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 4096  # (bytes)

LISTEN_PORT = 5001
SEND_PORT = 5002


class TransferTemplate(object):
    def __init__(self, file: str, filename: str, md5: str):
        self.__file = file
        self.__filename = filename
        self.__md5 = md5

    def get_file_bytes(self):
        return bytearray(self.__file)


def listen(storage_manager: object):
    while True:
        # Create bound socket
        s = socket.socket()
        s.bind((HOST, LISTEN_PORT))
        s.listen(4)

        logging.info(f'Listening as {HOST}:{LISTEN_PORT}')

        # Accept connections and receive filename and filesize
        client_socket, address = s.accept()
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)

        # Minor formatting
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # Receive file
        file = bytearray()
        for i in range(0, filesize//BUFFER_SIZE):
            bytes_read = client_socket.recv(BUFFER_SIZE)

            # If nothing is transmitted then file transfer is complete
            if not bytes_read:
                break

            file.extend(bytes_read)

        # ToDo: ensure this is all correct
        storage_manager.update_change()

# ToDo: Create send method


class NetworkManager(object):
    in_progress = False

    def __init__(self, storage_manager=object, permanent_connections=[]):
        self.__storage_manager = storage_manager
        self.__connections = []
        self.__connections.extend(permanent_connections)

    def start_listening(self):
        worker = Thread(target=listen, args=(self.__storage_manager,))

    def get_connections(self):
        return self.__connections

    def transfer_files(self):
        # ToDo
        pass
