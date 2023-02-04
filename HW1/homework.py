import heapq

neighbours = [
    [-1, -1], # Upper Left
    [-1, 0], # Left
    [-1, 1], # Lower Left
    [0, -1], # Up
    [0, 1], # Down
    [1, -1], # Upper Right
    [1, 0], # Right
    [1, 1], # Lower Right
    ]

pathCosts = [14, 10, 14, 10, 10, 14, 10, 14] # 10 = straight, 14 = diagonal

# Create node
def createNode(col, row):
    return tuple([int(col), int(row)])

# Function to check conditions if the move is valid
def isMoveValid(parent, node):
    if node[0] < 0 or node[0] >= mapSize[0] or node[1] < 0 or node[1] >= mapSize[1]: 
        return False

    if abs(elevation[parent[1]][parent[0]]) >= abs(elevation[node[1]][node[0]]):
        return True
    else:
        if elevation[node[1]][node[0]] > 0 and abs(elevation[node[1]][node[0]]) - abs(elevation[parent[1]][parent[0]]) <= stamina:
            return True
    return False

# Function for BFS
def BFS(start, goal):
    queue = list() # 2D array with each element containing node and its parent
    visited = dict() # Dictionary containing nodes that are visited and its parent

    queue.append((start, None))

    while(queue):
        node, parent = queue.pop(0)

        if node in visited:
            continue

        visited[node] = (parent)
        if node == goal:
            return visited

        # Check conditions for its neighbours
        for neighbour in neighbours:
            nextNode = createNode(node[0] + neighbour[0], node[1] + neighbour[1])
            if isMoveValid(node, nextNode) and nextNode not in visited:
                queue.append((nextNode, node))

    # If queue is empty
    return False

# Function for UCS
def UCS(start, goal):
    priorityQueue = list() # 2D array => [cost, node, parent]
    visited = dict() # Dictionary => [node : (cost, parent)]

    heapq.heappush(priorityQueue, (0, start, None))

    while(priorityQueue):
        cost, currentNode, parent = heapq.heappop(priorityQueue)

        if currentNode in visited and visited[currentNode][0] < cost:
            continue

        visited[currentNode] = (cost, parent) 
        if currentNode == goal:
            return visited

        for neighbour in neighbours:
            neighbourNode = createNode(currentNode[0] + neighbour[0], currentNode[1] + neighbour[1])
            if isMoveValid(currentNode, neighbourNode):
                neighbourCost = cost + pathCosts[neighbours.index(neighbour)]
                if neighbourNode not in visited or visited[neighbourNode][0] > neighbourCost:
                    heapq.heappush(priorityQueue, (neighbourCost, neighbourNode, currentNode))

    # If queue is empty
    return False


if __name__ == "__main__":
    # Read the input file
    file = open('input2.txt', 'r')
    Lines = file.readlines()

    # Store the data in variables
    input = [line.strip() for line in Lines]

    algorithm = input[0]
    mapSize = list(map(int,input[1].split())) # [col, row] [W, H]
    print("Map Size: ")
    print(mapSize)
    startPos = list(map(int,input[2].split()))
    stamina = int(input[3])
    numOfLodges = int(input[4])

    lodges = list()
    for i in range(numOfLodges):
        lodges.append(list(map(int, input[5 + i].split())))
    print("Lodges: ")
    print(lodges)

    elevation = list()
    for i in range(mapSize[1]):
        elevation.append(list(map(int, input[5 + numOfLodges + i].split())))
    print("Elevation: ")
    print(elevation)
    startNode = createNode(startPos[0], startPos[1])
    output = ""

    # Check the algorithm to use
    if algorithm == "BFS":
        print("Running BFS")
        for lodge in lodges:
            goal = createNode(lodge[0], lodge[1])
            visited = BFS(startNode, goal)
            outputList = list()

            if visited:
                if goal in visited:
                    node = goal
                    
                    while node != startNode:
                        outputList.append(node)
                        node = visited[node]
                    outputList.append(startNode)
                    outputList.reverse()
                    output = output + " ".join("%s,%s" %tup for tup in outputList) + "\n"
            else:
                output = "FAIL"

    elif algorithm == "UCS":
        print("Running UCS")
        for lodge in lodges:
            goal = createNode(lodge[0], lodge[1])
            visited = UCS(startNode, goal)
            outputList = list()

            if visited:
                if goal in visited:
                    node = goal
                    
                    while node != startNode:
                        outputList.append(node)
                        node = visited[node][1]
                    outputList.append(startNode)
                    outputList.reverse()
                    output = output + " ".join("%s,%s" %tup for tup in outputList) + "\n"
            else:
                output = "FAIL"
    elif algorithm == "A*":
        print("Running A*")

    print(str(output))
    file = open('output.txt','w')
    file.write(output)