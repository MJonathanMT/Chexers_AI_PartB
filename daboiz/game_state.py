# Local imports
from daboiz import mcts_helper
from daboiz import update_helper as update
from daboiz import init_helper as init
from daboiz.hex import Hex
from daboiz.winstate import WinState
from daboiz import movement_helper as action

# Python imports
import copy
import random


class GameState:
    """
    Board class
    """

    def __init__(self, start, player, pieces_exited, pieces, adj_dict, enemies, goals, board_dict, own_pieces_exited):
        # ((Hex, "type"), (Hex, "type"),...)
        self.board = start
        # "red"/"green"/"blue"
        self.turn = player
        # (1, 2, 3) in order (r, g, b)
        self.pieces_exited = pieces_exited

        self.own_pieces_exited = own_pieces_exited

        # Used for eval function/heuristics
        self.pieces = pieces
        self.adj_dict = adj_dict
        self.enemies = enemies
        self.goals = goals
        self.board_dict = board_dict

    def update_player_data(self, colour, action):
        if action[0] == "MOVE":
            del self.board_dict[action[1][0]]
            self.board_dict[action[1][1]] = colour
            if colour == self.turn:
                self.pieces.remove(action[1][0])
                self.pieces.append(action[1][1])
            else:
                self.enemies.remove(action[1][0])
                self.enemies.append(action[1][1])

        elif action[0] == "JUMP":
            # TODO

            del self.board_dict[action[1][0]]
            self.board_dict[action[1][1]] = colour
            if colour == self.turn:
                self.pieces.remove(action[1][0])
                self.pieces.append(action[1][1])
            else:
                self.enemies.remove(action[1][0])
                self.enemies.append(action[1][1])

            # Changing the piece that was 'eaten'(jumped over) to the
            # colour of the piece making the jump
            eaten = update.find_eaten(action[1][0], action[1][1])
            prev_colour = self.board_dict[eaten]

            # If the 'eaten' piece is not the same colour as the
            # piece making the jump, it officially gets eaten
            if colour != prev_colour:
                self.board_dict[eaten] = colour
                if self.turn == colour:
                    self.pieces.append(eaten)
                    self.enemies.remove(eaten)
                elif self.turn == prev_colour:
                    self.pieces.remove(eaten)
                    self.enemies.append(eaten)

        elif action[0] == "EXIT":
            # TODO
            del self.board_dict[action[1]]
            if self.turn == colour:
                self.pieces.remove(action[1])
                self.own_pieces_exited += 1
            else:
                self.enemies.remove(action[1])

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
                        eaten_hex_coordinates = update.find_eaten(
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
                        print(updated_before_hex)
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
        new_state.update_player_data(new_state.turn, action)

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
        pieces_left = 0
        for hex in board:
            if hex[1] == self.turn:
                pieces_left += 1
            board_dict[hex[0].coordinates] = hex[1]

        all_actions = []
        if not pieces_left:
            all_actions.append(("PASS", None))

        # Loop through all Hexes in the board state and finds all the current
        # player's pieces, and gets all their possible actions
        for hex in board:
            if hex[1] == self.turn:
                # If a piece is in position to exit
                if hex[0].coordinates in init.get_finish(self.turn):
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
                    return 5
                else:
                    return -3
        return 0

    # def best_action(self, legal_actions):
    #     # Function to CHOOSE which action is the best from a list of ALL legal actions

    #     # Prioritise the legal moves
    #     all_exits = []
    #     for action in legal_actions:
    #         if (action[0] == "EXIT"):
    #             all_exits.append(action)
    #     if all_exits:
    #         best_action = random.choice(all_exits)

    #     # Create a dictionary for searching purposes
    #     board_dict = {}
    #     for hex in self.board:
    #         board_dict[hex[0].coordinates] = hex[1]

    #     # Get the best move possible for each piece
    #     best_moves = helper.get_moves(self, self.dist_dict)

    #     # Get the best jump possible for each piece
    #     best_jumps = helper.get_jumps(self, self.dist_dict)

    #     # Get the best action possible for each piece
    #     final_moves = helper.final_movements(
    #         self.dist_dict, best_moves, best_jumps)

    #     # Choose the best piece to move
    #     final_move = helper.get_piece(self.dist_dict, final_moves)
    #     if final_move == ():
    #         return action
    #     elif final_move[2] == 'move':
    #         action = ("MOVE", (str(final_move[0]), str(final_move[1])))
    #     elif final_move[2] == 'jump':
    #         action = ("JUMP", (str(final_move[0]), str(final_move[1])))
    #     return action

    #     # # Categorize all the legal moves into exits, jumps and moves
    #     # all_exits = []
    #     # all_jumps = []
    #     # all_moves = []
    #     # for action in legal_actions:
    #     #     if (action[0] == "EXIT"):
    #     #         all_exits.append(action)
    #     #     elif (action[0] == "JUMP"):
    #     #         all_jumps.append(action)
    #     #     if (action[0] == "MOVE"):
    #     #         all_moves.append(action)

    #     # # Prioritise the legal moves
    #     # # 1 - EXITS, 2 - JUMPS, 3 - MOVES
    #     # if all_exits:
    #     #     best_action = random.choice(all_exits)
    #     # elif all_jumps:
    #     #     best_action = random.choice(all_jumps)
    #     # elif all_moves:
    #     #     best_action = random.choice(all_moves)
    #     # else:
    #     #     best_action = ("PASS", None)

    #     # return best_action

    def best_action(self):
        if not self.pieces:
            return ("PASS", None)

        # Fill distance dictionary with the least distance from each goal
        dist_dict = action.create_dist_dict()
        for goal in self.goals:
            if goal in self.enemies:
                continue
            distance = 0
            dist_dict = action.distance_fill(self, dist_dict, goal, distance)

        # TODO: Decide what action to take.
        # attempt to protect pieces that are in dangered
        in_dangered = action.check_trouble(self)

        # try to attack/eat enemy first

        defensive_move = action.defensive_moves(self, in_dangered)
        final_move = ()
        if defensive_move:
            final_move = defensive_move
        else:
            for piece in self.pieces:
                final_move = action.attack_move(self, piece)
                if final_move:
                    break
        if not final_move:
            final_move = ("PASS", None)
        # If no more pieces, end turn:
        if not self.pieces:
            return final_move

        # Try exit move if possible
        for piece in self.pieces:

            total_count = len(self.pieces) + self.own_pieces_exited
            if piece in self.goals and total_count >= 4:
                final_action = ("EXIT", piece)
                return final_action

        if final_move[0] == "PASS":
            # Get the best move possible for each piece
            best_moves = action.get_moves(self, dist_dict)

            # Get the best jump possible for each piece
            best_jumps = action.get_jumps(self, dist_dict)

            # Get the best action possible for each piece
            final_moves = action.final_movements(
                dist_dict, best_moves, best_jumps)
            if len(self.pieces) > 5:
                # Choose the best piece to move
                final_move = action.get_piece(dist_dict, final_moves, "front")
            else:
                final_move = action.get_piece(dist_dict, final_moves, "back")

            if not final_move:
                final_move = ("PASS", None)
        if final_move[0] == "PASS":
            final_action = ("PASS", None)
        elif final_move[2] == 'move':
            final_action = ("MOVE", (final_move[0], final_move[1]))
        else:
            final_action = ("JUMP", (final_move[0], final_move[1]))
        return final_action
