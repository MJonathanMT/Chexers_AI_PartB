# Library imports
from operator import itemgetter

# Local imports
from hex import Hex
import helper

# Tested
def initiate_board():
    """
    This function initiates our representation of the game board
    :return: A tuple of the starting coordinates with their corresponding attribute
      ((Hex, "type"), (Hex, "type")....., (Hex, "type"))
    """

    board = ()
    ran = range(-3, 4)
    for (q, r) in [(q, r) for q in ran for r in ran if -q - r in ran]:
        hex = Hex(q, r)
        if q == -3 and r >= 0:
            new_hex = (hex, "red")
        elif q >= 0 and r == -3:
            new_hex = (hex, "green")
        elif q+r == 3:
            new_hex = (hex, "blue")
        else:
            new_hex = (hex, "empty")
        board += (new_hex,)

    # # For testing purposes:
    # board = ()
    # ran = range(0, 3)
    # for r in ran:
    #     hex = Hex(0, r)
    #     if r == 0:
    #         new_hex = (hex, "red")
    #     elif r == 1:
    #         new_hex = (hex, "green")
    #     else:
    #         new_hex = (hex, "empty")
    #     board += (new_hex,)
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

# Tested
def update_board(prev_board, action, player):
    """
    This function updates the board based on the most recent action taken
    :return: the updated board
    """
    new_board = ()
    if (action[0] == "EXIT"):
        # Loop through all the hexes to look for hexes interacted
        i = 0
        while (i < len(prev_board)):
            current_hex = Hex(action[1][0], action[1][1])

            # Once we find the hex coordinates that the piece exited FROM
            if (prev_board[i][0] == current_hex):
                # Create a new (Hex, "updated type") and put in the new_board tuple
                exit_hex = (prev_board[i][0], "empty")
                new_board += (exit_hex,)

            # Just append the other uninteracted hexes into new_board
            else:
                new_board += (prev_board[i],)
            i += 1

        # Sort the board by Hex
        new_board = tuple(
            sorted(new_board, key=lambda hex: (hex[0].coordinates)))
        return new_board

    # When action is JUMP or MOVE
    else:
        before_hex = Hex(action[1][0][0], action[1][0][1])
        next_hex = Hex(action[1][1][0], action[1][1][1])

        # Loop through all the hexes to look for hexes interacted
        i = 0
        while (i < len(prev_board)):

            # If the action was a JUMP, we need to change the piece that was jumped over to the colour
            # of the piece that jumped (it got EATEN!)
            if (action[0] == "JUMP"):
                eaten_hex_coordinates = helper.find_eaten(
                    before_hex.coordinates, next_hex.coordinates)
                eaten_hex = Hex(
                    eaten_hex_coordinates[0], eaten_hex_coordinates[1])
                if (prev_board[i][0] == eaten_hex):
                    updated_eaten_hex = (prev_board[i][0], player)
                    new_board += (updated_eaten_hex,)
                    i += 1
                    continue

            # Once we find the hex coordinates that the piece acted FROM
            if (prev_board[i][0] == before_hex):
                # Create a new (Hex, "updated type") and put in the new_board tuple
                updated_before_hex = (prev_board[i][0], "empty")
                new_board += (updated_before_hex,)
            # Once we find the hex coordinates that the piece acted TO
            elif (prev_board[i][0] == next_hex):
                # Create a new (Hex, "updated type") and put in the new_board tuple
                updated_next_hex = (prev_board[i][0], player)
                new_board += (updated_next_hex,)
            # Just append the other uninteracted hexes into new_board
            else:
                new_board += (prev_board[i],)
            i += 1

        # Sort the board by Hex
        new_board = tuple(
            sorted(new_board, key=lambda hex: (hex[0].coordinates)))

        return new_board


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