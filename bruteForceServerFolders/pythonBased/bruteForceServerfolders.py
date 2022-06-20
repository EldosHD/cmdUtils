#!/usr/bin/python3
import requests
import os
from itertools import chain, product
import string
import argparse
import time


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


def checkUrl(url, dName, fName):
    # so that the variable can be used in the function, since it is outside the scope
    global urlsFound
    r = requests.get(url)
    # r.status_code --> Http responsecode (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
    if (r.status_code >= 200 and r.status_code <= 299):
        urlsFound = urlsFound + 1
        print(bcolors.OKGREEN + 'Found Url: ' + url + bcolors.ENDC)
        # opens File/creates it if it doesnt exist already and writes URL in it
        f = open(dName + '/' + fName, 'at')
        f.write(url + '\n')
        f.close
    else:
        print('checking Url: ' + url + ' -- Did not work.' +
              ' Urls found: ' + str(urlsFound))


def main(characterList):
    # automaticly creates a help message! Thats FUCKING AWESOME!!!
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory-name',
                        help=directoryNameHelp, default=directoryName)
    parser.add_argument('-f', '--file-name',
                        help=fileNameHelp, default=fileName)
    parser.add_argument('-m', '--max-length',
                        help=maxLengthHelp, type=int, default=maxLength)
    parser.add_argument('-s', '--starting-point',
                        help='The starting point for the brute force attempt. The default is the first character in the character list.', type=str, default=characterList[0])
    parser.add_argument('url', help=urlHelp)
    parser.add_argument('-c', '--character-list',
                        help=characterListHelp, default=characterList)
    parser.add_argument('-n', '--no-color', help=ColorHelp,
                        default=False, action='store_true')

    args = parser.parse_args()

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
                checkUrl(args.url + attempt, args.directory_name, args.file_name)
                # resets the starting point to the first character in the character list to ensure that the script will not stop and continue like normal
                args.starting_point = characterList[0]
        else:
            checkUrl(args.url + attempt, args.directory_name, args.file_name)

    print('\n\nThat was everything ;)\n')


if __name__ == "__main__":
    try:
        main(characterList)
    except KeyboardInterrupt:
        print('\n\n Script was cancelled\n')
        exit()
    except Exception as e:
        print('\n\n Script failed with error: ' + str(e) + '\n')
        exit()
