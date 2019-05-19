import sys
# sys.path.append("/Users/zacharyho/Documents/UoM/artificial_intelligence/AI_projB/AI_proj_B/daboiz")
print(sys.path)
import unittest
# from daboiz import mcts_helper
from daboiz import mcts_helper
from daboiz.hex import Hex


# print(sys.path)


class TestMCTSHelper(unittest.TestCase):
    """
    Test class for MCTS Helper functions
    """

    # def test_initiate_board(self):
    #     board = mcts_helper.initiate_board()
    #     self.assertEqual(board, ((Hex(0, 0), "red"), (Hex(
    #         0, 1), "green"), (Hex(0, 2), "empty")))

    def test_update_board(self):
        board = mcts_helper.initiate_board()

        print("Initial board is")
        print(board)

        # Testing EXIT action
        new_board = mcts_helper.update_board(board, ("EXIT", (0, 0)), "red")
        self.assertEqual(new_board, ((Hex(0, 0), "empty"), (Hex(
            0, 1), "green"), (Hex(0, 2), "empty")), msg="EXIT action test")


        # Testing MOVE action
        new_board = mcts_helper.update_board(board, ("MOVE", ((0, 1), (0, 2))), "green")
        self.assertEqual(new_board, ((Hex(0, 0), "red"), (Hex(
            0, 1), "empty"), (Hex(0, 2), "green")), msg="MOVE action test")
        
        # Testing JUMP action
        new_board = mcts_helper.update_board(board, ("JUMP", ((0, 0), (0, 2))), "red")
        self.assertEqual(new_board, ((Hex(0, 0), "empty"), (Hex(
            0, 1), "red"), (Hex(0, 2), "red")), msg="JUMP action test")

        print("JUMPED board is")
        print(new_board)

if __name__ == '__main__':
    unittest.main()
