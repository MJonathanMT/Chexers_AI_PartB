# import sys
# sys.path.append("/Users/zacharyho/Documents/UoM/artificial_intelligence/AI_projB/AI_proj_B/daboiz")
# print(sys.path)
import unittest
# from daboiz import mcts_helper
from daboiz import mcts_helper
from daboiz.hex import Hex
from daboiz.game_state import GameState
from daboiz.player import Player


# print(sys.path)


class TestMCTSHelper(unittest.TestCase):
    """
    Test class for MCTS Helper functions
    """

    # def test_initiate_board(self):
    #     board = mcts_helper.initiate_board()
    #     self.assertEqual(board, ((Hex(0, 0), "red"), (Hex(
    #         0, 1), "green"), (Hex(0, 2), "empty")))

    def test_convert_board(self):
        player = Player("red")
        converted_board = mcts_helper.convert_board(player.board_dict)
        self.assertEqual(converted_board, ((Hex(0, 0), "red"), (Hex(0, 1), "green"), (Hex(0, 2), "blue"), 
            (Hex(0, 3), "empty"), (Hex(0, 4), "empty")))


if __name__ == '__main__':
    unittest.main()
