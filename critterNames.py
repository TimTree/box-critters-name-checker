import time
import concurrent.futures
import argparse
import requests
import json
import re

print('--------------------------------------------')
print('BOX CRITTERS NAME CHECKER v2.0')
print('github.com/TimTree/box-critters-name-checker')
print('--------------------------------------------')

start = time.perf_counter()

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input',
    default='test.txt',
    help='Input file of nicknames to test. Defaults to "test.txt".')
parser.add_argument(
    '-th',
    '--thread',
    default='multi',
    help='Choose whether to use single threading "single" or multithreading \
        "multi" to check nicknames. Defaults to "multi".')
args = parser.parse_args()

apiURL = 'https://titleId.playfabapi.com/Client/RegisterPlayFabUser'
headers = {'Content-Type': 'application/json'}
count = 0
untakenNames = []
try:
    with open(args.input) as f:
        allNames = f.readlines()
        totalNames = len(allNames)
except Exception as e:
    print(f'ERROR: {e}')
    print('Is your terminal in the same directory as critterNames.py?')
    quit()


def checkNames(name):
    nickname = name.strip()
    returnPrint = f'{nickname} ... '
    # Check if nickname is valid (3-5 characters, letters/numbers/spaces
    # only)
    if (len(nickname) < 3 or len(nickname) >
            25 or not re.match('^[a-zA-Z0-9 ]*$', nickname)):
        returnPrint += '[X] (Invalid)'
        return returnPrint
    # If nickname is vaild, send to API to see if it's taken
    dictToSend = {
        'TitleId': '5417',
        'DisplayName': nickname,
        'Password': 'doesntmatter',
        'RequireBothUsernameAndEmail': False,
    }
    res = requests.post(apiURL, data=json.dumps(dictToSend),
                        headers=headers)
    while json.loads(res.text)['error'] == 'APIClientRequestRateLimitExceeded':
        res = requests.post(apiURL, data=json.dumps(dictToSend),
                            headers=headers)
    if json.loads(res.text)['error'] == 'InvalidParams':
        untakenNames.append(nickname)
        returnPrint += '[✓]'
    else:
        returnPrint += '[X] (Taken)'
    return returnPrint


if args.thread.lower() == 'single':  # single threading
    for name in allNames:
        count += 1
        print(f'Checked nickname {count}/{totalNames}: {checkNames(name)}')
else:  # multithreading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(checkNames, name) for name in allNames]
        for c in concurrent.futures.as_completed(results):
            count += 1
            print(f'Checked nickname {count}/{totalNames}: {c.result()}')

print('')
print('---')
print(f'Found {len(untakenNames)} untaken nickname(s)')
print('---')
for untakenName in sorted(untakenNames):
    print(untakenName)

finish = time.perf_counter()
print('')
print(f'Finished in {round(finish-start, 2)} second(s)')
