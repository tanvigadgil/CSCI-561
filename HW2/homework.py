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
