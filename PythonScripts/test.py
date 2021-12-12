import os
import sys
from os import listdir
from os.path import isfile, join
from colorama import init, Fore, Back, Style

import utils

init(autoreset=True)

COMMAND_NAME = ""


def print_files():
    mypath = os.getcwd()
    files = [f for f in listdir(mypath)]

    for file in files:
        if os.path.isdir(file):
            print(f"{Fore.YELLOW}{file}")
        else:
            print(f"{Fore.GREEN}{file}")

    print("\nTotal", len(files), "files and folders")


def main():
    COMMAND_NAME = sys.argv[1]

    for arg in sys.argv[2:]:
        if arg=="-d" or arg=="-D":
            utils.print_description(COMMAND_NAME)
            return
        else:
            utils.print_unknown_option(arg)
            return

    print_files()


if __name__=='__main__':
    main()
    exit()