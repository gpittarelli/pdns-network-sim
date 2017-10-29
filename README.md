# PowerDNS network simulation

Repro steps and helper files for
https://github.com/PowerDNS/pdns/issues/1066

Running everything on a single Ubuntu VM:
 - mininet for network simulation
 - multiple instances of pdns

## Usage

Setup:
```
sudo apt-get install -y mininet pdns-recursor openvswitch-testcontroller dnsutils tcpdump
sudo cp /usr/bin/ovs-testcontroller /usr/bin/ovs-controller
```

Run the experiment: (Takes a few hours to finish!)
```
sudo ./topo.py
```

`topo.py` will create an `ipchange-<>.pcap` file. You can generate a
graph of queries to each root server with:
```
./bin/qpm-all ipchange-.pcap > times
gnuplot graph2.p
```
