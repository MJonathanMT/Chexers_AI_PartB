def distance_fill(self, dist_dict, pos, dist):
    dist += 1
    # These '###' represents an unvisited hex
    if dist_dict[pos] == '###':
        dist_dict[pos] = dist
    # If distance is bigger than the distance in the dictionary,
    # exit from the recursion
    elif dist > dist_dict[pos]:
        return 0
    # If distance is less, change the value in the dictionary
    elif dist < dist_dict[pos]:
        dist_dict[pos] = dist

    next_jump = ()
    for next_pos in self.adj_dict[pos]:
        movable = True
        jumpable = True

        # Set movable to False if it is blocked
        if next_pos in self.enemies:
            movable = False

        # Check if can jump over the blocked piece, only happens when
        # the next piece is a blocked piece
        if not movable:
            q_move = (next_pos[0] - pos[0])*2
            r_move = (next_pos[1] - pos[1])*2
            next_jump = (pos[0] + q_move, pos[1] + r_move)
            if (next_jump not in self.adj_dict[next_pos] or
                    next_jump in self.enemies):
                jumpable = False

        # Recurse through the appropriate movement: move or jump
        if movable:
            distance_fill(self, dist_dict, next_pos, dist)
        elif jumpable:
            distance_fill(self, dist_dict, next_jump, dist)
    return dist_dict


def get_moves(self, dist_dict):
    best_moves = {}
    for piece in self.pieces:
        movement = []
        shortest_dist = 0
        best_move = ()
        for next_move in self.adj_dict[piece]:
            # Skips move if there is another piece in front of it or
            # if there is a blocked hex
            if next_move in self.board_dict:
                continue

            # the best move is where the distance of the next
            # location is the closest to the goal
            if shortest_dist == 0:
                shortest_dist = dist_dict[next_move]
                best_move = next_move
            elif dist_dict[next_move] < shortest_dist:
                shortest_dist = dist_dict[next_move]
                best_move = next_move

        # if the best move makes the piece go backward
        # (Worsen the piece condition) remove the best move instead
        if best_move != () and dist_dict[piece] <= dist_dict[best_move]:
            best_move = ()

        # Each value of the position contains the current position
        # and next position
        movement.append(piece)
        movement.append(best_move)
        best_moves[piece] = movement

    return best_moves


def get_jumps(self, dist_dict):
    best_jumps = {}
    final_kill = False
    for piece in self.pieces:
        shortest_dist = 0
        jumping = []
        best_jump = ()
        for next_move in self.adj_dict[piece]:
            current_kill = False
            # Skips if the next move is an empty hex,
            # this means its not jumpable
            if next_move not in self.board_dict:
                continue
            q_move = (next_move[0] - piece[0])*2
            r_move = (next_move[1] - piece[1])*2
            next_jump = (piece[0] + q_move, piece[1] + r_move)
            # Skips the next jump if the next jump location is
            # another piece, a block or it isn't within the board
            if (next_jump not in self.adj_dict[next_move] or
                    next_jump in self.board_dict):
                continue

            if next_move in self.enemies:
                current_kill = True

            # If its the first jump, change best jump to this jump
            if shortest_dist == 0:
                shortest_dist = dist_dict[next_jump]
                best_jump = next_jump
                final_kill = current_kill

            # If we already have a killing jump,
            # don't take a jump that doesnt kill
            if final_kill and not current_kill:
                continue

            # the best jump is where the distance of the next
            # location is the closest to the goal
            elif dist_dict[next_jump] < shortest_dist:
                shortest_dist = dist_dict[next_jump]
                best_jump = next_jump

        # if the best jump makes the piece go backward
        # (Worsen the piece condition) remove the best jump instead
        if best_jump != () and dist_dict[piece] <= dist_dict[best_jump]:
            best_jump = ()

        # Each value of the position contains the current position
        # and next position
        jumping.append(piece)
        jumping.append(best_jump)
        best_jumps[piece] = jumping

    return best_jumps


def final_movements(dist_dict, best_moves, best_jumps):
    """
    This function chooses whether each piece should do a move or jump action
    :param dist_dict: Dictionary containing the distance to the nearest goal
    :param best_moves: Dictionary containing the best move of each piece
    :param best_jumps: Dictionary containing the best jump of each piece
    :return: The best action each piece should take whether its a move or a jump
    """
    final_moves = {}
    for piece in best_moves:
        move = best_moves[piece][1]
        # If there are no jump action, make the best action the move action
        if best_jumps[piece][1] == ():
            final_moves[piece] = best_moves[piece]
            final_moves[piece].append('move')
            continue

        # If there are no move action, make the best action the jump action
        if move == ():
            final_moves[piece] = best_jumps[piece]
            final_moves[piece].append('jump')
            continue

        # Choose the action based on the next location the piece lands in.
        # Choose the action that pushes the piece closer to the goal
        jump = best_jumps[piece][1]
        if dist_dict[move] < dist_dict[jump]:
            final_moves[piece] = best_moves[piece]
            final_moves[piece].append('move')
        else:
            final_moves[piece] = best_jumps[piece]
            final_moves[piece].append('jump')

    return final_moves


def get_piece(dist_dict, final_moves):
    """
    This function choose the best piece to move amongst the piece on the board
    :param dist_dict: Dictionary containing the distance to the nearest goal
    :param final_moves: Dictionary containing the best action for each piece
    :return: The piece that is best to move given the current board position
    """
    final_move = []
    dist = 0
    for piece in final_moves:
        # Skip this piece if there aren't any good action available
        if final_moves[piece][1] == ():
            continue

        if dist == 0:
            dist = dist_dict[piece]
            final_move = final_moves[piece]

        # Choose the piece that is further away from the goal
        elif dist_dict[piece] > dist:
            dist = dist_dict[piece]
            final_move = final_moves[piece]

        # If the same distance away from the goal,
        # choose piece with the jump action
        elif dist_dict[piece] == dist:
            if final_moves[piece][2] == 'jump':
                final_move = final_moves[piece]

    return final_move


def create_dist_dict():
    """
    This function creates an unvisited distance dictionary filled with '###'
    :return: Returns unvisited distance dictionary
    """
    dist_dict = {}
    ran = range(-3, +3 + 1)
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        dist_dict[qr] = '###'
    return dist_dict