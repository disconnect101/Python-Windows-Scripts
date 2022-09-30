import os
import re
import sys
from os import listdir
from colorama import init, Fore

from PythonScripts import utils

init(autoreset=True)

COMMAND_NAME = ""
SEARCH_STRING = ""
CURRENT_DIR_PATH = ""

AVAILABLE_OPTIONS = ["-r", "-R", "-d", "-D"]


def search_in_current_directory(dir_path, search_string):
    files = [f for f in listdir(dir_path)]
    count = 0

    for file in files:
        if re.search(search_string, file, re.IGNORECASE):
            if os.path.isdir(file):
                print(f"{Fore.YELLOW}{file}")
            else:
                print(f"{Fore.GREEN}{file}")
            count += 1

    print("\nTotal", count, "files and folders matched")


def recursive_search_in_current_directory(dir_path, search_string):
    count = 0

    for root, dirs, files in os.walk(dir_path):
        for dir in dirs:
            if re.search(search_string, dir, re.IGNORECASE):
                print(f"{root}    {Fore.YELLOW}{dir}    {Fore.BLUE}folder")
                count += 1
        for file in files:
            if re.search(search_string, file, re.IGNORECASE):
                print(f"{root}    {Fore.GREEN}{file}    {Fore.BLUE}file")
                count += 1

    print("\nTotal", count, "files and folders matched")


def execute_cmd(options):
    if "-d" in options or "-D" in options:
        utils.print_description(COMMAND_NAME)
        return
    elif "-r" in options or "-R" in options:
        recursive_search_in_current_directory(CURRENT_DIR_PATH, SEARCH_STRING)
        return
    else:
        search_in_current_directory(CURRENT_DIR_PATH, SEARCH_STRING)

    return


def main():
    global COMMAND_NAME
    global SEARCH_STRING
    global CURRENT_DIR_PATH

    COMMAND_NAME = sys.argv[1]
    CURRENT_DIR_PATH = os.getcwd()

    options = {}

    for arg in sys.argv[2:]:
        if utils.is_option(arg):
            if arg in AVAILABLE_OPTIONS:
                options[arg] = True
            else:
                utils.print_unknown_option(arg)
                return
        else:
            SEARCH_STRING = arg

    execute_cmd(options)




if __name__=='__main__':
    main()
    exit()