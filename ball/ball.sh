#!/bin/bash

sleepTime=0.05
spaceNumber=10
spaceString=' '
onlySpace=' '
currentLevel=0

printFunction() {

    # check so recursion doesnt go on forever
    if [[ $currentLevel -eq $spaceNumber ]]
    then
	# to display the tip
	echo -ne "${1}0 \r"
	# extra sleep so the animation doesnt stutter
	sleep $sleepTime
	return
    else
	currentLevel=${currentLevel}+1
    fi
       
    echo -ne "${1}0 \r"
    sleep $sleepTime

    # call the function recursivly
    printFunction "${1}${onlySpace}"

    echo -ne "${1}0 \r"
    sleep $sleepTime
}


printHelp() {
    echo "This program displays a ball bouncing horizontally!"
    echo "Arguments:"
    echo "  -s TIME   | waittime between two frames in seconds. (Default: 0.05s)"
    echo "  -n NUMBER | width of the screen. (Default: 10)"
    echo "  -h        | displays this help."
    exit 
}


# get arguments
while getopts ":s:n:" o; do
    case "${o}" in
	s)
	    s=${OPTARG}
	    # check if value is a number
	    re='^[0-9]+([.][0-9]+)?$'
	    if ! [[ $s =~ $re ]] ; then
		echo "error: The value set for -s is not a number" >&2; exit 1
	    fi
	    sleepTime=$s
	    ;;
	n)
	    n=${OPTARG}
	    # check if value is an integer
	    re='^[0-9]+$'
	    if ! [[ $n =~ $re ]] ; then
		echo "error: The value set for -n is not an integer" >&2; exit 1
	    fi
	    spaceNumber=$n
	    ;;
	*)
	    printHelp
	    ;;
    esac
done

# check if values for flags are numbers



# Starting "frame"
echo -e "\n\n\n\n\n\n\n\n\n"
echo -ne "0 \r"
sleep $sleepTime

# Infinite Loop
while true
do
    printFunction "$spaceString"

    # extra "0" so the ball touches the wall
    echo -ne "0 \r"
    sleep $sleepTime
    #reset currentlvl for loop
    currentLevel=0
done
