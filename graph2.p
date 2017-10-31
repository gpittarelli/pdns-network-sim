pcap="ipchange-1509475279.91.pcap"
sha="e5d68d9fd"

set terminal png enhanced size 1280,720 font "Arial" 20
set output 'qpm.png'

set ylabel "Queries per minute"
set xlabel "Time"
set title "PowerDNS Root Server Queries (".pcap.") (pdns ".sha.")"
set key outside

set logscale y

set xdata time
set timefmt "%s"
set format x "%H:%M:%S"
set xtics rotate

set datafile missing '-'

plot "./times" \
     u 1:2 w l title "a-root" lw 2, \
  "" u 1:3 w l title "b-root" lw 2, \
  "" u 1:4 w l title "c-root" lw 2, \
  "" u 1:5 w l title "d-root" lw 4, \
  "" u 1:6 w l title "d2-root" lw 4 lc rgb "green", \
  "" u 1:7 w l title "e-root" lw 2, \
  "" u 1:8 w l title "f-root" lw 2, \
  "" u 1:9 w l title "g-root" lw 2, \
  "" u 1:10 w l title "h-root" lw 2, \
  "" u 1:11 w l title "i-root" lw 2, \
  "" u 1:12 w l title "j-root" lw 2, \
  "" u 1:13 w l title "k-root" lw 2, \
  "" u 1:14 w l title "l-root" lw 2, \
  "" u 1:15 w l title "m-root" lw 2
