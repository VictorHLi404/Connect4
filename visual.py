# handling all functions associated with displaying the board or other visual elements of the game

 #color values 
blue = "\033[1;34m"
white = "\033[0;37m"


def printBoard(board, playerOneColour, playerTwoColour): # iterate through 2d array and print frames, spaces, and player tokens as marked on the array

    #color values 
    blue = "\033[1;34m"
    white = "\033[0;37m"

    boardPrint = ""

    for t in range (22): # top frame
        boardPrint += (blue + "X ")
    boardPrint += "\n"

    for i in range (6): # main board
        for t in range (22): # dividing layer between chips
            boardPrint += (blue + "X ")
        boardPrint += "\n"    
        for t in range (2): # printing slots
            for j in range (7):
                boardPrint += (blue + "X ") 
                for c in range (2): # chips
                    if (board[i][j] == 1): # player 1's chips
                        boardPrint += (playerOneColour + "O ") 
                    if (board[i][j] == 2): #player 2's chips
                        boardPrint += (playerTwoColour + "O ") 
                    if (board[i][j] == 0): # empty
                        boardPrint += (white + "O ") 
            boardPrint += (blue + "X ")
            boardPrint += "\n" 

    for i in range (2): # bottom frame
        for t in range (22):
            boardPrint += (blue + "X ")
        boardPrint += "\n" 
    print(boardPrint, end = "\n")
    return

def printWin(gameBoard, playerOneColour, playerTwoColour, currentPlayerName, moveCounter): # function that prints current win
    printBoard(gameBoard, playerOneColour, playerTwoColour)
    print(currentPlayerName + " has won in", moveCounter, "moves!")
    return

def displayStats(gameResults, currentPage, currentPageLength): # function that prints list of results given an index range
    #print("To navigate the list of answers")

    index = "" # stores current entry
    gameMode = ""
    playerOneName = ""
    playerTwoName = ""
    winner = ""
    result = ""
    moveCounter = ""
    date = ""
    time = ""
    print("\n"+ " "*60 + "PAGE", currentPage+1) # page is zero indexed, so +1 for console output

    # currentpage in mainframe is 1-indexed, remove to work in this function

    for currentEntry in range (currentPageLength): # loop through current page till end and print results

        index = currentPage*10+currentEntry # currentPage*10 = beginning of current page
        gameMode = gameResults[index][0]
        playerOneName = gameResults[index][1]
        playerTwoName = gameResults[index][2]
        winner = gameResults[index][3]
        result = gameResults[index][4]
        moveCounter = gameResults[index][5]
        date = gameResults[index][6]
        time = gameResults[index][7]

        print(str(index+1)+".", end=" ") # index is 0-indexed, so +1 for display
        print(gameMode + " MATCH", end = " ")
        print("PLAYED BETWEEN PLAYER \"" + playerOneName + "\" AND PLAYER \"" + playerTwoName + "\"", end=" ")
        print("ON " + date + ", AT " + time, end= " ")
        print("   RESULT:", end=" ")

        if (result == "WIN"):
            print("PLAYER \"" + winner + "\" WON IN " + str(moveCounter) + " MOVES")
        else:
            print("TIE")
    
    return
