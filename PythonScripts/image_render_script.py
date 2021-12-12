import os
import sys

import cv2
from colorama import Fore, Back, Style, init

init(autoreset=True)

CONSOLE_WIDTH = 238  ## 238 chars

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


image_name = input("type file name: ")
resolution = input("choose resolution High(h) Medium(m) Low(l): ")

if resolution == 'l':
    CONSOLE_WIDTH = 150
elif resolution == 'm':
    CONSOLE_WIDTH = 500
elif resolution == 'h':
    CONSOLE_WIDTH = 850
else:
    CONSOLE_WIDTH = 238

original_image = cv2.imread(image_name)
grey_scale = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

##cv2.imshow("Amitach", grey_scale)

print(grey_scale.shape)
image_width = grey_scale.shape[1]
image_height = grey_scale.shape[0]

console_image_height = int(((image_height/image_width)*CONSOLE_WIDTH)/4)

os.system("cls")

print(f"console height: {console_image_height}  console width: {CONSOLE_WIDTH}")



s = ""

for i in range(0, console_image_height):
    arr = []
    for j in range(0, CONSOLE_WIDTH):
        row = int((image_height/console_image_height)*i)
        col = int((image_width/CONSOLE_WIDTH)*j)

        val = grey_scale[row][col]
        symbol = get_symbol(val)


        s += symbol
        #print(f"{Style.BRIGHT}{symbol}", end='')

    s += "\n"
    #print("\n")


print(s)


