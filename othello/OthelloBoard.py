import numpy as np
from collections import namedtuple

WinState = namedtuple('WinState','is_ended winner')

height=9
width=9
class Board:
    dirs = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
    def __init__(self,pieces=None,turn=1):
        self.height=height
        self.width=width
        if pieces is None:
            self.pieces=np.zeros([self.height,self.width])
            self.pieces[3,3]=-1
            self.pieces[3,4]=1
            self.pieces[4,3]=1
            self.pieces[4,4]=-1
        else:
            self.pieces=pieces
        self.turn=turn

    #returns a board
    def move(self,x,y):
        #maybe dont check valid cause its expensive
        new_board = self.__deepcopy__()
        moves = self.get_valid_moves()
        if not (x,y) in moves:
            raise ValueError("Not a legal move")
        new_board.pieces[x][y]=new_board.turn
        for direc in Board.dirs:
            piece, move = new_board.search((x,y),direc)
            if piece==new_board.turn:
                new_board.change((x,y),move,direc,new_board.turn)
        new_board.turn*=-1
        return new_board

    def __deepcopy__(self, memodict={}):
        pieces = np.copy(self.pieces)
        turn = self.turn
        return Board(pieces, turn)


    def get_valid_moves(self,player=None):
        if player==None:
            player=self.turn
        mine_x,mine_y=np.where(self.pieces[:,:]==player)
        moves=[]
        for i in range(len(mine_x)):
            for direc in Board.dirs:
                piece, move = self.search((mine_x[i],mine_y[i]),direc)
                if move!=(-1,-1) and piece==0 and not move in moves:
                    moves.append(move)
        return moves

    def change(self,start,end,direc,player):
        while start!=end:
            self.pieces[start[0],start[1]]=player
            start=(start[0]+direc[0],start[1]+direc[1])

    def search(self,start,direc):
        player=self.pieces[start[0],start[1]]
        cur = (start[0]+direc[0],start[1]+direc[1])
        #doesnt straddle opponnents pieces
        if not self.on_board(cur) or self.pieces[cur[0],cur[1]]!=-1*player:
            return player*-1, (-1,-1)
        while self.on_board(cur) and (self.pieces[cur[0],cur[1]]==-1*player):
            cur = (cur[0]+direc[0],cur[1]+direc[1])
        #off board
        if not self.on_board(cur):
            return player*-1, (-1,-1)
        #on board, but already mine
        if self.pieces[cur[0],cur[1]]==player:
            return player, cur
        #open
        return 0,cur

    def get_win_state(self):
        x,y = np.where(self.pieces[:,:]==0)
        empty = len(x)*len(y)
        x,y = np.where(self.pieces[:,:]==1)
        p1=len(x)*len(x)
        x,y = np.where(self.pieces[:,:]==-1)
        p2=len(x)*len(x)
        winner = None
        if p2>p1:
            winner=-1
        if p1>p2:
            winner=1
        if empty==0 or len(self.get_valid_moves())==0:
            return WinState(True,winner)
        return WinState(False,None)
        
        
    def on_board(self,pos):
        return pos[0]<self.height and pos[0]>=0 and pos[1]<width and pos[1]>=0

    def __str__(self):
        ret = ""
        for i in range(self.height):
            for j in range(self.width):
                ret+=f"{int(self.pieces[i][j])} "
            ret+="\n"
        return ret


if __name__=="__main__":
    b = Board()
    player=1
    for i in range(100):
        print(b)
        moves = b.get_valid_moves()
        print(moves)
        b = b.move(moves[0][0],moves[0][1])
        print(moves[0])
        win,winner = b.get_win_state()
        if win:
            print(f"winner is {winner}")
            break
width
