import json
import sys


def extract():
    try:
        with open('secrets.json', 'r+') as sc:
            tokens = json.loads(sc)

            return tokens
    except FileNotFoundError:
        print('Check whether secrets.json file exists')
        sys.exit(2)

e

if __name__ == '__main__':
    print(extract())