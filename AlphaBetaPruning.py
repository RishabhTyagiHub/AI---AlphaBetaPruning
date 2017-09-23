import sys
import operator
from copy import deepcopy
import os
import logging
import getopt

Game_Grid_Size = 8
rfile = open(sys.argv[0], 'r')
traverse_log = str()
count = 0
Inputs = {}
Inputs["Player_Turn"] = rfile.readline().rstrip('\n')
Inputs["Depth"] = int(rfile.readline().rstrip('\n'))
start_board = []
n = 0
while(n < 8):
    start_board.append(list(rfile.readline().strip()))
    n = n+1
Inputs["Board"] = start_board
player_to_move = Inputs["Player_Turn"]
rowsadjust = [1, 2, 3, 4, 5, 6, 7, 8]
columnsadjust = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
def get_input_file():
	opts, args = getopt.getopt(sys.argv[1:], "i:")
  	if len(opts) != 0:
   		return opts[0][1]
  	else:
   		return "./input.txt"

###Method to get opponent
def getOpponent(player):
    if player == "X":
        return "O"
    return "X"

### Method to check for valid moves and return the tiles to flip.
def ValidMoveFinder(board, my_player, xpush, ypush):

    if board[xpush][ypush] != "*" or not isOnBoard(xpush, ypush):
        return False
    board[xpush][ypush] = my_player
    otherplayer = getOpponent(my_player)
    flipped_tiles = gettileswon(board,xpush,ypush, my_player, otherplayer)
    board[xpush][ypush] = "*"
    if len(flipped_tiles) == 0:
        return False
    return flipped_tiles

###Method to find the tileswon by the player
def gettileswon(board,xpush, ypush, my_player, otherplayer):
    tileswon = []
    for directionx, directiony in ([[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]):
        x = xpush
        x = x + directionx
        y = ypush
        y = y + directiony

        if isOnBoard(x,y) and board[x][y] == otherplayer:
            x = x + directionx
            y = y + directiony
            if not isOnBoard(x,y):
                continue
            while board[x][y] == otherplayer:
                x = x + directionx
                y = y + directiony
                if not isOnBoard(x,y):
                    break
            if not isOnBoard(x,y):
                continue


            if board[x][y] == my_player:
                #start traversing in reverse to find
                while True:
                    x = x - directionx
                    y = y - directiony
                    if x == xpush and y == ypush:
                        break
                    tileswon.append((x,y))
    return tileswon

### Method check if the move is on board or not.
def isOnBoard(x, y):
    return ((x >= 0) and (x <= 7)) and ((y >= 0) and (y <= 7))

# Method to generate moves and find if the moves are valid.
def generate_moves(board, player):
    moves  = list()
    i, j = 0, 0
    while i < 8:
        j = 0
        while j < 8:

           if ValidMoveFinder(board, player, i, j) != False:
                #print moves,i,j
                moves.append((i, j))

           j += 1
        i += 1

    return moves

###Method to make a move by the player
def Take_Move(new_board, move, player):
    copy_board = deepcopy(new_board)
    i = move[0]
    j = move[1]
    flip = ValidMoveFinder(copy_board, player, i, j)
    if flip == False: return copy_board

    copy_board[i][j] = player
    for x,y in flip:
        copy_board[x][y] = player
    return copy_board

###Method to Evaluate Scores
def getEvaluation(me, opponent, board):
    my_score = 0
    opponent_score = 0
    i=0
    for i in range (8):
        for j in range(8):
            if board[i][j] == "*":
                continue
            elif board[i][j] == me:
                my_score += boardPositionalWeight(i,j)

            else:

                opponent_score +=boardPositionalWeight(i,j)
            j += 1
        i += 1
    return my_score - opponent_score

def output_log(self):
    wfile = open("./traverse_log.txt", "w")
    for i in range(0, len(self.traverse_log)):
        if i == len(self.traverse_log) - 1:
            wfile.write(self.traverse_log[i])
        else:
            wfile.write(self.traverse_log[i] + "\n")

def max_to_string(self, value):
    if value == self.int_min:
        return "-Infinity"
    if value == self.int_max:
        return "Infinity"
    return value

###Method to find positonal weights of each grid.
def boardPositionalWeight(x,y):
    l, b = 8,8
    weightmatrix = [[0 for i in range(l)] for j in range(b)]
    weights = [[99, -8, 8, 6, 6, 8, -8, 99],[-8, -24, -4, -3, -3, -4, -24, -8], [8, -4, 7, 4, 4, 7, -4, 8], [6, -3, 4, 0, 0, 4,-3,-6
                ],[6, -3, 4, 0, 0, 4, -3, -6],[8, -4, 7, 4, 4, 7, -4, 8], [-8, -24, -4, -3, -3, -4, -24, -8], [99, -8, 8, 6, 6, 8, -8, 99] ]
    for i in range(8):
        for j in range(8):
            weightmatrix[i][j] = weights[i].__getitem__(j)
    # for i in range(4):
    #     for j in range(4,8):
    #         weightmatrix[i][j] =  weights[i].__getitem__((j+3)%4)
    #         #str(list(reversed(weights[i]))).replace("'[","").replace("]'","")


    return weightmatrix[x][y]

###Method to find the Expansion Values
def getExpandValues(player):
    if player == player_to_move:
        best = -99999
    else:
        best = 99999
    flag = True
    while(flag == True):
        alpha = -99999
        beta = 99999
        flag = False
    return best, alpha, beta

###Method tp add recursive logs
def recursive_log(best, result, traverse_log, player):
    if player == player_to_move:
        traverse_log += '\n' + "pass" + ',' + str(1) + ',' + str(best) + "," + str(result[2]) + "," + str( result[1])
        traverse_log += '\n' + "root" + ',' + str(0) + ',' + str(best) + "," + str(result[1]) + "," + str(-1*result[2])
        return traverse_log

    else:
        traverse_log += '\n' + "pass" + ',' + str(1) + ',' + str(best) + "," + str(result[1]) + "," + str(result[2])
        traverse_log += '\n' + "root" + ',' + str(0) + ',' + str(best) + "," + str(result[2]) + "," + str(-1*result[1])

        return traverse_log

def alphabetaPruning(board, depth, player):
    val = ()
    i = 0
    global count
    expansionvalues = getExpandValues(player)
    best = expansionvalues[0]
    alpha = expansionvalues[1]
    beta = expansionvalues[2]
    global traverse_log
    moves = []
    ### Generates the moves suggested moves by player
    moves = generate_moves(board, player)


    finalboardmove = list()
    if len(moves) > 0:

        while(i < len(moves)):
            new_board = deepcopy(board)
            mv = Take_Move(new_board, moves[i], player)
            new_board = mv

            if(depth == Inputs["Depth"]):
                traverse_log += '\n' + "root" + "," + str(0) + "," + str(best) + "," + str(alpha) + "," + str(beta)
            else:
                traverse_log += '\n' + "pass" + "," + str(Inputs["Depth"] - depth) + "," + str(best) + "," + str(alpha) + "," + str(beta)

            if (player == player_to_move):
                result = alphabeta(new_board, depth - 1, getOpponent(player), alpha, beta, moves[i])
                val = max(result[0],best)
                if not val >= beta:
                    if alpha < min(beta, result[0]):
                        if result[1] is not None:
                            alpha = max(alpha,result[1])
                        else:
                            alpha = max(alpha, result[0])
                    else:
                        alpha = alpha
                else:
                    alpha = alpha
            else:
                result = alphabeta(new_board, depth - 1, player_to_move, alpha, beta, moves[i])
                val = min(result[0],best)
                if not val <= alpha:
                    if alpha < min(beta, result[0]):
                        if result[1] is not None:
                            beta = min(beta, result[1])
                        else:
                            beta = min(beta, result[0])
                    else:
                        beta = beta
                else:
                    beta = beta
            best = val
            finalboardmove.append((best, moves[i]))
            i += 1
        if Inputs["Depth"] == depth:
            traverse_log += '\n' + "root" + "," + str(0) + "," + str(best) + "," + str(alpha) + "," + str(beta)

    elif Inputs["Depth"] - depth == 0: #or count < 2:
        Evaluation = getEvaluation(player_to_move, getOpponent(player_to_move), board)
        traverse_log += '\n' + "root" + ',' + str(Inputs["Depth"] - depth) + ',' + str(best) + "," + str(alpha) + "," + str(beta)
        #if player == player_to_move:
        result = alphabetaPruning(board, depth - 1, getOpponent(player))
        val = result[0]
        finalboardmove = result[3]

        if player == player_to_move:
            alpha = result[1]
            beta = result[2]
            if not val >= beta:
                if alpha < min(beta, result[0]):
                    if result[1] is not None:
                        alpha = max(alpha,result[1])
                    else:
                        alpha = max(alpha, result[0])
                else:
                    alpha = alpha
            else:
                alpha = alpha

            best = val
            traverse_log += '\n' + "pass" + ',' + str(1) + ',' + str(best) + "," + str(alpha) + "," + str(
                beta)
            traverse_log += '\n' + "root" + ',' + str(0) + ',' + str(best) + "," + str(beta) + "," + str(-alpha
                )


        else:
            alpha = result[1]
            beta = result[2]
            if not val <= alpha:
                if alpha < min(beta, result[0]):
                    if result[1] is not None:
                        beta = min(beta, result[1])
                    else:
                        beta = min(beta, result[0])
                else:
                    beta = beta
            else:
                beta = beta
            best = val
            traverse_log += '\n' + "pass" + ',' + str(1) + ',' + str(best) + "," + str(result[2]) + "," + str(
                result[1])
            traverse_log += '\n' + "root" + ',' + str(0) + ',' + str(best) + "," + str(result[1]) + "," + str(
                -1 * result[2])

    else:
        count = count+1
        if count < 2:
            if player == player_to_move:
                traverse_log += '\n' + "pass" + ',' + str(Inputs["Depth"] - depth) + ',' + str(best) + ',' + str(
                    alpha) + ',' + str(beta)
                result = alphabetaPruning(board, depth - 1, getOpponent(player))
                val = result[0]
                finalboardmove = result[3]
                if alpha < min(beta, result[0]):
                    if alpha < min(beta, result[0]):
                        alpha = max(alpha, val)
                    else:
                        alpha = alpha
                else:
                    alpha = alpha
                best = val

            else:
                traverse_log += '\n' + "pass" + ',' + str(Inputs["Depth"] - depth) + ',' + str(best) + ',' + str(
                    alpha) + ',' + str(beta)
                result = alphabetaPruning(board, depth - 1, getOpponent(player))
                val = result[0]
                finalboardmove = result[3]
                if alpha < min(beta, result[0]):
                    if alpha < min(beta, result[0]):
                        beta = min(beta, val)
                    else:
                        beta = beta
                else:
                    beta = beta
                best = val

        else:
            Evaluation = getEvaluation(player, getOpponent(player), board)
            traverse_log += '\n' + "pass" + ',' + str(Inputs["Depth"]- depth) + ',' + str(Evaluation) + ',' + str(alpha) + ',' + str(beta)
            return Evaluation, alpha, beta, finalboardmove



    return best, alpha, beta, finalboardmove

def alphabeta(board, depth, player, alpha, beta, move, passv = None):
    global traverse_log
    moves = []
    global count
    ###Terminal test for leaf node.
    if depth == 0:
        utility = getEvaluation(player_to_move, getOpponent(player_to_move), board)
        traverse_log += '\n' + str(columnsadjust[move[1]]) + str(rowsadjust[move[0]]) + ',' + str(Inputs["Depth"]) + ',' + str(
            utility) + "," + str(alpha) + "," + str(beta)
        return utility, None, None

    if player == player_to_move:
        best = -99999
    else:
        best = 99999
    moves = generate_moves(board, player)

    if passv == None:
        traverse_log += "\n" + str(columnsadjust[move[1]]) + str(rowsadjust[move[0]]) + ',' + str(Inputs["Depth"]- depth) + ',' + \
                        str(best) + "," + str(alpha) + "," + str(beta)
    bool = True
    if len(moves) >= 1:
        i = 0

        while(i < len(moves)):
            while(bool == True):
                newbeta = beta
                newaplha = alpha
                bool = False
            if alpha < beta:
                new_board = deepcopy(board)
                mv = Take_Move(new_board, moves[i], player)
                new_board = mv
                if player == player_to_move:
                    result = alphabeta(new_board, depth - 1, getOpponent(player), alpha, beta, moves[i])
                    val = max(result[0], best)

                    if not val >= beta:
                        if alpha < min(beta, result[0]):
                            if result[1] is not None:
                                alpha = max(alpha,result[1])
                            else:
                                alpha = max(alpha, result[0])
                        else:
                            alpha = alpha
                    else:
                        alpha = alpha
                        best = val
                        traverse_log += '\n' + str(columnsadjust[move[1]]) + str(rowsadjust[move[0]]) + ',' + \
                                        str(Inputs["Depth"] - depth) + ',' + str(best) + ',' + str(alpha) + ',' + str(
                            beta)
                        return val, None, None

                else:

                    result = alphabeta(new_board, depth - 1, player_to_move, alpha, beta, moves[i])
                    val = min(result[0], best)
                    if not val <= alpha:
                        if alpha < min(beta, result[0]):
                            if result[1] is not None:
                                beta = min(beta, result[1])
                            else:
                                beta = min(beta, result[0])
                        else:
                            beta = beta
                    else:
                        beta = beta
                        best = val
                        traverse_log += '\n' + str(columnsadjust[move[1]]) + str(rowsadjust[move[0]]) + ',' + \
                                        str(Inputs["Depth"] - depth) + ',' + str(best) + ',' + str(alpha) + ',' + str(
                            beta)

                        return val, None, None
                best = val

                if passv == None:
                        traverse_log +=  '\n' + str(columnsadjust[move[1]]) + str(rowsadjust[move[0]]) + ',' + \
                                         str(Inputs["Depth"] - depth) + ',' + str(best) + ',' + str(alpha) + ',' + str(beta)

                elif passv == True:
                    traverse_log += '\n' + "pass" + ',' + str(Inputs["Depth"] - depth) + ',' + str(best) + ',' + str(alpha) + ',' + str(beta)

            ###use this for Pruning
            else:
                val = best
                if player == player_to_move:
                    return val, alpha, beta
                return val, beta, alpha

            i+=1


    elif passv == None:

        traverse_log += '\n' + "pass" + ',' + str(
        Inputs["Depth"] - depth+1) + ',' + str(-1*best) + ',' + str(alpha) + ',' + str(beta)
        if player == player_to_move:
            result = alphabeta(board, Inputs["Depth"] - depth, getOpponent(player), alpha, beta, move, True)
            val = max(result[0], best)
            if val >= beta:

                if alpha < min(result[0], beta) and (val < beta):
                    if result[1] is not None:
                        alpha = max(alpha, result[1])
                    else:
                        alpha = max(alpha, result[0])
                else:
                    alpha = alpha
            else:
                alpha = alpha


            traverse_log += '\n' + str(columnsadjust[move[1]]) + str(rowsadjust[move[0]]) + ',' + \
                            str(Inputs["Depth"] - depth) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta)
        else:
            result = alphabeta(board, Inputs["Depth"] - depth, getOpponent(player), alpha, beta, move, True)
            val = min(result[0], best)

            if alpha < min(result[0], beta):
                if result[1] is not None:
                    beta = min(beta, result[1])
                else:
                    beta = min(beta, result[0])
            else:
                beta = beta

            traverse_log += '\n' + str(columnsadjust[move[1]]) + str(rowsadjust[move[0]]) + ',' + \
                            str(Inputs["Depth"] - depth) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta)


        if player == player_to_move:
            return val, alpha, beta
        return val, beta, alpha

    elif passv == True:

        count = count + 1

        if count < 2:
            if player == player_to_move:

                result = alphabeta(board, Inputs["Depth"] - depth, getOpponent(player), alpha, beta, move, True)
                val = max(result[0], best)

                if alpha < min(result[0], beta):
                    if result[1] is not None:
                        alpha = max(alpha, result[1])
                    else:
                        alpha = max(alpha, result[0])
                else:
                    alpha = alpha

                traverse_log += '\n' + "pass" + ',' + \
                                str(Inputs["Depth"] - depth) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta)

            else:
                result = alphabeta(board, Inputs["Depth"] - depth, player_to_move, alpha, beta, move, True)
                val = min(result[0], best)

                if beta < min(result[0], alpha):
                    if result[1] is not None:
                        beta = min(beta, result[1])
                    else:
                        beta = min(beta, result[0])
                else:
                    beta = beta

                traverse_log += '\n' + "pass "+ ',' + \
                                str(Inputs["Depth"] - depth) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta)

        else:
            utility = getEvaluation(player_to_move, getOpponent(player_to_move), board)
            traverse_log += '\n' + "pass" + ',' + str(Inputs["Depth"]) + ',' + str(
                utility) + "," + str(alpha) + "," + str(beta)
            # count = count -1
            return utility, None, None

    if player == player_to_move:
        return val, alpha, beta
    else:
        return val, beta, alpha


best_move_ = list()
count = 0
final_move_ = alphabetaPruning(start_board, Inputs["Depth"], player_to_move)
best_moves = final_move_[3]

def getFinalBoard(best_moves):
    if(len(best_moves) > 0):
        i = 0
        best_move =best_moves[0]

        while i < len(best_moves):
            if(best_moves)[i][0]>best_move[0]:
                best_move = best_moves[i]
            i += 1

        board = deepcopy(start_board)
        Final_Board = Take_Move(board, best_move[1], player_to_move)

    else:
        Final_Board = start_board
    return Final_Board

Final_Board = getFinalBoard(best_moves)

traverse_log = traverse_log.replace("-99999", "-Infinity")
traverse_log = traverse_log.replace("99999", "Infinity")

Final = str()
i = 0
while i < len(Final_Board):
    line = str(Final_Board[i]).replace(']', '')
    line = line.replace(',', '')
    line = line.replace("\'", '')
    line = line.replace(" ", '')
    line = line.replace('[', '')
    Final += line + '\n'
    i += 1

Output = open("output.txt", "w")
Output.writelines(Final + "Node,Depth,Value,Alpha,Beta" + traverse_log)
Output.close()