import math

# Check if the move is valid
def isValidMove(board, move):
    if (move[0] >= 0 or move[0] < 19 or move[1] >= 0 or move[1] < 19) and board[move[0]][move[1]] == '.':
        return True
    else:
        return False

# Check if there are two consecutive stones of the same colour
def isTwoConsecutive(board, move, stone):
    if stone == 'b':
        opStone = 'w'
    else:
        opStone = 'b'
    # Check for horizontal
    if (move[1] > 2 and 
        board[move[0]][move[1]-1] == stone and
        board[move[0]][move[1]-2] == stone and
        board[move[0]][move[1]-3] == opStone):
        return True
    
    if (move[1] < 16 and
        board[move[0]][move[1]+1] == stone and
        board[move[0]][move[1]+2] == stone and
        board[move[0]][move[1]+3] == opStone):
        return True
    # Check for vertical
    if (move[0] > 2 and
        board[move[0]-1][move[1]] == stone and
        board[move[0]-2][move[1]] == stone and
        board[move[0]-3][move[1]] == opStone):
        return True
    
    if (move[0] < 16 and
        board[move[0]+1][move[1]] == stone and
        board[move[0]+2][move[1]] == stone and
        board[move[0]+3][move[1]] == opStone):
        return True
    
    # Check for diagonal \
    if (move[0] > 2 and move[1] > 2 and
        board[move[0]-1][move[1]-1] == stone and
        board[move[0]-2][move[1]-2] == stone and
        board[move[0]-3][move[1]-3] == opStone):
        return True
    
    if (move[0] < 16 and move[1] < 16 and
        board[move[0]+1][move[1]+1] == stone and
        board[move[0]+2][move[1]+2] == stone and
        board[move[0]+3][move[1]+3] == opStone):
        return True
    
    # Check for diagonal /
    if (move[0] > 2 and move[1] < 16 and
        board[move[0]-1][move[1]+1] == stone and
        board[move[0]-2][move[1]+2] == stone and
        board[move[0]-3][move[1]+3] == opStone):
        return True
    
    if (move[0] < 16 and move[1] > 2 and
        board[move[0]+1][move[1]-1] == stone and
        board[move[0]+2][move[1]-2] == stone and
        board[move[0]+3][move[1]-3] == opStone):
        return True    

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
            if (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4] != myStone) or (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4] != opponentStone):
                return True
    # Check for vertical
    for j in range(19):
        for i in range(15):
            if (board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == board[i+4][j] != myStone) or (board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == board[i+4][j] != opponentStone):
                return True
    # Check for diagonal \
    for i in range(15):
        for j in range(15):
            if (board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] != myStone) or (board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] != opponentStone):
                return True
    # Check for diagonal /
    for i in range(15):
        for j in range(4, 19):
            if (board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4] != myStone) or (board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4] != opponentStone):
                return True

    else:
        return False
    
# Get possible moves
# TODO: For white's turns, first => in the middle, second => random move leaving 3 intersections
def getPossibleMoves(board):
    possibleMoves = []
    for i in range(19):
        for j in range(19):
            if isValidMove(board, [i, j]):
                possibleMoves.append([i, j])
    return possibleMoves

# Evaluate board
def evaluateBoard(board):
    pass

# Alpha-Beta Pruning
def alphaBetaPruning(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or gameOver(board):
        return evaluateBoard(board), move
    
    if maximizingPlayer:
        maxValue = -math.inf
        bestMove = None
        for move in getPossibleMoves(board):
            board[move[0]][move[1]] = myStone 
            # TODO: What if here is a capture?
            value, _ = alphaBetaPruning(board, depth - 1, alpha, beta, False)
            board[move[0]][move[1]] = '.'
            maxValue = max(maxValue, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
            if value > maxValue:
                bestMove = move
        return maxValue, bestMove
    
    else:
        minValue = math.inf
        bestMove = None
        for move in getPossibleMoves(board):
            board[move[0]][move[1]] = opponentStone
            value, _ = alphaBetaPruning(board, depth - 1, alpha, beta, True)
            board[move[0]][move[1]] = '.'
            minValue = min(minValue, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
            if value < minValue:
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