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
    Returns player who has the next turn on a board.
    """
    Xs = 0
    Os = 0
    for y_axis in board:
        for x_axis in y_axis:
            if x_axis == X:
                Xs += 1
            elif x_axis == O:
                Os += 1

    if Xs <= Os:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set()

    for y, y_axis in enumerate(board):
        for x, x_axis in enumerate(y_axis):
            if x_axis == EMPTY:
                possible_actions.add((y, x))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if len(action) != 2:
        raise Exception("result function: incorrect action")

    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("result function: incorrect action value")

    y, x = action[0], action[1]

    board_copy = copy.deepcopy(board)

    if board_copy[y][x] != EMPTY:
        raise Exception("suggested action has already been taken")
    else:
        board_copy[y][x] = player(board)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Since the board is always 3x3, I believe this approach is reasonable
    for y in range(3):
        # Check horizontal lines
        if (board[y][0] == board[y][1] == board[y][2]) and (board[y][0] != EMPTY):
            return board[y][0]
        # check vertical lines
        if (board[0][y] == board[1][y] == board[2][y]) and (board[0][y] != EMPTY):
            return board[0][y]

    # Check diagonals
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]) \
            and board[1][1] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    elif EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
