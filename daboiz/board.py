# Local imports
from daboiz import mcts_helper
from daboiz import  helper


class Board:
    """
    Board class
    """

    num_players = 3

    def __init__(self, start):
        self.state = start
        self.turn = "red"

    def starting_state(self):
        # Returns a representation of the starting state of the game.
        return self.state

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

    def legal_actions(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.

        state = state_history[-1]
        print("state is ")
        print(state)

        # Create a dictionary for searching purposes
        board_dict = {}
        for hex in state:
            board_dict[hex[0].coordinates] = hex[1]
            # print(hex)
        
        all_actions = []

        # Loop through all Hexes in the board state and finds all the current
        # player's pieces,  and gets all their possible actions
        for hex in state:
            if hex[1] == self.turn:
                # If a piece is in position to exit
                if hex[0].coordinates in helper.get_finish(self.turn):
                    all_actions.append(("EXIT", hex[0].coordinates))

                # Get all 6 adjacent hexes of the current hex
                current_hex_adjacents = mcts_helper.get_adjacent(hex[0].coordinates)
                for adj in current_hex_adjacents:
                    print("adjacent is of type")
                    # print(board_dict[adj])
                    print(adj)
                    print(board_dict[adj])

                    # Check if MOVE action is possible for all adj hexes, append if yes
                    if board_dict[adj] == "empty":
                        all_actions.append(("MOVE", (hex[0].coordinates, adj)))
                    # Otherwise check if JUMP action is possible, append if yes
                    else:
                        hex_landed = mcts_helper.hex_after_jump(hex[0].coordinates, adj)
                        if board_dict[hex_landed] == "empty":
                            all_actions.append(("JUMP", (hex[0].coordinates, hex_landed)))
        
        return all_actions

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass
