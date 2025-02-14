import numpy as np

class HumanOthelloPlayer():
    def __init__(self, game):
        self.game = game
    def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1) #bug if play doesn't get passed cannonical form
        #print(f"board: {board}")
        i = input("Enter indicie of move. 'x,y'")
        coords = i.split(',')
        x, y = int(coords[0]),int(coords[1])
        return y*8+x
    


class RandomPlayer():
    def __init__(self,game):
        self.game = game
        
    def play(self, board):
        valid_moves = game.getValidMoves(board, 1)
        move_indicies = [i for i in range(len(valid_moves)) if valid_moves[i]]
        r = np.random.randint(len(move_indicies))
        return move_indicies(r)
