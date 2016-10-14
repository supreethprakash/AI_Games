# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys
from copy import deepcopy


class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands = {"b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down}
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

    def calculateHeight(self,board):
        aggHeight = []
        # print 'board3',board3
        for i in range(0, tetris.BOARD_WIDTH):
            ctr = 0
            for j in range(len(board)):
                if board[j][i] == 'x':
                    aggHeight.append(len(board) - j)
                    break
                if j == len(board) - 1:
                    aggHeight.append(0)
        return aggHeight

    def calculateBumpness(self,aggHeight):
        bumpness = 0

        for i in range(len(aggHeight)):
            if i < len(aggHeight) - 1:
                bumpness += abs(aggHeight[i] - aggHeight[i + 1])
        return bumpness

    def calculateHole(self,board3,aggHeight):
        holes = 0

        for i in range(0, tetris.BOARD_WIDTH):
            if sum(aggHeight) != 0:
                for j in range(len(board3) - aggHeight[i], len(board3)):
                    if board3[j][i] == ' ':
                        holes += 1
        return holes

    def calculateLines(self,board3):

        completeLines = 0

        for i in range(len(board3)):
            if board3[i].count(board3[i][0]) == len(board3[i]) and board3[i][0] == 'x':
                completeLines += 1
        return completeLines

    def piece_width(self,piece):
        width = 0
        count = 0
        for i in piece:
            count = len(i)
            if count > width:
                width = count
        return width

    def findBestPiece(self, boardx, piecex, next_piecex):
        board = deepcopy(boardx)
        piece = deepcopy(piecex)
        next_piece = deepcopy(next_piecex)
        bestScore = None
        bestRow = 0
        bestCol = 0
        r=0
        for angle1 in range(0,360,90):
            rotated = TetrisGame.rotate_piece(piece, angle1)
            for c in range(tetris.BOARD_WIDTH-ComputerPlayer.piece_width(self,rotated)+1):
                row = 0
                while not TetrisGame.check_collision((board, 0), rotated, row+1, c) and row < tetris.BOARD_HEIGHT:
                    row += 1
                board1 = TetrisGame.place_piece((board, 0), rotated, row, c)[0]
                placeRow = row - 1
                for angle2 in range(0,360,90):
                    rotated1 = TetrisGame.rotate_piece(next_piece,angle2)
                    for c1 in range(tetris.BOARD_WIDTH-ComputerPlayer.piece_width(self,rotated1)+1):
                        row1 = 0
                        while not TetrisGame.check_collision((board1, 0), rotated1, row1+1, c1) and row1 < tetris.BOARD_HEIGHT:
                            row1 += 1
                        board2 = TetrisGame.place_piece((board1, 0), rotated1, row1, c1)[0]
                        height = ComputerPlayer.calculateHeight(self,board2)
                        bump = ComputerPlayer.calculateBumpness(self,height)
                        line = ComputerPlayer.calculateLines(self,board2)
                        hole = ComputerPlayer.calculateHole(self,board2,height)
                        score = (-0.51066 * sum(height)) + (0.760666 * line) + (-0.35663 * hole) + (-0.184483 * bump)
                        if score > bestScore or bestScore == None:
                            bestScore = score
                            angle = angle1
                            if angle == 0:
                                r = 0
                            elif angle == 90:
                                r = 1
                            elif angle == 180:
                                r = 2
                            else:
                                r = 3
                            bestRow = placeRow
                            bestCol = c
        return r,bestRow,bestCol

    def get_moves(self, tetris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        return random.choice("mnb") * random.randint(1, 10)

    # This is the versrion that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)
            board = tetris.get_board()
            piece = tetris.get_piece()[0]
            #print piece
            next_piece = tetris.get_next_piece()
            #time.sleep(0.5)

            a,r,c = ComputerPlayer.findBestPiece(self,board,piece,next_piece)
            if TetrisGame.check_collision((board,0),piece,r,c) == True:
                print
            #print a,r,c
            offset = tetris.col - c
            if offset > 0:
                for f in range(a):
                    tetris.rotate()
                while offset != 0:
                    tetris.left()
                    offset -= 1
                #time.sleep(0.3)
                tetris.down()
            elif offset < 0:
                for f in range(a):
                    tetris.rotate()
                while offset != 0:
                    tetris.right()
                    offset += 1
                #time.sleep(0.3)
                tetris.down()
            else:
                for f in range(a):
                    tetris.rotate()
                #time.sleep(0.3)
                tetris.down()
            #tetris.rotate()
            #tetris.down()
###################
#### main program

(player_opt, interface_opt) = ["computer", "animated"]

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