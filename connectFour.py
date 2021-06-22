import random
import numpy as np
import time
from game import Board
from agents import agent_alphabeta1,agent_alphabeta2,agent_minimax1,agent_minimax2,agent_minimax1,agent_minimax2,agent_score,agent_smarter,agent_smart,agent_random

# Main Function
def Run():
    p1 = 0
    p2 = 0
    draw = 0
    N = 20
    for i in range(N):
        print(i, "/", N, end=" \n", sep="")
        game = Board(detail=True)
        result = game.start([agent_alphabeta1,agent_minimax2])
        if result == 1:
            p1 += 1
        elif result == 2:
            p2 += 1
        else:
            draw += 1

    print("Player1 win", p1, "times")
    print("Player2 win", p2, "times")
    print("Draw", draw, "times")


if __name__ == '__main__':
    Run()
