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


## Random notes

If stuff gets in a bad state, this can usually clean it up:
```
sudo pkill pdns
sudo mn
```

## data

2 sample runs are provided. `data/ipchange-1509315001.32.pcap.gz` is a
full run, but the new d-root had lower latency than the other roots,
so pinning to it was actually correct (though probing still
stopped). `data/ipchange-1509328629.75.pcap.gz` is a better run that
also demonstrates the pinning and the new d-root had a worse than
average latency, so overall qps goes down.
