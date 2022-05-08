import sys
from packet import *
from routingtables import *

routing_table = routing_tables("r7")
interface_table = interface_tables("r7")

r7_d2_socket = socket(AF_INET, SOCK_DGRAM)
r7_d2_socket.bind(('192.168.1.21', 8908))
log_write("bound r7d2 socket")
while True:
    data, addr = r7_d2_socket.recvfrom(1024)
    if data:
        pkttypestr = pkttype_string(data)
        log_write("Router 7 D2Socket: Received " + pkttypestr + " packet from source " + str(addr[0]) + "\n")
        
        route_packet(data, routing_table, interface_table, "Router 7 D2Socket: ")
