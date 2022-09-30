import os
import re
from . import config as conf

def is_option(arg):
    x = re.search("^-[a-zA-Z]+", arg)

    if x:
        return True
    return False


def print_unknmown_command(cmd):
    print("{} is an unknown command".format(cmd))


def print_unknown_option(option):
    print("{} is an unknown option".format(option))


def print_description(command_name, AVAILABLE_OPTIONS):
    description = conf.CMD_MAP[command_name]['description']
    print("\n")
    print(description)
    print("\n")

    for option in AVAILABLE_OPTIONS:
        print(f"{option}")
        print(f"          arguement required: {AVAILABLE_OPTIONS[option]['arg_required']}")
        print(f"          description       : {AVAILABLE_OPTIONS[option]['description']}")

    print("\n")

def clear_screen():
    os.system('cls')