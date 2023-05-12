#!/usr/bin/env python3

import re
import os
import requests
import argparse
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument('-s', help='hash', dest='hash')
parser.add_argument('-f', help='file containing hashes', dest='file')
parser.add_argument('-d', help='directory containing hashes', dest='dir')
parser.add_argument('-t', help='number of threads', dest='threads', type=int)
args = parser.parse_args()

#Colors and shit like that
end = '\033[0m'
red = '\033[91m'
green = '\033[92m'
white = '\033[97m'
dgreen = '\033[32m'
yellow = '\033[93m'
back = '\033[7;91m'
run = '\033[97m[~]\033[0m'
que = '\033[94m[?]\033[0m'
bad = '\033[91m[-]\033[0m'
info = '\033[93m[!]\033[0m'
good = '\033[92m[+]\033[0m'

cwd = os.getcwd()
directory = args.dir
file = args.file
thread_count = args.threads or 4

if directory and directory[-1] == '/':
    directory = directory[:-1]

def alpha(hashvalue, hashtype):
    response = requests.get(f'https://lea.kz/api/hash/{hashvalue}').text
    return (
        match.group(1)
        if (match := re.search(r': "(.*?)"', response))
        else False
    )

def beta(hashvalue, hashtype):
    response = requests.get('http://hashtoolkit.com/reverse-hash/?hash=', hashvalue).text
    if match := re.search(r'/generate-hash/?text=.*?"', response):
        return match[1]
    else:
        return False

def delta(hashvalue, hashtype):
    data = {'auth':'8272hgt', 'hash':hashvalue, 'string':'','Submit':'Submit'}
    response = requests.post('http://hashcrack.com/index.php' , data).text
    if match := re.search(
        r'<span class=hervorheb2>(.*?)</span></div></TD>', response
    ):
        return match[1]
    else:
        return False

def theta(hashvalue, hashtype):
    response = requests.get(
        f'http://md5decrypt.net/Api/api.php?hash={hashvalue}&hash_type={hashtype}&email=deanna_abshire@proxymail.eu&code=1152464b80a61728'
    ).text
    return response if response != "" else False

print ('''\033[1;97m_  _ ____ ____ _  _    ___  _  _ ____ ___ ____ ____
|__| |__| [__  |__|    |__] |  | [__   |  |___ |__/
|  | |  | ___] |  |    |__] |__| ___]  |  |___ |  \  %sv3.0\033[0m\n''' % red)

md5 = [alpha, beta, theta, delta]
sha1 = [alpha, beta, theta, delta]
sha256 = [alpha, beta, theta]
sha384 = [alpha, beta, theta]
sha512 = [alpha, beta, theta]

def crack(hashvalue):
    result = False
    if len(hashvalue) == 32:
        if not file:
            print(f'{info} Hash function : MD5')
        for api in md5:
            if r := api(hashvalue, 'md5'):
                return r
    elif len(hashvalue) == 40:
        if not file:
            print(f'{info} Hash function : SHA1')
        for api in sha1:
            if r := api(hashvalue, 'sha1'):
                return r
    elif len(hashvalue) == 64:
        if not file:
            print(f'{info} Hash function : SHA-256')
        for api in sha256:
            if r := api(hashvalue, 'sha256'):
                return r
    elif len(hashvalue) == 96:
        if not file:
            print(f'{info} Hash function : SHA-384')
        for api in sha384:
            if r := api(hashvalue, 'sha384'):
                return r
    elif len(hashvalue) == 128:
        if not file:
            print(f'{info} Hash function : SHA-512')
        for api in sha512:
            if r := api(hashvalue, 'sha512'):
                return r
    else:
        if file:
            return False
        print(f'{bad} This hash type is not supported.')
        quit()

result = {}

def threaded(hashvalue):
    if resp := crack(hashvalue):
        print(f'{hashvalue} : {resp}')
        result[hashvalue] = resp

def grepper(directory):
    os.system('''grep -Pr "[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}" %s --exclude=\*.{png,jpg,jpeg,mp3,mp4,zip,gz} |
        grep -Po "[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}" >> %s/%s.txt''' % (directory, cwd, directory.split('/')[-1]))
    print(f"{info} Results saved in {directory.split('/')[-1]}.txt")

def miner(file):
    lines = []
    found = set()
    with open(file, 'r') as f:
        lines.extend(line.strip('\n') for line in f)
    for line in lines:
        if matches := re.findall(
            r'[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}',
            line,
        ):
            for match in matches:
                found.add(match)
    print ('%s Hashes found: %i' % (info, len(found)))
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
    futures = (threadpool.submit(threaded, hashvalue) for hashvalue in found)
    for i, _ in enumerate(concurrent.futures.as_completed(futures)):
        if i + 1 == len(found) or (i + 1) % thread_count == 0:
            print('%s Progress: %i/%i' % (info, i + 1, len(found)), end='\r')

def single(args):
    if result := crack(args.hash):
        print (result)
    else:
        print(f'{bad} Hash was not found in any database.')

if directory:
    try:
        grepper(directory)
    except KeyboardInterrupt:
        pass

elif file:
    try:
        miner(file)
    except KeyboardInterrupt:
        pass
    with open(f"cracked-{file.split('/')[-1]}", 'w+') as f:
        for hashvalue, cracked in result.items():
            f.write(f'{hashvalue}:{cracked}' + '\n')
    print(f"{info} Results saved in cracked-{file.split('/')[-1]}")

elif args.hash:
    single(args)
