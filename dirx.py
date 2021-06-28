#!/usr/bin/env python3
import requests
import sys
import os
import threading
import random

#-----------------------------------------------------------#

arg_list = ['-w ', '-u ','-d ','-ra']
wordlist_agr = '-w '
url_arg = '-u '
wordlist = ''
url = ''
ac = '200,302,403,400'

#-----------------------------------------------------------#

args = sys.argv[1:]
args = ' '.join(args)
args = str(args)
wordlist = args.split(arg_list[0],1)[1]
wordlist = wordlist.split().pop(0)
url = args.split(arg_list[1],1)[1]
url = url.split().pop(0)
if arg_list[3] in args:
    random_agent = True
    rra = 'Random'
else:
    random_agent = False
    rra = 'dirx v1.0'
# print(f'url:{url}, wordlist:{wordlist}')


def main():
    with open(wordlist) as dirnum:
        n=0
        for i in dirnum:
            n += 1
    banner = f"""
=====================================================================================
-------------------------------------dirx v1.0---------------------------------------
=====================================================================================
 GET HTTP/1.1

 Url : {url}
 User-agent : {rra}
 Direcrories Loaded : {n}
 Accepting Status : {ac}

=====================================================================================
---------------------------------made-by-irealycode----------------------------------
=====================================================================================

    """
    print(banner)
    dirs = open(wordlist)
    dirs = dirs.readlines()
    ua = open('user-agents.txt').read().splitlines()
    for i in range(len(dirs)):
        directory = dirs[i].strip()
        full_url = url+'/'+directory
        if random_agent:
            user_agent = {'User-agent': random.choice(ua)}
        else:
            user_agent = {'User-agent': 'dirx v1.0'}
        # print(f'get {full_url}/{directory} user-agent:{user_agent}')random.choice(ua)
        req = requests.get(full_url, headers = user_agent, timeout=5)
        print(f'directories tested : {i}', end='\r')
        if str(req.status_code) != '404':
            print(f'{full_url} : {req.status_code}')



main()
