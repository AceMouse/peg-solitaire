import subprocess
import random
import time 
from after_move_split import _split as af_sol  
start = -time.time()
def format_time(in_sec):
    return f"{in_sec:.4f}"

def after_w_solve(b,l,c):
    return subprocess.run(args=["./after_w", f"{b:b}".zfill(l)], capture_output=True).returncode
def after_solve(b,l,c):
    return subprocess.run(args=["./after", f"{b:b}".zfill(l)], capture_output=True).returncode
def count_solve(b,l,c):
    return subprocess.run(args=["./count", f"{b:b}".zfill(l)], capture_output=True).returncode
def count_nm_solve(b,l,c):
    return subprocess.run(args=["./count_nm", f"{b:b}".zfill(l)], capture_output=True).returncode
def naive_solve(b,l,c):
    return subprocess.run(args=["./naive", f"{b:b}".zfill(l)], capture_output=True).returncode
def memo_solve(b,l,c):
    return subprocess.run(args=["./memo", f"{b:b}".zfill(l)], capture_output=True).returncode

def measure(b,i,c,sol):
    t = -time.time()
    global cashe 
    cashe = dict()
    ans = sol(b,i,c) 
    return (ans, t+time.time())

to_test = [after_w_solve, after_solve, count_solve, count_nm_solve, memo_solve, naive_solve]
names = ['n','DM1w', 'DM1', '"DM1+2"', '"DN1+2"', '"M"', '"N"']
max_board_sizes = [128,64,64,64,64,64]
min_board_size = 3
boards_pr_size = 10000
cutoff = 0.1 


max_board_size = max(max_board_sizes)
time_taken = 0 
ans = [[] for _ in range(len(to_test))]
bss = [[random.getrandbits(i) for _ in range(boards_pr_size)] for i in range(min_board_size,max_board_size)]
avg_f = open("avg.dat", "w")
med_f = open("med.dat", "w")
min_f = open("min.dat", "w")
max_f = open("max.dat", "w")
files = [avg_f, min_f, max_f, med_f]
def _print(*s, end="\n", files=avg_f):
    for file in files:
        print(*s, end=end, file=file)

on = [True]*len(to_test)
for n in names:
    _print(f"{n}\t", end = "", files = files)
_print(files = files)

for x,bs in enumerate(bss):
    i = x+min_board_size 
    _print(f"{i}\t", end = "", files = files)
    for n,sol in enumerate(to_test):
        if not on[n] or i >= max_board_sizes[n]:
            _print(f"--\t", end = "", files = files)
            continue
        max_board_size = i 
        ts = []
        for b in bs:
            c = b.bit_count()
            a, t = measure(b,i,c,sol)
            ans[n].append(a)
            ts += [t]
        ts.sort()
        s = sum(ts)
        time_taken += s 
        avg_t = s/len(ts)
        median_t = ts[len(bs)//2]
        _print(f"{ts[-1]:.10f}\t", end = "", files = [max_f])
        _print(f"{ts[0]:.10f}\t", end = "", files = [min_f])
        _print(f"{median_t:.10f}\t", end = "", files = [med_f])
        _print(f"{avg_t:.10f}\t", end = "", files = [avg_f])
        if avg_t > cutoff:
            on[n] = False
    _print(files = files)
    if not True in on:
        break

for f in files:
    f.close()

for an in ans[1:]:
    for i,a in enumerate(an):
        if ans[0][i] != a:
            print(f"Error! expected {ans[0][i]}, got {a}. on board {f'{bss[i//boards_pr_size][i%boards_pr_size]:b}'.zfill(i//boards_pr_size + 3)}")

f = open("avg.p", "w")
f.write('\n'.join([f"set terminal png size 640,480", 
                   f"set output 'cpp_comparison.png'",
                   f"set yr [:{cutoff}]",
                   f"set xr [{min_board_size}:{max_board_size}]",
                   f"set title 'avg'",
                   f"set xlabel 'n'",
                   f"set ylabel 'sec'",
                   f"set xtics 3",
                   f"plot for [col=2:{len(names)}] 'avg.dat' using 1:col with lines title columnheader"]))
f.close()
subprocess.run(args=["gnuplot", "-c", "avg.p"])

print("time % spent in cpp:", time_taken/(start + time.time()))
print("time spent:         ", (start + time.time()))
