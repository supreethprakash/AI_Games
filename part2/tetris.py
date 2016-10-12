# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys

class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #

    def rotateAndPlace(self, origBoard, piece, nextPiece):
        tempBoard = origBoard[:]
        tempPiece = piece[:]
        tempNextPiece = nextPiece[:]

        angles = [90,180,270]

        row, col = 0, 0
        highestScore = -9999
        bestrow = -1
        bestcol = -1
        bestPiece = []

        for rotation in angles:
            rotatedPiece = TetrisGame.rotate_piece(tempPiece, rotation)
            for i in range(TetrisGame.BOARD_HEIGHT - 1, -1, -1):
                for j in range(TetrisGame.BOARD_WIDTH):
                    if not TetrisGame.check_collision((origBoard, 0),rotatedPiece, i, j):
                        row, col = i, j
                        placedPiece = TetrisGame.place_piece((tempBoard, 0), rotatedPiece, row, col)
                        temporaryBoard = placedPiece[0][:]
                        for rotation1 in angles:
                            rotatedNextPiece = TetrisGame.rotate_piece(tempNextPiece, rotation1)
                            for row1 in range(TetrisGame.BOARD_HEIGHT - 1, -1, -1):
                                for col1 in range(TetrisGame.BOARD_WIDTH):
                                    if not TetrisGame.check_collision((temporaryBoard, 0), rotatedNextPiece, row1, col1):
                                        placedNextPiece = TetrisGame.place_piece((temporaryBoard, 0), rotatedNextPiece, row1, col1)
                                        board = placedNextPiece[0][:]

                                        aggHeight = []
                                        for i in range(0, tetris.BOARD_WIDTH):
                                            ctr = 0
                                            for j in range(len(board)):
                                                if board[j][i] == 'x':
                                                    aggHeight.append(len(board) - j)
                                                    break
                                                if j == len(board) - 1:
                                                    aggHeight.append(0)

                                        #print 'Agg Height', aggHeight

                                        bumpness = 0

                                        for i in range(len(aggHeight)):
                                            if i < len(aggHeight) - 1:
                                                bumpness += abs(aggHeight[i] - aggHeight[i + 1])
                                        #print 'Bumpness', bumpness

                                        holes = 0

                                        for i in range(0, tetris.BOARD_WIDTH):
                                            if sum(aggHeight) != 0:
                                                for j in range(len(board) - aggHeight[i], len(board)):
                                                    if board[j][i] == ' ':
                                                        holes += 1

                                        #print 'Holes', holes

                                        completeLines = 0

                                        for i in range(len(board)):
                                            if board[i].count(board[i][0]) == len(board[i]) and board[i][0] == 'x':
                                                completeLines += 1

                                        #print 'completeLines', completeLines

                                        score = (-0.51066 * sum(aggHeight)) + (0.760666 * completeLines) + (
                                        -0.35663 * holes) + (-0.184483 * bumpness)

                                        if score > highestScore:
                                            highestScore = score
                                            bestrow = row
                                            bestcol = col
                                            bestPiece = rotatedPiece
                                            angle = rotation

        return bestrow, bestcol, bestPiece, angle


    def evaluate(self, tetris):
        board = tetris.get_board()
        print board

    def get_moves(self, tetris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        return random.choice("mnb") * random.randint(1, 10)
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def evaluate(self, str):
        print str

    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)
            board = tetris.get_board()
            piece = tetris.get_piece()[0]
            row, col, piece1, angle = ComputerPlayer.rotateAndPlace(self, tetris.get_board(), piece, tetris.get_next_piece())
            #print row, tetris.col, col, piece, angle

            rotationNumber = {90: 1, 180: 2, 270: 3}
            numberOfRotations = rotationNumber.get(angle)

            while numberOfRotations > 0:
                tetris.rotate()
                numberOfRotations -= 1

            offset = tetris.col - col

            if offset > 0:
                while offset > 0:
                    tetris.left()
                    offset -= 1
            else:
                while offset < 0:
                    tetris.right()
                    offset += 1
            tetris.down()
            #column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            #index = column_heights.index(max(column_heights))
            #tetris.move(col, final)
            #tetris.place_piece((board, 0), piece1, row, col)
            #tetris.down()
'''
            if(index < tetris.col):
                tetris.left()
            elif(index > tetris.col):
                tetris.right()
            else:
                tetris.down()
'''


###################
#### main program

(player_opt, interface_opt) = ['computer', 'animated']

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s



