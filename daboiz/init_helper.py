def get_finish(colour):
    """
    This function returns a list of all the available goals
    that the pieces can exit from
    :param colour: The colour of the player's pieces
    :return: A set of all the available goals
    """
    finish = {}
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
    start = []
    if colour == 'red':
        start = [(-3, 3), (-3, 2), (-3, 1), (-3, 0)]
    elif colour == 'green':
        start = [(0, -3), (1, -3), (2, -3), (3, -3)]
    elif colour == 'blue':
        start = [(3, 0), (2, 1), (1, 2), (0, 3)]

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


def get_adjacent(pos, adj_dict):
    """
    This function returns all the adjacent hexes of each hex within the board
    :param pos: Position/coordinate of the current hex
    :param adj_dict: Dictionary with each hex being the key and all the adjacent
     hexes of the hex as the value
    :return: adj_dict: Complete dictionary of the adjacent hexes of all hex
     within the board
    """
    # If the current position is already a key in adj_dict, exit the recursion
    if pos in adj_dict:
        return adj_dict

    all_moves = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    pos_val = []
    # Iterate through all moves to check if its within the board
    for move in all_moves:
        q = pos[0] + move[0]
        r = pos[1] + move[1]
        # If it is not within the board range, skip this move (continue)
        if not (abs(q) <= 3 and abs(r) <= 3 and abs(q+r) <= 3):
            continue

        # next_pos is the current position + the move
        next_pos = (q, r)

        # add the next position to the value of the current position
        pos_val.append(next_pos)

    # pass the list of all possible moves to the dictionary with the key as the
    # current position
    adj_dict[pos] = pos_val

    # Recurse through each adjacent hex of the current hex
    for val in pos_val:
        get_adjacent(val, adj_dict)

    # returns final dictionary of all adjacent hexes
    return adj_dict


def get_enemies(self):
    enemies = []
    for piece in self.board_dict:
        if piece not in self.pieces:
            enemies.append(piece)
    return enemies

def get_corners():
    corners = [[], []]
    corners[0] = [(0, -3), (3, -3), (3, 0), (0, 3), (-3, 3), (-3, 0)]
    corners[1] =[(1, -3), (2, -3), (3, -2), (3, -1), (2, 1), (1, 2),
                 (-1, 3), (-2, 3), (-3, 2), (-3, 1), (-2, -1), (-1, -2)]
    return corners

