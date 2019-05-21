import daboiz.movement_helper as action
import daboiz.update_helper as update
import daboiz.init_helper as init


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
        # TODO: Set up state representation.

        # Set up starting coordinates of pieces, and goals for our pieces
        self.colour = colour
        self.pieces = init.get_start(colour)
        self.goals = init.get_finish(colour)
        self.pieces_exited = 0
        self.all_pieces_exited = (0, 0, 0)

        # Set up our representation of the game_board
        self.board_dict = init.initiate_board()

        # Get all available adjacent hexes within the board range
        empty_dict = {}
        self.adj_dict = init.get_adjacent((0, 0), empty_dict)

        self.enemies = init.get_enemies(self)

    # def action(self):
    #     """
    #     This method is called at the beginning of each of your turns to request
    #     a choice of action from your program.

    #     Based on the current state of the game, your player should select and
    #     return an allowed action to play on this turn. If there are no allowed
    #     actions, your player must return a pass instead. The action (or pass)
    #     must be represented based on the above instructions for representing
    #     actions.
    #     """

    #     initial_state = GameState(mcts_helper.convert_board(
    #         self.board_dict), self.colour, self.all_pieces_exited)
    #     monte_carlo = mcts(time_limit=1000)
    #     action = monte_carlo.search(initial_state=initial_state)

    #     return action

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
        if not self.pieces:
            return ("PASS", None)

        # Update our own dist_dict every time it's our turn
        for goal in self.goals:
            self.dist_dict = action.distance_fill(
                self, self.dist_dict, goal, 0)

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
        print(in_dangered)

        # try to attack/eat enemy first

        defensive_move = action.defensive_moves(self, in_dangered)
        final_move = ()
        if defensive_move:
            final_move = defensive_move
            print("defensive move is " + str(defensive_move))
        else:
            for piece in self.pieces:
                final_move = action.attack_move(self, piece)
                if final_move:
                    break
            print("attacking move is "+str(final_move))
        if not final_move:
            final_move = ("PASS", None)
        # If no more pieces, end turn:
        if not self.pieces:
            return final_move

        # Try exit move if possible
        for piece in self.pieces:

            total_count = len(self.pieces) + self.pieces_exited
            if piece in self.goals and total_count >= 4:
                final_action = ("EXIT", piece)
                return final_action

        if final_move[0] == "PASS":
            # Get the best move possible for each piece
            best_moves = action.get_moves(self, dist_dict)
            print("ALL BEST MOVES = "+str(best_moves))

            # Get the best jump possible for each piece
            best_jumps = action.get_jumps(self, dist_dict)
            print("ALL BEST JUMPS = "+str(best_jumps))

            # Get the best action possible for each piece
            final_moves = action.final_movements(
                dist_dict, best_moves, best_jumps)
            print("ALL FINAL MOVES = "+str(final_moves))
            if len(self.pieces) > 5:
                # Choose the best piece to move
                final_move = action.get_piece(dist_dict, final_moves, "front")
            else:
                final_move = action.get_piece(dist_dict, final_moves, "back")

            print("final move is "+str(final_move))
            if not final_move:
                final_move = ("PASS", None)
        if final_move[0] == "PASS":
            final_action = ("PASS", None)
        elif final_move[2] == 'move':
            final_action = ("MOVE", (final_move[0], final_move[1]))
        else:
            final_action = ("JUMP", (final_move[0], final_move[1]))
        return final_action

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
                self.pieces.append(action[1][1])

        elif action[0] == "JUMP":

            del self.board_dict[action[1][0]]
            self.board_dict[action[1][1]] = colour
            if colour == self.colour:
                self.pieces.remove(action[1][0])
                self.pieces.append(action[1][1])

            # Changing the piece that was 'eaten'(jumped over) to the
            # colour of the piece making the jump
            eaten = update.find_eaten(action[1][0], action[1][1])
            prev_colour = self.board_dict[eaten]

            # If the 'eaten' piece is not the same colour as the
            # piece making the jump, it officially gets eaten
            if colour != prev_colour:
                self.board_dict[eaten] = colour
                if self.colour == colour:
                    self.pieces.append(eaten)
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


def print_board(board_dict, message="Testing Board Condition", debug=False):
    """
    Helper function to print a drawing of a hexagonal board's contents.
    Arguments:
    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.
    Keyword arguments:
    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3 + 1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board)
