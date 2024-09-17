
# Main file used for running the game: Player should use this file


from statisticsFunctions import *
from RunAction import *
from inputHandler import *


#--------------------------------------------------- BEGINNING OF MAINFRAME ------------------------------------------------------
    
gameResults = readStats()
boardResults = readBoards()

print(white + "Welcome to the game of Connect 4!")
print(white + "This edition offers several variations of the original Connect 4, in a player vs. player format.")
print(white + "It also stores the results of previous games and overall usage statistics.")
print(white + "\nLet's get started! Do you want to PLAY a new game, or review the STATS of all games played? You can also QUIT to exit the program.")

consoleChoice = consoleInput(["PLAY", "STATS", "QUIT"]) # poll for valid input

while (consoleChoice != "QUIT"): # loop until player inputs quit

    gameData = "" # variable to store currrent game data
    lastMatch = "" # variable store stats of last match
    lastBoard = "" # variable to store last board
    
    writeData(gameResults, boardResults) # constantly update text files after each action

    if (consoleChoice == "PLAY"):

        gameData = runGame() # simulate game, store game results in gameData

        lastMatch = gameData[0]
        lastBoard = gameData[1]
        gameResults.insert(0, lastMatch) # insert game and board data into running data list
        boardResults.insert(0, lastBoard)

    if (consoleChoice == "STATS"):
        
        runStats(gameResults, boardResults) # run database viewer given current data lists

    # after action is done, reprint statements
    print(white + "Do you want to PLAY a new game, or review the STATS of all games played? You can also QUIT to exit the program.")
    consoleChoice = consoleInput(["PLAY", "STATS", "QUIT"])

writeData(gameResults, boardResults) # update text files before shutting down
print("\nThank you for playing!")