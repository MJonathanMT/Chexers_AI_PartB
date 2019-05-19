import unittest
# from daboiz import mcts_helper
from daboiz import mcts_helper
from daboiz.hex import Hex
from daboiz.board import Board

def test_legal_actions(self):
    board = Board(mcts_helper.initiate_board())
    history = [board.state]
    print("history is")
    print(history)
    print("board state is")
    print(board.state)
    self.assertEqual(board.legal_actions(history), [("EXIT", (0,0)), ("JUMP", ((0,0), (0,2)))])

if __name__ == '__main__':
    unittest.main()
