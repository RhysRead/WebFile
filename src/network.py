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


def listen(storage_manager: object):
    # Create bound socket
    s = socket.socket()
    s.bind((HOST, LISTEN_PORT))
    s.listen(4)

    logging.info(f'Listening as {HOST}:{LISTEN_PORT}')

    while True:
        # Accept connections and receive filename and filesize
        client_socket, address = s.accept()
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize, md5 = received.split(SEPARATOR)

        # Minor formatting
        filename = str(filename)
        filesize = int(filesize)
        md5 = str(md5)

        # Receive file
        file = bytearray()
        for i in range(0, filesize//BUFFER_SIZE):
            bytes_read = client_socket.recv(BUFFER_SIZE)

            # If nothing is transmitted then file transfer is complete
            if not bytes_read:
                break

            file.extend(bytes_read)

        # ToDo: ensure this is all correct
        # ToDo: Add md5 to transfer
        storage_manager.update_change(file, filename, md5)


def send(address, filename, md5):
    s = socket.socket()

    logging.info(f'Connecting to {address}:{LISTEN_PORT}')

    s.connect((address, LISTEN_PORT))

    logging.info('Connected.')

    s.send(f"{filename}{SEPARATOR}{os.path.getsize(filename)}".encode())

    with open(filename, 'rb') as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            s.sendall(bytes_read)
        # close the socket
    s.close()


class NetworkManager(object):
    in_progress = False

    def __init__(self, storage_manager=object, permanent_connections=[]):
        self.__storage_manager = storage_manager
        self.__connections = []
        self.__connections.extend(permanent_connections)
        self.__threads = []

    def start_listening(self):
        worker = Thread(target=listen, args=(self.__storage_manager,))
        worker.daemon = True
        worker.start()

        self.__threads.append(worker)

    def get_connections(self):
        return self.__connections

    def transfer_file(self, filename, md5):
        for address in self.__connections:
            send(address, filename, md5)
