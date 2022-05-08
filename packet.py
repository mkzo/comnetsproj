#/usr/bin/python
#Comnetsii APIs for Packet. Rutgers ECE423/544
#Author: S.Maheshwari
import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore
import os

# packet creation

def create_pkt_datamulticast(seq, src, N, K, dst1, dst2, dst3, data):
    # Type(1), SEQ(4), SRCID(1), N(1), K(1), DSTID1(1), DSTID2(1), DSTID3(1), LEN(4), DATA(1000)
    pkttype = 0
    pktlen = len(data)
    header = struct.pack('BLBBBBBBL', pkttype, seq, src, N, K, dst1, dst2, dst3, pktlen)
    pktFormat = "BLBBBBBBL"
    headerSize = struct.calcsize(pktFormat)
    zero = 0
    data = bytearray(data.encode())
    data.extend((zero.to_bytes(1024-headerSize-len(data), 'little')))
    data = bytes(data)
    return header + data

def create_pkt_dataunicast(seq, src, srccentroid, dst, data):
    # Type(1), SEQ(4), SRCID(1), SRCCENTROIDID(1), DSTID(1), LEN(4), DATA(1000)
    pkttype = 1
    pktlen = len(data)
    header = struct.pack('BLBBBL', pkttype, seq, src, srccentroid, dst, pktlen)
    pktFormat = "BLBBBL"
    headerSize = struct.calcsize(pktFormat)
    zero = 0
    data = bytearray(data.encode())
    data.extend((zero.to_bytes(1024-headerSize-len(data), 'little')))
    data = bytes(data)
    return header + data
    
def create_pkt_centroidrequest(seq, src, N, dst1, dst2, dst3):
    # Type(1), SEQ(4), SRCID(1), N(1), DSTID1(1), DSTID2(1), DSTID3(1)
    pkttype = 2
    header = struct.pack('BLBBBBB', pkttype, seq, src, N, dst1, dst2, dst3)
    pktFormat = "BLBBBBB"
    headerSize = struct.calcsize(pktFormat)
    zero = 0
    data = zero.to_bytes(1024-headerSize, 'little')
    return header + data

def create_pkt_centroidreply(seq, src, meandist):
    # Type(1), SEQ(4), SRCID(1), MEANDIST(1)
    pkttype = 3
    header = struct.pack('BLBf', pkttype, seq, src, meandist)
    pktFormat = "BLBf"
    headerSize = struct.calcsize(pktFormat)
    zero = 0
    data = zero.to_bytes(1024-headerSize, 'little')
    return header + data

def create_pkt_datamulticastack(seq, src, dst):
    # Type(1), SEQ(4), SRCID(1), DSTID(1)
    pkttype = 4
    header = struct.pack('BLBB', pkttype, seq, src, dst)
    pktFormat = "BLBB"
    headerSize = struct.calcsize(pktFormat)
    zero = 0
    data = zero.to_bytes(1024-headerSize, 'little')
    return header + data

def create_pkt_dataunicastack(seq, src, dst, dstcentroid):
    # Type(1), SEQ(4), SRCID(1), DSTID(1), DSTCENTROIDID(1)
    pkttype = 5
    header = struct.pack('BLBBB', pkttype, seq, src, dst, dstcentroid)
    pktFormat = "BLBBB"
    headerSize = struct.calcsize(pktFormat)
    zero = 0
    data = zero.to_bytes(1024-headerSize, 'little')
    return header + data

# decapsulate packets

def decapsulate_datamulticast(pkt):
    pktFormat = "BLBBBBBBL"
    pktSize = struct.calcsize(pktFormat)
    header = pkt[0:pktSize]
    data = pkt[pktSize:]
    pkttype, seq, src, N, K, dst1, dst2, dst3, pktlen = struct.unpack("BLBBBBBBL", header)
    data = data[:pktlen].decode()
    return pkttype, seq, src, N, K, dst1, dst2, dst3, pktlen, data

def decapsulate_dataunicast(pkt):
    pktFormat = "BLBBBL"
    pktSize = struct.calcsize(pktFormat)
    header = pkt[0:pktSize]
    data = pkt[pktSize:]
    pkttype, seq, src, srccentroid, dst, pktlen = struct.unpack("BLBBBL", header)
    data = data[:pktlen].decode()
    return pkttype, seq, src, srccentroid, dst, pktlen, data

def decapsulate_centroidrequest(pkt):
    pktFormat = "BLBBBBB"
    pktSize = struct.calcsize(pktFormat)
    header = pkt[0:pktSize]
    pkttype, seq, src, N, dst1, dst2, dst3 = struct.unpack("BLBBBBB", header)
    return pkttype, seq, src, N, dst1, dst2, dst3
    
def decapsulate_centroidreply(pkt):
    pktFormat = "BLBf"
    pktSize = struct.calcsize(pktFormat)
    header = pkt[0:pktSize]
    pkttype, seq, src, meandist = struct.unpack("BLBf", header)
    return pkttype, seq, src, meandist

def decapsulate_datamulticastack(pkt):
    pktFormat = "BLBB"
    pktSize = struct.calcsize(pktFormat)
    header = pkt[0:pktSize]
    pkttype, seq, src, dst = struct.unpack("BLBB", header)
    return pkttype, seq, src, dst

def decapsulate_dataunicastack(pkt):
    pktFormat = "BLBBB"
    pktSize = struct.calcsize(pktFormat)
    header = pkt[0:pktSize]
    pkttype, seq, src, dst, dstcentroid = struct.unpack("BLBBB", header)
    return pkttype, seq, src, dst, dstcentroid

# route packets

def route_packet(pkt, routing_table, interface_table, sourcestr):#, rtrsocket):
    pkttype = pkt[0]
    if pkttype == 0:
        #log_write("pkttype == 0 \n")
        route_pkt_datamulticast(pkt, routing_table, interface_table, sourcestr)#, rtrsocket)
    elif pkttype == 1:
        route_pkt_dataunicast(pkt, routing_table, sourcestr)
    elif pkttype == 2:
        route_pkt_centroidrequest(pkt, routing_table, sourcestr)
    elif pkttype == 3:
        route_pkt_centroidreply(pkt)
    elif pkttype == 4:
        route_pkt_datamulticastack(pkt, routing_table)
    elif pkttype == 5:
        route_pkt_dataunicastack(pkt, routing_table)
    return

def route_pkt_datamulticast(pkt, routing_table, interface_table, sourcestr):#, rtrsocket):
    #log_write("entered route_pkt_datamulticast\n")
    selfid = list(routing_table.keys())[(list(routing_table.values())).index(['127.0.0.1',0,0])]
    #log_write("computed selfid\n")
    pkttype, seq, src, N, K, dst1, dst2, dst3, pktlen, data = decapsulate_datamulticast(pkt)
    #log_write("decapsulated packet\n")
    dstlist = [dst1, dst2, dst3]
    if K == 1: # removes N=1 or K=1
        next_hop = routing_table[dst1][0]
        next_port = routing_table[dst1][2]
        unicast_pkt = create_pkt_dataunicast(seq, src, selfid, dst1, data)
        send_packet(unicast_pkt, next_hop, next_port, sourcestr)
    else: # left with N=2,K=2 or N=3,K=2 or N=3,K=3
        #log_write("reached else statement after K==1\n")
        next_hop_1 = routing_table[dst1][0]
        next_port_1 = routing_table[dst1][2]
        next_hop_2 = routing_table[dst2][0]
        next_port_2 = routing_table[dst2][2]
        if N == 3:
            next_hop_3 = routing_table[dst3][0]
            next_port_3 = routing_table[dst3][2]
        else:
            next_hop_3 = next_hop_2
            next_port_3 = next_port_2
        next_hop_list = [next_hop_1, next_hop_2, next_hop_3]
        next_port_list = [next_port_1, next_port_2, next_port_3]
        if next_hop_1 == next_hop_2 == next_hop_3:
            #log_write("reached equal next hops\n")
            #log_write("length of pkt = " + str(len(pkt)) + "\n")
            #log_write("next_hop_1 = " + next_hop_1 + "\n")
            #log_write("sending packet: " + str(pkt) + "\n")
            send_packet(pkt, next_hop_1, next_port_1, sourcestr)
            #log_write("done sending\n")
        else:
            if N == K: # removes N=2,K=2 and N=3,K=3
                for i in range(0, K):
                    dst = dstlist[i]
                    next_hop = next_hop_list[i]
                    next_port = next_port_list[i]
                    unicast_pkt = create_pkt_dataunicast(seq, src, selfid, dst, data)
                    send_packet(unicast_pkt, next_hop, next_port, sourcestr)
            else: # left with N=3, K=2
                #log_write("reached else statement after N==K\n")
                curr_next_hop = '127.0.0.1'
                curr_next_port = 0
                curr_min_dist = (routing_table[dst1][1] + routing_table[dst2][1] + routing_table[dst3][1])/3
                for i in range(0, N): # at most we should send centroid packets to N unique routers
                    if i == 0:
                        potential_next_hop = routing_table[dst1][0]
                        potential_next_port = routing_table[dst1][2]
                    elif i == 1:
                        potential_next_hop = routing_table[dst2][0]
                        potential_next_port = routing_table[dst2][2]
                        if routing_table[dst2][0] == routing_table[dst1][0]:
                            continue
                    elif i == 2:
                        potential_next_hop = routing_table[dst3][0]
                        potential_next_port = routing_table[dst3][2]
                        if routing_table[dst3][0] == routing_table[dst2][0]:
                            continue
                        elif routing_table[dst3][0] == routing_table[dst1][0]:
                            continue
                    intfaddress = interface_table[potential_next_hop][0]
                    intfport = interface_table[potential_next_hop][1]
                    # turn off the socket on the interface corresponding to potential_next_hop
                    #rtrsocket.close() # check
                    centroid_req_pkt = create_pkt_centroidrequest(seq, selfid, N, dst1, dst2, dst3)
                    send_packet(centroid_req_pkt, potential_next_hop, potential_next_port, sourcestr)
                    #log_write("lenpkt: " + str(len(centroid_req_pkt)) + "\n"))
                    #log_write("intf: " + str(intfaddress) + ":" + str(intfport) + "\n")
                    #centroid_reply_pkt = receive_packet(intfaddress, intfport)
                    # turn that socket back on
                    #potential_dist = route_pkt_centroidreply(centroid_reply_pkt)                    
                    # while loop that checks for payload file's existence
                    while True:
                        try:
                            f = open("centroidreplypayload.txt", "r")
                            break
                        except:
                            pass
                    # read data from file
                    potential_dist = float(f.read())
                    f.close()
                    # delete file
                    os.remove("centroidreplypayload.txt")
                    if potential_dist < curr_min_dist:
                        curr_next_hop = potential_next_hop
                        curr_next_port = potential_next_port
                        curr_min_dist = potential_dist
                if curr_next_hop == '127.0.0.1':
                    for i in range(0, K):
                        dst = dstlist[i]
                        next_hop = next_hop_list[i]
                        next_port = next_port_list[i]
                        unicast_pkt = create_pkt_dataunicast(seq, src, selfid, dst, data)
                        send_packet(unicast_pkt, next_hop, next_port, sourcestr)
                else:
                    if routing_table[dst1][0] == routing_table[dst2][0]:
                        newdst1 = dst1
                        newdst2 = dst2
                    elif routing_table[dst1][0] == routing_table[dst3][0]:
                        newdst1 = dst1
                        newdst2 = dst3
                    elif routing_table[dst2][0] == routing_table[dst3][0]:
                        newdst1 = dst2
                        newdst2 = dst3
                    else:
                        dist1 = routing_table[dst1][1]
                        dist2 = routing_table[dst2][1]
                        dist3 = routing_table[dst3][1]
                        if dist1 >= dist2 and dist1 >= dist3:
                            newdst1 = dst2
                            newdst2 = dst3
                        elif dist2 >= dist1 and dist2 >= dist3:
                            newdst1 = dst1
                            newdst2 = dst3
                        elif dist3 >= dist1 and dist3 >= dist2:
                            newdst1 = dst1
                            newdst2 = dst2
                    newdatamulticastpkt = create_pkt_datamulticast(seq, src, 2, 2, newdst1, newdst2, 0, data)
                    send_packet(newdatamulticastpkt, curr_next_hop, curr_next_port, sourcestr)      
    return
    
def route_pkt_dataunicast(pkt, routing_table, sourcestr):
    pkttype, seq, src, srccentroid, dst, pktlen, data = decapsulate_dataunicast(pkt)
    next_hop = routing_table[dst][0]
    next_port = routing_table[dst][2]
    send_packet(pkt, next_hop, next_port, sourcestr)
    
def route_pkt_centroidrequest(pkt, routing_table, sourcestr):
    pkttype, seq, src, N, dst1, dst2, dst3 = decapsulate_centroidrequest(pkt)
    selfid = list(routing_table.keys())[(list(routing_table.values())).index(['127.0.0.1',0,0])]
    dist1 = routing_table[dst1][1]
    dist2 = routing_table[dst2][1]
    dist3 = routing_table[dst3][1]
    meandist = (dist1+dist2+dist3)/3
    next_hop = routing_table[src][0]
    next_port = routing_table[src][2]
    centroidreplypkt = create_pkt_centroidreply(seq, selfid, meandist)
    send_packet(centroidreplypkt, next_hop, next_port, sourcestr)

def route_pkt_centroidreply(pkt):
    pkttype, seq, src, meandist = decapsulate_centroidreply(pkt)
    # write to file
    f = open("centroidreplypayload.txt", "w")
    f.write(f"{meandist}")
    f.close()
    return #meandist

def route_pkt_datamulticastack(pkt, routing_table): # not done
    pkttype, seq, src, dst = decapsulate_datamulticastack(pkt)
    return

def route_pkt_dataunicastack(pkt, routing_table): # not done
    pkttype, seq, src, dst, dstcentroid = decapsulate_dataunicastack(pkt)
    return

def host_route_pkt_dataunicast(pkt, routing_table): # not done
    pkttype, seq, src, srccentroid, dst, pktlen, data = decapsulate_dataunicast(pkt)
    # respond w ack
    return


# send/receive packets

#import IN
def send_packet(pkt, dst_addr, port_num, sourcestr):
    # """
    # Sends a packet to the dest_addr using the UDP socket
    # """

    pkttypestr = pkttype_string(pkt)
    log_write(sourcestr + "Sending " + str(pkttypestr) + " packet to destination: " + str(dst_addr) + ":" + str(port_num) + "\n")

    my_socket = socket(AF_INET, SOCK_DGRAM)
    #my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, str((intfstr + '\0').encode()))
    my_socket.sendto(pkt, (dst_addr, port_num))
    #log_write("packet sent successfully\n")
    my_socket.close()
    
    return

#def receive_packet(my_addr, port_num):
#    # """
#    # Listens at an IP:port
#    # """
#    my_socket = socket(AF_INET, SOCK_DGRAM)
#    my_socket.bind((my_addr, port_num))
#    data, addr = my_socket.recvfrom(1024)
#    my_socket.close()
#
#    pkttypestr = pkttype_string(data)
#    log_write("Received " + pkttypestr + " packet from source " + str(addr) + "\n")
#    
#    return pkt

def log_write(stringone):
    log_file = open("output.txt","a")
    log_file.write(stringone)
    log_file.close()

def pkttype_string(pkt):
    pkttype = pkt[0]
    if pkttype == 0:
        pkttypestr = "Data Multicast"
    elif pkttype == 1:
        pkttypestr = "Data Unicast"
    elif pkttype == 2:
        pkttypestr = "Centroid Request"
    elif pkttype == 3:
        pkttypestr = "Centroid Reply"
    elif pkttype == 4:
        pkttypestr = "Multicast ACK"
    elif pkttype == 5:
        pkttypestr = "Unicast ACK"
    return pkttypestr
