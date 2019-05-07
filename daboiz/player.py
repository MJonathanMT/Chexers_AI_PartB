def get_finish(colour):
    """
    This function returns a list of all the available goals
    that the pieces can exit from
    :param colour: The colour of the player's pieces
    :return: A set of all the available goals
    """
    if colour == 'red':
        finish = {(3, -3), (3, -2), (3, -1), (3, 0)}
    elif colour == 'blue':
        finish = {(0, -3), (-1, -2), (-2, -1), (-3, 0)}
    elif colour == 'green':
        finish = {(-3, 3), (-2, 3), (-1, 3), (0, 3)}

    # Returns the final list of end_points/goals
    return finish


def get_start(colour):
    """
    This function returns a list of all the starting coordinates
    of the pieces
    :param colour: The colour of the player's pieces
    :return: A set of the starting coordinates
    """
    if colour == 'red':
        start = {(-3, 3), (-3, 2), (-3, 1), (-3, 0)}
    elif colour == 'blue':
        start = {(0, -3), (1, -3), (2, -3), (3, -3)}
    elif colour == 'green':
        start = {(3, 0), (2, 1), (1, 2), (0, 3)}

    # Returns the final list of end_points/goals
    return start


def initiate_board():
    """
    This function initiates our representation of the game board
    :return: A set of the starting coordinates
    """

    board_dict = {}
    ran = range(-3, 4)
    for (q, r) in [(q, r) for q in ran for r in ran if -q - r in ran]:
        if q == -3 and r >= 0:
            board_dict[(q, r)] = "red"
        elif q >= 0 and r == -3:
            board_dict[(q, r)] = "green"
        elif q+r == 3:
            board_dict[(q, r)] = "blue"

    # Returns the final list of end_points/goals
    return board_dict


def find_eaten(before_jump, after_jump):
    """
    This function finds the coordinates of the piece that was 'eaten'
    :return: The coordinate of the 'eaten' piece
    """
    eaten = ()
    eaten[0] = (after_jump[0] - before_jump[0])/2
    eaten[1] = (after_jump[1] - before_jump[1])/2

    return eaten


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
        self.pieces = get_start(colour)
        self.goals = get_finish(colour)
        self.pieces_exited = 0

        # Set up our representation of the game_board
        self.board_dict = initiate_board()

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
        # TODO: Decide what action to take.
        return ("PASS", None)

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
        # TODO: Update state representation in response to action.

        if action[0] == "MOVE":
            self.board_dict[action[1][0]] = ""
            self.board_dict[action[1][1]] = colour
            if (colour == self.colour):
                self.pieces.remove(action[1][0])
                self.pieces.add(action[1][1])

        elif action[0] == "JUMP":
            # TODO
            self.board_dict[action[1][0]] = ""
            self.board_dict[action[1][1]] = colour
            if (colour == self.colour):
                self.pieces.remove(action[1][0])
                self.pieces.add(action[1][1])

            # Changing the piece that was 'eaten'(jumped over) to the colour of the piece making the jump
            eaten = find_eaten(action[1][0], action[1][1])
            prev_colour = board_dict[eaten]

            # If the 'eaten' piece is not the same colour as the piece making the jump, it officially gets eaten
            if colour != prev_colour:
                board_dict[eaten] = colour
                if self.colour == colour:
                    self.pieces.add(eaten)
                elif self.colour == prev_colour:
                    self.pieces.remove(eaten)

        elif action[0] == "EXIT":
            # TODO
            self.board_dict[action[1]] = ""
            if (self.colour == colour):
                self.pieces_exited += 1
