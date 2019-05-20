# Local imports
from daboiz import mcts_helper
from daboiz import helper
from daboiz.hex import Hex
from daboiz.winstate import WinState

# Python imports
import copy


class GameState:
    """
    Board class
    """

    def __init__(self, start, player, pieces_exited):
        # ((Hex, "type"), (Hex, "type"),...)
        self.board = start
        # "red"/"green"/"blue"
        self.turn = player
        # (1, 2, 3) in order (r, g, b)
        self.pieces_exited = pieces_exited

    def current_player(self):
        # Returns the current player colour
        return self.turn

    def next_state(self, action):
        # Takes the game state, and the action to be applied.
        # Returns the new game state.

        new_state = copy.deepcopy(self)
        new_board = []
        if action[0] == "PASS":
            new_board = self.board
            new_state.pieces_exited = self.pieces_exited
            # state =  prev_state
        else:
            # state = ()
            if (action[0] == "EXIT"):
                # Loop through all the hexes to look for hexes interacted
                i = 0
                while (i < len(self.board)):
                    current_hex = Hex(action[1][0], action[1][1])

                    # Once we find the hex coordinates that the piece exited FROM
                    if (self.board[i][0] == current_hex):
                        # Create a new (Hex, "updated type") and put in the state tuple
                        exit_hex = (self.board[i][0], "empty")
                        new_board.append(exit_hex)
                        # state += (exit_hex,)

                    # Just append the other uninteracted hexes into state
                    else:
                        new_board.append(self.board[i])
                        # state += (prev_state[i],)
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

                new_state.pieces_exited = tuple(updated_pieces_exited)

            # When action is JUMP or MOVE
            else:
                before_hex = Hex(action[1][0][0], action[1][0][1])
                next_hex = Hex(action[1][1][0], action[1][1][1])

                # Loop through all the hexes to look for hexes interacted
                i = 0
                while (i < len(self.board)):

                    # If the action was a JUMP, we need to change the piece that was jumped over to the colour
                    # of the piece that jumped (it got EATEN!)
                    if (action[0] == "JUMP"):
                        eaten_hex_coordinates = helper.find_eaten(
                            before_hex.coordinates, next_hex.coordinates)
                        eaten_hex = Hex(
                            eaten_hex_coordinates[0], eaten_hex_coordinates[1])
                        if (self.board[i][0] == eaten_hex):
                            updated_eaten_hex = (self.board[i][0], self.turn)
                            new_board.append(updated_eaten_hex)
                            # state += (updated_eaten_hex,)
                            i += 1
                            continue

                    # Once we find the hex coordinates that the piece acted FROM
                    if (self.board[i][0] == before_hex):
                        # Create a new (Hex, "updated type") and put in the state tuple
                        updated_before_hex = (self.board[i][0], "empty")
                        new_board.append(updated_before_hex)
                        # state += (updated_before_hex,)
                    # Once we find the hex coordinates that the piece acted TO
                    elif (self.board[i][0] == next_hex):
                        # Create a new (Hex, "updated type") and put in the state tuple
                        updated_next_hex = (self.board[i][0], self.turn)
                        new_board.append(updated_next_hex)
                        # state += (updated_next_hex,)
                    # Just append the other uninteracted hexes into state
                    else:
                        new_board.append(self.board[i])
                        # state += (prev_state[i],)
                    new_state.pieces_exited = self.pieces_exited
                    i += 1

            # Sort the board by Hex
            new_board.sort(key=lambda hex: hex[0].coordinates)
            new_board = tuple(new_board)
            # state = tuple(
            #     sorted(state, key=lambda hex: (hex[0].coordinates)))

        new_state.board = new_board
        new_state.update_turn(self.turn)

        return new_state

    def update_turn(self, current_player):
        if current_player == "red":
            self.turn = "green"
        elif current_player == "green":
            self.turn = "blue"
        elif current_player == "blue":
            self.turn = "red"

    def legal_actions(self):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.

        board = self.board

        # Create a dictionary for searching purposes
        board_dict = {}
        # i = 0
        for hex in board:
            board_dict[hex[0].coordinates] = hex[1]
            # print("Coordinate is")
            # print(hex[0].coordinates)
            # print("hex type is")
            # print(hex[1])
            # i += 1
            # print(i)
        all_actions = []

        # Loop through all Hexes in the board state and finds all the current
        # player's pieces, and gets all their possible actions
        for hex in board:
            if hex[1] == self.turn:
                # If a piece is in position to exit
                if hex[0].coordinates in helper.get_finish(self.turn):
                    all_actions.append(("EXIT", hex[0].coordinates))

                # Get all 6 adjacent hexes of the current hex
                current_hex_adjacents = mcts_helper.get_adjacent(
                    hex[0].coordinates)
                for adj in current_hex_adjacents:
                    # print("adjacent is ")
                    # print(adj)
                    # Check if MOVE action is possible for all adj hexes, append if yes
                    if board_dict[adj] == "empty":
                        all_actions.append(("MOVE", (hex[0].coordinates, adj)))
                    # Otherwise check if JUMP action is possible, append if yes
                    else:
                        if not mcts_helper.hex_after_jump(hex[0].coordinates, adj) == 0:
                            hex_landed = mcts_helper.hex_after_jump(
                                hex[0].coordinates, adj)
                            if board_dict[hex_landed] == "empty":
                                all_actions.append(
                                    ("JUMP", (hex[0].coordinates, hex_landed)))
        print("legal actions are")
        print(all_actions)
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

    def is_terminal(self):
        # Check if any colour has already gotten 4 pieces off the board
        for colour_exited in self.pieces_exited:
            if colour_exited >= 4:
                return 1
        # Check if there are any self pieces left on the board
        self_pieces_remaining = 0
        for hex in self.board:
            if hex[1] == self.turn:
                self_pieces_remaining = 1
        return not self_pieces_remaining

    def get_reward(self):
        player_index = 0
        if self.turn == "red":
            player_index = 0
        elif self.turn == "green":
            player_index = 1
        elif self.turn == "blue":
            player_index = 2

        for colour_exited in self.pieces_exited:
            if colour_exited >= 4:
                if self.pieces_exited.index(colour_exited) == player_index:
                    return 1
                else:
                    return 0
        return 0
