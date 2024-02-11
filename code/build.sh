#!/bin/bash

set -ex 

g++ naive.cpp -o naive -lm -Wall -O3 -march=native 
g++ memo.cpp -o memo -lm -Wall -O3 -march=native 
g++ count_split_no_memo.cpp -o count_nm -lm -Wall -O3 -march=native 
g++ count_split.cpp -o count -lm -Wall -O3 -march=native 
g++ after_move_split.cpp -o after -lm -Wall -O3 -march=native 
g++ after_wide.cpp -o after_w -lm -Wall -O3 -march=native 
 
