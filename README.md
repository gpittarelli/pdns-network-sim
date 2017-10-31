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
./bin/qpm-all ipchange-{}.pcap > times

# update "pcap" line at start of graph2.p
$EDITOR graph2.p

gnuplot graph2.p
```

## Using pdns master

```
# build dependencies:
sudo apt-get install git build-essential dh-autoreconf pkg-config bison flex libssl-dev ragel libboost-all-dev virtualenv lua5.2 lua5.2-dev

git clone https://github.com/PowerDNS/pdns.git
cd pdns

./bootstrap
./configure --build=x86_64-linux-gnu --prefix=/usr --includedir=${prefix}/include --mandir=${prefix}/share/man --infodir=${prefix}/share/info --sysconfdir=/etc --localstatedir=/var --disable-silent-rules --libdir=${prefix}/lib/x86_64-linux-gnu --libexecdir=${prefix}/lib/x86_64-linux-gnu --disable-maintainer-mode --disable-dependency-tracking --sysconfdir=/etc/powerdns --enable-reproducible --with-modules="bind"
make

cd pdns/recursordist/
./bootstrap
./configure
make

# edit topo.py to point the recursor node at ./pdns/pdns/recursordist/pdns_recursor
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
