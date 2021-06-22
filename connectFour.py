import random
import numpy as np
import time
from game import Board
from agents import agent_minimax, agent_minimax4

# Main Function
def Run():
    p1 = 0
    p2 = 0
    draw = 0
    N = 10
    for i in range(N):
        print(i, "/", N, end=" \t", sep="")
        game = Board()
        result = game.start(agent_minimax, agent_minimax4)
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
