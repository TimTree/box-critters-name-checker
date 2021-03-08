import argparse
import requests
import json
import re

print('--------------------------------------------')
print('BOX CRITTERS NAME CHECKER v1.0')
print('github.com/TimTree/box-critters-name-checker')
print('--------------------------------------------')

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input',
    default='test.txt',
    help='Input file of nicknames to test. If not specified, \
        the file used is "test.txt".')
args = parser.parse_args()

apiURL = 'https://titleId.playfabapi.com/Client/RegisterPlayFabUser'
headers = {'Content-Type': 'application/json'}
count = 1
untakenNames = []
try:
    with open(args.input) as f:
        allNames = f.readlines()
        totalNames = len(allNames)
except Exception as e:
    print(f'ERROR: {e}')
    print('Is your terminal in the same directory as critterNames.py?')
    quit()
for name in allNames:
    nickname = name.strip()
    print(f'Checking nickname {count}/{totalNames}: {nickname} ... ', end='')
    # Check if nickname is valid (3-5 characters, letters/numbers/spaces only)
    if (len(nickname) < 3 or len(nickname) >
            25 or not re.match('^[a-zA-Z0-9 ]*$', nickname)):
        print('[X] (Invalid)')
        count += 1
        continue
    # If nickname is vaild, send to API to see if it's taken
    dictToSend = {
        'TitleId': '5417',
        'DisplayName': nickname,
        'Password': 'doesntmatter',
        'RequireBothUsernameAndEmail': False,
    }
    res = requests.post(apiURL, data=json.dumps(dictToSend), headers=headers)
    if json.loads(res.text)['error'] == 'InvalidParams':
        untakenNames.append(nickname)
        print('[✓]')
    else:
        print('[X] (Taken)')
    count += 1
print('')
print('---')
print(f'Found {len(untakenNames)} untaken nicknames')
print('---')
for all in untakenNames:
    print(all)
