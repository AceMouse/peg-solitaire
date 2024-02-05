#include <bits/stdc++.h> 
#include <cstdint>
#include <stdint.h>
#include <unordered_map>
#include <stdio.h>
#include <stdlib.h>

using namespace std; 
  
uint64_t dfs(uint64_t b, uint64_t l, uint64_t ones, unordered_map<uint64_t, uint64_t> cashe){
    if (cashe.find(b) != cashe.end()){
        return cashe[b];
    }

    uint64_t m = ones;
    for (uint64_t i = 0  ; i < l-2ULL; i++) {
        uint64_t x = ((b>>i) & 0b111);
        if (x == 0b011 || x == 0b110){
            b ^= 0b111ULL << i;
            uint64_t res = dfs(b,l,ones-1ULL, cashe);
            if (res < m){
                m = res;
            }
            b ^= 0b111ULL << i;
        }
    }
    cashe[b] = m;
    return m;

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
    unordered_map<uint64_t, uint64_t> cashe;
    uint64_t res = dfs(b, l, ones, cashe);
    printf("%" PRIu64 "\n", res);
    return res; 
} 
