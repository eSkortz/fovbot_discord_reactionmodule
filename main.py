import requests as r
import json
import time
import io
import Levenshtein
import pandas as pd
import threading
from threading import Thread
import csv
from random import choice
import random
import colorama
from colorama import Fore, Back, Style


def func_get(chat_id, usertoken):
    header = {
        'authorization': usertoken
    }
    chat_id = chat_id
    s = r.Session()
    s.headers = header
    rg = s.get(f'https://discord.com/api/v8/channels/{chat_id}/messages', headers=header)
    jsn = json.loads(rg.text)
    return jsn


def func_put_reaction(usertoken, chat_id, reaction, message_id):
    header = {
        'authorization': usertoken
    }
    chat_id = chat_id
    s = r.Session()
    s.headers = header
    s.put(f'https://discord.com/api/v9/channels/{chat_id}/messages/{message_id}/reactions/{reaction}/%40me')


def main(j):
    i = int(j)

    global array_chats_first
    global array_users_first
    global array_chats_last
    global array_users_last

    global emoji_set
    global user_token_set
    global chat_set
    global user_chatid_set

    global message_limit
    global total_sent

    user_number = random.randint(array_users_first[i], array_users_last[i] - 1)
    user_token = user_token_set[user_number]
    current_user_id = user_chatid_set[user_number]

    chat_number = random.randint(array_chats_first[i], array_chats_last[i] - 1)
    current_chat_id = chat_set[chat_number]

    print(Fore.LIGHTBLUE_EX + f'Scanning {i + 1} project {chat_number + 1} chat from user {user_number + 1}')

    chat_new_message_jsn = func_get(current_chat_id, user_token)
    try:
        rand_id = random.randint(0, message_limit)
        chat_new_message = chat_new_message_jsn[rand_id]['content']
        new_user_id = chat_new_message_jsn[rand_id]['author']['id']
        message_id = chat_new_message_jsn[rand_id]['id']
    except Exception:
        print(Fore.MAGENTA + '*** Some problems with get_message ***')

    if new_user_id != current_user_id:
        emoji = choice(emoji_set)
        func_put_reaction(user_token, current_chat_id, emoji, message_id)
        print(f'*** Sending reaction to {chat_number} chat for {rand_id} message: ***')
        print()
        total_sent += 1

    print(Fore.LIGHTWHITE_EX + f'*** Total sent {total_sent} reactions ***')
    print()

print(Fore.LIGHTGREEN_EX)
print('''
                               ....
                                    %
                            L
                            "F3  $r
                           $$$$.e$"  .
                           "$$$$$"   "
 (FovReactionBot)            $$$$c  /
        .                   $$$$$$$P
       ."c                      $$$
      .$c3b                  ..J$$$$$e
      4$$$$             .$$$$$$$$$$$$$$c
       $$$$b           .$$$$$$$$$$$$$$$$r
          $$$.        .$$$$$$$$$$$$$$$$$$
           $$$c      .$$$$$$$  "$$$$$$$$$r

        
*** Hello, I'm FovReactionBot, for my work fill the files:
    user_tokens.txt, chat_to_sent.txt, user_chat_id.txt ***
''')
print(Fore.LIGHTWHITE_EX)

array_chats_first = []
array_users_first = []
array_chats_last = []
array_users_last = []

project_num = int(input('Enter the number of threads: '))
for i in range(0, project_num):
    u1 = int(input(f'Enter the number of first user in {i+1} project: '))
    u1 -= 1
    array_users_first.append(u1)
    u2 = int(input(f'Enter the number of last user in {i+1} project: '))
    array_users_last.append(u2)
    c1 = int(input(f'Enter the number of first chat in {i+1} project: '))
    c1 -= 1
    array_chats_first.append(c1)
    c2 = int(input(f'Enter the number of last chat in {i+1} project: '))
    array_chats_last.append(c2)

emoji_set: list = open('emoji.txt', 'r', encoding='utf-8').read().splitlines()
user_token_set: list = open('user_tokens.txt', 'r', encoding='utf-8').read().splitlines()
chat_set: list = open('chat_to_sent.txt', 'r', encoding='utf-8').read().splitlines()
user_chatid_set: list = open('user_chat_id.txt', 'r', encoding='utf-8').read().splitlines()

delay = int(input('Enter a delay for sending reactions: '))
message_limit = int(input('Enter number of scanning messages from last in chat: '))
total_sent = 0

print()
print('*** Successful scanning of chats ***')
print()

print('*** I start sending reactions. ***')
print()

main_thread = []

while True:

    for i in range(0, project_num):
        for i in range(0, project_num):
            j = f'{i}'
            main_thread.append(threading.Thread(target=main, name=f'thread{i}', args=(j)))
            main_thread[i].start()
            # print()
            # print(Fore.LIGHTRED_EX + f'поток {i} проснулся')
        for i in range(0, project_num):
            main_thread[i].join()
            # print()
            # print(Fore.LIGHTRED_EX + f'поток {i} схлопнулся')
        main_thread = []
        print(Fore.LIGHTWHITE_EX + f'*** Total sent {total_sent} messages ***')
        print()
        time.sleep(delay)
