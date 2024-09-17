# file to handle simulating interfaces for both games and the database

from visual import *
from statisticsFunctions import *
from GameLogic import *
from inputHandler import *


# list of colors

white = "\033[1;37m"

#list of general variables for inputs and data handling

consoleChoice = ""
statsChoice = ""
gameResults = []
boardResults = []


def runGame(): # function to run and simulate the actual game
    
    #represent board as 2d array
    gameBoard = [[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0]]
    
    # variables for handling players

    currentPlayer = ""
    moveCounter = ""

    moveChoice = ""
    moveRow = ""
    moveColumn = ""

    # variables for handling type of game

    rows = ""
    columns = ""
    validRange = ""
    gameMode = ""

    result = ""

    gameMode = pickGamemode()

    # variables for handling name

    currentNames = []
    playerOneName = ""
    playerTwoName = ""

    # pick names for players, names cannot be the same

    playerOneName = pickName(currentNames, 1)
    currentNames.append(playerOneName)
    playerTwoName = pickName(currentNames, 2)
    currentNames.append(playerTwoName)

    # variables for picking colors, colors canno tbe the same

    playerOneColour = ""
    playerTwoColour = ""
    colours = colourPick(playerOneName, playerTwoName)

    playerOneColour = colours[0]
    playerTwoColour = colours[1]

    if gameMode == 1: # standard connect 4
        # set up game variables
        rows = 6
        columns = 7
        currentPlayer = 1
        validRange = ["1","2","3","4","5","6","7"]
        moveCounter = 0

        print('''You have picked the game of Connect 4. In this game, you and another player will take alternating turns dropping chips into a board.
                 The goal is to connect four of your own pieces vertically, horizontally, or diagonally while preventing your opponent from doing the same.
                 If neither player has successfully connected four pieces and the board is full, it is considered a tie.\n''')
        print("Let's begin! Indicate the column you want to drop your chip in using the numbers 1-7, representing the columns left to right.\n")
    
    elif gameMode == 2: # pop out
        # set up game variables
        rows = 6
        columns = 7
        currentPlayer = 1
        validRange = ["1","2","3","4","5","6","7"]
        moveCounter = 0

        print('''You have picked the game of Pop Out. In this game, you and another player will take alternating turns either dropping chips into a board\nor removing your own chips from the bottom of the board. The goal is to connect four of your own pieces vertically, horizontally, or diagonally while preventing your opponent from doing the same.\nIf neither player has successfully connected four pieces and the board is full, it is considered a tie.\n''')
        print("Let's begin! First indicate whether you want to POP or DROP a chip,\nand then indicate the column you want to do your action in using the numbers 1-7, representing the columns left to right.\n")   
        
    while (checkTie(rows, columns, gameBoard) == False): # while the game does not result in a tie
        printBoard(gameBoard, playerOneColour, playerTwoColour)

        moveData = gameInput(gameBoard, validRange, currentPlayer, gameMode, currentNames) # take in the move of the current player
        moveColumn = moveData[0]
        moveChoice = moveData[1]

        updateBoard(moveChoice, moveColumn, gameBoard, currentPlayer) #update board based on column and move chioice
        moveRow = determineDropRow(moveColumn, gameBoard) #check the newest toptop row if it was dropped
        moveCounter += 1

        if (moveChoice == "DROP"): # calculate if dropped piece results in win
            if (winCheck_drop(moveRow, moveColumn, gameBoard)): # if it does, print win and resulting stuff
                printWin(gameBoard, playerOneColour, playerTwoColour, currentNames[currentPlayer-1], moveCounter)
                result = currentPlayer
                break
        elif (moveChoice == "POP"): # calculate if a popped piece resulted in a win for a player, break game loop if win
            result = winCheck_pop(moveColumn, gameBoard)
            if (result == 1 or result == 2):
                printWin(gameBoard, playerOneColour, playerTwoColour, currentNames[currentPlayer-1], moveCounter)
                break
            elif (result == 3):
                printBoard(gameBoard, playerOneColour, playerTwoColour)
                print("It's a tie!")
                break

        currentPlayer = switchPlayer(currentPlayer) # if game is not won, swap active player and keep playing
    
    if (checkTie(rows, columns, gameBoard) == True): # setting result as tie when tie occurs
        result = 3
    
    print("\nReturning to main page...\n")


    # return result of game and endstate of board
    return [addEntry(gameMode, playerOneName, playerTwoName, currentNames[currentPlayer-1], result, moveCounter), gameBoard]

def runStats(gameResults, boardResults): # function to run database access functions CHANGE CHANGE CHANGE - POLL FOR VALID INPUT BEFORE REPRITING PAGE

    print("This is the database of previous games.")

    #variable to pick page analyze
    analyzeIndex = ""

    # variables to manage scrolling through pages

    totalEntryLength = len(gameResults)
    totalPageCount = totalEntryLength//10
    currentPage = 0
    currentPageLength = updatePageLength(totalEntryLength, currentPage)

    # default colors for p1 and p2 are red for p1 and yellow for p2

    red = '\033[0;31m'
    yellow = '\033[0;33m'

    displayStats(gameResults, currentPage, currentPageLength) # print current page of results
    print("Type ANALYZE to look at the end state of a game on the current page, type PREVIOUS or NEXT to advance to a different page, or type QUIT to return to the main menu.")
    statsChoice = statsInput(["ANALYZE", "PREVIOUS", "NEXT", "QUIT"], currentPage, totalPageCount, currentPageLength)

    while (statsChoice != "QUIT"):
        if (statsChoice == "ANALYZE"): # allow user to pick a specific index on the current page to look at how that game ended
            print("Pick which game you want to analyze by typing the index number on the left of the entries:", end = " ")
            analyzeIndex = analyzeInput(currentPage, currentPageLength) # return index of input to use to access data files and check for valid input

            print(analyzeIndex)
            print(white + "Printing the board of this game...\n")

            # names of players that played this game
            playerOneName = gameResults[analyzeIndex][1]
            playerTwoName = gameResults[analyzeIndex][2]

            print("\"" + playerOneName + "\"" +  " will be represented by red, while " + "\"" + playerTwoName + "\"" +  " will be represented by yellow.\n")
            printBoard(boardResults[analyzeIndex], red, yellow) # use index to print board from data list of previous boards
            print(white + "Board printed! Returning to main database...")

        elif (statsChoice == "PREVIOUS"): # scroll to previous page if not at the start
            currentPage -= 1
            currentPageLength = updatePageLength(totalEntryLength, currentPage)
        elif (statsChoice == "NEXT"): # scroll to next page if not at the end
            currentPage += 1
            currentPageLength = updatePageLength(totalEntryLength, currentPage)
        
        displayStats(gameResults, currentPage, currentPageLength)
        print("Type ANALYZE to look at the end state of a game on the current page, type PREVIOUS or NEXT to advance to a different page, or type QUIT to return to the main menu.")
        statsChoice = statsInput(["ANALYZE", "PREVIOUS", "NEXT", "QUIT"], currentPage, totalPageCount, currentPageLength)

    print("\nReturning to main page...\n")

