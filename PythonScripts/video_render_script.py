import os
import sys
import time
from tqdm import tqdm
import cv2
from colorama import Fore, Back, Style, init

import utils


init(autoreset=True)


COMMAND_NAME = ""
AVAILABLE_OPTIONS = {
    '-r': {
        'arg_required': True,
        'description': 'to set the resolution of video'
    },
    '-d': {
        'arg_required': False,
        'description': 'gives description of the command'
    },
    '-overlay': {
        'arg_required': True,
        'description': 'overlay video with another video or image'
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

    factor = 255 / 14
    brightness_number = int(val / factor)
    return map[brightness_number]


def initialize_video_data(video_path):
    video = None
    try:
        video = cv2.VideoCapture(video_path)
    except Exception as e:
        print(str(e))
    return video


def convert_image_to_2D_array(image):
    grey_scale = None
    try:
        grey_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        print(str(e))
    return grey_scale


def get_console_values(video, resolution):
    ret, image = video.read()
    image = convert_image_to_2D_array(image)
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    console_image_width = 0
    console_image_height = 0

    if resolution == 'l':
        console_image_width = LOW_RESOLUTION
    elif resolution == 'm':
        console_image_width = MEDIUM_RESOLUTION
    elif resolution == 'h':
        console_image_width = HIGH_RESOLUTION
    else:
        console_image_width = DEFAULT_RESOLUTION

    image_width = image.shape[1]
    image_height = image.shape[0]
    console_image_height = int(((image_height / image_width) * console_image_width) / 4)

    return { 'console_image_width': console_image_width, 'console_image_height': console_image_height }


def make_image_ASCII_string(image_array, params):
    console_image_height = params['console_image_height']
    console_image_width = params['console_image_width']
    image_height = len(image_array)
    image_width = len(image_array[0])

    s = ""
    for i in range(0, console_image_height):
        arr = []
        for j in range(0, console_image_width):
            row = int((image_height / console_image_height) * i)
            col = int((image_width / console_image_width) * j)
            val = image_array[row][col]
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
            options['video_path'] = arg

    return options


def print_ASCII_video(frames, params):
    utils.clear_screen()
    print(f"console height: {params['console_image_height']}  console width: {params['console_image_width']}")

    for frame in frames:
        #utils.clear_screen()
        os.system("cls")
        print(frame)
        time.sleep(0.1)


def convert_video_frames_to_2D_array(video, frame_jumps):
    frame_number = 0
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_jump_factor = frame_jumps
    frames = []
    total_jumps = int(total_frames / frame_jump_factor)

    for jump in tqdm(range(0, total_jumps)):
        ret, image = video.read()
        image_array = convert_image_to_2D_array(image)

        if frame_number > total_frames:
            break
        frame_number += frame_jump_factor
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        frames.append(image_array)

    return frames


def convert_frames_to_ASCII_string_array(video_frames_array, console_params):
    string_frame_array = []
    for frame in tqdm(video_frames_array):
        s = make_image_ASCII_string(frame, console_params)
        string_frame_array.append(s)

    return string_frame_array


def get_video_as_ASCII_video(video_path, resolution):
    video = initialize_video_data(video_path)
    if not video: return

    console_params = get_console_values(video, resolution)
    video_with_2D_frames = convert_video_frames_to_2D_array(video)
    ASCII_video = convert_frames_to_ASCII_string_array(video_with_2D_frames, console_params)

    return ASCII_video, console_params


def multipy_frames_of_video(ASCII_video, overlay_ASCII_video, console_params):
    height = console_params['console_image_height']
    width = console_params['console_image_width']

    print(height, width)
    print(len(ASCII_video[0]), len(ASCII_video[0][0]))

    multiplied_frames = []
    number_of_frames_in_main_video = len(ASCII_video)
    number_of_frames_in_overlay = len(overlay_ASCII_video)

    for k in tqdm(range(0, number_of_frames_in_main_video)):
        frame = []
        for i in range(0, height):
            row = []
            for j in range(0, width):
                prod = int( (int(ASCII_video[k][i][j]) * int(overlay_ASCII_video[k%number_of_frames_in_overlay][i][j])) / 255)
                #if (ASCII_video[k][i][j] * overlay_ASCII_video[k%number_of_frames_in_overlay][i][j]) > 255:
                #print(type(ASCII_video[k][i][j]), ASCII_video[k][i][j], overlay_ASCII_video[k%number_of_frames_in_overlay][i][j])
                row.append(prod)
            frame.append(row)
        multiplied_frames.append(frame)

    return multiplied_frames


def resize_frames(video, width, height):
    video_height = len(video[0])
    video_width = len(video[0][0])

    #print(video_height, video_width, height, width)

    resized_frames = []
    for frame in tqdm(video):
        resized_frame = []
        for i in range(0, height):
            row = []
            for j in range(0, width):
                #print(video_width, width, j, (video_width/width)*j)
                r = int((video_height/height)*i)
                c = int((video_width/width)*j)
                #print(r, c)
                row.append(frame[r][c])

            resized_frame.append(row)

        #print(resized_frame)
        resized_frames.append(resized_frame)

    return resized_frames


def get_video_as_ASCII_video_with_overlay(video_path, overlay_path, resolution):
    video = initialize_video_data(video_path)
    if not video: return
    console_params = get_console_values(video, resolution)
    video_with_2D_frames = convert_video_frames_to_2D_array(video, 20)
    video_with_2D_frames = resize_frames(video_with_2D_frames, console_params['console_image_width'], console_params['console_image_height'])

    overlay_video = initialize_video_data(overlay_path)
    if not overlay_video: return
    overlay_video_with_2D_frames = convert_video_frames_to_2D_array(overlay_video, 5)
    overlay_video_with_2D_frames = resize_frames(overlay_video_with_2D_frames, console_params['console_image_width'], console_params['console_image_height'])

    multiplied_video = multipy_frames_of_video(video_with_2D_frames, overlay_video_with_2D_frames, console_params)

    overlay_ASCII_video = convert_frames_to_ASCII_string_array(multiplied_video, console_params)

    return overlay_ASCII_video, console_params


def execute_cmd(options):
    video_path = options['video_path'] if 'video_path' in options else None
    resolution = 'default'
    overlay_path = None

    if '-d' in options:
        utils.print_description(COMMAND_NAME)
        return
    if not video_path:
        print("No video path provided")
        return
    if '-r' in options:
        resolution = options['-r']
    if '-overlay' in options:
        overlay_path = options['-overlay']
        #print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")


    ASCII_video = None
    console_params =  None
    if not overlay_path:
        ASCII_video, console_params = get_video_as_ASCII_video(video_path, resolution)
    elif overlay_path:
        ASCII_video, console_params = get_video_as_ASCII_video_with_overlay(video_path, overlay_path, resolution)

    print_ASCII_video(ASCII_video, console_params)


def main():
    global COMMAND_NAME
    COMMAND_NAME = sys.argv[1]

    options = register_options()
    execute_cmd(options)


if __name__ == '__main__':
    main()
    exit()





