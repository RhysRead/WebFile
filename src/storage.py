#!/usr/bin/env python3

"""storage.py: The storage file for the WebFile project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2020, Rhys Read"

import os
import hashlib
import logging

CUR_PATH = os.path.abspath(os.getcwd())


class StorageManager(object):
    def __init__(self, folder_path: str):
        self.__folder_path = folder_path
        self.__known_files = {}

    def get_folder_path(self):
        return self.__folder_path

    def check_files_for_changes(self):
        logging.info(f'Checking files for changes in: {self.get_folder_path()}')

        # Create return variable for changed files
        changed_files = []  # [[filename, filestatus]] (filestatus: 0=created, 1=deleted, 2=updated)
        # Get list of file names in sync directory
        file_names = os.listdir(self.__folder_path)

        # Check for creation, deletion, or changes in files
        for file_name in file_names:

            file_md5 = get_md5_for_file(self.__folder_path + '\\' + file_name)

            # ToDo: Check if the follow if statement is most efficient?
            # Check if file is known
            if file_name in self.__known_files.keys():
                # If file is known, check if the md5 checksum has changed
                if file_md5 != self.__known_files[file_name]:
                    # If file md5 checksum has changed, log file name and set new checksum
                    # file: UPDATED
                    logging.info(f'File updated: {file_name}')
                    changed_files.append([file_name, 2, file_md5])
                    self.__known_files[file_name] = file_md5
            else:
                # file: CREATED
                logging.info(f'File created: {file_name}')
                changed_files.append([file_name, 0, file_md5])
                self.__known_files[file_name] = file_md5

        # Get removed file names
        removed_file_names = list(set(self.__known_files.keys()) - set(file_names))
        for file_name in removed_file_names:
            # file: DELETED
            logging.info(f'File deleted: {file_name}')
            changed_files.append([file_name, 1, file_md5])

        return changed_files

    def get_known_files(self):
        return self.__known_files

    def __create_file(self, file_bytes, filename):
        with open(self.__folder_path + '/' + filename, 'w') as file:
            file.write(file_bytes)

    def update_change(self, file_bytes, filename, md5):
        if filename not in self.__known_files.keys():
            self.__create_file(file_bytes, filename)

        got_md5 = get_md5_for_file(self.__folder_path + '/' + filename)

        # ToDo: Not sure if __create_file will work to just overwrite an existing file
        if got_md5 != md5:
            self.__create_file(file_bytes, filename)


def get_md5_for_file(file_path: str):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
