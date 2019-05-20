# Library imports
from operator import itemgetter

# Local imports
from daboiz.hex import Hex
from daboiz import helper

# Tested
def initiate_board():
    """
    This function initiates our representation of the game board
    :return: A tuple of the starting coordinates with their corresponding attribute
      ((Hex, "type"), (Hex, "type")....., (Hex, "type"))
    """

    # board = ()
    # ran = range(-3, 4)
    # for (q, r) in [(q, r) for q in ran for r in ran if -q - r in ran]:
    #     hex = Hex(q, r)
    #     if q == -3 and r >= 0:
    #         new_hex = (hex, "red")
    #     elif q >= 0 and r == -3:
    #         new_hex = (hex, "green")
    #     elif q+r == 3:
    #         new_hex = (hex, "blue")
    #     else:
    #         new_hex = (hex, "empty")
    #     board += (new_hex,)

    # # For testing purposes:
    board = ()
    ran = range(0, 3)
    for r in ran:
        hex = Hex(0, r)
        if r == 0:
            new_hex = (hex, "red")
        elif r == 1:
            new_hex = (hex, "green")
        else:
            new_hex = (hex, "empty")
        board += (new_hex,)
    # for (q, r) in [(q, r) for q in ran for r in ran]:
    #     hex = Hex(q, r)
    #     if q == 0:
    #         new_hex = (hex, "red")
    #     else:
    #         new_hex = (hex, "green")
    #     board += (new_hex,)

    # Sort the board by Hex
    board = tuple(sorted(board, key=lambda hex: (hex[0].coordinates)))

    # Returns the final list of end_points/goals
    return board


def get_adjacent(current):
    """
    This function returns all the adjacent hexes of each hex within the board
    :param pos: Position/coordinate of the current hex
    :param adj_dict: Dictionary with each hex being the key and all the adjacent
     hexes of the hex as the value
    :return: adj_dict: Complete dictionary of the adjacent hexes of all hex
     within the board
    """

    all_moves = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    adjacent_list = []
    # Iterate through all moves to check if its within the board
    for move in all_moves:
        next_q = current[0] + move[0]
        next_r = current[1] + move[1]
        # If it is not within the board range, skip this move (continue)
        if not (abs(next_q) <= 3 and abs(next_r) <= 3 and abs(next_q+next_r) <= 3):
            continue

        ### TESTING PURPOSES ###
        # # TODO: remove this when submitting
        # if not (abs(next_q) == 0 and next_r < 3 and next_r >= 0):
        #     continue

        # add the next position to the value of the current position
        adjacent_list.append((next_q, next_r))

    # returns list of all adjacent hexes of the current hex (disregard if adjacents are blocked or not)
    return adjacent_list

def hex_after_jump(hex_before, hex_eaten):
    """
    This function returns the coordinates for the hex where a piece lands after it does a JUMP action
    :param hex_before: Coordinates of the jumping piece before the jump
    :param hex_eaten: Coordinates of the hex being jumped over
    :return: hex_landed: Coordinates of the jumping piece after the jump
    """

    q_jump = hex_eaten[0] - hex_before[0]
    r_jump = hex_eaten[1] - hex_before[1]

    hex_landed = (hex_eaten[0] + q_jump, hex_eaten[1] + r_jump)

    return hex_landed