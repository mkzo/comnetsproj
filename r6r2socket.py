import sys
from packet import *
from routingtables import *

routing_table = routing_tables("r6")
interface_table = interface_tables("r6")

r6_r2_socket = socket(AF_INET, SOCK_DGRAM)
r6_r2_socket.bind(('192.168.1.8', 8895))
while True:
    data, addr = r6_r2_socket.recvfrom(1024)
    if data:
        pkttypestr = pkttype_string(data)
        log_write("Router 6 R2Socket: Received " + pkttypestr + " packet from source " + str(addr[0]) + "\n")
        
        route_packet(data, routing_table, interface_table, "Router 6 R2Socket: ")

