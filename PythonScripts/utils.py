import re

import config as conf


def is_option(arg):
    x = re.search("^-[a-zA-Z]+", arg)

    if x:
        return True
    return False


def print_unknmown_command(cmd):
    print("{} is an unknown command".format(cmd))


def print_unknown_option(option):
    print("{} is an unknown option".format(option))


def print_description(command_name):
    description = conf.CMD_MAP[command_name]['description']
    print(description)