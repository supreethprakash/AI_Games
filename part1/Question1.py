import heapq
import copy
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
    #print("The initial board is"), initialboard

def heuristic(board):
    return(1)


def successors(initialboard1,Player,j):
    index = 0
    checkingfordimensions = listdimensions[0] * listdimensions[1]
    board = copy.deepcopy(initialboard1)
    for i in board:
        if(i == j):
            board[index] = Player
        index += 1

    x = [[] for i in range(listdimensions[0])]
    k = 0
    count = 0

    for j in range(0, checkingfordimensions):
        if (count <= listdimensions[0] - 1):
            x[k].append(board[j])
            count += 1
        else:
            count = 1
            k += 1
            x[k].append(board[j])

    heapq.heappush(fringe, (heuristic(x), x))


def creatingsuccessors(list):
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
        Player = 'w'
    else:
        print("The Player 2 (black) has his/her turn")
        Player = 'b'

    print("Planning of the best move to make..... Hold on for a few seconds")
    for i in list:
        if(i == '.'):
            initialboard1.append(x)
            x += 1

        else:
            initialboard1.append(i)


    for i in range(counter):
        successors(initialboard1,Player,j)
        j += 1


def solution():
    smallestsuccessor = heapq.heappop(fringe)[-1]
    print("The next best state is going to be"), smallestsuccessor

listdimensions = input('Enter the dimensions of the board')
list1 = input('Please give the initial state of the board within quotes')
creating_initialboard(list1)
creatingsuccessors(list1)
solution()





