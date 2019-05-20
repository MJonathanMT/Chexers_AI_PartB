import unittest
# from daboiz import mcts_helper
from daboiz import mcts_helper
from daboiz.hex import Hex
from daboiz.game_state import GameState
from daboiz.winstate import WinState

class TestBoard(unittest.TestCase):
    """
    Test class for Board class functions
    """
    # def test_legal_actions(self):
    #     game_state = GameState(mcts_helper.initiate_board(), "red", (1, 2, 1))
    #     history = [game_state.state]
    #     print("history is")
    #     print(history)
    #     print("board state is")
    #     print(game_state.board)
    #     self.assertEqual(game_state.legal_actions(history), [("EXIT", (0,0)), ("JUMP", ((0,0), (0,2)))])

    def test_next_state(self):
        game_state = GameState(mcts_helper.initiate_board(), "red", (1, 2, 1))

        print("Initial board is")
        print(game_state.board)
        print("Initial player is")
        print(game_state.turn)
        print("Initial pieces exited are")
        print(game_state.pieces_exited)
        # Testing EXIT action
        new_state = game_state.next_state(game_state.board, ("EXIT", (0, 0)))
        self.assertEqual(new_state.board, ((Hex(0, 0), "empty"), (Hex(
            0, 1), "green"), (Hex(0, 2), "empty")), msg="EXIT action test")

        # Testing new pieces exited after "EXIT" action
        self.assertEqual(new_state.pieces_exited, (2, 2, 1))

        # Testing whose turn it is after next_state is called
        self.assertEqual(new_state.turn, "green")

        print("Next board is")
        print(new_state.board)
        print("Next player is")
        print(new_state.turn)
        print("Next pieces exited are")
        print(new_state.pieces_exited)
        # game_state.update_turn("red")

        # # Testing MOVE action
        # new_state = game_state.next_state(game_state.board, ("MOVE", ((0, 1), (0, 2))))
        # self.assertEqual(new_state, ((Hex(0, 0), "red"), (Hex(
        #     0, 1), "empty"), (Hex(0, 2), "green")), msg="MOVE action test")
        
        # game_state.update_turn("blue")
        
        # # Testing JUMP action
        # new_state = game_state.next_state(game_state.board, ("JUMP", ((0, 0), (0, 2))))
        # self.assertEqual(new_state, ((Hex(0, 0), "empty"), (Hex(
        #     0, 1), "red"), (Hex(0, 2), "red")), msg="JUMP action test")


    # def test_winner(self):
    #     board = Board(mcts_helper.initiate_board(), "red", (4, 2, 1))

    #     self.assertEqual(board.winner(), WinState.RED)

if __name__ == '__main__':
    unittest.main()
