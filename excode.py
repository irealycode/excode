import socket
import select
import errno
import sys, getopt
from colorama import Fore, Back, Style
import random
import os


HEADER_LENGTH = 10
b = 0
using = "nothing"
HOST = ""
LPORT = ""
PORT = 0
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockets_list = [server_socket]
clients = {}
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
        print("excode made by : irealycode")
        print("https://github.com/irealycode")
        print("                               ")
    elif b == 2:
        print(Fore.WHITE + '.------..------..------..------..------..------.')
        print('|E.--. ||X.--. ||C.--. ||O.--. ||D.--. ||E.--. |')
        print('| (\/) || :/\: || :/\: || :/\: || :/\: || (\/) |')
        print('| :\/: || (__) || :\/: || :\/: || (__) || :\/: |')
        print("| '--'E|| '--'X|| '--'C|| '--'O|| '--'D|| '--'E|")
        print("`------'`------'`------'`------'`------'`------'" + Fore.RESET)
        print("                                                ")
        print("excode made by : irealycode")
        print("https://github.com/irealycode")
        print("                               ")
    elif b == 3:
        print(Fore.GREEN + "                               .___      ")
        print("  ____ ___  ___ ____  ____   __| _/____  ")
        print("_/ __ \\  \/  // ___\/  _ \ / __ |/ __ \ ")
        print("\  ___/ >    <\  \__(  <_> ) /_/ \  ___/ ")
        print(" \___  >__/\_ \\___  >____/\____ |\___  >")
        print("     \/      \/    \/           \/    \/ " + Fore.RESET)
        print("                                         ")
        print("excode made by : irealycode")
        print("https://github.com/irealycode")
        print("                               ")
    elif b == 4:
        print(Fore.RED + "                     (          ")
        print("   (     )           )\ )   (   ")
        print("  ))\ ( /(  (   (   (()/(  ))\ ")
        print(" /((_))\()) )\  )\   ((_))/((_)")
        print("(_)) ((_)\ ((_)((_)  _| |(_))  ")
        print("/ -_)\ \ // _|/ _ \/ _` |/ -_) ")
        print("\___|/_\_\\__|\___/\__,_|\___| " + Fore.RESET)
        print("                               ")
        print("excode made by : irealycode")
        print("https://github.com/irealycode")
        print("                               ")

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

def serverlisten():
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                user = receive_message(client_socket)
                if user is False:
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user

                print(Fore.LIGHTGREEN_EX +'new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')) + Fore.RESET)

            else:
                message = receive_message(notified_socket)
                if message is False:
                    print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]

                    continue
                user = clients[notified_socket]

                print(Fore.LIGHTGREEN_EX +'Message from ' + Fore.BLUE + f'{user["data"].decode("utf-8")} : ' + Fore.YELLOW +  f'{message["data"].decode("utf-8")}' + Fore.RESET)
                for client_socket in clients:
                    if client_socket != notified_socket:

                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]



def serverconnet():
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print('listening on ' + HOST + ':' + LPORT + '...')
    serverlisten()



baner()
excodeInput = "eXcode> "
while True:
    excode = input(Fore.GREEN + excodeInput + Fore.RESET)
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
    elif excode == "banner":
        baner()
    elif excode == "clear" or excode == "cls":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif excode.startswith('use '):
        try:
            use = excode.split("use ",1)[1]
            if use == "socket/server":
                excodeInput = "eXcode(" + Fore.RED + "socket/server" + Fore.LIGHTGREEN_EX + ")> "
                using = "socket"
            elif use == "nothing":
                using = "nothing"
                excodeInput = "eXcode> "
            else:
                print("can't find" + Fore.RED + use + Fore.RESET + " in excode library")
        except:
            print("error on using")
    elif excode.startswith('set '):
        if using == "socket":
            try:
                setL = excode.split("set ",1)[1]
                if setL.startswith('HOST '):
                    try:
                        HOST = setL.split("HOST ",1)[1]
                    except:
                        print("error in HOST")
                elif setL.startswith('PORT '):
                    try:
                        LPORT = setL.split("PORT ",1)[1]
                        PORT = int(LPORT)
                    except:
                        print("error in PORT")                
            except:
                print("error in seting")
        
    elif excode == "run":
        if using == "socket":
            if HOST != "" and PORT != 0:
                serverconnet()
            else:
                print("you need to set values to both port and host")
        else:
            print('run what??')
    elif excode.startswith(' '):
        print("you can't use spaces in the begining of the command.")
    elif excode == '':
        pass
    else:
        print('unknown command: ' + excode)
