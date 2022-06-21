#!/usr/bin/python3
import traceback
import requests
import os
from itertools import chain, product
import string
import argparse
import time
import errno


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getCurrentTime():
    currentTime = time.localtime()
    t = ''
    for atr in currentTime:
        t = t + '_' + str(atr)
    return(t)


directoryName = 'Results'
directoryNameHelp = 'Uses the specified directory to store the results of the brute force attempt. The default name is "Brute Force Results".'
fileName = 'Url_Finder' + getCurrentTime() + '.txt'
fileNameHelp = 'Uses the specified file to store the results of the brute force attempt. The default name is Url_theCurrenTime.txt.'
maxLength = 4
maxLengthHelp = 'Uses the specified integer as the maximum length of the bute force attempt. The maxLength is 4 by default.'
url = ''
urlHelp = 'Uses the specified Url as the base for the brute force attempt. This must be a complete link like https://www.google.com/. The https:// must be included.'
characterList = string.ascii_letters
characterListHelp = 'The default list are the upper and lowercase ascii letters. If you want to specify your own character List you can combine the following: l for lowercase, u for uppercase, d for digits, p for punktuation or a for all of them.'
ColorHelp = 'The script will use color codes (https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal) to dye the output in case an Url is found. The --no-color option disables that. This only works with an registry Tweak on Windows.'
version = '1.0.0'
urlsFound = 0


def bruteforce(charset, maxlength):
    """Returns a generator that yields all possible strings smaller or equall in length as the given maxlength"""
    attemptList = (''.join(candidate)
                   for candidate in chain.from_iterable(product(charset, repeat=i)
                                                        for i in range(1, maxlength + 1)))
    return attemptList


def checkIfFolderExists(folder):
    if os.path.exists(folder) == False:
        os.mkdir(folder)


def checkUrl(url, dName, fName, maxTries):
    """Checks if the url is valid a given number of times and if it is, it will write it to the file."""
    global urlsFound
    for i in range(1, maxTries + 1):
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            print(f'{bcolors.FAIL}The script failed with a no connection error. Check your internet connection.{bcolors.ENDC}\n\n')
            traceback.print_exc()
            exit()
        except Exception as e:
            print(bcolors.FAIL + 'Error: ' + str(e) + bcolors.ENDC)
            break

        if r.status_code == 200:
            urlsFound = urlsFound + 1
            with open(dName + '/' + fName, 'a') as f:
                f.write('Response: ' + str(r.status_code) +
                        ' url: ' + url + '\n')
                f.close()
                print(f'{bcolors.OKGREEN} Response: {r.status_code} url: {url}{bcolors.ENDC}')
                return True
        elif r.status_code != 200 and r.status_code != 404:
            with open(dName + '/' + fName, 'a') as f:
                f.write('Response: ' + str(r.status_code) +
                        ' url: ' + url + '\n')
                f.close()
                print(f'{bcolors.WARNING} Response: {r.status_code} url: {url}{bcolors.ENDC}')
    print(f' Response: {r.status_code} url: {url}')
    return False


def main(characterList):
    # automaticly creates a help message! Thats FUCKING AWESOME!!!
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='?', help=urlHelp, type=str, default='')
    parser.add_argument('-d', '--directory-name',
                        help=directoryNameHelp, default=directoryName)
    parser.add_argument('-f', '--file-name',
                        help=fileNameHelp, default=fileName)
    parser.add_argument('-m', '--max-length',
                        help=maxLengthHelp, type=int, default=maxLength)
    parser.add_argument('-s', '--starting-point',
                        help='The starting point for the brute force attempt. The default is the first character in the character list.', type=str, default=characterList[0])
    parser.add_argument('-c', '--character-list',
                        help=characterListHelp, default=characterList)
    parser.add_argument(
        '-t', '--max-tries', help='The maximum number of tries per url. The default is 1.', type=int, default=1)
    parser.add_argument('-n', '--no-color', help=ColorHelp,
                        default=False, action='store_true')
    parser.add_argument('--test', help='Just a quicked way to start the script for testing.', action='store_true')

    parser.add_argument('--version', action='version', version=version)

    args = parser.parse_args()

    if args.test:
        args.url = 'https://www.google.com/'
        args.max_length = 2
        args.character_list = 'l'
        args.max_tries = 2
        args.directory_name = 'test'
        args.file_name = 'test.txt'
    
    if args.url == '':
        print('No url given. Please use the -h option to see the help message.')
        return
    # check if the last character in the url is an /
    if args.url[-1] != '/':
        args.url = args.url + '/'

    print('Base Url: ' + args.url)

    # checks if the resultsfolder exists
    checkIfFolderExists(args.directory_name)

    if args.no_color == True:
        bcolors.OKGREEN = ''
        bcolors.ENDC = ''

    if (args.character_list != string.ascii_letters):
        characterList = ''
        if "l" in args.character_list:
            characterList = characterList + string.ascii_lowercase
        if "u" in args.character_list:
            characterList = characterList + string.ascii_uppercase
        if "d" in args.character_list:
            characterList = characterList + string.digits
        if "p" in args.character_list:
            characterList = characterList + string.punctuation
        if "a" in args.character_list:
            characterList = string.ascii_uppercase + \
                string.ascii_lowercase + string.digits + string.punctuation
    if (len(args.starting_point) > args.max_length):
        print('\n\nThe starting point is longer than the max length\n')
        exit()

    # bruteforces all possible Urls
    for attempt in bruteforce(characterList, args.max_length):
        # if a starting point is given, it will start from that point
        if args.starting_point != characterList[0]:
            if attempt == args.starting_point:
                checkUrl(args.url + attempt,
                         args.directory_name, args.file_name, args.max_tries)
                # resets the starting point to the first character in the character list to ensure that the script will not stop and continue like normal
                args.starting_point = characterList[0]
        else:
            checkUrl(args.url + attempt, args.directory_name,
                     args.file_name, args.max_tries)

    print('\n\nThat was everything ;)\n')


if __name__ == "__main__":
    try:
        main(characterList)
    except KeyboardInterrupt:
        print('\n\n Script was cancelled\n')
        exit()
    except Exception as e:
        print('\n\n Script failed with error: ' + str(e) + '\n')
        traceback.print_exc()
        exit()
