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
def isMoveValid(parent, node, momentum = 0):
    if node[0] < 0 or node[0] >= mapSize[0] or node[1] < 0 or node[1] >= mapSize[1]: 
        return False

    if abs(elevation[parent[1]][parent[0]]) >= abs(elevation[node[1]][node[0]]):
        return True
    else:
        if elevation[node[1]][node[0]] > 0 and abs(elevation[node[1]][node[0]]) - abs(elevation[parent[1]][parent[0]]) <= stamina + momentum:
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

# Function for Heuristic
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# Function for A*
def AStar(start, goal):
    priorityQueue = list() # 2D array => [cost, node, parent, parentHCost, momentum]
    visited = dict() # Dictionary => [node : (cost, parent, momentum)]

    heapq.heappush(priorityQueue, (0, start, None, 0, 0))

    while(priorityQueue):
        cost, currentNode, parent, parentHCost, momentum = heapq.heappop(priorityQueue)
        cost = cost - parentHCost

        if currentNode in visited and visited[currentNode][0] < cost and visited[currentNode][2] >= momentum:
            continue

        visited[currentNode] = (cost, parent, momentum) 
        if currentNode == goal:
            return visited

        for neighbour in neighbours:
            neighbourNode = createNode(currentNode[0] + neighbour[0], currentNode[1] + neighbour[1])
            newMomentum = 0
                
            if isMoveValid(currentNode, neighbourNode, newMomentum):
                if abs(elevation[neighbourNode[1]][neighbourNode[0]]) - abs(elevation[currentNode[1]][currentNode[0]]) > 0 and parent is not None:
                    newMomentum = max(0, elevation[parent[1]][parent[0]] - elevation[currentNode[1]][currentNode[0]])

                ecc = max(0, elevation[neighbourNode[1]][neighbourNode[0]] - elevation[currentNode[1]][currentNode[0]] - newMomentum)
                neighbourCost = cost + pathCosts[neighbours.index(neighbour)] + heuristic(neighbourNode, goal) + ecc

                inPQ = False
                nodeIndex = -1
                for node in priorityQueue:
                    if node[1] == neighbourNode:
                        inPQ = True
                        nodeIndex = priorityQueue.index(node)
                        break

                if neighbourNode not in visited and not inPQ:
                    heapq.heappush(priorityQueue, (neighbourCost, neighbourNode, currentNode, heuristic(neighbourNode, goal), newMomentum))
                elif inPQ:
                    if priorityQueue[nodeIndex][0] > neighbourCost:
                        priorityQueue.remove((neighbourCost, neighbourNode, currentNode, heuristic(neighbourNode, goal), newMomentum))
                        heapq.heappush(priorityQueue, (neighbourCost, neighbourNode, currentNode, heuristic(neighbourNode, goal), newMomentum))
                    elif priorityQueue[nodeIndex][4] < newMomentum:
                        heapq.heappush(priorityQueue, (neighbourCost, neighbourNode, currentNode, heuristic(neighbourNode, goal), newMomentum))
                elif neighbourNode in visited:
                    if visited[neighbourNode][0] > neighbourCost:
                        visited[neighbourNode] = (neighbourCost, currentNode, newMomentum)
                        heapq.heappush(priorityQueue, (neighbourCost, neighbourNode, currentNode, heuristic(neighbourNode, goal), newMomentum))
                    elif visited[neighbourNode][2] < newMomentum:
                        heapq.heappush(priorityQueue, (neighbourCost, neighbourNode, currentNode, heuristic(neighbourNode, goal), newMomentum))

                # if neighbourNode not in visited or visited[neighbourNode][0] > neighbourCost or visited[neighbourNode][2] < newMomentum:
                #     heapq.heappush(priorityQueue, (neighbourCost, neighbourNode, currentNode, heuristic(neighbourNode, goal), newMomentum))

    # If queue is empty
    return False

if __name__ == "__main__":
    # Read the input file
    file = open('input5.txt', 'r')
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
                    output += " ".join("%s,%s" %tup for tup in outputList) + "\n"
                    print(output)
            else:
                output += "FAIL\n"

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
                    output += " ".join("%s,%s" %tup for tup in outputList) + "\n"
                    print(output)
            else:
                output += "FAIL\n"
                
    elif algorithm == "A*":
        print("Running A*")
        for lodge in lodges:
            goal = createNode(lodge[0], lodge[1])
            visited = AStar(startNode, goal)
            outputList = list()

            if visited:
                if goal in visited:
                    node = goal
                    print(visited[goal][0])
                    
                    while node != startNode:
                        outputList.append(node)
                        node = visited[node][1]

                    outputList.append(startNode)
                    outputList.reverse()
                    output += " ".join("%s,%s" %tup for tup in outputList) + "\n"
                    print(output)
            else:
                output += "FAIL\n"

    # print(output)
    file = open('output.txt','w')
    file.write(output)