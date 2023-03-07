import math
import random

# Check if the move is valid
def isValidMove(board, move):
    if (move[0] >= 0 or move[0] < 19 or move[1] >= 0 or move[1] < 19) and board[move[0]][move[1]] == '.':
        return True
    else:
        return False

# Check if there are two consecutive stones of the same colour
# TODO: Do this to check the number of captures
# TODO: Preventing captures
# TODO: Check all directions and then return DONE
def isTwoConsecutive(board, move, stone):
    captureCount = 0
    if stone == 'b':
        opStone = 'w'
    else:
        opStone = 'b'
    # Check for horizontal
    # Check if opponent's stones are captured
    # TODO: Can I skip if my stones are getting captured? Also can I udpated the scores like this? 
    # ANS: Count the number of bCaptures and wCaptures and send the updated ones to evalutate function?
    # This checks if my stones are captured
    if (move[1] > 2 and 
        board[move[0]][move[1]-1] == stone and
        board[move[0]][move[1]-2] == stone and
        board[move[0]][move[1]-3] == opStone):
        captureCount += 1

    if (move[1] < 16 and
        board[move[0]][move[1]+1] == stone and
        board[move[0]][move[1]+2] == stone and
        board[move[0]][move[1]+3] == opStone):
        captureCount += 1
    # Check for vertical
    if (move[0] > 2 and
        board[move[0]-1][move[1]] == stone and
        board[move[0]-2][move[1]] == stone and
        board[move[0]-3][move[1]] == opStone):
        captureCount += 1
    
    if (move[0] < 16 and
        board[move[0]+1][move[1]] == stone and
        board[move[0]+2][move[1]] == stone and
        board[move[0]+3][move[1]] == opStone):
        captureCount += 1
    
    # Check for diagonal \
    if (move[0] > 2 and move[1] > 2 and
        board[move[0]-1][move[1]-1] == stone and
        board[move[0]-2][move[1]-2] == stone and
        board[move[0]-3][move[1]-3] == opStone):
        captureCount += 1
    
    if (move[0] < 16 and move[1] < 16 and
        board[move[0]+1][move[1]+1] == stone and
        board[move[0]+2][move[1]+2] == stone and
        board[move[0]+3][move[1]+3] == opStone):
        captureCount += 1
    
    # Check for diagonal /
    if (move[0] > 2 and move[1] < 16 and
        board[move[0]-1][move[1]+1] == stone and
        board[move[0]-2][move[1]+2] == stone and
        board[move[0]-3][move[1]+3] == opStone):
        captureCount += 1
    
    if (move[0] < 16 and move[1] > 2 and
        board[move[0]+1][move[1]-1] == stone and
        board[move[0]+2][move[1]-2] == stone and
        board[move[0]+3][move[1]-3] == opStone):
        captureCount += 1

    if captureCount > 0:
        return True
    else:
        return False  

# Check winner
# TODO: Check if I need to return the winner
def gameOver(board):
    # Check if there are 10 or more captures
    if captures[0] >= 10 or captures[1] >= 10:
        return True
    # Check if there are 5 consecutive stones of the same colour

    # Check for horizontal
    for i in range(19):
        for j in range(15):
            if (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4] == myStone) or (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4] == opponentStone):
                return True
    # Check for vertical
    for j in range(19):
        for i in range(15):
            if (board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == board[i+4][j] == myStone) or (board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == board[i+4][j] == opponentStone):
                return True
    # Check for diagonal \
    for i in range(15):
        for j in range(15):
            if (board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] == myStone) or (board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] == opponentStone):
                return True
    # Check for diagonal /
    for i in range(15):
        for j in range(4, 19):
            if (board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4] == myStone) or (board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4] == opponentStone):
                return True

    else:
        return False
    
# Get possible moves
# TODO: For white's turns, first => in the middle, second => random move leaving 3 intersections DONE
def getPossibleMoves(board):
    wCount = sum(x.count('w') for x in board)
    bCount = sum(board.count('b') for x in board)
    possibleMoves = []
    print(wCount, bCount)

    if wCount == 0:
        possibleMoves.append([9, 9])
        return possibleMoves
    
    elif wCount == 1 and bCount == 1:
        row = 9
        col = 9
        while not isValidMove(board, [row, col]):
            row = random.randint(6, 12)
            col = random.randint(6, 12)
        possibleMoves.append([row, col])
        return possibleMoves
    
    if bCount == 0:
        row = 9
        col = 9
        while not isValidMove(board, [row, col]):
            row = random.randint(8, 10)
            col = random.randint(8, 10)
        possibleMoves.append([row, col])
        return possibleMoves
    
    for i in range(19):
        for j in range(19):
            if isValidMove(board, [i, j]):
                possibleMoves.append([i, j])
    return possibleMoves

# Evaluate board
def evaluateBoard(board, wCapture, bCapture, stone, move):
    count = 1
    row = move[0]
    col = move[1]
    diff = 0

    if stone == 'w':
        diff = bCapture - wCapture
    else:
        diff = wCapture - bCapture

    # Check horizontal
    i = col - 1
    while i >= 0 and board[row][i] == stone:
        count += 1
        i -= 1
    i = col + 1
    while i < len(board[row]) and board[row][i] == stone:
        count += 1
        i += 1

    # Check vertical
    j = row - 1
    while j >= 0 and board[j][col] == stone:
        count += 1
        j -= 1
    j = row + 1
    while j < len(board) and board[j][col] == stone:
        count += 1
        j += 1

    # Check diagonal \
    i, j = col - 1, row - 1
    while i >= 0 and j >= 0 and board[j][i] == stone:
        count += 1
        i -= 1
        j -= 1
    i, j = col + 1, row + 1
    while i < len(board[row]) and j < len(board) and board[j][i] == stone:
        count += 1
        i += 1
        j += 1

    # Check diagonal /
    i, j = col + 1, row - 1
    while i < len(board[row]) and j >= 0 and board[j][i] == stone:
        count += 1
        i += 1
        j -= 1
    i, j = col - 1, row + 1
    while i >= 0 and j < len(board) and board[j][i] == stone:
        count += 1
        i -= 1
        j += 1

    return ((100 * count / 5) + diff)


# Alpha-Beta Pruning
def alphaBetaPruning(board, depth, alpha, beta, myStone, opponentStone, maximizingPlayer, prevMove):
    if depth == 0 or gameOver(board):
        print(prevMove)
        return evaluateBoard(board, captures[0], captures[1], myStone, prevMove),prevMove
    
    if maximizingPlayer:
        maxValue = -math.inf
        bestMove = None
        for move in getPossibleMoves(board):
            board[move[0]][move[1]] = myStone 
            # TODO: What if here is a capture?
            value, _ = alphaBetaPruning(board, depth - 1, alpha, beta, opponentStone, myStone, False, move)
            board[move[0]][move[1]] = '.'
            maxValue = max(maxValue, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
            if value >= maxValue:
                bestMove = move
        return maxValue, bestMove
    
    else:
        minValue = math.inf
        bestMove = None
        for move in getPossibleMoves(board):
            board[move[0]][move[1]] = opponentStone
            value, _ = alphaBetaPruning(board, depth - 1, alpha, beta, opponentStone, myStone, True, move)
            board[move[0]][move[1]] = '.'
            minValue = min(minValue, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
            if value <= minValue:
                bestMove = move
        return minValue, bestMove

if __name__ == "__main__":
    # Read input file
    file = open('input.txt', 'r')
    Lines = file.readlines()

    # Store the data in variables
    input = [line.strip() for line in Lines]

    # Get which colour I play
    myColour = input[0]
    print(myColour)

    timeRemaining = float(input[1])
    print(timeRemaining)

    # Captures [White, Black]
    stringOfCaptures = input[2].split(',')
    captures = [int(i) for i in stringOfCaptures]
    print(captures)

    # Board
    board = [[i for i in col] for col in input[3: 22]]
    print(board)

    # Stone
    if myColour == 'BLACK':
        myStone = 'b'
        opponentStone = 'w'
    else:
        myStone = 'w'
        opponentStone = 'b'

    # TODO: Caliberate depth
    score, move = alphaBetaPruning(board, 1, -math.inf, math.inf, myStone, opponentStone, True, None)
    print(score, move)
    row = 19 - move[0]
    if move[1] < 8:
        col = chr(ord('A') + move[1])
    else:
        col = chr(ord('A') + move[1] + 1)
    output = str(row) + col

    # TODO: Write to output file with the move in proper format DONE
    file = open('output.txt', 'w')
    file.write(output)
