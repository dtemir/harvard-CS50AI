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

    if Xs - Os == 0:
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
            if x_axis != X and x_axis != O:
                possible_actions.add((y, x))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if len(action) != 2:
        raise Exception("result function: incorrect action")

    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action > 2:
        raise Exception("result function: incorrect action value")

    y, x = action[0], action[1]

    board_copy = copy.deepcopy(board)

    if player(board) == X:
        board_copy[y][x] = X
    else:
        board_copy[y][x] = O


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for y, y_axis in enumerate(board):
        for x, x_axis in enumerate(y_axis):
            pass

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
