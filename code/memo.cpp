#include <bits/stdc++.h> 
#include <cstdint>
#include <stdint.h>
#include <unordered_map>
#include <stdio.h>
#include <stdlib.h>

using namespace std; 
  
uint8_t dfs(uint64_t b, uint8_t l, uint8_t ones, unordered_map<uint64_t, uint8_t> &cashe){
    if (cashe.find(b) != cashe.end()){
        return cashe[b];
    }

    uint8_t m = ones;
    uint64_t mask = 0b111;
    for (uint8_t i = 0  ; i < l-2; i++) {
        uint64_t x = ((b>>i) & 0b111);
        if (x == 0b011 || x == 0b110){
            b ^= mask << i;
            uint8_t res = dfs(b,l,ones-1, cashe);
            if (res < m){
                m = res;
            }
            b ^= mask << i;
        }
    }
    cashe[b] = m;
    return m;

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
    unordered_map<uint64_t, uint8_t> cashe;
    uint8_t res = dfs(b, l, ones, cashe);
    printf("%u\n", res);
    return res; 
} 
