# Local imports
from daboiz import mcts_helper
from daboiz import  helper
from daboiz.hex import Hex
from daboiz.winstate import WinState

# Python imports
import copy


class Board:
    """
    Board class
    """

    def __init__(self, start, player, pieces_exited):
        # ((Hex, "type"), (Hex, "type"),...)
        self.state = start
        # "red"/"green"/"blue"
        self.turn = player
        # (1, 2, 3) in order (r, g, b)
        self.pieces_exited = pieces_exited

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
            state =  prev_state
        else:
            state = ()
            if (action_type == "EXIT"):
                # Loop through all the hexes to look for hexes interacted
                i = 0
                while (i < len(prev_state)):
                    current_hex = Hex(action[1][0], action[1][1])

                    # Once we find the hex coordinates that the piece exited FROM
                    if (prev_state[i][0] == current_hex):
                        # Create a new (Hex, "updated type") and put in the state tuple
                        exit_hex = (prev_state[i][0], "empty")
                        state += (exit_hex,)

                    # Just append the other uninteracted hexes into state
                    else:
                        state += (prev_state[i],)
                    i += 1
                updated_pieces_exited = []
                if self.turn == "red":
                    updated_pieces_exited.append(self.pieces_exited[0] + 1)
                    updated_pieces_exited.append(self.pieces_exited[1])
                    updated_pieces_exited.append(self.pieces_exited[2])
                elif self.turn == "green":
                    updated_pieces_exited.append(self.pieces_exited[0])
                    updated_pieces_exited.append(self.pieces_exited[1] + 1)
                    updated_pieces_exited.append(self.pieces_exited[2])  
                elif self.turn == "blue":
                    updated_pieces_exited.append(self.pieces_exited[0])
                    updated_pieces_exited.append(self.pieces_exited[1])
                    updated_pieces_exited.append(self.pieces_exited[2] + 1)

                self.pieces_exited = tuple(updated_pieces_exited)           

            # When action is JUMP or MOVE
            else:
                before_hex = Hex(action[1][0][0], action[1][0][1])
                next_hex = Hex(action[1][1][0], action[1][1][1])

                # Loop through all the hexes to look for hexes interacted
                i = 0
                while (i < len(prev_state)):

                    # If the action was a JUMP, we need to change the piece that was jumped over to the colour
                    # of the piece that jumped (it got EATEN!)
                    if (action_type == "JUMP"):
                        eaten_hex_coordinates = helper.find_eaten(
                            before_hex.coordinates, next_hex.coordinates)
                        eaten_hex = Hex(
                            eaten_hex_coordinates[0], eaten_hex_coordinates[1])
                        if (prev_state[i][0] == eaten_hex):
                            updated_eaten_hex = (prev_state[i][0], self.turn)
                            state += (updated_eaten_hex,)
                            i += 1
                            continue

                    # Once we find the hex coordinates that the piece acted FROM
                    if (prev_state[i][0] == before_hex):
                        # Create a new (Hex, "updated type") and put in the state tuple
                        updated_before_hex = (prev_state[i][0], "empty")
                        state += (updated_before_hex,)
                    # Once we find the hex coordinates that the piece acted TO
                    elif (prev_state[i][0] == next_hex):
                        # Create a new (Hex, "updated type") and put in the state tuple
                        updated_next_hex = (prev_state[i][0], self.turn)
                        state += (updated_next_hex,)
                    # Just append the other uninteracted hexes into state
                    else:
                        state += (prev_state[i],)
                    i += 1

             # Sort the board by Hex
            state = tuple(
                sorted(state, key=lambda hex: (hex[0].coordinates)))
        

        self.update_turn(self.turn)
        return state


    def update_turn(self, current_player):
        if current_player == "red":
            self.turn = "green"
        elif current_player == "green":
            self.turn = "blue"
        elif current_player == "blue":
            self.turn = "red"

    def legal_actions(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.

        state = state_history[-1]


        # Create a dictionary for searching purposes
        board_dict = {}
        for hex in state:
            board_dict[hex[0].coordinates] = hex[1]

        
        all_actions = []

        # Loop through all Hexes in the board state and finds all the current
        # player's pieces, and gets all their possible actions
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

    def winner(self):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        for colour_exited in self.pieces_exited:
            if colour_exited >= 4:
                if self.pieces_exited.index(colour_exited) == 0:
                    return WinState.RED
                elif self.pieces_exited.index(colour_exited) == 1:
                    return WinState.GREEN
                elif self.pieces_exited.index(colour_exited) == 2:
                    return WinState.BLUE
        return WinState.ONGOING


