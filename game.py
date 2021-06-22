import numpy as np
import time

class Board:
    def __init__(self,row=6,column=7,detail=True):
        self.column=column
        self.row=row
        self.table=np.asarray([[0]*column for i in range(row)]).reshape(self.row,self.column)
        self.mark=1
        self.connect=4
        self.cnt=0
        self.round = 1
        self.valid=range(self.column)
        self.last=-1
        self.detail=detail
    def print(self,dep=0):
        for row in self.table:
            print("\t"*dep,end="")
            for point in row:
                print(point,end=" ")
            print()
    def put(self,col):
        if col<0 or col>=self.column:
            return False
        if self.table[0][col]==0:
            for row in range(self.row-1,-1,-1):
                if self.table[row][col]==0:
                    break
            self.table[row][col]=self.mark
        else:
            return False
        self.mark=3-self.mark
        self.cnt+=1
        self.last=col
        self.valid=[col for col in range(self.column) if self.table[0][col]==0]
        # self.print()
        return True
    def win(self,piece):
        # horizontal
        for row in range(self.row):
            for col in range(self.column-(self.connect-1)):
                window=list(self.table[row,col:col+self.connect])
                if window.count(piece)==self.connect:
                    return True
        # vertical
        for row in range(self.row-(self.connect-1)):
            for col in range(self.column):
                window=list(self.table[row:row+self.connect,col])
                if window.count(piece)==self.connect:
                    return True
        # positive diagonal
        for row in range(self.row-(self.connect-1)):
            for col in range(self.column-(self.connect-1)):
                window=list(self.table[range(row, row+self.connect),range(col,col+self.connect)])
                if window.count(piece)==self.connect:
                    return True
        # negative diagonal
        for row in range(self.connect-1,self.row):
            for col in range(self.column-(self.connect-1)):
                window=list(self.table[range(row,row-self.connect,-1),range(col,col+self.connect)])
                if window.count(piece)==self.connect:
                    return True
        return False
    def terminate(self):
        if self.win(self.mark) or self.win(3-self.mark):
            return True
        if self.cnt==self.row*self.column:
            return True
        return False

    def start(self,agents):
        while not self.terminate():
            if self.detail:
                self.print()
                # print("\t"*dep,"Player",self.mark,"'s turn....",sep="")
            # if self.mark==1:

            start_time = time.time()
            # if not self.put(int(input())):
            if not self.put(agents[self.mark-1](self)):
                print("Invalid input.")
                break
            end_time = time.time()
            if self.detail:
                print('Use %.3fs to make this step.' %(end_time - start_time))

            # elif self.mark==2:
            #     start_time = time.time()
            #     # if not self.put(int(input())):
            #     if not self.put(agent2(self)):
            #         print("Invalid input.")
            #         break
            #     end_time = time.time()
            #     if self.detail:
            #         print('Use %.3fs to make this step.' %(end_time - start_time))
                self.round += 1
            # print("---------------------")
        print("Game finished.")

        if self.win(1):
            print("Player1 Win!!",sep="")
            print("========================================")
            return 1
        elif self.win(2):
            print("Player2 Win!!",sep="")
            print("========================================")
            return 2
        else:
            print("It's a draw game.")
            print("========================================")
            assert(self.cnt==self.row*self.column)
            return 0

import copy

def drop_piece(grid, col):
    next_grid=copy.deepcopy(grid)
    next_grid.put(col)
    return next_grid

# Returns True if dropping piece in column results in game win
def check_winning_move(grid, col, piece):
    # Convert the board to a 2D grid
    next_grid = drop_piece(grid, col)
    if next_grid.win(piece):
        return True
    return False

def score_move(grid, col):
    next_grid = drop_piece(grid, col)
    score = get_heuristic(next_grid,grid.mark)
    return score

# Helper function for score_move: calculates value of heuristic for grid
def get_heuristic(grid, piece):
    num_twos = count_windows(grid, 2, 1)
    num_threes = count_windows(grid, 3, 1)
    num_fours = count_windows(grid, 4, 1)
    num_twos_opp = count_windows(grid, 2, 3-1)
    num_threes_opp = count_windows(grid, 3, 3-1)
    num_fours_opp = count_windows(grid, 4, 3-1)
    score = 1e10*grid.win(1) + 1e6*num_threes + 10*num_twos - 10*num_twos_opp - 1e6*num_threes_opp - 1e10*grid.win(3-1)
    return score

# Helper function for get_heuristic: checks if window satisfies heuristic conditions
def check_window(grid, window, num_discs, piece):
    return (window.count(piece) == num_discs and window.count(0) == grid.connect-num_discs)

# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
def count_windows(grid, num_discs, piece):
    num_windows = 0
    # horizontal
    for row in range(grid.row):
        for col in range(grid.column-(grid.connect-1)):
            window = list(grid.table[row, col:col+grid.connect])
            if check_window(grid, window, num_discs, piece):
                num_windows += 1
    # vertical
    for row in range(grid.row-(grid.connect-1)):
        for col in range(grid.column):
            window = list(grid.table[row:row+grid.connect, col])
            if check_window(grid, window, num_discs, piece):
                num_windows += 1
    # positive diagonal
    for row in range(grid.row-(grid.connect-1)):
        for col in range(grid.column-(grid.connect-1)):
            window = list(grid.table[range(row, row+grid.connect), range(col, col+grid.connect)])
            if check_window(grid, window, num_discs, piece):
                num_windows += 1
    # negative diagonal
    for row in range(grid.connect-1, grid.row):
        window = list(grid.table[range(row, row-grid.connect, -1), range(col, col+grid.connect)])
        for col in range(grid.column-(grid.connect-1)):
            if check_window(grid, window, num_discs, piece):
                num_windows += 1
    return num_windows
