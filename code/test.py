from after_move_split import split as a_solve 
from split import dfs as s_solve
from memo import dfs as m_solve
from naive import dfs as n_solve

import random
import time 
def format_time(in_sec):
    return f"{in_sec:.4}"

def measure(b,i,c,sol):
    t = -time.time()
    ans = sol(b,i,c) 
    return (ans, t+time.time())

time_taken = [0,0,0,0]
for i in range(3,80):
    print(i)
    for x in range(10):
        b = random.getrandbits(i)
        c = b.bit_count()
        a_ans, a_t = measure(b,i,c,a_solve)
        time_taken[0] += a_t 
        s_ans, s_t = measure(b,i,c,s_solve)
        time_taken[1] += s_t
#        m_ans, m_t = measure(b,i,c,m_solve)
#        time_taken[2] += m_t
#        ans, t = measure(b,i,c,n_solve)
#        time_taken[3] += t
        if s_ans != a_ans:
            print(f"Fault on board {b}! got o_ans: {a_ans} expected {s_ans}")

    print(f"a_t:{format_time(time_taken[0])}")
    print(f"s_t:{format_time(time_taken[1])}")
#    print(f"m_t:{format_time(time_taken[2])}")
 #   print(f"n_t:{format_time(time_taken[3])}")

