import sys
import os
import config as conf

cmd = sys.argv[1]
args = " ".join([i for i in sys.argv[1:]])

if cmd in conf.CMD_MAP:
    command_string = "python {path} {args}".format(path=conf.CMD_MAP[cmd]['path'], args=args)
    os.system(command_string)
else:
    print("Unknown command")
    exit()