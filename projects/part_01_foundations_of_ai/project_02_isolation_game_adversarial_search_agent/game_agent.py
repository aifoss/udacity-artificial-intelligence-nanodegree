"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    return squared_num_moves_diff_score(game, player)

def custom_score_2(game, player):
    return one_step_look_ahead_score(game, player)

def custom_score_3(game, player):
    return num_moves_ratio_score(game, player)


"""
One-Step Look-Ahead Heuristic:
This heuristic forecasts each of legal moves for either player or opponent, 
depending on who is the active player at the game state,
calculates weighted number of moves according to the next state that the move leads to,
and returns the difference between weighted average numbers of moves as the score.
In case player is the active player in the current game state,
the score reflects how good the next forecast state can be for the player.
In case player is the inactive player in the current game state,
the score reflets how bad the next forecast state can be for the player. 
"""
def one_step_look_ahead_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # if game outcome is already decided, return corresponding score
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    # get legal moves for player and opponent
    opponent = game.get_opponent(player)
    
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)
    
    num_own_moves = len(own_moves)
    num_opp_moves = len(opp_moves)
    
    # if no legal moves for either player or opponent, return corresponding score
    if num_own_moves == 0:
        return float("-inf")
    if num_opp_moves == 0:
        return float("inf")
    
    # check next game states with each of legal moves for player or opponent, depending on who is active
    weighted_num_own_moves = 0
    weighted_num_opp_moves = 0
    
    favorable_move_weight = 10
    unfavorable_move_weight = -10
    
    if player == game.active_player:
        for own_move in own_moves:
            next_state = game.forecast_move(own_move) # player is now inactive
            
            if next_state.is_winner(player): # opponent has no moves
                weighted_num_own_moves += favorable_move_weight
            elif not next_state.get_legal_moves(player): # player has no moves
                weighted_num_own_moves += unfavorable_move_weight
            else:
                weighted_num_own_moves += compute_num_move_diff(next_state, player, opponent)
    else:
        for opp_move in opp_moves:
            next_state = game.forecast_move(opp_move) # player is now active
            
            if next_state.is_winner(opponent): # player has no moves
                weighted_num_opp_moves += favorable_move_weight
            elif not next_state.get_legal_moves(opponent): # opponent has no moves
                weighted_num_opp_moves += unfavorable_move_weight
            else:
                weighted_num_opp_moves += compute_num_move_diff(next_state, opponent, player)
                    
    # calculate the difference between weighted average number of player moves and number of opponent moves
    own_move_weight_avg = float(weighted_num_own_moves) / float(num_own_moves) # 0 if player is inactive
    opp_move_weight_avg = float(weighted_num_opp_moves) / float(num_opp_moves) # 0 if player is active
    weighted_num_move_diff = float(own_move_weight_avg - opp_move_weight_avg)
    
    return weighted_num_move_diff

def compute_num_move_diff(game, player_1, player_2):
    num_player_1_moves = len(game.get_legal_moves(player_1))
    num_player_2_moves = len(game.get_legal_moves(player_2))
    return float(num_player_1_moves - num_player_2_moves)


"""
Squared Num-Moves-Diff Heuristic:
This heuristic computes the squared difference between the number of legal moves
for the player and the number of legal moves for the opponent.
"""
def squared_num_moves_diff_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # if game outcome is already decided, return corresponding score
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    # get legal moves for player and opponent
    opponent = game.get_opponent(player)
    
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)
    
    num_own_moves = len(own_moves)
    num_opp_moves = len(opp_moves)
    
    # if no legal moves for either player or opponent, return corresponding score
    if num_own_moves == 0:
        return float("-inf")
    if num_opp_moves == 0:
        return float("inf")
    
    return float(num_own_moves**2 - num_opp_moves**2)


"""
Num-Moves-Ratio Heuristic:
This heuristic computes the ratio of the number of legal moves for the player
to the number of legal moves for the opponent.
"""
def num_moves_ratio_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # if game outcome is already decided, return corresponding score
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    # get legal moves for player and opponent
    opponent = game.get_opponent(player)
    
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)
    
    num_own_moves = len(own_moves)
    num_opp_moves = len(opp_moves)
    
    # if no legal moves for either player or opponent, return corresponding score
    if num_own_moves == 0:
        return float("-inf")
    if num_opp_moves == 0:
        return float("inf")
    
    return float(num_own_moves) / float(num_opp_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = (-1, -1)

        try:
            return self.minimax(game, self.search_depth)
        except SearchTimeout:
            pass
        return best_move
    
    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        
        return self.mm(game, depth, True)[0]
    
    def mm(self, game, depth, maximizing=True):
        """
        Get best move and score according to the depth-limited minimax algorithm.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return (game.get_player_location(self), self.score(game, self))
        
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return ((-1, -1), self.score(game, self))
        
        best_move = (-1, -1)    
        
        if maximizing:
            best_score = float("-inf")
            for move in legal_moves:
                next_state = game.forecast_move(move)
                _, score = self.mm(next_state, depth-1, False)
                if score > best_score:
                    best_move = move
                    best_score = score
        else:
            best_score = float("inf")
            for move in legal_moves:
                next_state = game.forecast_move(move)
                _, score = self.mm(next_state, depth-1, True)
                if score < best_score:
                    best_move = move
                    best_score = score
        
        return (best_move, best_score)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)
        max_depth = 100
        
        for depth in range(1, max_depth+1):
            try:
                best_move = self.alphabeta(game, depth)
            except SearchTimeout:
                break

        return best_move
    
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        
        return self.ab(game, depth, alpha, beta, True)[0]
        
    def ab(self, game, depth, alpha, beta, maximizing=True):
        """
        Get best move and score according to the depth-limited minimax algorithm
        using alpha-best pruning.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return (game.get_player_location(self), self.score(game, self))
        
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return ((-1, -1), self.score(game, self))
        
        best_move = (-1, -1)
 
        if maximizing:
            best_score = float("-inf")

            for move in legal_moves:
                next_state = game.forecast_move(move)
                _, score = self.ab(next_state, depth-1, alpha, beta, False)
                
                if score > best_score:
                    best_move, best_score = move, score

                if best_score >= beta:
                    return (best_move, best_score)
                else:
                    alpha = max(alpha, best_score)
        else:
            best_score = float("inf")

            for move in legal_moves:
                next_state = game.forecast_move(move)
                _, score = self.ab(next_state, depth-1, alpha, beta, True)
                
                if score < best_score:
                    best_move, best_score = move, score
                
                if best_score <= alpha:
                    return (best_move, best_score)
                else:
                    beta = min(beta, best_score)
                
        return (best_move, best_score)
