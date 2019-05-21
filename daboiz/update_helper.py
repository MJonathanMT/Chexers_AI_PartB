def find_eaten(before_jump, after_jump):
    """
    This function finds the coordinates of the piece that was 'eaten'
    :return: The coordinate of the 'eaten' piece
    """
    q_move = (after_jump[0] - before_jump[0])/2
    r_move = (after_jump[1] - before_jump[1])/2

    eaten = (before_jump[0] + q_move, before_jump[1] + r_move)
    return eaten

