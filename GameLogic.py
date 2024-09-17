# GAME LOGIC:
# Contains functions pertaining to running the game itself

# Picking a gamemode
def pickGamemode():
    
    print("\nPlease enter the number corresponding to the game mode you want to play.")
    print('1: Classic Connect 4')
    print('2: Pop Out')

    # Prompts user for chosen gamemode
    gamemode = input()

    # While input is not in valid range of 1-2, continues prompting for new input until valid
    while gamemode not in ["1", "2"]:
        gamemode = input('Please pick gamemode 1 or 2 to start a game:\n')
    
    # Returns number of selected gamemode
    return int(gamemode)

# Picking an action (Pop Out only)
def pickAction():  
    # Prompts for input
    action = input('Would you like to DROP or POP? \n\n').upper()

    # If input is not drop or pop, keeps prompting for new input until valid
    while action not in ['DROP', 'POP']:
        action = input('Please select either "DROP" or "POP". \n\n').upper()
    
    # Returns chosen action
    return action

# Checking if a drop is valid/possible
# Takes the inputed column (move), the current board arrangement, and the valid range of columns as parameters
def checkValid_drop(move, board, validRange):

    # First checks if the inputed column number is in the valid range of columns (1-7 in a normal 7x6 board)
    # If NOT in valid range, prints new prompt and returns false
    if move not in validRange:
        print('Please pick a column number between 1-7.')
        return False

    # Second checks if inputed column number has an empty space
    # Because board always fills from bottom to top (index 5-0), an unfilled column will always have an empty top space--so, only need to check top space for availability
    # If top space is NOT empty, prints new prompt and returns false
    if board[0][int(move) - 1] != 0:
        print('This column is full. Please pick another.')
        return False

    # If move passes both tests, it is a valid move and function returns true
    return True

# Checking if a pop is valid/possible
# Takes the inputed column (move), the current board arrangement, the player whose turn it is, and the valid range of columns as parameters
def checkValid_pop(move, board, currentPlayer, validRange):

    # First checks if the inputed column number is in the valid range of columns (1-7)
    # If NOT in valid range, prints new prompt and returns false
    if move not in validRange:
        print('Please pick a column number between 1-7.')
        return False

    # Second checks if inputed column number has a piece at the bottom to pop out
    # If bottom space is empty, prints new prompt and returns false
    if board[5][int(move) - 1] == 0:
        print('There are no chips to pop out in this column. Please pick another.')
        return False
    
    # Third checks if bottom piece in selected column belongs to player (players can only pop their own pieces)
    # If piece is not theirs, prints new prompt and returns false
    if board[5][int(move) - 1] != currentPlayer:
        print('You can only pop your own chips out. Please pick another column.')
        return False
    
    # If move passes all tests, function returns true
    return True

# Checking if there are any pieces to pop (and therefore if asking drop or pop is necessary)
# Takes current board arrangement and player whose turn it is as parameters
def checkPossiblePop(gameBoard, currentPlayer):

    # Variable determining whether popping is possible initialized as false 
    possiblePop = False

    # Loops through every column in the board and checks the bottom row
    # If a bottom piece is filled by the player's piece, there is a possible pop that can be performed
    # If loop completes and finds no bottom pieces belonging to the player, possiblePop remains false
    for i in range(len(gameBoard[0])):
        if gameBoard[len(gameBoard) - 1][i] == currentPlayer:
            possiblePop = True
            break
    
    return possiblePop

# Updates board after a move
# Takes action type (drop/pop), column of move, current board arrangement, and current player as parameters
def updateBoard(action, move, board, player):
    # If action is drop, checks the column of move from bottom to top for free space
    # Free space is turned into player's chip
    if action == 'DROP':
        for i in range(5, -1, -1):
            if board[i][move] == 0:
                board[i][move] = player
                break

    # If action is pop, goes through column of move from bottom to top and replaces each chip with the chip on top of it
    # If the changed chip becomes empty, it means there are no other chips to move down and the loops breaks
    else:
        for i in range(5, -1, -1):
            board[i][move] = board[i - 1][move]
            if board[i][move] == 0:
                break
            
    return

# Determines the row of a newly dropped chip
# Takes the move column and the current board arrangement as parameters
def determineDropRow(move, board):
    # Checks each row from top to bottom
    # Because chips fill from bottom to top, the top chip is always the most recently placed
    for i in range(len(board)):
        # If the space is filled by a chip, the row is returned
        if board[i][move] != 0:
            return i

# Checks the horizontal wincon for a specific chip
# Takes the row and column of the target chip and the current arrangement of the board
def winCheck_horizontal(row, column, board):
    # Counters for number of chips in a row initialized at 0
    chips = 0

    # Checks 3 spaces to the left and right of the target chip to see if it is part of a 4-in-a-row
    for i in range(-3, 4):
        # If there are less than 4 spaces left to check and there are still 0 chips in a row, there is no possibility of a 4-in-a-row and loop breaks
        if i >= 1 and chips == 0:
            break

        # If the space i spaces away from the target chip is not actually on the board, skips to next i value
        if column + i not in range(7):
            continue

        # If the space being checked is the same as the target chip, 1 is added to number of chips in a row
        if board[row][column + i] == board[row][column]:
            chips += 1
        # If the space being checked is NOT the same as the target chip, the counter is reset to 0
        else:
            chips = 0
    
        # If 4 chips are counted in a row, function returns true
        if chips == 4:
            return True
    
    # Otherwise, returns false
    return False

# Checks the vertical wincon for a specific chip
# Takes the row and column of target chip and current arrangement of board as parameters
def winCheck_vertical(row, column, board):
    # Only checks if the row of the newly placed chip is within the top 3 rows
        # Chips must be placed from bottom to top; newly placed chip must be the top of a potential 4-in-a-row
        # If newly placed chip is not at least 3rd column from the top, there is no possibility for a 4-in-a-row underneath it
    if row <= 2:
        # Checks the 4 pieces underneath it; if they are all equal to the target chip, there is a 4 in a row
        if board[row][column] == board[row + 1][column] == board[row + 2][column] == board[row + 3][column]:
            return True
    
    #Otherwise, function returns false
    return False

# Checks the diagonal wincon for a specific chip
# Takes the row and column of target chip and current arrangement of board as parameters
def winCheck_diagonal(row, column, board):
    # First checks for left-right down-up diagonal

    # There are only specific diagonals in which a 4-in-a-row is possible
    # If sum of row and column of dropped chip is within 3-8, it is in a diagonal where a 4-in-a-row is possible
    if row + column in range(3, 9):

        # Determines base row and column (bottom of the diagonal) to be checked
        if row + column <= 5:
            baseColumn = 0
            baseRow = row + column
        else:
            baseColumn = row + column - 5
            baseRow = 5

        # Counter for number of chips in a row initialized at 0
        chips = 0

        # Loop for while the space being checked is within the range of the board
        while baseRow in range(6) and baseColumn in range(7) :
            # If the row or column goes past 3, there are less than 4 spaces left
            # If the number of chips is still 0 with less than 4 spaces left to check, there is no possibility of a 4-in-a-row and loop breaks
            if (row < 3 or column > 3) and chips == 0:
                break

            # Checks if the space being checked has the target chip and adds 1 to chip counter if so
            if board[baseRow][baseColumn] == board[row][column]:
                chips += 1
            # Otherwise, counter is reset to 0
            else:
                chips = 0
            
            # If 4 chips are counted in a row, function returns true
            if chips == 4:
                return True
            
            # Otherwise, moves up the diagonal and checks the next space
            baseRow -= 1
            baseColumn += 1
    
    # Second checks for left-right up-down diagonal

    # Same concepts
    if column - row in range(-2, 4):

        if column - row >= 1:
            baseColumn = 6
            baseRow = 6 - (column - row)
        else:
            baseColumn = column - row + 5
            baseRow = 5
        
        chips = 0

        while baseRow in range(6) and baseColumn in range(7):
            if (row < 3 or column < 3) and chips == 0:
                break

            if board[baseRow][baseColumn] == board[row][column]:
                chips += 1
            else:
                chips = 0
            
            if chips == 4:
                return True
        
            baseRow -= 1
            baseColumn -= 1
    
    # If both tests do not find a 4-in-a-row, function returns false
    return False

# Checks the overall wincon for a dropped piece
# Takes row and column of dropped piece and current board as parameters
def winCheck_drop(row, column, board):
    if winCheck_vertical(row, column, board) or winCheck_horizontal(row, column, board) or winCheck_diagonal(row, column, board):
        return True

    return False

# Checks the overall wincon for a popped piece
# Takes the column and current board as parameters
def winCheck_pop(column, board):
    # Because a popped chip changes the orientation of multiple chips on top of it, there is the capacity for multiple wins
    # List of all win occurences is initialized as 0
    wins = []

    # Checks all rows from bottom to top, except the top as at least one space must be empty after a pop
    for i in range(5, 0, -1):

        # If the checked space is empty, there are no more chips to check on top and loop breaks
        if board[i][column] == 0:
            break
        
        # Otherwise, checks the horizontal and diagonal wincons for every moved chip
        # Vertical does not need to be checked as vertical orientation of popped column does not change
        if winCheck_horizontal(i, column, board) or winCheck_diagonal(i, column, board):
            # If a wincon is fulfilled, the player that has a 4-in-a-row is added to list of wins
            wins.append(board[i][column])
    
    # If number of unique elements in list of wins is 1, only one player has decisively won with a 4-in-a-row and function returns the player number
    if len(set(wins)) == 1:
        return wins[0]
    # Otherwise if there are 2 unique elements in list of wins, both players have won and function returns 3 representing a tie
    elif len(set(wins)) == 2:
        return 3
    # Otherwise (no wins), no one has won and function returns 0
    else:
        return 0

# Checks if the board is filled and if a tie has occurred
# Takes number of rows and columns and current board arrangement as parameters
def checkTie(rows, columns, board): 
    # Loops through all rows and all columns in each row and checks for an empty space
    # If empty space is found, there is not a tie and function returns false
    for i in range (rows):
        for j in range(columns):
            if board[i][j] == 0:
                return False
    
    # If every space is looped through and no empty space is found, board is entirely filled and a tie has occurred
    return True

# Manages turn switches and tracks whose turn it is
# Takes the current player as a parameter
def switchPlayer(currentPlayer):
    # If current player is player 1, next player is changed to player 2
    if currentPlayer == 1:
        currentPlayer = 2
    # Vice versa
    else:
        currentPlayer = 1
    
    # Returns next player
    return currentPlayer