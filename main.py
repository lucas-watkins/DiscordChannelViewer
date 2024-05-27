from requests import get
import pickle
from pathlib import Path
import os
import sys
from datetime import datetime

try:
    hidden_only = True if sys.argv[1] == '-h' else False 
except IndexError:
    hidden_only = False

token_file_path = os.path.dirname(__file__) + '/token.dat' 

if not Path.exists(Path(token_file_path)):
    token = input('Discord Token: ')
    with open(token_file_path, 'wb') as file_handler:
        pickle.dump(token, file_handler)

else:
    with open(token_file_path, 'rb') as file_handler:
        token = pickle.load(file_handler)

server_id = input('Server ID: ')
headers = {'Authorization': f'{token}', 'Content-Type': 'application/json', 'User-Agent': 'LucasBot/Infinity'}
req = get(f'https://discord.com/api/v10/guilds/{server_id}/channels', headers=headers)
json = req.json()

if req.status_code in (401, 5001):
    sys.exit('Discord API Unauthorized, Check API Key')


def parse_snowflake_id(snowflake: str) -> str:
    if snowflake in ('N/A', None):
        return 'N/A'
    
    time_stamp = datetime.fromtimestamp(((int(snowflake) >> 22) + 1420070400000) / 1000)
    return time_stamp.strftime('%Y-%m-%d, %-I:%M %p')


def get_type(c: dict) -> str:
    for i in c:
        if i['deny'] == '1024':
            return ' (Hidden)'
    
    return ''
    

def parse_channel(c: dict) -> str | None:
    match c['type']:
        case 2:
            resp = f'VC Name: {c['name']}, Last Connect On: {parse_snowflake_id(c.get('last_message_id', 'N/A'))}'
        case 0:
            resp = f'Name: #{c['name']}, Topic: {c.get('topic', 'N/A')}, \
Last Message Sent On: {parse_snowflake_id(c.get('last_message_id', 'N/A'))}'
        case _:
            return None
    
    return resp + f'{get_type(c['permission_overwrites'])}\n'
        
      
def printfunc(x: list):
    for i in x:
        print(i)
        
        
def append(item, l1, l2):
    if '#' in channel:
        l1.append(item)
    else:
        l2.append(item)


channels = map(lambda x: parse_channel(x), json)
vcs = []
txtc = []
for channel in channels:
    if channel is not None:
        if hidden_only:
            if '(Hidden)' in channel:
                append(channel, txtc, vcs)
        else:
            append(channel, txtc, vcs)

if not all(i is None for i in txtc):
    print('\nText Channels -->')
    printfunc(txtc)

if not all(i is None for i in vcs):
    print('\nVoice Channels -->')
    printfunc(vcs)
