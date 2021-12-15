import os
import sys
import cv2
from colorama import Fore, Back, Style, init

import utils


##COLORAMA INIT()
init(autoreset=True)


COMMAND_NAME = ""
AVAILABLE_OPTIONS = {
    '-r': {
        'arg_required': True,
        'description': 'to set the resolution of image'
    },
    '-R': {
        'arg_required': True,
        'description': 'to set the resolution of image'
    },
    '-d': {
        'arg_required': False,
        'description': 'gives description of the command'
    },
    '-D': {
        'arg_required': False,
        'description': 'gives description of the command'
    }
}

DEFAULT_RESOLUTION = 238  ## 238 chars
HIGH_RESOLUTION = 850
MEDIUM_RESOLUTION = 500
LOW_RESOLUTION = 150


def get_symbol(val):
    map = {
        0: ' ',
        1: '.',
        2: ',',
        3: '-',
        4: '~',
        5: ':',
        6: ';',
        7: '=',
        8: '!',
        9: '*',
        10: 'h',
        11: '#',
        12: '$',
        13: '@',
        14: '@'
    }

    factor = 255/14
    brightness_number = int(val/factor)
    return map[brightness_number]


def initialize_image_data(image_path):
    image = None
    try:
        image = cv2.imread(image_path)
    except Exception as e:
        print(str(e))
    return image


def preprocess_image(image):
    grey_scale = None
    try:
        grey_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        print(str(e))
    return grey_scale


def get_console_values(image, resolution):
    console_image_width = 0
    console_image_height = 0

    if resolution == 'l':
        console_image_width =LOW_RESOLUTION
    elif resolution == 'm':
        console_image_width = MEDIUM_RESOLUTION
    elif resolution == 'h':
        console_image_width = HIGH_RESOLUTION
    else:
        console_image_width = DEFAULT_RESOLUTION

    image_width = image.shape[1]
    image_height = image.shape[0]
    console_image_height = int(((image_height / image_width) * console_image_width) / 4)

    return console_image_width, console_image_height


def make_image_ASCII_string(params):
    console_image_height = params['console_image_height']
    console_image_width = params['console_image_width']
    image = params['image']
    image_height = image.shape[0]
    image_width = image.shape[1]

    s = ""
    for i in range(0, console_image_height):
        arr = []
        for j in range(0, console_image_width):
            row = int((image_height / console_image_height) * i)
            col = int((image_width / console_image_width) * j)
            val = image[row][col]
            symbol = get_symbol(val)
            s += symbol
        s += "\n"

    return s


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
        else:
            options['image_path'] = arg

    return options


def execute_cmd(options):
    if '-d' in options:
        utils.print_description(COMMAND_NAME)
        return

    image_path = options['image_path'] if 'image_path' in options else None
    if not image_path:
        print("No image path provided")
        return

    resolution = 'default'
    if '-r' in options:
        resolution = options['-r']

    image = initialize_image_data(image_path)
    processed_image = preprocess_image(image)
    if processed_image is None: return
    console_image_width, console_image_height = get_console_values(processed_image, resolution)

    params = {'image': processed_image, 'console_image_width': console_image_width, 'console_image_height': console_image_height}
    s = make_image_ASCII_string(params)

    utils.clear_screen()
    print(f"console height: {console_image_height}  console width: {console_image_width}")
    print(s)


def main():
    global COMMAND_NAME
    COMMAND_NAME = sys.argv[1]

    options = register_options()
    execute_cmd(options)


if __name__=='__main__':
    main()
    exit()

