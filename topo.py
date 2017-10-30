#!/usr/bin/env python
"""
PowerDNS weird NS selection simulation via mininet

"""

import time
import shutil
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.util import dumpNodeConnections, pmonitor

def int2dpid( dpid ):
   try:
      dpid = hex( dpid )[ 2: ]
      dpid = '0' * ( 16 - len( dpid ) ) + dpid
      return dpid
   except IndexError:
      raise Exception('Unable to derive default datapath ID - '
                      'please either specify a dpid or use a '
		                  'canonical switch name such as s23.')

# https://stackoverflow.com/a/7001371/922613
def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)

# Define our simulated root servers. Note that d and d2 should have
# similar, worse-than-average latencies. The rest of the servers can
# all be equal, but having 1 or 2 with below average latencies makes
# the DEWMA behavior (is that still in use?) stand out.
#
# Note: These are one-way latencies, so ping times (RTT) will be
# double the numbers here
#
# Note: IP addresses should match the mock named.root hints file
roots = {
    'a':  {'latency': 50,   'ip': '10.0.1.1'},
    'b':  {'latency': 50,   'ip': '10.0.1.2'},
    'c':  {'latency': 50,   'ip': '10.0.1.3'},
    'd':  {'latency': 100,  'ip': '10.0.1.4'},
    'd2': {'latency': 100,  'ip': '10.0.2.4'},
    'e':  {'latency': 50,   'ip': '10.0.1.5'},
    'f':  {'latency': 50,   'ip': '10.0.1.6'},
    'g':  {'latency': 50,   'ip': '10.0.1.7'},
    'h':  {'latency': 30,   'ip': '10.0.1.8'},
    'i':  {'latency': 50,   'ip': '10.0.1.9'},
    'j':  {'latency': 50,   'ip': '10.0.1.10'},
    'k':  {'latency': 50,   'ip': '10.0.1.11'},
    'l':  {'latency': 50,   'ip': '10.0.1.12'},
    'm':  {'latency': 50,   'ip': '10.0.1.13'}
}

class PdnsTopo(Topo):
    "Network topology to repro potential pdns NS selection bug"

    def __init__(self):
        Topo.__init__(self)

        # Makes DNS requests:
        client = self.addHost('client')

        # Serves DNS answers using recursive root server queries:
        recursor = self.addHost('recursor')

        # Simulated Internet with globally distributed root servers
        internet = self.addSwitch('internet', dpid=int2dpid(1))

        self.addLink(client, internet)
        self.addLink(recursor, internet)

        for letter, root in roots.items():
            latency = root['latency']
            ip = root['ip']
            print("Creating root-{} with delay {}ms".format(letter, latency))

            server = self.addHost('root-{}'.format(letter), ip=ip)
            self.addLink(internet, server, delay='{}ms'.format(latency))

# Export the main topology, so it can be tested with, eg:
#   sudo mn --custom ~/topo.py --topo pdns --test pingall --link tc
topos = { 'pdns': ( lambda: PdnsTopo() ) }


def runExperiment(net):
    epoch = time.time()
    pcapOut = "ipchange-{}.pcap".format(epoch)
    shutil.copy("/etc/powerdns/root.orig.zone", "/etc/powerdns/root.zone")

    print("Dumping host connections")
    dumpNodeConnections(net.hosts)

    # debug:
#    print("Testing network connectivity")
#    net.pingAllFull()

    client, recursor = net.get('client', 'recursor')
    rootServers = {
        letter: net.get('root-{}'.format(letter))
        for letter, _ in roots.items()
    }

    print("Launching root servers")
    serverProcesses = {}
    for letter, server in rootServers.items():
        print("Launching root {} on: {}".format(letter, server.IP()))

        serverProcesses[server] = server.popen(
            "/usr/sbin/pdns_server",
            "--allow-recursion=no",
            "--socket-dir=root-{}".format(letter),
            "--local-address={}".format(server.IP()),
            "--launch=bind",
            "--bind-config=/etc/powerdns/bind.conf"
        )

    print("Launching recursor server")
    serverProcesses[recursor] = recursor.popen(
        "/usr/sbin/pdns_recursor",
        "--local-address={}".format(recursor.IP()),
        "--hint-file=named.root",
        "--dont-query="
    )



def testPdns():
    epoch = time.time()
    pcapOut = "ipchange-{}.pcap".format(epoch)
    shutil.copy("/etc/powerdns/root.orig.zone", "/etc/powerdns/root.zone")

    topo = PdnsTopo()
    net = Mininet(
        topo=topo,
        link=TCLink,
        controller=OVSController
    )

    net.start()

    print("Dumping host connections")
    dumpNodeConnections(net.hosts)

    client, recursor = net.get('client', 'recursor')
    rootServers = {
        letter: net.get('root-{}'.format(letter))
        for letter, _ in roots.items()
    }

    print("Launching root servers")
    serverProcesses = {}
    for letter, server in rootServers.items():
        print("Launching root {} on: {}".format(letter, server.IP()))

        serverProcesses[server] = server.popen(
            "/usr/sbin/pdns_server",
            "--allow-recursion=no",
            "--socket-dir=root-{}".format(letter),
            "--local-address={}".format(server.IP()),
            "--launch=bind",
            "--bind-config=/etc/powerdns/bind.conf"
        )

    print("Launching recursor server")
    serverProcesses[recursor] = recursor.popen(
        "/usr/sbin/pdns_recursor",
        "--local-address={}".format(recursor.IP()),
        "--hint-file=named.root",
        "--dont-query="
    )

    print("Starting tcpdump")
    tcpdump = recursor.popen("/usr/sbin/tcpdump", "port 53", "-w", pcapOut)

    print("Let stuff startup and settle...")
    time.sleep(2)

    print("Starting query traffic")
    client.cmd(
        "while true; do dig @{} asdf$(date +%s%N).; done > /tmp/date.out &".format(recursor.IP())
    )

    # Length of experiment:
#    time.sleep(10 * 60)
    print("Waiting for some baseline traffic...")
    time.sleep(10 * 60)

    # d-root IP address switchover
    print("Swapping d-root IP")
    shutil.copy("/etc/powerdns/root.new-d.zone", "/etc/powerdns/root.zone")
    for letter, server in rootServers.items():
        print("  Swapping over: {}".format(letter))
        print(server.cmd(
            "pdns_control",
            "--socket-dir=root-{}".format(letter),
            "bind-reload-now",
            "."
        ))

    print("Testing new root prime:")
    print(recursor.cmd(
        "dig @{} -t ns .".format(rootServers["a"].IP())
    ))

    print("Waiting for switchover to be picked up...")
    time.sleep(3 * 60 * 60)

    print("Stopping query traffic")
    client.cmd('kill %while')

    print("Killing PowerDNS servers")
    for _, p in serverProcesses.items():
        p.kill()
    time.sleep(4)
    for _, p in serverProcesses.items():
        p.terminate()

    net.stop()

    print("Experiment done. Analyze: {}".format(pcapOut))

if __name__ == '__main__':
    testPdns()
