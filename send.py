#!/usr/bin/env python
# 'destino / repeticoes / tamanho / intervalo'
    
import argparse
import sys
import socket
import random
import struct
import time
import os

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def main():
    time.sleep(1) # espera o receive.py subir
    if len(sys.argv)<3:
        print 'pass 2 arguments: <destination> "<message>"'
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    print "sending on interface %s to %s" % (iface, str(addr))
    i=0
    nSeq=0
    while i<int(sys.argv[2]):
        nSeq = nSeq +1
        pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
        pkt = pkt /IP(dst=addr) / TCP(dport=1234, sport=54321,seq=nSeq) / "{:.11f}".format(time.time())
        if len(pkt)<(int(sys.argv[3])+14):
            myString = "\x00"*(int(sys.argv[3])-len(pkt)+14)
            pkt=pkt/myString
        i=i+1
        sendp(pkt, iface=iface, verbose=False)

if __name__ == '__main__':
    main()