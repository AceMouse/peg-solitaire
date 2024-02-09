import subprocess
import random
import time 
def format_time(in_sec):
    return f"{in_sec:.4f}"

def after_solve(b,l,c):
    return subprocess.run(args=["./after", f"{b:b}".zfill(l)], capture_output=True).returncode
def count_solve(b,l,c):
    return subprocess.run(args=["./count", f"{b:b}".zfill(l)], capture_output=True).returncode
def count_no_solve(b,l,c):
    return subprocess.run(args=["./count_no", f"{b:b}".zfill(l)], capture_output=True).returncode
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

to_test = [after_solve, count_solve, count_no_solve, memo_solve, naive_solve]
time_taken = [[] for _ in range(len(to_test))]
ans = [[] for _ in range(len(to_test))]
bss = [[random.getrandbits(i) for _ in range(10000)] for i in range(3,64)]
avg_f = open("avg.dat", "w")
med_f = open("med.dat", "w")
min_f = open("min.dat", "w")
max_f = open("max.dat", "w")
files = [avg_f, min_f, max_f, med_f]
def _print(*s, end="\n", files=avg_f):
    for file in files:
        print(*s, end=end, file=file)

names = ['n', '"DM1"', '"DM1+2"', '"DN1+2"', '"M"', '"N"']
on = [True]*len(to_test)
for n in names:
    _print(f"{n}\t", end = "", files = files)
_print(files = files)
cutoff = 0.02
for x,bs in enumerate(bss):
    i = x+3 
    _print(f"{i}\t", end = "", files = files)
    for n,sol in enumerate(to_test):
        if not on[n]:
            _print(f"--\t", end = "", files = files)
            continue
        ts = []
        for b in bs:
            c = b.bit_count()
            a, t = measure(b,i,c,sol)
            ans[n].append(a)
            ts += [t]
        ts.sort()
        avg_t = sum(ts)/len(ts)
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

for an in ans[1:]:
    for i,a in enumerate(an):
        if ans[0][i] != a:
            print(f"Error! expected {ans[0][i]}, got {a}. on board {f'{bss[i//1000][i%1000]:b}'.zfill(i//1000 + 3)}")

subprocess.run(args=["gnuplot", "-p", "-c", "avg.p"])
