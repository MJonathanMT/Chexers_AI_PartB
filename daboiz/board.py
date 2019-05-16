# Local imports
import daboiz.helper as helper

# Only one instance of Board


class Board:

    num_players = 3

    def __init__(self):
        self.board = helper.initiate_board()
        self.turn = "red"

    def start(self):
        # Returns a representation of the starting state of the game.
        return helper.initiate_board()

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        return self.turn

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        pass

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        pass

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass
