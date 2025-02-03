"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who  (either X or O) has the next turn on a board
    In the initial game state, X gets the first move. 
    Subsequently, the player alternates with each additional move.
    Any return value is acceptable if a terminal board is provided as input     
    """
    Xcount = 0
    Ocount = 0

    # Count moves for both players
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                Xcount += 1
            elif board[i][j] == O:
                Ocount += 1
    # Turn for who moved the less. X gets the first move
    return O if Ocount < Xcount else X          
    

def actions(board):
    """
    Returns set of all possible actions, tuples (i, j), available on the board.
    i is the row of the move (0, 1, or 2) 
    j is the cell in the row corresponds to the move (also 0, 1, or 2).
    Possible moves are any cells that do not already have an X or an O in them.
    Any return value is acceptable if a terminal board is provided as input.
    """
    possible_actions = set()
    
    # check the board, look for all empty spaces
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                # add free tuple to the 'possible' set
                possible_actions.add((i, j))
    return possible_actions      
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board without modifying the original.

    If action is not a valid action for the board, raise an exception.
    Let the player whose turn it is make their move at the cell indicated by the input action.
    
    """
    # keep the original board untouched
    res_board = copy.deepcopy(board)
    
    # ckeck the validity of the action
    if res_board[action[0]][action[1]] != EMPTY:
        # raise Exception
        raise Exception()
    if action[0] > 2 or action[0] < 0 or action[1] > 2 or action[1] < 0:
        # raise IndexOutOfBoundsException
        raise Exception()

    # check who is playing
    current_player = player(board)

    # do the move fot the right player
    if current_player == O:
        res_board[action[0]][action[1]] = O  
    else:
        res_board[action[0]][action[1]] = X  
    
    return res_board       
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    If the X player has won the game, return X. If the O player has won the game, return O.
    One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    Assume that there will be at most one winner (both players with three-in-a-row would be an invalid board state).
    If there is no winner of the game (either because the game is in progress, or because it ended in a tie), return None.
    """
    
    for i in range(3):
        # check if there is a horizontal winner        
        if (board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY):
            return board[i][0]
        
        # check if there is a 1 st diagonal winner  
        if (board[0][0] == board[1][1] == board[2][2] or (board[0][2] == board[1][1] == board[2][0]) and board[1][1] != EMPTY):
            return board[1][1]

        # check if there is a vertical winner     
        if (board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY):
            return board[1][i]

    # There is no winner
    return None


def terminal(board):
    """
    Returns True if game is over, 
    False if the game is still in progress.
    """     

    # game over, someone wins
    if winner(board) == X or winner(board) == O:
        return True

    # empty spaces. game in progress    
    for row in range(3):
        if board[row][0] == EMPTY or board[row][1] == EMPTY or board[row][2] == EMPTY:
            return False       

    # game over, no one wins
    return True
        

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Assume utility will only be called on a board if terminal(board) is True.
    """

    won = winner(board) 
    # print(
    #    f"###utility - winner {won} ")

    if won == X:
        return 1 
    
    if won == O:
        return -1
    
    if won == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. 
    If multiple moves are equally optimal, any of those moves is acceptable.
    If the board is a terminal board, the minimax function should return None.

    """
    if terminal(board) == True:
        return None

    cur_player = player(board)
    if cur_player == X:
        moves = []
        for a in actions(board):
            move = min_value(result(board, a))
            moves.append([move, a])
        optimal = sorted(moves, key=lambda x: x[0], reverse=True)[0][1]
        
    elif cur_player == O:
        moves = []
        for a in actions(board):
            move = max_value(result(board, a))
            moves.append([move, a])       
        optimal = sorted(moves, key=lambda x: x[0])[0][1]
    # print(
    #    f"###minimax player {cur_player} moves {moves} optimal {optimal}")
    return optimal


def max_value(board):
    if terminal(board) == True:
        return utility(board)
    
    # The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. 
    v = -math.inf
    for a in actions(board):
        min_v = min_value(result(board, a))
        v = max(v, min_v)
    # print(
    #    f"###max_value {v} ")
    return v


def min_value(board):
    if terminal(board) == True:
        return utility(board)
    v = math.inf
    for a in actions(board):        
        max_v = max_value(result(board, a))
        v = min(v, max_v)
    # print(
    #    f"###min_value {v} ")

    return v
