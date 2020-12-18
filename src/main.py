#!/usr/bin/env python3

"""main.py: The main file for the WebFile project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2020, Rhys Read"

import configparser
import time
import logging

from storage import StorageManager
from network import NetworkManager

logging.basicConfig(level=logging.DEBUG)

CONFIG_PATH = "../data/config.ini"
CUSTOM_SYNC_PATH = False


class Main(object):
    def __init__(self):
        self.__active = True

        self.__config = get_config()

        self.__unhandled_files = []

        self.__sleep_time = int(self.__config.get('Settings', 'frequency'))

        if not CUSTOM_SYNC_PATH:
            self.__sync_directory_path = self.__config.get('Settings', 'path')
        else:
            self.__sync_directory_path = input('Please enter custom sync path: ')

        self.__storage_manager = StorageManager(self.__sync_directory_path)
        self.__network_manager = NetworkManager(self.__storage_manager, permanent_connections=['127.0.0.1'])

    def start(self):
        self.__network_manager.start_listening()

        # Main Loop
        while self.__active:
            # Check files for changes
            changed_files = self.__storage_manager.check_files_for_changes()

            # Ensure network functionality is not already in use
            if self.__network_manager.in_progress:
                self.__unhandled_files.extend(changed_files)
                continue

            # Add unhandled changes to changed files
            changed_files.extend(self.__unhandled_files)

            # If any files have changed and there are active connections
            if changed_files != [] and self.__network_manager.get_connections() != []:
                # Iterate through changes and attempt to transmit to active connections
                # code: O
                for filename_code_md5 in changed_files:

                    if filename_code_md5[1] == 0 or filename_code_md5[1] == 2:
                        # try:
                        # Send file
                        logging.info('Sending file changes for file name: ' + filename_code_md5[0])
                        self.__network_manager.transfer_file(filename_code_md5[0], filename_code_md5[2])
                        changed_files.remove(filename_code_md5)
                        # except Exception as E:
                        # logging.info('Exception:\n' + str(E))

                self.__unhandled_files.extend(changed_files)

            time.sleep(self.__sleep_time)


def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config


if __name__ == "__main__":
    main = Main()
    main.start()
