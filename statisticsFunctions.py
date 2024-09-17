#save each game as a single line
#format: gamemode, player 1 name, player 2 name, player that won / tie, number of moves

import datetime

def addEntry(gameMode, playerOneName, playerTwoName, winner, result, moveCounter): # file to add 
    newEntry = [] # list to store current entry results
    gameModeList = ["CONNECT-4", "POP-OUT"]

    newEntry.append(gameModeList[gameMode-1]) 
    newEntry.append(playerOneName)
    newEntry.append(playerTwoName)

    if (result == 3): #append result and winner of game depending on result
        newEntry.append("N/A")
        newEntry.append("TIE")
    else:
        newEntry.append(winner)
        newEntry.append("WIN")

    newEntry.append(moveCounter)

    now = datetime.datetime.now() # adding date and time to game
    date = now.date()
    time = now.strftime("%H:%M:%S")
    
    newEntry.append(str(date))
    newEntry.append(str(time))

    return newEntry

def readStats(): # reading text file that contains previous games
    data = [] # to store all text data
    dataLength = ""
    with open("stats.txt", "r+") as file:
        data = file.readlines() # split text file into list, each item represents one game result
        dataLength = len(data)
        file.close()
    for i in range(dataLength): 
        data[i] = data[i].split() # split each game result into distinct parts (p1, p2, winner, etc)
    return data

def readBoards(): # reading textfile that contains previous endstates of boards
    data = [] # to store all text data
    dataLength = ""
    entryLength = 7 # board is 7 pieces long
    entryHeight = 6 # board is 6 pieces long
    currentBoard = [] # variables for breaking down text data
    currentRow = []
    currentColumn = ""

    with open("boardData.txt", "r+") as file:
        data = file.read().split("\n\n") # text file seperates boards with \n\n, break down into list that contains different boards
        if (data == [""]): # handle weird exception that occurs when document is blank
            data = []
        dataLength = len(data)
        file.close()
    for entry in range(dataLength): # loop through list that contains different boards
        currentBoard = data[entry].split("\n") # break down individual board into rows
        for row in range(entryHeight):
            currentRow = []
            for column in range(entryLength):
                currentColumn = int(currentBoard[row][column]) # convert text into int of current row and column
                currentRow.append(currentColumn)
            currentBoard[row] = currentRow # replace text board with list of row
        data[entry] = currentBoard # replace text board in list with 2d array board
    return data

def writeData(gameResults, boardResults): # writiing both game results and endstate boards to respective text files
    entryLength = "" # variable representing length of list of entry
    entryListLength = "" # variable representing number of entries
    with open("stats.txt", "w+") as file:
        entryLength = 8
        entryListLength = len(gameResults)
        for entry in range(entryListLength):
            for entryItem in range(entryLength):
                file.write(str(gameResults[entry][entryItem]) + " ") # write each entry item
            file.write("\n") # seperate each entry with new line
        file.close()

    entryHeight = "" # variable used for treating 2d array in text
    with open("boardData.txt", "w+") as file:
        entryLength = 7
        entryHeight = 6
        entryListLength = len(boardResults)
        for entry in range(entryListLength):
            for row in range(entryHeight):
                for column in range(entryLength):
                    file.write(str(boardResults[entry][row][column])) # write each board position to text file
                if (row != entryHeight-1): # if row is not the last one, write a new line to seperate from next entry
                    file.write("\n") 
            if (entry != entryListLength-1): # if entry is not the last one, write two new lines to seperate from next one
                file.write("\n\n")
        file.close()

    return

def updatePageLength(totalEntryLength, currentPage): # change page length depending on remaining results in database
    currentPageLength = ""
    if (totalEntryLength - (currentPage+1)*10 < 0): # if this page is the last page, then return however many are left
        currentPageLength = totalEntryLength - (currentPage)*10
    else: # otherwise return 10
        currentPageLength = 10
    return currentPageLength
