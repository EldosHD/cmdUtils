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

directoryName = 'BruteForceResults'
directoryNameHelp = 'Uses the specified directory to store the results of the brute force attempt. The default name is "Brute Force Results".'
fileName = 'Url_Finder' + getCurrentTime() + '.txt'
fileNameHelp = 'Uses the specified file to store the results of the brute force attempt. The default name is Url_theCurrenTime.txt.'
maxLength = 4
maxLengthHelp = 'Uses the specified integer as the maximum length of the bute force attempt. The maxLength is 4 by default.'
url = ''
urlHelp = 'Uses the specified Url as the base for the brute force attempt. This must be a complete link like https://www.google.com/. The https:// must be included.'
characterList = string.ascii_letters
characterListHelp = 'The default list are the upper and lowercase ascii letters. If you want to specify your own character List you can combine the following: l for lowercase, u for uppercase, d for digits, p for punktuation or a for all of them.'
Color = False
ColorHelp = 'This is false by default. Use the -n flag to disable it. The script will use color codes (https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal) to dye the output in case an Url is found. This only works with an registry Tweak on Windows.'

def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(1, maxlength + 1)))

def checkIfFolderExists(folder):
    if os.path.exists(folder) == False:
        os.mkdir(folder)

def checkUrl(url,dName,fName):
    r = requests.get(url)
    if (r.status_code >= 200 and r.status_code <= 299):             #r.status_code --> Http responsecode (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
        print(bcolors.OKGREEN + '----------found Url: ' + url + '----------' + bcolors.ENDC)
        f = open(dName + '/' + fName, 'at')            #opens File/creates it if it doesnt exist already and writes URL in it
        f.write(url + '\n')
        f.close
    else:
        print('checking Url: ' + url +' -- Did not work.')
def main(characterList):
    parser = argparse.ArgumentParser()      #automaticly creates a help message! Thats FUCKING AWESOME!!!
    parser.add_argument('-d','--directory-name', help=directoryNameHelp, default=directoryName)
    parser.add_argument('-f','--file-name', help=fileNameHelp, default=fileName)
    parser.add_argument('-m','--max-length', help=maxLengthHelp, type=int, default=maxLength)
    parser.add_argument('url',help=urlHelp)
    parser.add_argument('-c', '--character-list', help=characterListHelp, default=characterList)
    parser.add_argument('--color-mode',help=ColorHelp, default=Color, action='store_true')

    args = parser.parse_args()
    print('Base Url: ' + args.url)
    
    checkIfFolderExists(args.directory_name) #checks if the resultsfolder exists

    if args.color_mode == False:
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
            characterList = string.ascii_uppercase + string.ascii_lowercase +string.digits + string.punctuation

    for attempt in bruteforce(characterList, args.max_length):     #bruteforces all possible Urls
        url = args.url + attempt
        checkUrl(url,args.directory_name, args.file_name)

    print('\n\nThat was everything ;)\n')


if __name__ == "__main__":
    main(characterList)


