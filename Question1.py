import heapq
import copy
import timeit

fringe = []
counter = 0

def creating_initialboard(list):
    initialboard1 = []
    checkingfordimensions = listdimensions[0] * listdimensions[1]
    numberofitems = 0
    global counter
    for i in list:
        numberofitems += 1
    if (numberofitems != checkingfordimensions):
        print("Please enter the correct input or dimensions!")
    for i in list:
        if(i == '.'):
            initialboard1.append(0)
            counter += 1
        else:
            initialboard1.append(i)

    initialboard = [[] for i in range(listdimensions[0])]
    k = 0
    count = 0
    for j in range(0,checkingfordimensions):
        if(count <= listdimensions[0] - 1):
            initialboard[k].append(initialboard1[j])
            count += 1
        else:
            count = 1
            k += 1
            initialboard[k].append(initialboard1[j])
    return(initialboard)

def heuristic(userinput,successor,Player):
    h = 0
    p = []
    count = 0
    indexx = 0
    indexy = 0
    score = 0
    scoreofdiagonal = 0
    totalheuristic = 0
    for y in range(listdimensions[0]):
        for c in range(listdimensions[0]):
            if(successor[y][c] == Player):
                indexx = y
                indexy = c

    for g in successor[indexx]:
        if (g == Player):
            indexy = h
        h += 1
    successor[indexx][indexy] = successor[indexx][indexy].lower()
    Player = Player.lower()

    column = 0
    for b in range(0, listdimensions[0]):
        if (successor[indexx][column] == Player):
            score += 1
        column += 1
    row = 0
    for b in range(0, listdimensions[0]):
        if (successor[row][indexy] == Player):
            score += 1
        row += 1
    x = indexx
    y = indexy
    while (x > -1 and y < listdimensions[0]):
        if (successor[x][y] == Player):
            scoreofdiagonal += 1
        x = x - 1
        y += 1
    x = indexx
    y = indexy
    while (x < listdimensions[0] and y < listdimensions[0]):
        if (successor[x][y] == Player):
            scoreofdiagonal += 1
        x += 1
        y += 1
    x = indexx
    y = indexy
    while (x > -1 and y > -1):
        if (successor[x][y] == Player):
            scoreofdiagonal += 1
        x = x - 1
        y = y - 1
    x = indexx
    y = indexy
    while (y > -1 and x < listdimensions[0]):
        if (successor[x][y] == Player):
            scoreofdiagonal += 1
        y = y - 1
        x += 1
    totalheuristic = score + scoreofdiagonal
    return totalheuristic , successor

def successors(initialboard1,Player,j,userinput):
    index = 0
    checkingfordimensions = listdimensions[0] * listdimensions[1]
    board = copy.deepcopy(initialboard1)
    for i in board:
        if(i == j):
            board[index] = Player
        index += 1

    successor = [[] for i in range(listdimensions[0])]
    k = 0
    count = 0

    for j in range(0, checkingfordimensions):
        if (count <= listdimensions[0] - 1):
            successor[k].append(board[j])
            count += 1
        else:
            count = 1
            k += 1
            successor[k].append(board[j])

    cost = heuristic(userinput,successor,Player)
    heapq.heappush(fringe, (cost[0], cost[1]))

def creatingsuccessors(list,initialboard):
    userinput = initialboard
    countw = 0
    countb = 0
    j = 0
    x = 0
    initialboard1 = []
    Player = 'a'
    for i in list:
        if (i == 'w'):
            countw += 1

        if (i == 'b'):
            countb += 1

    if (countw == countb):
        print("The Player 1 (white) has his/her turn")
        Player = 'W'
    else:
        print("The Player 2 (black) has his/her turn")
        Player = 'B'

    print("Planning of the best move to make..... Hold on for a few seconds")
    for i in list:
        if(i == '.'):
            initialboard1.append(x)
            x += 1
        else:
            initialboard1.append(i)
    for i in range(counter):
        successors(initialboard1,Player,j,userinput)
        j += 1

def solution():
    smallestsuccessorsolution = []
    initialboard3 = []
    index = 0
    checkingfordimensions = listdimensions[0] * listdimensions[1]
    smallestsuccessor = heapq.heappop(fringe)[-1]
    for i in smallestsuccessor:
        for j in range(listdimensions[0]):
            smallestsuccessorsolution.append(i[j])
    j = 0
    for p in smallestsuccessorsolution:
        if(p != 'w' and p != 'b'):
            smallestsuccessorsolution[j] = '.'
        j += 1
    str1 = ''.join(smallestsuccessorsolution)
    l = 0
    z = 0
    while (l < checkingfordimensions):
        if (list[l] != str1[l]):
            z = l
        l = l + 1
    rowi =  z/ listdimensions[0]
    coli = z % listdimensions[0]
    print("You have to place your marble at row"), rowi, ("and column"), coli
    str1 = ''.join(smallestsuccessorsolution)
    print("Hence,the next best state is going to be"), str1



listdimensions = []
list = []
time = 0
listdimensions = input('Enter the dimensions of the board')
list = input('Please give the initial state of the board within quotes')
time = input('Please enter the time in seconds')
starttime = timeit.default_timer()
initialboard = creating_initialboard(list)
creatingsuccessors(list,initialboard)
solution()
stoptime = timeit.default_timer()
completetime = stoptime - starttime
print ("The total time taken is"),completetime





