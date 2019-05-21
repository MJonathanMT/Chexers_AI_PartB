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

def check_trouble(self):
    in_dangered = []
    for piece in self.pieces:
        for enemy in self.enemies:
            if enemy in self.adj_dict[piece]:
                # # get the q,r difference between our piece and enemy piece
                # q_diff = enemy[0] - piece[0]
                # r_diff = enemy[1] - piece[1]
                # protection = (piece[0] - q_diff, piece[1] - r_diff)
                # if (protection not in self.board_dict
                #     and piece not in in_dangered
                #     and protection in self.adj_dict[piece]):
                #         in_dangered.append(piece)
                in_dangered.append(piece)
    return in_dangered

def defensive_moves(self, in_dangered):
    """
    Function for defensive actions if any piece is under attack
    :param self: Player object
    :param in_dangered: Pieces that are under attack
    :return: defensive action
    """
    method = 1
    while method != 4:
        action = ()
        protected = False
        for piece in in_dangered:
            # check if any of the movements are available
            # Methods go in decreasing priority
            # method 1 will take priority over method 4 because eating/attacking
            # a piece will improve the player's winning condition.
            # More explanation in report
            if method == 1:
                action = try_attack(self, piece)
                print("attempt to attack " + str(action) )
            elif method == 2:
                for enemy in self.enemies:
                    if enemy in self.adj_dict[piece]:
                        q_diff = enemy[0] - piece[0]
                        r_diff = enemy[1] - piece[1]
                        protection = (piece[0] - q_diff, piece[1] - r_diff)
                        if protection not in self.board_dict:
                            action = try_protect(self, piece)
                            protected = False
                        else:
                            protected = True
                print("attempt to defend " + str(action) )
            elif method == 3:
                action = move_away(self, piece)
                print("attempt to walk away " + str(action) )

            if action or protected:
                print("returning action = "+ str(action))
                return action
        if protected:
            return action
        method += 1
    return action

def try_attack(self, piece):
    """
    Function to check if the piece that is under attack could attack back
    :param self: Player object
    :param piece: Piece that is under attack
    :return: If exist, moves to capture the opposing piece
    """
    movement = []
    for enemy in self.enemies:
        if enemy in self.adj_dict[piece]:
            q_diff = enemy[0] - piece[0]
            r_diff = enemy[1] - piece[1]
            attack_able = (enemy[0] + q_diff, enemy[1] + r_diff)
            if (attack_able in self.adj_dict[enemy]
                    and attack_able not in self.board_dict):
                movement.append(piece)
                movement.append(attack_able)
                movement.append("jump")
                return movement
    return False

def try_protect(self, piece):
    """
    Function to a another piece behind the current piece that is in danger
    :param self: Player object
    :param piece: Piece that is under attack
    :return: If exist, moves to a protect the piece in danger position
    """
    movement = []
    for adj in self.adj_dict[piece]:
        for enemy in self.enemies:
            if adj == enemy:
                # get the q,r difference between our piece and enemy piece
                q_diff = piece[0] - enemy[0]
                r_diff = piece[1] - enemy[1]
                protection = (piece[0] + q_diff, piece[1] + r_diff)
                if (protection in self.board_dict
                    and protection in self.adj_dict[piece]):
                    continue
                for other in self.pieces:
                    if other == protection or other == piece:
                        continue
                    elif protection in self.adj_dict[other]:
                        movement.append(other)
                        movement.append(protection)
                        movement.append("move")
                        return movement
    return movement

def move_away(self, piece):
    """
    Function to make the piece in danger run away
    :param self: Player object
    :param piece: Piece that is under attack
    :return: A move or jump that runs away
    """
    movement = []
    for next_move in self.adj_dict[piece]:
        if (next_move in self.board_dict
            or bool(set(self.adj_dict[next_move]) & set(self.enemies))):
                continue
        else:
            movement.append(piece)
            movement.append(next_move)
            movement.append("move")
            return movement
    if not movement:
        # try jump back
        for next_move in self.adj_dict[piece]:
            if next_move in self.pieces:
                q_move = (next_move[0] - piece[0]) * 2
                r_move = (next_move[1] - piece[1]) * 2
                next_jump = (piece[0] + q_move, piece[1] + r_move)
                if next_jump in self.adj_dict[next_move]:
                    movement.append(piece)
                    movement.append(next_jump)
                    movement.append("jump")
                    return movement
    return movement


def is_protecting(self, in_danger, piece):
    q_diff = (piece[0] - in_danger[0])
    r_diff = (piece[1] - in_danger[1])
    possible_enemy = (in_danger[0] - q_diff, in_danger[1] - r_diff)
    if possible_enemy in self.enemies:
        return True
    return False

def attack_move(self, piece):
    """
    Function to check if the piece that is under attack could attack back
    :param self: Player object
    :param piece: Piece that is under attack
    :return: If exist, moves to capture the opposing piece
    """
    movement = []
    for enemy in self.enemies:
        if enemy in self.adj_dict[piece]:
            q_diff = enemy[0] - piece[0]
            r_diff = enemy[1] - piece[1]
            attack_able = (enemy[0] + q_diff, enemy[1] + r_diff)
            if (attack_able in self.adj_dict[enemy]
                    and attack_able not in self.board_dict):
                movement.append(piece)
                movement.append(attack_able)
                movement.append("jump")
                return movement
    return False


def get_moves(self, dist_dict):
    best_moves = {}
    for piece in self.pieces:
        movement = []
        shortest_dist = 0
        best_move = ()
        not_safe_move = ()
        for next_move in self.adj_dict[piece]:
            safety = True
            # Skips move if there is another piece in front of it or
            # if there is a blocked hex
            if next_move in self.board_dict:
                continue

            # check if enemy is adjacent to the next move
            for enemy in self.enemies:
                if enemy in self.adj_dict[next_move]:
                    if next_move in self.corners[0]:
                        continue
                    if next_move in self.corners[1]:
                        if (enemy not in self.corners[0]
                            and enemy not in self.corners[1]):
                            continue
                    # get the x,y behind the next_move parallel to the enemy
                    # check if the move there is safe
                    x_diff = enemy[0] - next_move[0]
                    y_diff = enemy[1] - next_move[1]
                    protection = (next_move[0] - x_diff, next_move[1] - y_diff)
                    if protection == piece or protection not in self.pieces:
                        safety = False
            if not safety:
                not_safe_move = next_move
                continue
            # the best move is where the distance of the next
            # location is the closest to the goal
            if shortest_dist == 0:
                shortest_dist = dist_dict[next_move]
                best_move = next_move
            elif dist_dict[next_move] <= shortest_dist:
                shortest_dist = dist_dict[next_move]
                best_move = next_move
        if not best_move:
            best_move = not_safe_move
        # Each value of the position contains the current position
        # and next position
        movement.append(piece)
        movement.append(best_move)
        best_moves[piece] = movement

    return best_moves


def get_jumps(self, dist_dict):
    best_jumps = {}
    for piece in self.pieces:
        final_kill = False
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
            # another piece or it isn't within the board
            if (next_jump not in self.adj_dict[next_move] or
                    next_jump in self.board_dict):
                continue

            # check if the jump kills an enemy
            if next_move in self.enemies:
                current_kill = True
            safety = True
            if not current_kill:
                # check if enemy is adjacent to the next move
                for enemy in self.enemies:
                    if enemy in self.adj_dict[next_jump]:
                        if next_move in self.corners[0]:
                            continue
                        if next_move in self.corners[1]:
                            if (enemy not in self.corners[0]
                                    and enemy not in self.corners[1]):
                                continue
                        # get the x,y behind the next_move parallel to the enemy
                        # check if the move there is safe
                        x_diff = enemy[0] - next_jump[0]
                        y_diff = enemy[1] - next_jump[1]
                        protection = (next_jump[0] - x_diff, next_jump[1] - y_diff)
                        if protection == piece or protection not in self.pieces:
                            safety = False
            if not safety:
                continue
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
        # and its not a kill move
        if (best_jump != () and dist_dict[piece] <= dist_dict[best_jump]
            and not final_kill):
            best_jump = ()

        # Each value of the position contains the current position
        # and next position
        jumping.append(piece)
        jumping.append(best_jump)
        jumping.append(final_kill)
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
        if best_jumps[piece][2]:
            final_moves[piece] = best_jumps[piece]
            print("yea killing move check.1")
            final_moves[piece].append('jump')
        elif dist_dict[move] < dist_dict[jump]:
            final_moves[piece] = best_moves[piece]
            final_moves[piece].append('move')
        else:
            final_moves[piece] = best_jumps[piece]
            final_moves[piece].append('jump')

    return final_moves


def get_piece(dist_dict, final_moves, position):
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

        if len(final_moves[piece]) == 4 and final_moves[piece][2]:
            final_move.append(final_moves[piece][0])
            final_move.append(final_moves[piece][1])
            final_move.append(final_moves[piece][3])
            print("yea killing move check.1")
            break

        elif dist == 0:
            dist = dist_dict[piece]
            final_move = final_moves[piece]
        if position == "back":
            # Choose the piece that is further away from the goal
            if dist_dict[piece] > dist:
                dist = dist_dict[piece]
                final_move = final_moves[piece]
        elif position == "front":
            if dist_dict[piece] < dist:
                dist = dist_dict[piece]
                final_move = final_moves[piece]
        # If the same distance away from the goal,
        # choose piece with the jump action
        if dist_dict[piece] == dist:
            if final_moves[piece][2] == 'jump':
                final_move = final_moves[piece]

    return final_move

