from daboiz import helper
from daboiz import mcts_helper
from daboiz.game_state import GameState
from daboiz.montecarlo import mcts


class Player:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.
        The parameter colour will be a string representing the player your
        program will play as (Red, Green or Blue). The value will be one of the
        strings "red", "green", or "blue" correspondingly.
        """

        # Set up starting coordinates of pieces, and goals for our pieces
        self.colour = colour
        self.pieces = helper.get_start(colour)
        self.goals = helper.get_finish(colour)
        self.all_pieces_exited = (0, 0, 0)

        # Set up our representation of the game_board
        self.board_dict = helper.initiate_board()

        # Get all available adjacent hexes within the board range
        empty_dict = {}
        self.adj_dict = helper.get_adjacent((0, 0), empty_dict)

        # Create an unvisited distance dictionary
        self.dist_dict = helper.create_dist_dict()

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. If there are no allowed
        actions, your player must return a pass instead. The action (or pass)
        must be represented based on the above instructions for representing
        actions.
        """

        initial_state = GameState(mcts_helper.convert_board(
            self.board_dict), self.colour, self.all_pieces_exited)
        monte_carlo = mcts(time_limit=1000)
        action = monte_carlo.search(initial_state=initial_state)

        return action

    # def action(self):
        # """
        # This method is called at the beginning of each of your turns to request
        # a choice of action from your program.

        # Based on the current state of the game, your player should select and
        # return an allowed action to play on this turn. If there are no allowed
        # actions, your player must return a pass instead. The action (or pass)
        # must be represented based on the above instructions for representing
        # actions.
        # """
    #     # Fill distance dictionary with the least distance from each goal
    #     dist_dict = self.dist_dict
    #     for goal in self.goals:
    #         distance = 0
    #         dist_dict = helper.distance_fill(self, dist_dict, goal, distance)

    #     action = ("PASS", None)
    #     for piece in self.pieces:
    #         if piece in self.goals:
    #             action = ("EXIT", piece)
    #             self.pieces.remove(piece)
    #             return action

    #     # Get the best move possible for each piece
    #     best_moves = helper.get_moves(self, dist_dict)

    #     # Get the best jump possible for each piece
    #     best_jumps = helper.get_jumps(self, dist_dict)

    #     # Get the best action possible for each piece
    #     final_moves = helper.final_movements(dist_dict, best_moves, best_jumps)

    #     # Choose the best piece to move
    #     final_move = helper.get_piece(dist_dict, final_moves)
    #     if final_move == ():
    #         return action
    #     elif final_move[2] == 'move':
    #         action = ("MOVE", (str(final_move[0]), str(final_move[1])))
    #     elif final_move[2] == 'jump':
    #         action = ("JUMP", (str(final_move[0]), str(final_move[1])))
    #     return action

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.
        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red",
        "green", or "blue" correspondingly.
        The parameter action is a representation of the most recent action (or
        pass) conforming to the above in- structions for representing actions.
        You may assume that action will always correspond to an allowed action
        (or pass) for the player colour (your method does not need to validate
        the action/pass against the game rules).
        """

        if action[0] == "MOVE":
            del self.board_dict[action[1][0]]
            self.board_dict[action[1][1]] = colour
            if colour == self.colour:
                self.pieces.remove(action[1][0])
                self.pieces.add(action[1][1])

        elif action[0] == "JUMP":

            del self.board_dict[action[1][0]]
            self.board_dict[action[1][1]] = colour
            if colour == self.colour:
                self.pieces.remove(action[1][0])
                self.pieces.add(action[1][1])

            # Changing the piece that was 'eaten'(jumped over) to the
            # colour of the piece making the jump
            eaten = helper.find_eaten(action[1][0], action[1][1])
            prev_colour = self.board_dict[eaten]

            # If the 'eaten' piece is not the same colour as the
            # piece making the jump, it officially gets eaten
            if colour != prev_colour:
                self.board_dict[eaten] = colour
                if self.colour == colour:
                    self.pieces.add(eaten)
                elif self.colour == prev_colour:
                    self.pieces.remove(eaten)

        elif action[0] == "EXIT":
            del self.board_dict[action[1]]
            if self.colour == colour:
                self.pieces.remove(action[1])

                all_pieces_exited = []
                if self.colour == "red":
                    all_pieces_exited.append(self.all_pieces_exited[0] + 1)
                    all_pieces_exited.append(self.all_pieces_exited[1])
                    all_pieces_exited.append(self.all_pieces_exited[2])
                elif self.colour == "green":
                    all_pieces_exited.append(self.all_pieces_exited[0])
                    all_pieces_exited.append(self.all_pieces_exited[1] + 1)
                    all_pieces_exited.append(self.all_pieces_exited[2])
                elif self.colour == "blue":
                    all_pieces_exited.append(self.all_pieces_exited[0])
                    all_pieces_exited.append(self.all_pieces_exited[1])
                    all_pieces_exited.append(self.all_pieces_exited[2] + 1)
                self.all_pieces_exited = tuple(all_pieces_exited)

    # def __init__(self, colour):
    #     """
    #     This method is called once at the beginning of the game to initialise
    #     your player. You should use this opportunity to set up your own internal
    #     representation of the game state, and any other information about the
    #     game state you would like to maintain for the duration of the game.
    #     The parameter colour will be a string representing the player your
    #     program will play as (Red, Green or Blue). The value will be one of the
    #     strings "red", "green", or "blue" correspondingly.
    #     """
    #     # Zach's MCTS version
    #     self.colour = colour
    #     self.pieces = helper.get_start(colour)
    #     self.goals = helper.get_finish(colour)
    #     self.pieces_exited = 0

    #     self.game_state = GameState()
