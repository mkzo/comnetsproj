from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
from mininet.node import Node
from mininet.link import TCLink
from cleanup import cleanup

def finaltopo():
    net = Mininet(link=TCLink, controller=None, cleanup=True)
    
    # Creating Hosts
    info("Creating nodes\n")
    r1 = net.addHost('r1', ip='192.168.1.2/24', inNamespace=False)
    r2 = net.addHost('r2', ip='192.168.1.4/24', inNamespace=False)
    r3 = net.addHost('r3', ip='192.168.1.6/24', inNamespace=False)
    r4 = net.addHost('r4', ip='192.168.1.10/24', inNamespace=False)
    r5 = net.addHost('r5', ip='192.168.1.12/24', inNamespace=False)
    r6 = net.addHost('r6', ip='192.168.1.8/24', inNamespace=False)
    r7 = net.addHost('r7', ip='192.168.1.16/24', inNamespace=False)
    s = net.addHost('s', ip='192.168.1.1/24', inNamespace=False)
    d1 = net.addHost('d1', ip='192.168.1.20/24', inNamespace=False)
    d2 = net.addHost('d2', ip='192.168.1.22/24', inNamespace=False)
    d3 = net.addHost('d3', ip='192.168.1.18/24', inNamespace=False)
    # Establishing the links from hosts to routers
    info("Creating links\n")
    net.addLink(s, r1, intfName1='s-eth0', params1={'ip' : '192.168.1.1/24'}, intfName2='r1-eth1', params2={'ip' : '192.168.1.2/24'})
    net.addLink(d1, r6, intfName1='d1-eth0', params1={'ip' : '192.168.1.20/24'}, intfName2='r6-eth2', params2={'ip' : '192.168.1.19/24'})
    net.addLink(d2, r7, intfName1='d2-eth0', params1={'ip' : '192.168.1.22/24'}, intfName2='r7-eth2', params2={'ip' : '192.168.1.21/24'})
    net.addLink(d3, r5, intfName1='d3-eth0', params1={'ip' : '192.168.1.18/24'}, intfName2='r5-eth3', params2={'ip' : '192.168.1.17/24'})
    net.addLink(r1, r2, intfName1='r1-eth2', params1={'ip' : '192.168.1.3/24'}, intfName2='r2-eth1', params2={'ip' : '192.168.1.4/24'})
    net.addLink(r1, r3, intfName1='r1-eth3', params1={'ip' : '192.168.1.5/24'}, intfName2='r3-eth1', params2={'ip' : '192.168.1.6/24'})
    net.addLink(r2, r6, intfName1='r2-eth2', params1={'ip' : '192.168.1.7/24'}, intfName2='r6-eth1', params2={'ip' : '192.168.1.8/24'})
    net.addLink(r3, r4, intfName1='r3-eth2', params1={'ip' : '192.168.1.9/24'}, intfName2='r4-eth1', params2={'ip' : '192.168.1.10/24'})
    net.addLink(r3, r5, intfName1='r3-eth3', params1={'ip' : '192.168.1.11/24'}, intfName2='r5-eth1', params2={'ip' : '192.168.1.12/24'})
    net.addLink(r4, r5, intfName1='r4-eth2', params1={'ip' : '192.168.1.13/24'}, intfName2='r5-eth2', params2={'ip' : '192.168.1.14/24'})
    net.addLink(r4, r7, intfName1='r4-eth3', params1={'ip' : '192.168.1.15/24'}, intfName2='r7-eth1', params2={'ip' : '192.168.1.16/24'})

    # Build the specified network
    info("Building network\n")
    net.build()
    
    return net
