#!/usr/bin/env python3

"""main.py: The main file for the WebFile project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2020, Rhys Read"

import configparser
import time

from storage import StorageManager

CONFIG_PATH = "../data/config.ini"


class Main(object):
    def __init__(self):
        self.__active = True

        self.__config = get_config()

        self.__sleep_time = int(self.__config.get('Settings', 'frequency'))
        self.__sync_directory_path = self.__config.get('Settings', 'path')

        self.__storage_manager = StorageManager(self.__sync_directory_path)

    def start(self):
        while self.__active:
            changed_files = self.__storage_manager.check_files_for_changes()

            if changed_files != []:



            time.sleep(self.__sleep_time)


def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config


if __name__ == "__main__":
    main = Main()
    main.start()
