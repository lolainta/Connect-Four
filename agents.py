import numpy as np
import random
import game

DEBUG=False

def minimax(grid, depth, maximizingPlayer, piece,dep=1):
    if depth == 0 or grid.terminate():
        if DEBUG:
            print("\t"*dep,depth,maximizingPlayer,piece)
            grid.print(dep)
            print("\t"*dep,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
            print("\t"*dep,"--------------------------")
        return game.get_heuristic(grid, piece),{grid.last}
    if maximizingPlayer:
        value = (-np.Inf,{-1})
        for col in grid.valid:
            child = game.drop_piece(grid, col)
            nxt_value=minimax(child, depth-1, not maximizingPlayer, piece,dep+1)
            # print(nxt_value)
            if nxt_value[0]>value[0]:
                # print("\t"*dep,"update_max: ",value,nxt_value)
                value=(nxt_value[0],{col})
            elif nxt_value[0]==value[0]:
                value[1].add(col)
            # value = max(value, (minimax(child, depth-1, not maximizingPlayer, piece,dep+1)[0],col))
        if DEBUG:
            print("\t"*dep,depth,maximizingPlayer,piece)
            grid.print(dep)
            print("\t"*dep,value,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
            print("\t"*dep,"--------------------------")
        return value
    else:
        value = (np.Inf,{-1})
        for col in grid.valid:
            child = game.drop_piece(grid, col)
            nxt_value=minimax(child, depth-1, not maximizingPlayer, piece,dep+1)
            if nxt_value[0]<value[0]:
                # print("\t"*dep,"update_min: ",value,nxt_value)
                value=(nxt_value[0],{col})
            elif nxt_value[0]==value[0]:
                value[1].add(col)
            # value = min(value, (minimax(child, depth-1, not maximizingPlayer, piece,dep+1)[0],col))
        if DEBUG:
            print("\t"*dep,depth,maximizingPlayer,piece)
            grid.print(dep)
            print("\t"*dep,value,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
            print("\t"*dep,"--------------------------")        
        return value

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

# You can only put this agent in player 2
def agent_minimax1(grid):
    return random.sample(minimax(grid,3,True,1)[1],1)[0]

# You can only put this agent in player 1
def agent_minimax2(grid):
    return random.sample(minimax(grid,2,False,2)[1],1)[0]