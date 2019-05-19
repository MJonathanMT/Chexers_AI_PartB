# Local imports
import mcts_helper


class Board:
    """
    Board class
    """

    num_players = 3

    def __init__(self):
        self.board = mcts_helper.initiate_board()
        self.turn = "red"

    def starting_state(self):
        # Returns a representation of the starting state of the game.
        return self.board

    def current_player(self):
        # Returns the current player colour
        return self.turn

    def next_state(self, prev_state, action):
        # Takes the game state, and the action to be applied.
        # Returns the new game state.
        action_type = action[0]
        if action_type == "PASS":
            return prev_state
        else:
            # Pass the work to a helper function
            return mcts_helper.update_board(prev_state, action, self.turn)

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.

        state = state_history[-1]
        
        pass

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass
