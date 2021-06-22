import random
import numpy as np
import time
from game import Board
from agents import agent_minimax1,agent_minimax2,agent_score,agent_smarter,agent_smart,agent_random
from agents import agent_alphabeta1_1,agent_alphabeta1_2,agent_alphabeta1_3,agent_alphabeta1_4
from agents import agent_alphabeta2_1,agent_alphabeta2_2,agent_alphabeta2_3,agent_alphabeta2_4
# Main Function
def Run():
    p1=0
    p2=0
    draw=0
    N=100
    begin_time=time.time()
    for i in range(N):
        print(i, "/", N,end="\n",sep="")
        game=Board(detail=False)
        agents=[agent_alphabeta1_4,agent_alphabeta2_4]
        result=game.start(agents)
        if result==1:
            p1+=1
        elif result==2:
            p2+=1
        else:
            draw+=1
    end_time=time.time()
    print(agents)
    print("Player1 win",p1,"times")
    print("Player2 win",p2,"times")
    print("Draw",draw,"times")
    print("Cost %.3fs to play %d games."%(end_time-begin_time,N))
if __name__=='__main__':
    Run()
