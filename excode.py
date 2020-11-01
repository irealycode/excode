import socket
import select
import errno
import sys, getopt
from colorama import Fore, Back, Style
import random

b = 0

def baner():
    b = random.randrange(1, 5)
    if b == 1:
        print(Fore.LIGHTYELLOW_EX + '▓█████ ▒██   ██▒ ▄████▄   ▒█████  ▓█████▄ ▓█████ ')
        print('▓█   ▀ ▒▒ █ █ ▒░▒██▀ ▀█  ▒██▒  ██▒▒██▀ ██▌▓█   ▀ ')
        print('▒███   ░░  █   ░▒▓█    ▄ ▒██░  ██▒░██   █▌▒███   ')
        print('▒▓█  ▄  ░ █ █ ▒ ▒▓▓▄ ▄██▒▒██   ██░░▓█▄   ▌▒▓█  ▄ ')
        print('░▒████▒▒██▒ ▒██▒▒ ▓███▀ ░░ ████▓▒░░▒████▓ ░▒████▒')
        print('░░ ▒░ ░▒▒ ░ ░▓ ░░ ░▒ ▒  ░░ ▒░▒░▒░  ▒▒▓  ▒ ░░ ▒░ ░')
        print(' ░ ░  ░░░   ░▒ ░  ░  ▒     ░ ▒ ▒░  ░ ▒  ▒  ░ ░  ░')
        print('   ░    ░    ░  ░        ░ ░ ░ ▒   ░ ░  ░    ░   ')
        print('   ░  ░ ░    ░  ░ ░          ░ ░     ░       ░  ░')
        print('                ░                  ░             ' + Fore.RESET)
        print("                                                 ")
    elif b == 2:
        print(Fore.WHITE + '.------..------..------..------..------..------.')
        print('|E.--. ||X.--. ||C.--. ||O.--. ||D.--. ||E.--. |')
        print('| (\/) || :/\: || :/\: || :/\: || :/\: || (\/) |')
        print('| :\/: || (__) || :\/: || :\/: || (__) || :\/: |')
        print("| '--'E|| '--'X|| '--'C|| '--'O|| '--'D|| '--'E|")
        print("`------'`------'`------'`------'`------'`------'" + Fore.RESET)
        print("                                                ")
    elif b == 3:
        print(Fore.GREEN + "                               .___      ")
        print("  ____ ___  ___ ____  ____   __| _/____  ")
        print("_/ __ \\  \/  // ___\/  _ \ / __ |/ __ \ ")
        print("\  ___/ >    <\  \__(  <_> ) /_/ \  ___/ ")
        print(" \___  >__/\_ \\___  >____/\____ |\___  >")
        print("     \/      \/    \/           \/    \/ " + Fore.RESET)
        print("                                         ")
    elif b == 4:
        print(Fore.RED + "                     (          ")
        print("   (     )           )\ )   (   ")
        print("  ))\ ( /(  (   (   (()/(  ))\ ")
        print(" /((_))\()) )\  )\   ((_))/((_)")
        print("(_)) ((_)\ ((_)((_)  _| |(_))  ")
        print("/ -_)\ \ // _|/ _ \/ _` |/ -_) ")
        print("\___|/_\_\\__|\___/\__,_|\___| " + Fore.RESET)
        print("                               ")
baner()
while True:
    excode = input(Fore.LIGHTGREEN_EX + "eXcode> " + Fore.RESET)
    if excode.startswith('search '):
        try:
            searchfor = excode.split("search ",1)[1]
            print(searchfor)
        except:
            print('unknown command: ' + excode)
    elif excode == "exit":
        sys.exit()
    elif excode == "help":
        print("you can do nothing in the current time :/")
    else:
        print('unknown command: ' + excode)