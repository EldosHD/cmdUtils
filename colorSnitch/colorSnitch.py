#!/usr/bin/python3
import sys
import re
import argparse
from os import isatty
from subprocess import check_output

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def calcToDoPrio(inputString: str):
    return str(inputString.count('O') - 1)


parser = argparse.ArgumentParser(description='TODO: describe that')

parser.add_argument('-r','--run', action='store_true', default=False, help='run "snitch list" and use it as input')
parser.add_argument('--count', action='store_true', default=False, help='Print the priority')


args = parser.parse_args()

snitchOutput = []

if isatty(sys.stdin.fileno()):
    # the script doesnt get input from a pipe
    if args.run == True:
        # run script
        snitchOutput = check_output(['snitch','list'],text=True).split('\n')
        snitchOutput.pop() # last element is empty for some reason
    else:
        print('Use the -r option to run snitch list, or pipe the output of snitch list to this program')
        sys.exit()
else:
    # the script gets input
    for line in sys.stdin:
        snitchOutput.append(line.replace('\n',''))

for line in snitchOutput:
    toDo = line.split(':')
    
    fileName = color.CYAN + toDo[0] + color.END
    lineNumber = color.RED + toDo[1] + color.END

    # remove filename and linenumber from that list
    toDo.pop(0)
    toDo.pop(0)

    for index, word in enumerate(toDo):
        if re.search('TODOOO+',word):
            if args.count == True:
                newWord = color.RED + calcToDoPrio(word) + color.END
            else:
                newWord = re.search('TODOOO+', word)
                newWord = color.RED + newWord.group() + color.END
            toDo[index] = newWord
            break
        elif re.search('TODOO',word):
            if args.count == True:
                newWord = color.YELLOW + calcToDoPrio(word) + color.END
            else:
                newWord = re.search('TODOO', word)
                newWord = color.YELLOW + newWord.group() + color.END
            toDo[index] = newWord
            break
        elif re.search('TODO', word):
            if args.count == True:
                newWord = color.GREEN + calcToDoPrio(word) + color.END
            else:
                newWord = re.search('TODO', word)
                newWord = color.GREEN + newWord.group() + color.END
            toDo[index] = newWord
            break
    # stitch the colored todo str back together
    line = ':'.join(toDo)
    print(fileName + ':' + lineNumber + ':' + line)

    
# TODOO: only supports the word "TODO" currently. should support others too! <--------------------- this line is buggy
# TODOO: remove unnessesary whitespace from each line
# TODOO: make the program format snitch nicely
