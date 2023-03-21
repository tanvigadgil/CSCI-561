import math
import random

# Check if the move is valid
def isValidMove(board, move):
    if (move[0] >= 0 and move[0] < 19 and move[1] >= 0 and move[1] < 19) and board[move[0]][move[1]] == '.':
        return True
    else:
        return False

# Check if there are two consecutive stones of the same colour
# TODO: Do this to check the number of captures DONE
# TODO: Check all directions and then return DONE
def checkCaptures(board, move, myStone):
    captured = 0
    stonesCapturedAt = []

    if myStone == 'b':
        opStone = 'w'
    else:
        opStone = 'b'

    # Check if opponent's stones are captured
    # TODO: Can I skip if my stones are getting captured? Also can I udpate the scores like this? 
    # ANS: Count the number of bCaptures and wCaptures and send the updated ones to evalutate function?

    # Check for horizontal
    # I Captured
    if (move[1] > 2 and 
        board[move[0]][move[1]-1] == opStone and
        board[move[0]][move[1]-2] == opStone and
        board[move[0]][move[1]-3] == myStone):
        captured += 2
        stonesCapturedAt.append([move[0], move[1]-1])
        stonesCapturedAt.append([move[0], move[1]-2])

    if (move[1] < 16 and
        board[move[0]][move[1]+1] == opStone and
        board[move[0]][move[1]+2] == opStone and
        board[move[0]][move[1]+3] == myStone):
        captured += 2
        stonesCapturedAt.append([move[0], move[1]+1])
        stonesCapturedAt.append([move[0], move[1]+2])

    # Check for vertical
    # I Captured
    if (move[0] > 2 and
        board[move[0]-1][move[1]] == opStone and
        board[move[0]-2][move[1]] == opStone and
        board[move[0]-3][move[1]] == myStone):
        captured += 2
        stonesCapturedAt.append([move[0]-1, move[1]])
        stonesCapturedAt.append([move[0]-2, move[1]])
    
    if (move[0] < 16 and
        board[move[0]+1][move[1]] == opStone and
        board[move[0]+2][move[1]] == opStone and
        board[move[0]+3][move[1]] == myStone):
        captured += 2
        stonesCapturedAt.append([move[0]+1, move[1]])
        stonesCapturedAt.append([move[0]+2, move[1]])
    
    # Check for diagonal \
    # I Captured
    if (move[0] > 2 and move[1] > 2 and
        board[move[0]-1][move[1]-1] == opStone and
        board[move[0]-2][move[1]-2] == opStone and
        board[move[0]-3][move[1]-3] == myStone):
        captured += 2
        stonesCapturedAt.append([move[0]-1, move[1]-1])
        stonesCapturedAt.append([move[0]-2, move[1]-2])
    
    if (move[0] < 16 and move[1] < 16 and
        board[move[0]+1][move[1]+1] == opStone and
        board[move[0]+2][move[1]+2] == opStone and
        board[move[0]+3][move[1]+3] == myStone):
        captured += 2
        stonesCapturedAt.append([move[0]+1, move[1]+1])
        stonesCapturedAt.append([move[0]+2, move[1]+2])
    
    # Check for diagonal /
    # I Captured
    if (move[0] > 2 and move[1] < 16 and
        board[move[0]-1][move[1]+1] == opStone and
        board[move[0]-2][move[1]+2] == opStone and
        board[move[0]-3][move[1]+3] == myStone):
        captured += 2
        stonesCapturedAt.append([move[0]-1, move[1]+1])
        stonesCapturedAt.append([move[0]-2, move[1]+2])
    
    if (move[0] < 16 and move[1] > 2 and
        board[move[0]+1][move[1]-1] == opStone and
        board[move[0]+2][move[1]-2] == opStone and
        board[move[0]+3][move[1]-3] == myStone):
        captured += 2
        stonesCapturedAt.append([move[0]+1, move[1]-1])
        stonesCapturedAt.append([move[0]+2, move[1]-2])

    if captured > 0:
        return True, captured, stonesCapturedAt
    else:
        return False, captured, stonesCapturedAt 

# Check winner
# TODO: Check if I need to return the winner Nope DONE
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
    bCount = sum(x.count('b') for x in board)
    possibleMoves = []

    if wCount == 0 and bCount == 0:
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
# TODO: Add scores for capturing stones DONE
# TODO: Add score for game over DONE
def evaluateBoard(board, myCaptures, opCaptures, stone, move):
    if stone == 'w':
        opStone = 'b'
    else:
        opStone = 'w'

    myCount = 1
    hCount = 0
    vCount = 0
    d1Count = 0
    d2Count = 0
    opCount = 0
    row = move[0]
    col = move[1]
    diff = myCaptures - opCaptures

    # Check if game over
    if gameOver(board):
        return 1000000

    # Check horizontal
    # Check for my stones
    i = col - 1
    while i >= 0 and board[row][i] == stone:
        hCount += 1
        i -= 1
    i = col + 1
    while i < len(board[row]) and board[row][i] == stone:
        hCount += 1
        i += 1

    # Check for opponent's stones
    i = col - 1
    while i >= 0 and board[row][i] == opStone:
        opCount += 1
        i -= 1
    i = col + 1
    while i < len(board[row]) and board[row][i] == opStone:
        opCount += 1
        i += 1

    # Check vertical
    # Check for my stones
    j = row - 1
    while j >= 0 and board[j][col] == stone:
        vCount += 1
        j -= 1
    j = row + 1
    while j < len(board) and board[j][col] == stone:
        vCount += 1
        j += 1

    # Check for opponent's stones
    j = row - 1
    while j >= 0 and board[j][col] == opStone:
        opCount += 1
        j -= 1
    j = row + 1
    while j < len(board) and board[j][col] == opStone:
        opCount += 1
        j += 1

    # Check diagonal \
    # Check for my stones
    i, j = col - 1, row - 1
    while i >= 0 and j >= 0 and board[j][i] == stone:
        d1Count += 1
        i -= 1
        j -= 1
    i, j = col + 1, row + 1
    while i < len(board[row]) and j < len(board) and board[j][i] == stone:
        d1Count += 1
        i += 1
        j += 1

    # Check for opponent's stones
    i, j = col - 1, row - 1
    while i >= 0 and j >= 0 and board[j][i] == opStone:
        opCount += 1
        i -= 1
        j -= 1
    i, j = col + 1, row + 1
    while i < len(board[row]) and j < len(board) and board[j][i] == opStone:
        opCount += 1
        i += 1
        j += 1

    # Check diagonal /
    # Check for my stones
    i, j = col + 1, row - 1
    while i < len(board[row]) and j >= 0 and board[j][i] == stone:
        d2Count += 1
        i += 1
        j -= 1
    i, j = col - 1, row + 1
    while i >= 0 and j < len(board) and board[j][i] == stone:
        d2Count += 1
        i -= 1
        j += 1

    # Check for opponent's stones
    i, j = col + 1, row - 1
    while i < len(board[row]) and j >= 0 and board[j][i] == opStone:
        opCount += 1
        i += 1
        j -= 1
    i, j = col - 1, row + 1
    while i >= 0 and j < len(board) and board[j][i] == opStone:
        opCount += 1
        i -= 1
        j += 1

    if (hCount + vCount + d1Count + d2Count) >= 4:
        myCount += hCount + vCount + d1Count + d2Count
    else:
        myCount += max(hCount, vCount, d1Count, d2Count)

    return ((200 * myCount / 5) + (100 * opCount / 5) + 1000 * diff)


# Alpha-Beta Pruning
def alphaBetaPruning(board, depth, alpha, beta, maximizingPlayer, prevMove, myCaptures, opCaptures):
    if depth == 0 or gameOver(board):
        if maximizingPlayer:
            player = opponentStone
        else:
            player = myStone
        return evaluateBoard(board, myCaptures, opCaptures, player, prevMove), prevMove
    
    if maximizingPlayer:
        maxValue = -math.inf
        bestMove = None

        for move in getPossibleMoves(board):
            board[move[0]][move[1]] = myStone 
            # TODO: What if there is a capture here?
            isCaptured, iCaptured, stonesCapturedAt = checkCaptures(board, move, myStone)
            if isCaptured:
                capturedStone = board[stonesCapturedAt[0][0]][stonesCapturedAt[0][1]]
                for place in stonesCapturedAt:
                    board[place[0]][place[1]] = '.'
            value, _ = alphaBetaPruning(board, depth - 1, alpha, beta, False, move, myCaptures + iCaptured, opCaptures)

            board[move[0]][move[1]] = '.'
            if isCaptured:
                for place in stonesCapturedAt:
                    board[place[0]][place[1]] = capturedStone
            maxValue = max(maxValue, value)
            alpha = max(alpha, value)
            if value >= maxValue:
                bestMove = move
            if beta <= alpha:
                break
        # print("Maximizing Player")
        # print("Move: ", move, "Max Value:", maxValue, "best Move:", bestMove)
        return maxValue, bestMove
    
    else:
        minValue = math.inf
        bestMove = None

        for move in getPossibleMoves(board):
            board[move[0]][move[1]] = opponentStone
            # TODO: What if there is a capture here?
            isCaptured, iCaptured, stonesCapturedAt = checkCaptures(board, move, opponentStone)
            if isCaptured:
                capturedStone = board[stonesCapturedAt[0][0]][stonesCapturedAt[0][1]]
                for place in stonesCapturedAt:
                    board[place[0]][place[1]] = '.'
            value, _ = alphaBetaPruning(board, depth - 1, alpha, beta, True, move, myCaptures, opCaptures + iCaptured)
            
            board[move[0]][move[1]] = '.'
            if isCaptured:
                for place in stonesCapturedAt:
                    board[place[0]][place[1]] = capturedStone
            minValue = min(minValue, value)
            beta = min(beta, value)
            if value <= minValue:
                bestMove = move
            if beta <= alpha:
                break
        # print("Minimizing Player")  
        # print("Move: ", move, "Min Value:", minValue, "best Move:", bestMove)
        return minValue, bestMove

if __name__ == "__main__":
    # Read input file
    file = open('input1.txt', 'r')
    Lines = file.readlines()

    # Store the data in variables
    input = [line.strip() for line in Lines]

    # Get which colour I play
    myColour = input[0]
    # print(myColour)

    timeRemaining = float(input[1])
    # print(timeRemaining)

    # Captures [White, Black]
    stringOfCaptures = input[2].split(',')
    captures = [int(i) for i in stringOfCaptures]
    # print(captures)

    # Board
    board = [[i for i in col] for col in input[3: 22]]
    # print(board)

    # Stone
    if myColour == 'BLACK':
        myStone = 'b'
        opponentStone = 'w'
        myCaptures = captures[1]
        opCaptures = captures[0]
    elif myColour == 'WHITE':
        myStone = 'w'
        opponentStone = 'b'
        myCaptures = captures[0]
        opCaptures = captures[1]

    # TODO: Caliberate depth
    score, move = alphaBetaPruning(board, 1, -math.inf, math.inf, True, None, myCaptures, opCaptures)
    # print(score, move)

    row = 19 - move[0]
    if move[1] < 8:
        col = chr(ord('A') + move[1])
    else:
        col = chr(ord('A') + move[1] + 1)
    output = str(row) + col
    # print(output)

    # TODO: Write to output file with the move in proper format DONE
    file = open('output.txt', 'w')
    file.write(output)
