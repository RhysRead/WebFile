#!/usr/bin/env python3

"""storage.py: The storage file for the WebFile project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2020, Rhys Read"

import os
import hashlib

CUR_PATH = os.path.abspath(os.getcwd())


class StorageManager(object):
    def __init__(self, folder_path: str):
        self.__folder_path = folder_path
        self.__known_files = {}

    def check_files_for_changes(self):
        # Create return variable for changed files
        changed_files = []  # [[filename, filestatus]] (filestatus: 0=created, 1=deleted, 2=updated)
        # Get list of file names in sync directory
        file_names = os.listdir(self.__folder_path)

        # Check for creation, deletion, or changes in files
        for file_name in file_names:

            file_md5 = get_md5_for_file(CUR_PATH + file_name)

            # ToDo: Check if the follow if statement is most efficient?
            # Check if file is known
            if file_name in self.__known_files.keys():
                # If file is known, check if the md5 checksum has changed
                if file_md5 != self.__known_files[file_name]:
                    # If file md5 checksum has changed, log file name and set new checksum
                    # UPDATED
                    changed_files.append([file_name, 2])
                    self.__known_files[file_name] = changed_files
            else:
                # CREATED
                changed_files.append([file_name, 0])
                self.__known_files[file_name] = changed_files

        # Get removed file names
        removed_file_names = list(set(self.__known_files.keys()) - set(file_names))
        for file_name in removed_file_names:
            # DELETED
            changed_files.append([file_name, 1])

        return changed_files

    def get_known_files(self):
        return self.__known_files


def get_md5_for_file(file_path: str):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()