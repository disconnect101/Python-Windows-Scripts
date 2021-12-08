import os
import sys
from os import listdir
from os.path import isfile, join

import config as conf
import utils


COMMAND_NAME = ""


def print_description(command_name):
    description = conf.CMD_MAP[command_name]['description']
    print(description)


def print_files():
    mypath = os.getcwd()
    files = [f for f in listdir(mypath)]

    for file in files:
        print(file)

    print("\nTotal", len(files), "files and folders")


def main():
    COMMAND_NAME = sys.argv[1]

    for arg in sys.argv[2:]:
        if arg=="-d" or arg=="-D":
            print_description(COMMAND_NAME)
            return
        else:
            utils.unknown_option(arg)
            return

    print_files()


if __name__=='__main__':
    main()
    exit()