from packet import *
from finaltopo import finaltopo
from mininet.cli import CLI

net = finaltopo()

s = net.get('s')
d1 = net.get('d1')
d2 = net.get('d2')
d3 = net.get('d3')

r1 = net.get('r1')
r2 = net.get('r2')
r3 = net.get('r3')
r4 = net.get('r4')
r5 = net.get('r5')
r6 = net.get('r6')
r7 = net.get('r7')

s.cmd('sudo python3 ssocket.py &')
r1.cmd('sudo python3 r1ssocket.py &')
r1.cmd('sudo python3 r1r2socket.py &')
r1.cmd('sudo python3 r1r3socket.py &')
r2.cmd('sudo python3 r2r1socket.py &')
r2.cmd('sudo python3 r2r6socket.py &')
r3.cmd('sudo python3 r3r1socket.py &')
r3.cmd('sudo python3 r3r4socket.py &')
r3.cmd('sudo python3 r3r5socket.py &')
r4.cmd('sudo python3 r4r3socket.py &')
r4.cmd('sudo python3 r4r5socket.py &')
r4.cmd('sudo python3 r4r7socket.py &')
d3.cmd('sudo python3 d3socket.py &')
r5.cmd('sudo python3 r5r3socket.py &')
r5.cmd('sudo python3 r5r4socket.py &')
r5.cmd('sudo python3 r5d3socket.py &')
d1.cmd('sudo python3 d1socket.py &')
r6.cmd('sudo python3 r6r2socket.py &')
r6.cmd('sudo python3 r6d1socket.py &')
d2.cmd('sudo python3 d2socket.py &')
r7.cmd('sudo python3 r7r4socket.py &')
r7.cmd('sudo python3 r7d2socket.py &')

s.cmd('ip route add default via 192.168.1.2')
d1.cmd('ip route add default via 192.168.1.19')
d2.cmd('ip route add default via 192.168.2.21')
d3.cmd('ip route add default via 192.168.3.17')
r1.cmd('sysctl net.ipv4.ip_forward=1')
r2.cmd('sysctl net.ipv4.ip_forward=1')
r3.cmd('sysctl net.ipv4.ip_forward=1')
r4.cmd('sysctl net.ipv4.ip_forward=1')
r5.cmd('sysctl net.ipv4.ip_forward=1')
r6.cmd('sysctl net.ipv4.ip_forward=1')
r7.cmd('sysctl net.ipv4.ip_forward=1')

for seq in range(1, 4): # 6
    log_write("\n\nSequence #: " + str(seq) + "\n")

    s.cmd('sudo python3 ssendmulticast.py ' + str(seq))

with open('output.txt', 'r') as fin:
    print(fin.read())

CLI(net)

