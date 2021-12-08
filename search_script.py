import os
import re
import sys
from os import listdir
from os.path import isfile, join

search_string = sys.argv[2]

mypath = os.getcwd()
files = [f for f in listdir(mypath)]

found_files = []

for file in files:
    if re.search(search_string, file, re.IGNORECASE):
        found_files.append(file)

for file in found_files:
    print(file)

print("\nTotal", len(found_files), "files and folders matched")