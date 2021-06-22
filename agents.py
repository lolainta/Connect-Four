import numpy as np
import random
import game

DEBUG=False

def minimax(grid,depth,maximizingPlayer,dep=1):
    if depth == 0 or grid.terminate():
        if DEBUG:
            print("\t"*dep,depth,maximizingPlayer)
            grid.print(dep)
            print("\t"*dep,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
            print("\t"*dep,"--------------------------")
        return game.get_heuristic(grid),{grid.last}
    if maximizingPlayer:
        value = (-np.Inf,{-1})
        for col in grid.valid:
            child = game.drop_piece(grid, col)
            nxt_value=minimax(child, depth-1, not maximizingPlayer,dep+1)
            if nxt_value[0]>value[0]:
                value=(nxt_value[0],{col})
            elif nxt_value[0]==value[0]:
                value[1].add(col)
        if DEBUG:
            print("\t"*dep,depth,maximizingPlayer)
            grid.print(dep)
            print("\t"*dep,value,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
            print("\t"*dep,"--------------------------")
        return value
    else:
        value = (np.Inf,{-1})
        for col in grid.valid:
            child = game.drop_piece(grid, col)
            nxt_value=minimax(child, depth-1, not maximizingPlayer,dep+1)
            if nxt_value[0]<value[0]:
                value=(nxt_value[0],{col})
            elif nxt_value[0]==value[0]:
                value[1].add(col)
        if DEBUG:
            print("\t"*dep,depth,maximizingPlayer)
            grid.print(dep)
            print("\t"*dep,value,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
            print("\t"*dep,"--------------------------")        
        return value

def alphabeta(grid,depth,maximizingPlayer,low,up,dep=1):

    def get_min(grid,depth,maximizingPlayer,low,up,dep=1):
        if depth==0 or grid.terminate():
            return game.get_heuristic(grid),{grid.last}
        value=(np.Inf,{-1})
        for col in grid.valid:
            child=game.drop_piece(grid, col)
            nxt_value=get_max(child,depth-1,not maximizingPlayer,low,up,dep+1)
            if nxt_value[0]<value[0]:
                value=(nxt_value[0],{col})
            elif nxt_value[0]==value[0]:
                value[1].add(col)
            if value[0]<low:
                return value
            else:
                up=min(up,value[0])
        return value

    def get_max(grid,depth,maximizingPlayer,low,up,dep=1):
        if depth==0 or grid.terminate():
            return game.get_heuristic(grid,),{grid.last}
        value=(-np.Inf,{-1})
        for col in grid.valid:
            child=game.drop_piece(grid, col)
            nxt_value=get_min(child,depth-1,not maximizingPlayer,low,up,dep+1)
            if nxt_value[0]>value[0]:
                value=(nxt_value[0],{col})
            elif nxt_value[0]==value[0]:
                value[1].add(col)
            if value[0]>up:
                return value
            else:
                low=max(value[0],low)
        return value

    if maximizingPlayer:
        return get_max(grid,depth,maximizingPlayer,low,up,dep)
    else:
        return get_min(grid,depth,maximizingPlayer,low,up,dep)


def agent_random(grid):
    return random.choice(grid.valid)

def agent_smart(grid):
    wins=list(col for col in grid.valid if game.check_winning_move(grid,col,grid.mark)==True)
    if wins:
        return random.choice(wins)
    return random.choice(grid.valid)

def agent_smarter(grid):
    wins=list(col for col in grid.valid if game.check_winning_move(grid,col,grid.mark)==True)
    if wins:
        if DEBUG:
            print("wins:",wins)
        return random.choice(wins)
    block=list(col for col in grid.valid if game.check_winning_move(grid,col,3-grid.mark)==True)
    if block:
        if DEBUG:
            print("block:",block)
        return random.choice(block)
    return random.choice(grid.valid)

def agent_score(grid):
    scores = dict(zip(grid.valid,[game.score_move(grid,col) for col in grid.valid]))
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    if DEBUG:
        print("scores:",scores)
        print("max_cols:",max_cols)
    return random.choice(max_cols)

## The last parameter for minimax agent depends on player 1 or player 2
# You can only put this agent in player 1
def agent_alphabeta1(grid):
    return random.sample(alphabeta(grid,4,True,-float("inf"),float("inf"))[1],1)[0]
def agent_minimax2(grid):
    return random.sample(minimax(grid,4,False)[1],1)[0]
# You can only put this agent in player 2
def agent_minimax1(grid):
    return random.sample(minimax(grid,2,True)[1],1)[0]
def agent_alphabeta2(grid):
    return random.sample(alphabeta(grid,4,False,-float("inf"),float("inf"))[1],1)[0]