pcap="ipchange-1509259779.58.pcap"
set ylabel "Queries per minute"
set xlabel "time"
set title "PowerDNS Root Server Query Distribution"

set xdata time
set timefmt "%s"
set format x "%H:%M:%S"
set xtics rotate

plot \
  "<./bin/qpm \"".pcap."\" 10.0.1.1" u 2:1 w l title "a-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.2" u 2:1 w l title "b-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.3" u 2:1 w l title "c-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.4" u 2:1 w l title "d-root", \
  "<./bin/qpm \"".pcap."\" 10.0.2.4" u 2:1 w l title "d2-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.5" u 2:1 w l title "e-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.6" u 2:1 w l title "f-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.7" u 2:1 w l title "g-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.8" u 2:1 w l title "h-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.9" u 2:1 w l title "i-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.10" u 2:1 w l title "j-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.11" u 2:1 w l title "k-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.12" u 2:1 w l title "l-root", \
  "<./bin/qpm \"".pcap."\" 10.0.1.13" u 2:1 w l title "m-root"
