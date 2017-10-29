pcap="ipchange-1509259779.58.pcap"
set ylabel "Queries per minute"
set xlabel "time"
set title "PowerDNS Root Server Query Distribution"

set xdata time
set timefmt "%s"
set format x "%H:%M:%S"
set xtics rotate

set datafile missing '-'

plot "./times" \
     u 1:2 w l title "a-root", \
  "" u 1:3 w l title "b-root", \
  "" u 1:4 w l title "c-root", \
  "" u 1:5 w l title "d-root", \
  "" u 1:6 w l title "d2-root", \
  "" u 1:7 w l title "e-root", \
  "" u 1:8 w l title "f-root", \
  "" u 1:9 w l title "g-root", \
  "" u 1:10 w l title "h-root", \
  "" u 1:11 w l title "i-root", \
  "" u 1:12 w l title "j-root", \
  "" u 1:13 w l title "k-root", \
  "" u 1:14 w l title "l-root", \
  "" u 1:15 w l title "m-root"
