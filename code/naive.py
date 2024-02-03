def solve(board,mark ='1'):
    b = 0
    ones = 0
    for bit in board:
        c = int(bit==mark)
        b = (b<<1) | c
        ones += c 
    print(dfs(b, len(board), ones))
    
def dfs(b, l, ones):
    m = ones
    for i in range(l-2):
        if (b>>i) & 0b111 in [0b011, 0b110]: #check if valid move. 
            b ^= 0b111 << i #perform move. 
            m = min(dfs(b,l, ones-1), m)
            b ^= 0b111 << i #undo move.  
    return m
def kattis():
    n = int(input())
    for i in range(n):
        solve(input(),mark='o')
if __name__ == "__main__":
    solve(input())
