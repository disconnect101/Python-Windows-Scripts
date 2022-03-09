from PythonScripts.utils import config as conf
from colorama import Fore, init

init(autoreset=True)

print("\nCOMMANDS AVAILABLE\n")
for cmd in conf.CMD_MAP:
    print(f"{Fore.CYAN}{cmd}")

print("\n")
