import os
import sys


def add_path_init():
    print("Add src to path.")
    current_directory = os.getcwd()
    directories = ["dataset", "config", "tools", "src"]
    for directory in directories:
        sys.path.insert(0, os.path.join(current_directory, directory))