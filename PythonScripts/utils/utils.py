import os
import re
from . import config as conf
from colorama import init, Fore, Style
import pyfiglet

init(autoreset=True)


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
    ascii_text_command_name = pyfiglet.figlet_format(command_name)
    print("\n")
    print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}{ascii_text_command_name}")

    print(description)
    print("")

    for option in AVAILABLE_OPTIONS:
        print(f"{option}", end="")
        if 'short' in AVAILABLE_OPTIONS[option].keys():
            print(f", {AVAILABLE_OPTIONS[option]['short']}")
        else:
            print("")
        print(f"             arguement required: {AVAILABLE_OPTIONS[option]['arg_required']}")
        print(f"             description       : {AVAILABLE_OPTIONS[option]['description']}")
        print("")


def clear_screen():
    os.system('cls')

