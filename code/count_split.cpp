#include <bits/stdc++.h> 
#include <cstdint>
#include <stdint.h>
#include <unordered_map>
#include <stdio.h>
#include <stdlib.h>

using namespace std; 
  
uint8_t dfs(uint64_t b, uint8_t l, uint8_t ones, unordered_map<uint64_t, uint8_t> (&cashe)[64]){
    if (ones <= 1 || ones == l){
        return ones;
    }
    if (cashe[l].find(b) != cashe[l].end()){
        return cashe[l][b];
    }
    uint64_t x = b;
    uint8_t largest_group = 0;
    while(x>0){
        x &= b>>(++largest_group);
    }
    if (largest_group == ones){
        return (ones+1)>>1;
    }

    uint8_t m = ones;
    uint8_t ones_before_cut = 0;
    uint64_t mask = 0b111;
    uint64_t o = 1;
    for (uint8_t i = 0  ; i < l-2; i++) {
        ones_before_cut += b>>i & 0b1;
        if (((b>>i) & mask) == 0b011){
            b ^= mask << i;
            if (i>0 && ((b>>(i-1))&mask) == 0b000){
                uint8_t res = dfs(b>>(i+1), l-(i+1),ones- ones_before_cut, cashe) +
                              dfs(b&((o<<i)-1),i,ones_before_cut-1, cashe);
                if (res < m){
                    m = res;
                    if (m <= 1) {
                        return m;
                    }
                }
            } else {
                uint8_t res = dfs(b,l,ones-1, cashe);
                if (res < m){
                    m = res;
                    if (m <= 1) {
                        return m;
                    }
                }
            }
            b ^= mask << i;
        }
        if (((b>>i) & mask) == 0b110){
            b ^= mask << i;
            if (i<l-2 && ((b>>(i+1))&0b111) == 0b000){
                uint8_t res = dfs(b>>(i+3), l-(i+3),ones- ones_before_cut-2, cashe) +
                              dfs(b&((o<<(i+2))-1),i+2,ones_before_cut+1, cashe);
                if (res < m){
                    m = res;
                    if (m <= 1) {
                        return m;
                    }
                }
            } else {
                uint8_t res = dfs(b,l,ones-1, cashe);
                if (res < m){
                    m = res;
                    if (m <= 1) {
                        return m;
                    }
                }
            }
            b ^= mask << i;
        }
    }
    cashe[l][b] = m;
    return m;

}

uint8_t _split(uint64_t b, uint8_t l, uint8_t ones, unordered_map<uint64_t, uint8_t> (&cashe)[64]){
    uint8_t ones_before_cut = 0;
    uint8_t end = 0;
    uint64_t o = 1; 
    for (uint8_t i = 0; i<l-3; i++){
        ones_before_cut += (b>>i)&0b1;
        if (((b>>i) & 0b1111) == 0b0001){
            end = i+2;
        }
        if  (((b>>i) & 0b1111) == 0b1000){
            if (end == 0){
                uint8_t m =_split(b>>(i+1), l-(i+1), ones, cashe);
                return m;
            } else {
                uint8_t m = dfs(b&((o<<(end+1))-1), end, ones_before_cut, cashe) + 
                            _split(b>>end , l-end , ones- ones_before_cut, cashe);
                cashe[l][b] = m;
                return m;
            }
        }
    }
    return dfs(b,l,ones, cashe);
}
uint8_t split(uint64_t b, uint8_t l, uint8_t ones){
    unordered_map<uint64_t, uint8_t> cashe[64];
    return _split(b, l, ones, cashe);
}
int main(int argc, char* argv[]) 
{ 
    uint64_t b = 0;
    uint8_t ones = 0;
    uint8_t l = 0;
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
    uint8_t res = split(b, l, ones);
    printf("%u\n", res);
    return res; 
} 

