#!/usr/bin/env python
"""Downloading of files using 4chan's read-only JSON API"""

import configparser
import requests
import time
import urllib.request
import hashlib
import os
import sys

cfg = configparser.ConfigParser()
cfg.read('config.ini')

searchterm = sys.argv[2]
board = sys.argv[1]
savedir = cfg['DEFAULT']['saveto'] + board + "/"
url = "https://a.4cdn.org/" + board + "/catalog.json"

html = requests.get(url)
data = html.json()
threads = []
filenames = []


def md(dir):
    if not os.path.exists(dir):
        print("Creating directory: " + dir + "\n")
        os.makedirs(dir)
    else:
        print("Directory " + dir + " exists, continuing...\n")
        print("=" * 80)


def save_pic(url, save_path):
    """Saves a file to disk when given a URL"""
    hashval = hashlib.md5(url.encode('UTF-8')).hexdigest()
    file_ext = url.split(".")[-1]
    to_save = (save_path + hashval + "." + file_ext)
    file_name = hashval + "." + file_ext
    if os.path.isfile(to_save):
        #print(file_name + "\texists, skipping...")
        pass
    else:
        print(file_name + "\tdownloading...")
        try:
            urllib.request.urlretrieve(url, to_save)
        except:
            pass


def get_thread_url(board, thread_no):
    return "https://boards.4chan.org/" + board + "/thread/" + str(thread_no)

for p in range(0, 9):
    for t in range(0, 15):
        thread = data[p]['threads'][t]['no']
        if searchterm in data[p]['threads'][t]['semantic_url']:
            threads.append(thread)

time.sleep(1.2)  # Give 4chan some breathing space between requests.

for thread in threads:
    thread_url = "https://a.4cdn.org/" + board + "/thread/" + \
        str(thread) + ".json"
    thread_html = requests.get(thread_url)
    thread_data = thread_html.json()

    for post in range(0, len(thread_data['posts'])):
        if 'tim' in thread_data['posts'][post]:
            filename = "https://i.4cdn.org/" + board + "/" + \
                str(thread_data['posts'][post]['tim']) + \
                thread_data['posts'][post]['ext']
            fname = "https://i.4cdn.org/" + board + "/" + \
                (hashlib.md5(thread_data['posts'][post]['md5'].encode('UTF-8'))).hexdigest() + \
                thread_data['posts'][post]['ext']
            """
            May use fname instead of filename in future, this uses 4chan's
            MD5 value for the file in question. This may prevent us from
            downloading duplicates.
            """

            filenames.append(filename)

    time.sleep(1)

print("=" * 80)
print("\nCurrently " + str(len(filenames)) +
      " items downloadable for search \'" + searchterm + "\'...")

saveto = savedir + searchterm + "/"
md(saveto)

if __name__ == "__main__":
    for pic in filenames:
        save_pic(pic, saveto)
