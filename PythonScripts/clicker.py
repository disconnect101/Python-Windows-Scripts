from pynput.mouse import Button, Controller
import time
import keyboard
from colorama import init
import sys
from utils import utils

COMMAND_NAME = ""
AVAILABLE_OPTIONS = {
    '-i': {
        'arg_required': True,
        'description': 'to set interval of clicks'
    },
    '-d': {
        'arg_required': False,
        'description': 'gives description of the command'
    }
}

init(autoreset=True)
mouse = Controller()


def start_clicks(interval):
    while True:
        if keyboard.is_pressed('q'):
            print("clicker quited")
            return
        mouse.click(Button.left, 1)
        time.sleep(interval)



def execute_cmd(options):
    click_intervals = 3  # seconds

    if '-d' in options:
        utils.print_description(COMMAND_NAME)
        return
    if '-i' in options:
        click_intervals = options['-i']

    print(f"click intervals set to {click_intervals}")
    start_clicks(int(click_intervals))


def register_options():
    options = {}
    iterable_args = iter(sys.argv[2:])
    for arg in iterable_args:
        if utils.is_option(arg):
            if arg.lower() in AVAILABLE_OPTIONS:
                if AVAILABLE_OPTIONS[arg]['arg_required']:
                    options[arg.lower()] = next(iterable_args)
                else:
                    options[arg.lower()] = True
            else:
                utils.print_unknown_option(arg)
                return

    return options


def main():
    global COMMAND_NAME
    COMMAND_NAME = sys.argv[1]

    options = register_options()
    execute_cmd(options)


if __name__ == '__main__':
    main()
    exit()
