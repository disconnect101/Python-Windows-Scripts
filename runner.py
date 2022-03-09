import sys
import os
from PythonScripts.utils import utils, config as conf

if len(sys.argv) == 1:
    sys.argv.append("list")

cmd = sys.argv[1]
args = " ".join([i for i in sys.argv[1:]])

if cmd in conf.CMD_MAP:
    command_string = "python {path} {args}".format(path=conf.CMD_MAP[cmd]['path'], args=args)
    os.system(command_string)
else:
    utils.print_unknmown_command(cmd)
    exit()

