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
HOST = "127.0.0.1"
LPORT = ""
PORT = 1234
library_list = ["socket/server", "socket/client", "lib/test"]
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if using == "socketS":
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
        print(Fore.GREEN + "                               .___")
        print("  ____ ___  ___ ____  ____   __| _/____")
        print("_/ __ \\  \/  // ___\/  _ \ / __ |/ __ \ ")
        print("\  ___/ >    <\  \__(  <_> ) /_/ \  ___/")
        print(" \___  >__/\_ \\___  >____/\____ |\___  >")
        print("     \/      \/    \/           \/    \/ " + Fore.RESET)
        print("                                         ")
        print("excode made by : irealycode")
        print("https://github.com/irealycode")
        print("                               ")
    elif b == 4:
        print(Fore.RED + "                     (")
        print("   (     )           )\ )   (")
        print("  ))\ ( /(  (   (   (()/(  ))\ ")
        print(" /((_))\()) )\  )\   ((_))/((_)")
        print("(_)) ((_)\ ((_)((_)  _| |(_))")
        print("/ -_)\ \ // _|/ _ \/ _` |/ -_)")
        print("\___|/_\_\\__|\___/\__,_|\___|" + Fore.RESET)
        print("                               ")
        print("excode made by : irealycode")
        print("https://github.com/irealycode")
        print("                               ")

#---------------------------server side------------------------------#

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

#------------------------end of server side--------------------------#

#---------------------------client side------------------------------#

def clientconnet():
    server_sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sockets.connect((HOST, PORT))
    server_sockets.setblocking(False)
    my_username = input("username: ")
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    server_sockets.send(username_header + username)
    print(Fore.LIGHTGREEN_EX + 'loged in as ' + my_username + ' seccessfully.')
    while True:
        message = input(Fore.WHITE +'[-'+ Fore.CYAN + f'{my_username}' + Fore.WHITE + '-] : ')
        if message == 'exit -y':
            print("goodbye.")
            
            break
        if len(message) <= 200:
            if message:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                server_sockets.send(message_header + message)
        elif len(message) > 200:
            print("you can't send messages that are longer than 200 characters")
            print("your message is " + str(len(message)) + " characters long")

        try:
            while True:
                username_header = server_sockets.recv(HEADER_LENGTH)
                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()
                username_length = int(username_header.decode('utf-8').strip())
                username = server_sockets.recv(username_length).decode('utf-8')
                message_header = server_sockets.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = server_sockets.recv(message_length).decode('utf-8')
                print(Fore.WHITE + '[-' + Fore.GREEN + f'{username}' + Fore.WHITE + '-] : ' + Fore.YELLOW + f'{message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue

        except Exception as e:
            print('error')
            sys.exit()
#------------------------end of client side----------------------------#

baner()
excodeInput = "eXcode> "
while True:
    excode = input(Fore.GREEN + excodeInput + Fore.RESET)
    #can't do nothing for now
    if excode.startswith('search '):
        try:
            searchfor = excode.split("search ",1)[1]
            matching = [s for s in library_list if searchfor in s]
            matchingCount = len(matching)
            if matching:
                for i in range(matchingCount):
                    print(matching[i])
            else:
                print(searchfor + ' not found.')
        except:
            print('error searching')
    elif excode == "libs":
        libsCount = len(library_list)
        for i in range(libsCount):
            print(library_list[i])
    elif excode == "exit":
        print("goodbye.")
        sys.exit()
    elif excode == "help":
        print("use : for using libraries")
        print("search : searching for libraries")
        print("clear or cls : clear the terminal window")
        print("set : for setting variables for libraries")
        print("show options : showing options for libraries")
        print("run : running or executing the command")
        print("libs : show available libraries")
        print("banner : show one of our banners")
        print("help : this menu that you are reading")
        print("exit : exit excode")
    elif excode == "banner":
        baner()
    elif excode == "clear" or excode == "cls":
        os.system('cls' if os.name == 'nt' else 'clear')
#------------------use is here------------------#
    elif excode.startswith('use '):
        try:
            use = excode.split("use ",1)[1]
            print(str(library_list[0]))
            if use == str(library_list[0]):
                excodeInput = "eXcode(" + Fore.RED + str(library_list[0]) + Fore.LIGHTGREEN_EX + ")> "
                using = "socketS"
            elif use == str(library_list[1]):
                excodeInput = "eXcode(" + Fore.RED + str(library_list[1]) + Fore.LIGHTGREEN_EX + ")> "
                using = "socketC"
            elif use == str(library_list[2]):
                excodeInput = "eXcode(" + Fore.RED + str(library_list[2]) + Fore.LIGHTGREEN_EX + ")> "
                using = "test"
            elif use == "nothing":
                using = "nothing"
                excodeInput = "eXcode> "
            else:
                print("can't find " + Fore.RED + use + Fore.RESET + " in excode library")
        except:
            print("error on using")
    elif excode == "back":
        using = "nothing"
        excodeInput = "eXcode> "
#------------------use is here------------------#
    elif excode.startswith('set '):
        if using == "socketS" or using == "socketC":
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
    elif excode == "show":
        print("do you mean: 'show options' ?")
    elif excode.startswith('show '):
        if using == "socketS" or using == "socketC":
            try:
                show = excode.split("show ",1)[1]
                if show == "options":
                    print("HOST: " + HOST)
                    print("PORT: " + str(PORT))
                else:
                    print("show what?")
            except:
                print("error showing options")
    elif excode == "run":
        if using == "socketS":
            if HOST != "" and PORT != 0:
                serverconnet()
            else:
                print("you need to set values to both port and host")
        elif using == "socketC":
            if HOST != "" and PORT != 0:
                clientconnet()
            else:
                print("you need to set values to both port and host1")
        else:
            print('run what??')
    elif excode.startswith(' '):
        print("you can't use spaces in the begining of the command.")
    elif excode == '':
        pass
    else:
        print('unknown command: ' + excode)
