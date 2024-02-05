#include <bits/stdc++.h> 
#include <cstdint>
#include <stdint.h>
#include <unordered_map>
#include <stdio.h>
#include <stdlib.h>

using namespace std; 
  
uint64_t dfs(uint64_t b, uint64_t l, uint64_t ones, unordered_map<uint64_t, uint64_t> cashe[]){
    if (ones <= 1 || ones == l){
        return ones;
    }
    if (cashe[l].find(b) != cashe[l].end()){
        return cashe[l][b];
    }
    uint64_t x = b;
    uint64_t largest_group = 0;
    while(x>0){
        x &= b>>(++largest_group);
    }
    if (largest_group == ones){
        return (ones+1)>>1;
    }


    uint64_t m = ones;
    uint64_t ones_before_cut = 0;
    for (uint64_t i = 0  ; i < l-2ULL; i++) {
        ones_before_cut += b>>i & 0b1;
        if (((b>>i) & 0b111) == 0b011){
            b ^= 0b111ULL << i;
            if (i>0 && ((b>>(i-1))&0b111) == 0b000){
                uint64_t res = dfs(b>>(i+1ULL), l-(i+1ULL),ones- ones_before_cut, cashe) +
                              dfs(b&((1ULL<<i)-1ULL),i,ones_before_cut-1ULL, cashe);
                if (res < m){
                    m = res;
                    if (m <= 1) {
                        return m;
                    }
                }
            } else {
                uint64_t res = dfs(b,l,ones-1ULL, cashe);
                if (res < m){
                    m = res;
                    if (m <= 1) {
                        return m;
                    }
                }
            }
            b ^= 0b111ULL << i;
        }
        if (((b>>i) & 0b111) == 0b110){
            b ^= 0b111ULL << i;
            if (i<l-2ULL && ((b>>(i+1ULL))&0b111) == 0b000){
                uint64_t res = dfs(b>>(i+3ULL), l-(i+3ULL),ones- ones_before_cut-2ULL, cashe) +
                              dfs(b&((1ULL<<(i+2ULL))-1ULL),i+2ULL,ones_before_cut+1ULL, cashe);
                if (res < m){
                    m = res;
                    if (m <= 1) {
                        return m;
                    }
                }
            } else {
                uint64_t res = dfs(b,l,ones-1ULL, cashe);
                if (res < m){
                    m = res;
                    if (m <= 1) {
                        return m;
                    }
                }
            }
            b ^= 0b111ULL << i;
        }
    }
    cashe[l][b] = m;
    return m;

}

uint64_t _split(uint64_t b, uint64_t l, uint64_t ones, unordered_map<uint64_t, uint64_t> cashe[]){
    uint64_t ones_before_cut = 0;
    uint64_t end = 0;
    for (uint64_t i = 0; i<l-3; i++){
        ones_before_cut += (b>>i)&0b1;
        if (((b>>i) & 0b1111) == 0b0001){
            end = i+2;
        }
        if  (((b>>i) & 0b1111) == 0b1000){
            if (end == 0){
                uint64_t m =_split(b>>(i+1), l-(i+1), ones, cashe);
                return m;
            } else {
                uint64_t m = dfs(b&((1ULL<<(end+1ULL))-1ULL), end, ones_before_cut, cashe) + 
                            _split(b>>end , l-end , ones- ones_before_cut, cashe);
                cashe[l][b] = m;
                return m;
            }
        }
    }
    return dfs(b,l,ones, cashe);
}
uint64_t split(uint64_t b, uint64_t l, uint64_t ones){
    unordered_map<uint64_t, uint64_t> cashe[64];
    return _split(b, l, ones, cashe);
}
int main(int argc, char* argv[]) 
{ 
    uint64_t b = 0;
    uint64_t ones = 0;
    uint64_t l = 0;
    if (argc != 2){
        printf("please provide a board!");
    }
    char * board = argv[1];
    while(*board){
        uint64_t c = *board - '0';
        b = (b<<1) | c;
        ones += c;
        l++;
        board++;
    }
    uint64_t res = split(b, l, ones);
    printf("%" PRIu64 "\n", res);
    return res; 
} 
