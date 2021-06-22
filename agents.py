import numpy as np
import random
import game

def minimax(grid, depth, maximizingPlayer, piece,dep=1):

    if depth == 0 or grid.terminate():
        # print("\t"*dep,depth,maximizingPlayer,piece)
        # grid.print(dep)
        # print("\t"*dep,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
        # print("\t"*dep,"--------------------------")
        return game.get_heuristic(grid, piece),grid.last
    if maximizingPlayer:
        value = (-np.Inf,grid.column)
        for col in grid.valid:
            child = game.drop_piece(grid, col)
            value = max(value, (minimax(child, depth-1, not maximizingPlayer, piece,dep+1)[0],col))

        # print("\t"*dep,depth,maximizingPlayer,piece)
        # grid.print(dep)
        # print("\t"*dep,value,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
        # print("\t"*dep,"--------------------------")
        return value

    else:
        value = (np.Inf,grid.column)
        for col in grid.valid:
            child = game.drop_piece(grid, col)
            value = min(value, (minimax(child, depth-1, not maximizingPlayer, piece,dep+1)[0],col))
        # print("\t"*dep,depth,maximizingPlayer,piece)
        # grid.print(dep)
        # print("\t"*dep,value,game.get_heuristic(grid,1),game.get_heuristic(grid,2))
        # print("\t"*dep,"--------------------------")
        return value

def agent_random(grid):
    return random.choice(grid.valid)
def agent_smart(grid):
    wins=list(col for col in grid.valid if check_winning_move(grid,col)==True)
    if wins:
        return random.choice(wins)
    return random.choice(grid.valid)

def agent_smarter(grid):
    # Your code here: Amend the agent!
    wins=list(col for col in grid.valid if check_winning_move(grid,col)==True)
    if wins:
        return random.choice(wins)
    block=list(win for win in grid.valid if check_winning_move(grid,win)==True)
    if block:
        return random.choice(block)
    return random.choice(grid.valid)

def agent_score(grid):
    scores = dict(zip(grid.valid,[score_move(grid,col) for col in grid.valid]))
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    return random.choice(max_cols)

## The last parameter for minimax agent depends on player 1 or player 2

# You can only put this agent in player 2
def agent_minimax4(grid):
    return minimax(grid,4,True,2)[1]

# You can only put this agent in player 1
def agent_minimax(grid):
    return minimax(grid,2,True,1)[1]
