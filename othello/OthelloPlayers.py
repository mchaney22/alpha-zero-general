import numpy as np

class HumanPlayer():
	def __init__(self, game):
		self.game = game

	def play(self, board):
		valid_moves = game.getValidMoves(board, 1) #bug if play doesn't get passed cannonical form
		print(f"valid moves: {valid_moves}")
		i = input("Enter indicie of move. I'm not verifying input right now so don't screw me on this")
		move = valid_moves[int(i)]
		return move
    


class RandomPlayer():
    def __init__(self,game):
        self.game = game
        
    def play(self, board):
        valid_moves = game.getValidMoves(board, 1)
        i = np.random.randint(len(valid_moves))
        return valid_moves(i)
