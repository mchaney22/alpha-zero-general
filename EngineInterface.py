from MCTS import MCTS
from othello.OthelloGame import OthelloGame as Game
from othello.pytorch.NNet import NNetWrapper as nn
import numpy as np

class Othello_AI:
    def __init__(self):
        self.game = Game
        self.nnet = nn
        self.nmcts = MCTS(self.game, self.nnet, self.args)

    def get_move(self, board_state):
        action = np.argmax(self.nmcts.getActionProb(board_state, temp=0))
        print(action)
        return action