import os
import sys
import time
import keyword

import cv2
from colorama import Fore, Back, Style, init

init(autoreset=True)

CONSOLE_WIDTH = 238  ## 238 chars
console_image_height = 0
image_width = 0
image_height = 0

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


#image_name = input("type file name: ")
resolution = input("choose resolution High(h) Medium(m) Low(l): ")

if resolution == 'l':
    CONSOLE_WIDTH = 150
elif resolution == 'm':
    CONSOLE_WIDTH = 500
elif resolution == 'h':
    CONSOLE_WIDTH = 850
else:
    CONSOLE_WIDTH = 238


video = cv2.VideoCapture("lena.mp4")
frame_number = 0
total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

frames = []

while video.isOpened():

    ret, image = video.read()
    #print(image.shape)
    grey_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    frame_number += 20
    if frame_number > total_frames:
        break
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    print(grey_scale.shape)
    image_width = grey_scale.shape[1]
    image_height = grey_scale.shape[0]

    console_image_height = int(((image_height/image_width)*CONSOLE_WIDTH)/4)

    os.system("cls")

    print(f"console height: {console_image_height}  console width: {CONSOLE_WIDTH}")

    s = ""
    for i in range(0, console_image_height):

        for j in range(0, CONSOLE_WIDTH):
            row = int((image_height/console_image_height)*i)
            col = int((image_width/CONSOLE_WIDTH)*j)

            val = grey_scale[row][col]
            symbol = get_symbol(val)

            s += symbol
            #print(f"{Style.BRIGHT}{symbol}", end='')

        s += "\n"

        #print("\n")

    frames.append(s)


print("Loading completed")
while True:
    x = input("enter 'p' to play: ")
    if x == 'p':
        break


for frame in frames:
    print(frame)
    time.sleep(0.1)
    os.system("cls")





