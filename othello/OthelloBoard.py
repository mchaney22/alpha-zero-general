import numpy as np
from collections import namedtuple

WinState = namedtuple('WinState','is_ended winner')

height=8
length=8
class Board:
    dirs = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
    def __init__(self,pieces=None,turn=1):
        self.height=height
        self.length=length
        if pieces is None:
            self.pieces=np.zeros([self.height,self.length])
            self.pieces[3,3]=-1
            self.pieces[3,4]=1
            self.pieces[4,3]=1
            self.pieces[4,4]=-1
        else:
            self.pieces=pieces
        self.turn=turn

    #returns a board
    def move(self,action):
        #maybe dont check valid cause its expensive
        x=action%self.length
        y=action//self.length
        new_board = self.__deepcopy__()
        #moves = self.get_valid_moves()
        #if action>=len(moves) or not moves[action]:
        #    raise ValueError(f"Not a legal move {action}")
        new_board.pieces[y][x]=new_board.turn
        changed =False
        for direc in Board.dirs:
            piece, move = new_board.search((y,x),direc)
            if piece==new_board.turn:
                new_board.change((y,x),move,direc,new_board.turn)
                changed=True
        if not changed:
            print(f"bad action {action//8},{action%8}")
        new_board.turn*=-1
        return new_board

    def __deepcopy__(self, memodict={}):
        pieces = np.copy(self.pieces)
        turn = self.turn
        return Board(pieces, turn)


    def get_valid_moves(self,player=None):
        if player==None:
            player=self.turn
        mine_y,mine_x=np.where(self.pieces==player)
        moves=[]
        for i in range(len(mine_x)):
            for direc in Board.dirs:
                piece, m = self.search((mine_y[i],mine_x[i]),direc)
                if m!=(-1,-1) and piece==0 and not m in moves:
                    #print(f"adding {m}")
                    moves.append(m)
        vec = np.full(self.height*self.length,False)
        for m in moves:
            vec[m[0]*self.length+m[1]]=True
        return vec

    def change(self,start,end,direc,player): #start and end are (y,x)
        #print(f"{start} -> {end}")
        while start!=end:
            #print(f"changed {start}")
            self.pieces[start[0],start[1]]=player
            start=(start[0]+direc[0],start[1]+direc[1])

    def search(self,start,direc): #start is (y,x)
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
        y,x = np.where(self.pieces==0)
        empty = len(x)
        y,x = np.where(self.pieces==1)
        p1=len(x)
        y,x = np.where(self.pieces==-1)
        p2=len(x)
        winner = None
        if p2>p1:
            winner=-1
        if p1>p2:
            winner=1
        total=0
        for m in self.get_valid_moves():
            if m:
                total+=1
        if empty==0 or total==0:
            return WinState(True,winner)
        return WinState(False,None)
        
        
    def on_board(self,pos):
        return pos[1]<self.height and pos[0]>=0 and pos[0]<self.length and pos[1]>=0

    def __str__(self):
        ret = ""
        for i in range(self.height):
            for j in range(self.length):
                ret+=f"{int(self.pieces[i][j])} "
            ret+="\n"
        return ret


if __name__=="__main__":
    b = Board()
    player=1
    for i in range(100):
        print(b)
        moves = b.get_valid_moves()
        actions = [i for i in range(len(moves)) if moves[i]]
        print(actions)
        if actions:
            print(actions[0]//8,actions[0]%8)
            b = b.move(actions[-1])
        win,winner = b.get_win_state()
        if win:
            print(f"winner is {winner}")
            break
