set terminal png size 640,480
set output 'cpp_comparison.png'
set yr [:0.02]
set xr [3:64]
set title "avg"
set xlabel "n"
set ylabel "sec"
set xtics 3
plot for [col=2:6] "avg.dat" using 1:col with lines title columnheader
