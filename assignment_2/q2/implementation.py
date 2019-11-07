"""
This is the only file you should change in your submission!
"""
from enum import Enum

from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function, INFINITY, NEG_INFINITY


# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

# STUDENT_ID = 12345678
# AGENT_NAME =
# COMPETE = False

# TODO Change this evaluation function so that it tries to win as soon as possible
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    CHAIN_VALUES = {
        1: 1,
        2: 100,
        3: 400,
        4: 1000,
    }

    if board.is_tie():
        return 0

    if board.is_win():
        # As with basic_evaluate, winning must mean lost.
        return -1000

    current_chain = board.chain_cells(board.get_current_player_id())
    other_chain = board.chain_cells(board.get_other_player_id())

    # Longer chains should correlate with closer wins (value 3 chains more than 2 chains
    current_score = sum([CHAIN_VALUES[len(current)] for current in current_chain])
    other_score = sum([CHAIN_VALUES[len(other)] for other in other_chain])

    return current_score - other_score


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)


# TODO Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.

# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.
def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    """
     board is the current tree node.

     depth is the search depth.  If you specify depth as a very large number then your search will end at the leaves of trees.
     
     def eval_fn(board):
       a function that returns a score for a given board from the
       perspective of the state's current player.
    
     def get_next_moves(board):
       a function that takes a current node (board) and generates
       all next (move, newboard) tuples.
    
     def is_terminal_fn(depth, board):
       is a function that checks whether to statically evaluate
       a board/node (hence terminating a search branch).
    """
    # For each possible move, traverse with given alpha/beta from previous recursions.
    alpha = NEG_INFINITY
    beta = INFINITY
    best_val = NEG_INFINITY
    best_move = -1
    for move, new_board in get_next_moves_fn(board):
        val = alpha_beta_min_recurse(new_board, depth - 1, eval_fn, alpha, beta,
                                     get_next_moves_fn, is_terminal_fn)

        if val > best_val:
            best_move = move
            best_val = val
            alpha = max(val, alpha)
    return best_move


def alpha_beta_max_recurse(board, depth, eval_fn, alpha, beta,
                           get_next_moves_fn=get_all_next_moves,
                           is_terminal_fn=is_terminal):
    """

    Args:
        board: A Connect4 game board object.
        depth: The depth to perform alpha_beta_recursively downwards.
        alpha:
        beta:
        eval_fn: An evaluation function for board states.
        get_next_moves_fn: A function that returns all possible next moves
        is_terminal_fn: A function that checks if the algorithm should terminate at
            this depth.

    Returns:
        The value of the search path.
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    # For each possible move, traverse with given alpha/beta from previous recursions.
    val = NEG_INFINITY
    for move, new_board in get_next_moves_fn(board):
        val = max(val,
                  alpha_beta_min_recurse(new_board, depth - 1, eval_fn, alpha, beta,
                                         get_next_moves_fn, is_terminal_fn))

        alpha = max(val, alpha)

        # If Alpha > beta, this node will select some val >= alpha > beta and min player (above in tree) will then
        # select beta instead of val. Can finish early.
        if alpha >= beta:
            return val

    return val


def alpha_beta_min_recurse(board, depth, eval_fn, alpha, beta,
                           get_next_moves_fn=get_all_next_moves,
                           is_terminal_fn=is_terminal):
    """

    Args:
        board: A Connect4 game board object.
        depth: The depth to perform alpha_beta_recursively downwards.
        is_max:
        alpha:
        beta:
        eval_fn: An evaluation function for board states.
        get_next_moves_fn: A function that returns all possible next moves
        is_terminal_fn: A function that checks if the algorithm should terminate at
            this depth.

    Returns:
        The value of the search path.
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    # For each possible move, traverse with given alpha/beta from previous recursions.
    val = INFINITY
    for move, new_board in get_next_moves_fn(board):
        val = min(val,
                  alpha_beta_max_recurse(new_board, depth - 1, eval_fn, alpha, beta,
                                         get_next_moves_fn, is_terminal_fn))

        beta = min(val, beta)

        # If Alpha > beta, this node will select val <= beta < alpha and max player (above in tree) will then
        # select alpha instead of val. Can finish early.
        if alpha >= beta:
            return val

    return val


# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=8, eval_fn=focused_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search,
                               eval_fn=focused_evaluate, timeout=5)


# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.

def better_evaluate(board):
    raise NotImplementedError


# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)


# A player that uses alpha-beta and better_evaluate:
def my_player(board):
    return run_search_function(board, search_fn=alpha_beta_search,
                               eval_fn=better_evaluate, timeout=5)

# my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
