import unittest
# from daboiz import mcts_helper
from daboiz import mcts_helper
from daboiz.hex import Hex
from daboiz.board import Board
from daboiz.winstate import WinState

class TestBoard(unittest.TestCase):
    """
    Test class for Board class functions
    """
    # def test_legal_actions(self):
    #     board = Board(mcts_helper.initiate_board(), "red", (1, 2, 1))
    #     history = [board.state]
    #     print("history is")
    #     print(history)
    #     print("board state is")
    #     print(board.state)
    #     self.assertEqual(board.legal_actions(history), [("EXIT", (0,0)), ("JUMP", ((0,0), (0,2)))])

    def test_next_state(self):
        board = Board(mcts_helper.initiate_board(), "red", (1, 2, 1))

        print("board state is initially")
        print(board.state)
        # # Testing EXIT action
        # new_state = board.next_state(board.state, ("EXIT", (0, 0)))
        # self.assertEqual(new_state, ((Hex(0, 0), "empty"), (Hex(
        #     0, 1), "green"), (Hex(0, 2), "empty")), msg="EXIT action test")

        # # Testing board.pieces_exited after "EXIT" action
        # self.assertEqual(board.pieces_exited, (2, 2, 1))

        board.update_turn("red")

        # Testing MOVE action
        new_state = board.next_state(board.state, ("MOVE", ((0, 1), (0, 2))))
        self.assertEqual(new_state, ((Hex(0, 0), "red"), (Hex(
            0, 1), "empty"), (Hex(0, 2), "green")), msg="MOVE action test")
        
        board.update_turn("blue")
        
        # Testing JUMP action
        new_state = board.next_state(board.state, ("JUMP", ((0, 0), (0, 2))))
        self.assertEqual(new_state, ((Hex(0, 0), "empty"), (Hex(
            0, 1), "red"), (Hex(0, 2), "red")), msg="JUMP action test")


    # def test_winner(self):
    #     board = Board(mcts_helper.initiate_board(), "red", (4, 2, 1))

    #     self.assertEqual(board.winner(), WinState.RED)

if __name__ == '__main__':
    unittest.main()
