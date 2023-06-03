#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct

import subprocess
import time 
from datetime import datetime



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
    return int(entry_val)

def read_register(register, idx, thrift_port):
    p = subprocess.Popen(['simple_switch_CLI', '--thrift-port', str(thrift_port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input="register_read %s %d" % (register, idx))
    reg_val = [l for l in stdout.split('\n') if ' %s[%d]' % (register, idx) in l][0].split('= ', 1)[1]
    return int(reg_val)

def write_register(register, idx, value ,thrift_port):
    p = subprocess.Popen(['simple_switch_CLI', '--thrift-port', str(thrift_port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input="register_write %s %d %d" % (register, idx, value))
    #reg_val = [l for l in stdout.split('\n') if ' %s[%d]' % (register, idx) in l][0].split('= ', 1)[1]
    return 
    
def table_delete(table, idx, thrift_port):
    p = subprocess.Popen(['simple_switch_CLI', '--thrift-port', str(thrift_port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input="table_delete %s %d" % (table, idx))
    return 

def table_add(table, parametro, thrift_port):
    p = subprocess.Popen(['simple_switch_CLI', '--thrift-port', str(thrift_port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input="table_add %s" % (parametro))
    var_handle = [l for l in stdout.split('\n') if ' %s' % ('added') in l][0].split('handle ', 1)[1]
    return int(var_handle)



def main():
    lista_switches=['S1C1','S1C2','S1C3','S1C4','S1CORE','S2C1','S2C2','S2C3','S2C4','S2CORE','S3C1','S3C2','S3C3','S3C4','S3CORE','S4C1','S4C2','S4C3','S4C4','S4CORE']
    portas_thrift= [9090  ,9091  ,9092  ,9093  ,9094    ,9095,9096,9097,9098,9099,9100,9101,9102,9103,9104,9105,9106,9107,9108,9109]
    varIntervaloPooling=5
    faca_laco=True
    procuraerro=True
    procurarollbak=False
    while faca_laco:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time.sleep(now.second%varIntervaloPooling+((1000000-now.microsecond)/1000000))
        #print("Current Time =", current_time)

        for i in range(0,len(lista_switches)):
            
            pstatus=read_registerAll("porta_status",portas_thrift[i])
            #print (pstatus)

            #varGatilho=read_registerAll("pacote_gatilho",portas_thrift[i])
            #print(varGatilho)
            for j in range(0,len(pstatus)):
                #Achou erro
                if pstatus[j]=="1" and procuraerro:
                    #prepara variaveis
                    print("\n \n ERRO Encontrado")
                    file = open("/home/p4/FRRFTK4/teste.txt", 'r')
                    varTemp1=file.readline()
                    file.close()
                    varTemp2=varTemp1.split('-')
                    varScriptErro=int(varTemp2[0][-1])
                    varHostSrc=int(varTemp2[1])
                    varPodSrc=int(varTemp2[2])
                    varHostDst=int(varTemp2[3])
                    varPodDst=int(varTemp2[4]) 
                    varEntry=[0,0,0,0,0,0,0,0,0]       
                    # erro 0 usado para gerar o baseline
                    #executa acoes para script erro 1 ou 2
                    if varScriptErro==1 or varScriptErro==2:
                        #arruma agregacao src
                        if varHostSrc<=2:
                            varThriftSrc=9099+varPodSrc
                            varThriftDst=9099+varPodDst
                        else:
                            varThriftSrc=9104+varPodSrc
                            varThriftDst=9104+varPodDst

                    if varScriptErro==3 or  varScriptErro==4:
                        #arruma agregacao src
                        if varHostSrc<=2:
                            varThriftSrc=9089+varPodSrc
                            varThriftDst=9089+varPodDst
                        else:
                            varThriftSrc=9094+varPodSrc
                            varThriftDst=9094+varPodDst
                    #apaga rota no agregacao de saida
                    networkEntry=table_entry("MyIngress.ipv4_lpm","10."+str(varPodDst)+".0.0/16",varThriftSrc)
                    table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftSrc)
                    # insere rota para outro no agregacao
                    #
                    # verificar se nao precisar ajustar o mac direito... esta gerando mac errado                                                
                    varEntry[0]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPodDst)+".0.0/16 => 00:00:0"+str(varPodDst+1)+":00:00:00 4",varThriftSrc)
                    #gera o gatilho para saida
                    #usa o registrador 5 para nao conflitar com a porta
                    #precisava ler o registrado para atualizar a variavel automaticamente
                    write_register("pacote_gatilho", 5, 250 ,varThriftSrc)
                    #arruma agregacao DST
                    #armazena codigos de entrada da tabela de rotas para fazer o roll back
                    varIndice=1
                    if varPodDst!=1:
                        networkEntry=table_entry("MyIngress.ipv4_lpm","10.1.0.0/16",varThriftDst)
                        table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftDst)
                        varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.1.0.0/16 => 00:00:01:00:00:00 4",varThriftDst)
                        varIndice=varIndice+1
                    if varPodDst!=2:
                        networkEntry=table_entry("MyIngress.ipv4_lpm","10.2.0.0/16",varThriftDst)
                        table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftDst)
                        varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.2.0.0/16 => 00:00:02:00:00:00 4",varThriftDst)                                
                        varIndice=varIndice+1
                    if varPodDst!=3:
                        networkEntry=table_entry("MyIngress.ipv4_lpm","10.3.0.0/16",varThriftDst)
                        table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftDst)
                        varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.3.0.0/16 => 00:00:03:00:00:00 4",varThriftDst)
                        varIndice=varIndice+1
                    if varPodDst!=4:
                        networkEntry=table_entry("MyIngress.ipv4_lpm","10.4.0.0/16",varThriftDst)
                        table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftDst)
                        varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.4.0.0/16 => 00:00:04:00:00:00 4",varThriftDst)
                        varIndice=varIndice+1
                    #
                    #
                    #ARRUMA segunda rota no segundo agregacao
                    #
                    #
                    if varScriptErro==4:
                        #arruma agregacao src
                        if varHostSrc<=2:
                            varThriftSrc=9104+varPodSrc
                            varThriftDst=9104+varPodDst
                        else:
                            varThriftSrc=9099+varPodSrc
                            varThriftDst=9099+varPodDst
                        #apaga rota no agregacao de saida
                        networkEntry=table_entry("MyIngress.ipv4_lpm","10."+str(varPodDst)+".0.0/16",varThriftSrc)
                        table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftSrc)
                        # insere rota para outro no agregacao
                        #
                        # verificar se nao precisar ajustar o mac direito... esta gerando mac errado                                                
                        varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPodDst)+".0.0/16 => 00:00:0"+str(varPodDst+1)+":00:00:00 4",varThriftSrc)
                        varIndice=varIndice+1
                        #gera o gatilho para saida
                        #usa o registrador 5 para nao conflitar com a porta
                        #precisava ler o registrado para atualizar a variavel automaticamente
                        write_register("pacote_gatilho", 5, 250 ,varThriftSrc)
                        #arruma agregacao DST
                        #armazena codigos de entrada da tabela de rotas para fazer o roll back
                        if varPodDst!=1:
                            networkEntry=table_entry("MyIngress.ipv4_lpm","10.1.0.0/16",varThriftDst)
                            table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftDst)
                            varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.1.0.0/16 => 00:00:01:00:00:00 4",varThriftDst)
                            varIndice=varIndice+1
                        if varPodDst!=2:
                            networkEntry=table_entry("MyIngress.ipv4_lpm","10.2.0.0/16",varThriftDst)
                            table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftDst)
                            varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.2.0.0/16 => 00:00:02:00:00:00 4",varThriftDst)                                
                            varIndice=varIndice+1
                        if varPodDst!=3:
                            networkEntry=table_entry("MyIngress.ipv4_lpm","10.3.0.0/16",varThriftDst)
                            table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftDst)
                            varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.3.0.0/16 => 00:00:03:00:00:00 4",varThriftDst)
                            varIndice=varIndice+1
                        if varPodDst!=4:
                            networkEntry=table_entry("MyIngress.ipv4_lpm","10.4.0.0/16",varThriftDst)
                            table_delete("MyIngress.ipv4_lpm",networkEntry,varThriftDst)
                            varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.4.0.0/16 => 00:00:04:00:00:00 4",varThriftDst)
                            varIndice=varIndice+1

                    #prepara o gatilho de volta
                    write_register("pacote_gatilho", 5, 250 ,varThriftDst)                  
                    procuraerro=False
                    procurarollbak=True
                #
                #
                # Faz plano de volta
                #
                #

                if pstatus[j]=="2" and procurarollbak:
                    print("\n \n Roll back inciado")
                    #prepara variaveis
                    file = open("/home/p4/FRRFTK4/teste.txt", 'r')
                    varTemp1=file.readline()
                    file.close()
                    varTemp2=varTemp1.split('-')
                    varScriptErro=int(varTemp2[0][-1])
                    varHostSrc=int(varTemp2[1])
                    varPodSrc=int(varTemp2[2])
                    varHostDst=int(varTemp2[3])
                    varPodDst=int(varTemp2[4]) 
            
                    #executa acoes para script erro 1 ou 2
                    if varScriptErro==1 or varScriptErro==2:
                        #arruma agregacao src
                        if varHostSrc<=2:
                            varThriftSrc=9099+varPodSrc
                            varThriftDst=9099+varPodDst
                        else:
                            varThriftSrc=9104+varPodSrc
                            varThriftDst=9104+varPodDst
                    if varScriptErro==3 or  varScriptErro==4:
                        #arruma agregacao src
                        if varHostSrc<=2:
                            varThriftSrc=9089+varPodSrc
                            varThriftDst=9089+varPodDst
                        else:
                            varThriftSrc=9094+varPodSrc
                            varThriftDst=9094+varPodDst
                    #apaga rota no agregacao de saida
                    table_delete("MyIngress.ipv4_lpm",varEntry[0],varThriftSrc)
                    # insere rota para outro no agregacao
                    #
                    # verificar se nao precisar ajustar o mac direito... esta gerando mac errado                        
                    varEntry[0]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPodDst)+".0.0/16 => 00:00:0"+str(varPodDst+1)+":00:00:00 3",varThriftSrc)
                    #arruma agregacao DST
                    #armazena codigos de entrada da tabela de rotas para fazer o roll back
                    varIndice=1
                    if varPodDst!=1:
                        table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftDst)
                        table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.1.0.0/16 => 00:00:01:00:00:00 3",varThriftDst)
                        varIndice=varIndice+1
                    if varPodDst!=2:
                        table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftDst)
                        varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.2.0.0/16 => 00:00:02:00:00:00 3",varThriftDst)                                
                        varIndice=varIndice+1
                    if varPodDst!=3:
                        table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftDst)
                        varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.3.0.0/16 => 00:00:03:00:00:00 3",varThriftDst)
                        varIndice=varIndice+1
                    if varPodDst!=4:
                        table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftDst)
                        varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.4.0.0/16 => 00:00:04:00:00:00 3",varThriftDst)
                        varIndice=varIndice+1

                    #ARRUMA segunda rota no segundo agregacao
                    if varScriptErro==4:
                        #arruma agregacao src
                        if varHostSrc<=2:
                            varThriftSrc=9104+varPodSrc
                            varThriftDst=9104+varPodDst
                        else:
                            varThriftSrc=9099+varPodSrc
                            varThriftDst=9099+varPodDst
                        #apaga rota no agregacao de saida
                        table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftSrc)

                        # insere rota para outro no agregacao
                        #
                        # verificar se nao precisar ajustar o mac direito... esta gerando mac errado                        
                        table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPodDst)+".0.0/16 => 00:00:0"+str(varPodDst+1)+":00:00:00 3",varThriftSrc)
                        varIndice=varIndice+1
                        #arruma agregacao DST
                        #armazena codigos de entrada da tabela de rotas para fazer o roll back
                        if varPodDst!=1:
                            table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftDst)
                            table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.1.0.0/16 => 00:00:01:00:00:00 3",varThriftDst)
                            varIndice=varIndice+1
                        if varPodDst!=2:
                            table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftDst)
                            varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.2.0.0/16 => 00:00:02:00:00:00 3",varThriftDst)                                
                            varIndice=varIndice+1
                        if varPodDst!=3:
                            table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftDst)
                            varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.3.0.0/16 => 00:00:03:00:00:00 3",varThriftDst)
                            varIndice=varIndice+1
                        if varPodDst!=4:
                            table_delete("MyIngress.ipv4_lpm",varEntry[varIndice],varThriftDst)
                            varEntry[varIndice]=table_add("MyIngress.ipv4_lpm","MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.4.0.0/16 => 00:00:04:00:00:00 3",varThriftDst)
                            varIndice=varIndice+1
                    faca_laco=False
                    procurarollbak=False

                
if __name__ == '__main__':
    main()
