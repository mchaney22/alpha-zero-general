import numpy as np
import sys

sys.path.append('..')
from Game import Game
from .OthelloBoard import Board
class OthelloGame(Game):

    def __init__(self):
        Game.__init__(self)
        self.base_board = Board()

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return self.base_board

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return self.base_board.height, self.base_board.length

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        height = 8
        width = 8
        return height*width

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        assert(player==board.turn, "Attempted turn by wrong player")
        assert(action<=self.getActionSize(), "Attempted actions not in action vector")
        x = action % self.length
        y = action // self.length
        
        return board.move(x, y)


    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        b = Board(board,player)
        return b.get_valid_moves()

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        b = Board(board,player)
        has_won, winner = b.get_win_state()
        if not has_won:
            return 0
        if winner is None:
            return 1e-4
        elif winner==player:
            return +1
        elif winner==-player:
            return -1
        raise ValueError("Invalid Win Sate",winner)



    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        return board * player

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        _board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5): 
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l
    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return board.__str__()
