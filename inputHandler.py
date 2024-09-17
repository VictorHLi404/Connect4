# File to handle all of the game inputs, includes checking if inputs are valid and converting them to the respective data type needed

from GameLogic import *

# list of colors

blue = "\033[1;34m"
red = "\033[1;31m"
yellow = "\033[1;33m"
white = "\033[1;37m"

def printValidList(validChoiceList): # print list of valid inputs with commas and text
    listLength = len(validChoiceList)
    for i in range(listLength-1): # print list of valid inputs
        print(validChoiceList[i], end="")
        if i != listLength-2: # decide whether to end with period or comma
            print(",", end= " ")
        else:
            print(", or " + validChoiceList[listLength-1] + ".")

def consoleInput(validChoiceList): # handling all user inputs outside of the game, picking what they want to do
    choice = "" # store input
    choice = input().upper()
    while choice not in validChoiceList: # while not valid input, poll for another
        print("That is not a valid choice. Please enter", end=" ")
        printValidList(validChoiceList)
        choice = input().upper()
    return choice

def statsInput(validChoiceList, currentPage, totalPageCount, currentPageLength): # handling inputs regarding the database
    choice = "" # store input
    validInput = False
    while (validInput == False): #loop through several if statements to check if their choice of action is valid
        choice = input().upper()
        validInput = True
        if (choice not in validChoiceList): # if choice is not one of the valid options presented
            print("That is not a valid choice. Please enter", end=" ")
            printValidList(validChoiceList)
            validInput = False
        elif (choice == "PREVIOUS" and currentPage < 1):  # if choice is PREVIOUS and page is first page, cannot go back
            print("This is the first page. It is not possible to go to a previous page.")
            validInput = False
        elif (choice == "NEXT" and currentPage == totalPageCount):
            print("This is the last page. It is not possible to advance to another page.")
            validInput = False
        elif (choice == "ANALYZE" and currentPage*10+currentPageLength < 1): # if choice is ANALYZE and theres no entrys in the database
            print("There are no entries to analyze.")
            validInput = False
    return choice
        
def analyzeInput(currentPage, currentPageLength): # handling user inputs regarding picking games to analyze
    validIndexList = []
    for index in range(1, currentPageLength+1): # create string list of valid indices
        validIndexList.append(str((currentPage*10)+index)) # currentPag*10 = beginning point of current page indice
    choice = "" # store input
    choice = input()
    while (choice not in validIndexList): # poll until valid input
        print("This input is not one of the valid indexes on this current page. Please enter one of the indexes listed.")
        choice = input()
    return int(choice)-1


def pickName(currentNames, currentPlayer): # handle name selection given list of names already picked
    print("It is player " + str(currentPlayer)+"'s " + "turn to pick a name. Names can only contain letters.")
    print("Please enter your name:", end= " ")

    name = "" # stores currentName
    name = input()

    while (name in currentNames or name.isalpha() == False):

        if (name in currentNames):
            print("It seems that someone has already picked this name.")
        if (name.isalpha() == False):
            print("Names can only contain letters.")
        print("Please enter your name:", end= " ")
        name = input()

    return name

def colourPick(playerOneName, playerTwoName):
    colours = ['RED', 'GREEN', 'ORANGE', 'PINK', 'CYAN', 'PURPLE']
    ANSIcodes = ['\033[0;31m', '\033[0;32m', '\033[0;33m', '\033[0;35m', '\033[0;36m', '\033[1;35m']

    print('\nPlease pick a colour for ' + playerOneName + "'s chips.")

    print('Colours:')
    for i in range(6):
        print(ANSIcodes[i] + colours[i])
    
    selection = input('\033[0;37m' + '\n').upper()
    while selection not in colours:
        selection = input('Please pick a colour above and try again. \n').upper()

    colour_1 = ANSIcodes[colours.index(selection)]

    ANSIcodes.remove(colour_1)
    colours.remove(selection)

    print('\nPlease pick a colour for ' + playerTwoName + "'s chips.")

    print('Colours:')
    for i in range(5):
        print(ANSIcodes[i] + colours[i])
    
    selection = input('\033[0;37m' + '\n').upper()
    while selection not in colours:
        selection = input('Please pick a colour above and try again. \n').upper()
    
    colour_2 = ANSIcodes[colours.index(selection)]
    
    return [colour_1, colour_2]

def dropInput(gameBoard, validRange): # handling user input for dropping piece
    choice = "" # store input
    choice = input()
    while (checkValid_drop(choice, gameBoard, validRange) != True): # check if valid column given current gameboard
        choice = input()
    return int(choice) # cast to int to be used as index

def popInput(gameBoard, currentPlayer, validRange): # handling user input for popping piece
    choice = "" # store input
    choice = input()
    while (checkValid_pop(choice, gameBoard, currentPlayer, validRange) != True): # check if valid column given current player and gameboard
        choice = input()
    return int(choice) # cast to int to be used as index

def gameInput(gameBoard, validRange, currentPlayer, gameMode, currentNames): # handle selecting what kind of move along with column choice

    moveChoice = "" # stores what kind of move
    move = "" # stores column
    playerName = ""

    playerName = currentNames[currentPlayer-1]

    print(white + "It is "+ playerName + "'s turn.")

    if (gameMode == 1): # connect 4

        print("Which column would you like to drop your piece in?")
        moveChoice = "DROP" # only choice is to drop
        move = dropInput(gameBoard, validRange)-1 

    elif (gameMode == 2): # POP OUT

        if (checkPossiblePop(gameBoard, currentPlayer) == True): # check if there are any chips at the bottom
            moveChoice = pickAction()
        else:
            moveChoice = "DROP" # force drop if no valid pops

        if (moveChoice == "DROP"): # decide which column to drop in
            print(white + "Which column would you like to drop your piece in?")
            move = dropInput(gameBoard, validRange)-1

        elif (moveChoice == "POP"):
            print(white + "Which column would you like to pop your piece out of?")
            move = popInput(gameBoard, currentPlayer, validRange)-1

    return [move, moveChoice]
    #updateBoard("DROP", move, gameBoard, player)