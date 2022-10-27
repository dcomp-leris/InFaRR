#!/usr/bin/env python
import sys
import struct
import os
import time
import random

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import Ether, IP, TCP, UDP, Raw
from scapy.layers.inet import _IPOption_HDR

def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

class IPOption_MRI(IPOption):
    name = "MRI"
    option = 31
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B",
                                  length_of="swids",
                                  adjust=lambda pkt,l:l+4),
                    ShortField("count", 0),
                    FieldListField("swids",
                                   [],
                                   IntField("", 0),
                                   length_from=lambda pkt:pkt.count*4) ]
def handle_pkt(pkt):
    if TCP in pkt and pkt[TCP].dport == 1234:
        timeatual = float("{:.11f}".format(time.time()))
        timeorigem = float(pkt[Raw].load[:22])
        deltatime=timeatual-timeorigem
        newlog=["{:.11f}".format(timeatual),pkt[IP].src,pkt[IP].dst,pkt[IP].ttl,pkt[IP].len,pkt[TCP].sport,pkt[TCP].dport,pkt[TCP].seq,pkt[TCP].ack,"{:.11f}".format(timeorigem),"{:.11f}".format(deltatime)]
        for j in newlog:
            file.write(str(j))
            file.write(";")
        file.write(str(sys.argv[1]))
        file.write(";")
        file.write(str(sys.argv[2]))
        file.write(";")
        file.write(str(sys.argv[2][:-1]))
        file.write(";")
        file.write(str(varLote))

        file.write("\n")
        sys.stdout.flush()
        if pkt[TCP].seq>=750:
            file.close
            exit(1)

def main():
    global varLote
    varLote=random.randint(1,1000000)

    if len(sys.argv)<1:
        print 'pass 1 arguments: <destination> "<message>"'
        exit(1)
    global logflow
    logflow=["Time","IP_SRC","IP_DST","IP_TTL","IP_LEN","TCP_SPORT","TCP_DPORT","TCP_SEQ","TCP_ACK","TIME_ORIGEM","TIME_DELTA"]
    global file
    if os.path.isfile(str(sys.argv[1])):
        try:
            file = open(str(sys.argv[1]), 'a') #append to file
        except OSError:
            print("erro ao abrir o arquivo")
            sys.exit()
    else:    
        file = open(str(sys.argv[1]), 'w') #write new file
        for i in logflow:
            file.write(i)
            file.write(";")
        file.write("ARQUIVO;TESTE;ALGORITMO;LOTE")
        file.write("\n")
    ifaces = filter(lambda i: 'eth' in i, os.listdir('/sys/class/net/'))
    iface = ifaces[0]
    print "sniffing on %s" % iface
    sys.stdout.flush()
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()