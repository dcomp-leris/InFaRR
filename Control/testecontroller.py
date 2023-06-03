#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct

import subprocess
import time 
#import sleep


from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP



def read_registerAll(register, thrift_port):
    p = subprocess.Popen(['simple_switch_CLI', '--thrift-port', str(thrift_port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input="register_read %s" % (register))
    reg_val = [l for l in stdout.split('\n') if ' %s' % (register) in l][0].split('= ', 1)[1]
    return reg_val.split(", ")

def table_entry(table, network, thrift_port):
    p = subprocess.Popen(['simple_switch_CLI', '--thrift-port', str(thrift_port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input="table_dump_entry_from_key %s %s" % (table, network))
    entry_val = [l for l in stdout.split('\n') if ' %s' % ('Dumping') in l][0].split('0x', 1)[1]
    return entry_val


def table_delete(table, idx, thrift_port):
    p = subprocess.Popen(['simple_switch_CLI', '--thrift-port', str(thrift_port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input="table_delete %s %d" % (table, idx))
    return 

def table_add(table, parametro, thrift_port):
    p = subprocess.Popen(['simple_switch_CLI', '--thrift-port', str(thrift_port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input="table_add %s" % (parametro))
    var_handle = [l for l in stdout.split('\n') if ' %s' % ('added') in l][0].split('handle ', 1)[1]
    print(var_handle)
    return int(var_handle)


def main():
    lista_switches=['S1C1','S1C2','S1C3','S1C4','S1CORE','S2C1','S2C2','S2C3','S2C4','S2CORE','S3C1','S3C2','S3C3','S3C4','S3CORE','S4C1','S4C2','S4C3','S4C4','S4CORE']
    portas_thrift=[9090,9091,9092,9093,9094,9095,9096,9097,9098,9099,9100,9101,9102,9103,9104,9105,9106,9107,9108,9109]
    pstatus=read_registerAll("porta_status",portas_thrift[5])
    varEntry=[0,0]
    print(pstatus)
    networkEntry=table_entry("MyIngress.ipv4_lpm","10.3.0.0/16",portas_thrift[4])
    print(networkEntry)
    table_delete("MyIngress.ipv4_lpm",int(networkEntry),9094)
    varEntry[0]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.3.0.0/16 => 00:00:00:04:03:00 4",9094)
    table_delete("MyIngress.ipv4_lpm",varEntry[0],9094)
    varEntry[0]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.3.0.0/16 => 00:00:00:03:03:00 3",9094)
    table_delete("MyIngress.ipv4_lpm",varEntry[0],9094)


    
if __name__ == '__main__':
    main()
