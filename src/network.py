#!/usr/bin/env python3

"""network.py: The network file for the WebFile project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2020, Rhys Read"

import socket
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # (bytes)

PORT = 5001


class TransferTemplate(object):
    def __init__(self, file: str, filename: str, md5: str):
        self.__file = file
        self.__filename = filename
        self.__md5 = md5

    def get_file_bytes(self):
        return bytearray(self.__file)


class NetworkManager(object):
    def __init__(self, permanent_connections=[]):
        self.__connections = []
        self.__connections.extend(permanent_connections)

        self.__currently_receiving = False

    def get_connections(self):
        return self.__connections

    def transfer_files(self):
        # ToDo
        pass
