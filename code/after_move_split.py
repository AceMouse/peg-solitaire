def solve(board, mark = '1'):
    b = 0
    ones = 0 
    for bit in board:
        c = int(bit==mark )
        b = (b<<1) | c
        ones += c 
    print(split(b, len(board), ones))

def split(b, l, ones):
    ones_before_cut = 0 
    end = 0
    for i in range(l-3):
        ones_before_cut += b>>i & 0b1 
        if (b>>i) & 0b1111 == 0b0001: #split on 3+ consecutive zeroes.
            end = i+2 
        if (b>>i) & 0b1111 == 0b1000: 
            if end == 0: 
                return split(b>>(i+1),l-(i+1), ones)
            else:
                m = dfs(b&((1<<(end+1))-1),end,ones_before_cut) + split(b>>end,l-end, ones-ones_before_cut) 
                cashe[(b,l)] = m
                return m 
    return dfs(b,l,ones)

cashe = dict()    
def _dfs(b, l, ones):
    if ones <= 1: 
        return ones
    if (b,l) in cashe:
        return cashe[(b,l)]

    m = ones
    for i in range(l-2):
        if (b>>i) & 0b111 in [0b011,0b110]: #check if valid move. 
            b ^= 0b111 << i #perform move. 
            m = min(_dfs(b,l, ones-1), m)
            b ^= 0b111 << i #undo move.  
    cashe[(b,l)] = m
    return m

def dfs(b, l, ones):
    if ones <= 7: 
        return _dfs(b,l,ones)
    if (b,l) in cashe:
        return cashe[(b,l)]
    end = 0 

    m = ones
    ones_before_cut = 0 
    for i in range(l-2):
        ones_before_cut += b>>i & 0b1
        if (b>>i) & 0b111 == 0b011: #check if valid move. 
            b ^= 0b111 << i #perform move. 
            if i > 0 and (b>>(i-1)) & 0b111 == 0b000:
                m = min(dfs(b>>(i+1), l-(i+1), ones - ones_before_cut) + 
                        dfs(b&((1<<i)-1), i, ones_before_cut-1), m)
            else:            
                m = min(dfs(b,l, ones-1), m)
            b ^= 0b111 << i #undo move.  
        if (b>>i) & 0b111 == 0b110: #check if valid move. 
            b ^= 0b111 << i #perform move. 
            if i < l-2 and (b>>(i+1)) & 0b111 == 0b000:
                m = min(dfs(b>>(i+3), l-(i+3), ones - ones_before_cut-2) + 
                        dfs(b&((1<<(i+2))-1), i+2, ones_before_cut+1), m)
            else:            
                m = min(dfs(b,l, ones-1), m)
            b ^= 0b111 << i #undo move.  
    cashe[(b,l)] = m
    return m

def kattis():
    n = int(input())
    for i in range(n):
        solve(input(), mark = 'o')
if __name__ == "__main__":
    solve(input())
