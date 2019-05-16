def initiate_board():
    """
    This function initiates our representation of the game board
    :return: A set of the starting coordinates
    """

    board = ())
    ran=range(-3, 4)
    for (q, r) in [(q, r) for q in ran for r in ran if -q - r in ran]:
        if q == -3 and r >= 0:
            board_dict[(q, r)]="red"
        elif q >= 0 and r == -3:
            board_dict[(q, r)]="green"
        elif q+r == 3:
            board_dict[(q, r)]="blue"

    # Returns the final list of end_points/goals
    return board_dict
