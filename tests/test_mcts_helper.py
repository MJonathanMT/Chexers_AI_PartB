# import sys
# sys.path.append("/Users/zacharyho/Documents/UoM/artificial_intelligence/AI_projB/AI_proj_B/daboiz")
# print(sys.path)
import unittest
# from daboiz import mcts_helper
from daboiz import mcts_helper
from daboiz.hex import Hex
from daboiz.game_state import GameState


# print(sys.path)


class TestMCTSHelper(unittest.TestCase):
    """
    Test class for MCTS Helper functions
    """

    def test_initiate_board(self):
        board = mcts_helper.initiate_board()
        self.assertEqual(board, ((Hex(0, 0), "red"), (Hex(
            0, 1), "green"), (Hex(0, 2), "empty")))


if __name__ == '__main__':
    unittest.main()
