#!/usr/bin/env python
import sys
import struct
import os
import time
import random

def main():
    k=int(sys.argv[1])
#cria conf comutadores cORE
    varCore=1
    while varCore<=((k/2)**2):
        file = open("s"+str(varCore)+"core.txt", 'w')
        varPod=1      
        while varPod<=k:
            file.write("table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPod)+".0.0/16 => 08:00:00:"+str(varPod).zfill(2)+":03:00 "+str(varPod) +"\n")
            varPod=varPod+1     
        varPod=1      
        while varPod<=k:
            if varPod<k:
                file.write("table_add MyIngress.ipv4_lpm_backup MyIngress.ipv4_forward_backup 10."+str(varPod)+".0.0/16 => 08:00:00:"+str(varPod).zfill(2)+":03:00 "+str(varPod+1)+"\n")
            else:
                file.write("table_add MyIngress.ipv4_lpm_backup MyIngress.ipv4_forward_backup 10."+str(varPod)+".0.0/16 => 08:00:00:"+str(varPod).zfill(2)+":03:00 "+str(1)+"\n")
            varPod=varPod+1
        varPod=1      
        while varPod<=k:
            file.write("mirroring_add "+str(varPod)+" "+str(varPod)+"\n")
            varPod=varPod+1
        varCore=varCore+1
        file.close()      
        
#cria conf comutadores TOR

#cria rota principal para o host
    varPod=1
    while varPod<=(k):
        varTor=1
        while varTor<=(k/2):
            file = open("s"+str(varTor)+"c"+str(varPod)+".txt", 'w')          
            varHost=1
            varPorta=1
            while varHost<=((k/2)**2):
                if (varHost>((varTor-1)*(k/2))) and (varHost<=(varTor*(k/2))):
                   file.write("table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPod)+"."+str(varHost)+"."+str(varHost)+"/32 => 08:00:00:"+str(varPod).zfill(2)+":"+str(varHost).zfill(2)+":"+str(varHost).zfill(2)+" "+str(varPorta) +"\n")
                   varPorta=varPorta+1
                else:
                   file.write("table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPod)+"."+str(varHost)+"."+str(varHost)+"/32 => 08:00:00:"+str(varPod).zfill(2)+":"+str(varHost).zfill(2)+":00 "+str(int((k/2)+1)) +"\n")
                varHost=varHost+1 
            varTor=varTor+1
            file.close()
        varPod=varPod+1 

#cria rota backup para o host
    varPod=1
    while varPod<=(k):
        varTor=1
        while varTor<=(k/2):
            file = open("s"+str(varTor)+"c"+str(varPod)+".txt", 'a')          
            varHost=1
            varPorta=1
            while varHost<=((k/2)**2):
                if (varHost>((varTor-1)*(k/2))) and (varHost<=(varTor*(k/2))):
                   file.write("table_add MyIngress.ipv4_lpm_lpm_backup MyIngress.ipv4_forward_lpm_backup 10."+str(varPod)+"."+str(varHost)+"."+str(varHost)+"/32 => 08:00:00:"+str(varPod).zfill(2)+":"+str(varHost).zfill(2)+":"+str(varHost).zfill(2)+" "+str(varPorta) +"\n")
                   varPorta=varPorta+1
                else:
                   file.write("table_add MyIngress.ipv4_lpm_lpm_backup MyIngress.ipv4_forward_lpm_backup 10."+str(varPod)+"."+str(varHost)+"."+str(varHost)+"/32 => 08:00:00:"+str(varPod).zfill(2)+":"+str(varHost).zfill(2)+":00 "+str(int((k/2)+2)) +"\n")
                varHost=varHost+1 
            varTor=varTor+1
            file.close()
        varPod=varPod+1 

#cria rota para as redes
    varPod=1
    while varPod<=(k):
        varTor=1
        while varTor<=(k/2):
            file = open("s"+str(varTor)+"c"+str(varPod)+".txt", 'a')          
            varRede=1
            while varRede<=k:
                if varRede!=varPod:
                   file.write("table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varRede)+".0.0/16 => 08:00:00:"+str(varPod).zfill(2)+":"+str(int((k/2)+1)).zfill(2)+":00 "+str(int((k/2)+1)) +"\n")
                varRede=varRede+1 
            varTor=varTor+1
            file.close()
        varPod=varPod+1 


#cria rota backup para as redes
    varPod=1
    while varPod<=(k):
        varTor=1
        while varTor<=(k/2):
            file = open("s"+str(varTor)+"c"+str(varPod)+".txt", 'a')          
            varRede=1
            while varRede<=k:
                if varRede!=varPod:
                   file.write("table_add MyIngress.ipv4_lpm_lpm_backup MyIngress.ipv4_forward_lpm_backup 10."+str(varRede)+".0.0/16 => 08:00:00:"+str(varPod).zfill(2)+":"+str(int((k/2)+2)).zfill(2)+":00 "+str(int((k/2)+2)) +"\n")
                varRede=varRede+1 
            varTor=varTor+1
            file.close()
        varPod=varPod+1 



#cria rota backup para as redes
    varPod=1
    while varPod<=(k):
        varTor=1
        while varTor<=(k/2):
            file = open("s"+str(varTor)+"c"+str(varPod)+".txt", 'a')          
            varPorta=1
            while varPorta<=k:
                file.write("mirroring_add "+str(varPorta)+" "+str(varPorta)+"\n")
                varPorta=varPorta+1 
            varTor=varTor+1
            file.close()
        varPod=varPod+1 


#cria conf comutadores AGGR

#cria rota principal para o host
    varPod=1
    while varPod<=(k):
        varAggr=1
        while varAggr<=(k/2):
            file = open("s"+str(int(varAggr+(k/2)))+"c"+str(varPod)+".txt", 'w')          
            varHost=1
            varPorta=1
            while varHost<=((k/2)**2):
                if (varHost>((varAggr-1)*(k/2))) and (varHost<=(varAggr*(k/2))):
                   file.write("table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPod)+"."+str(varHost)+"."+str(varHost)+"/32 => 08:00:00:"+str(varPod).zfill(2)+":"+str(varHost).zfill(2)+":00 1" +"\n")
                   i=1
                   while i<(k/2):
                       varHostTemp=int(((k/2)**2)-((k/2)*i)+varHost)
                       if (varHostTemp>((k/2)**2)):
                          varHostTemp=int(varHostTemp-((k/2)**2))
                       file.write("table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPod)+"."+str(varHostTemp)+"."+str(varHostTemp)+"/32 => 08:00:00:"+str(varPod).zfill(2)+":"+str(varHostTemp).zfill(2)+":00 "+str(i+1) +"\n")
                       i=i+1
                varHost=varHost+1 
            varAggr=varAggr+1
            file.close()
        varPod=varPod+1 

#cria rota backup para o host
    varPod=1
    while varPod<=(k):
        varAggr=1
        while varAggr<=(k/2):
            file = open("s"+str(int(varAggr+(k/2)))+"c"+str(varPod)+".txt", 'a')          
            varHost=1
            varPorta=1
            while varHost<=((k/2)**2):
                if (varHost>((varAggr-1)*(k/2))) and (varHost<=(varAggr*(k/2))):
                   file.write("table_add MyIngress.ipv4_lpm_forward_backup MyIngress.ipv4_forward_forward_backup 10."+str(varPod)+"."+str(varHost)+"."+str(varHost)+"/32 => 08:00:00:"+str(varPod).zfill(2)+":"+str(varHost).zfill(2)+":00 2" +"\n")
                   i=1
                   while i<(k/2):
                       varHostTemp=int(((k/2)**2)-((k/2)*i)+varHost)
                       if (varHostTemp>((k/2)**2)):
                          varHostTemp=int(varHostTemp-((k/2)**2))
                       iTemp=i+2
                       if iTemp>k/2:
                          iTemp=int(iTemp-(k/2))
                       file.write("table_add MyIngress.ipv4_lpm_forward_backup MyIngress.ipv4_forward_forward_backup 10."+str(varPod)+"."+str(varHostTemp)+"."+str(varHostTemp)+"/32 => 08:00:00:"+str(varPod).zfill(2)+":"+str(varHostTemp).zfill(2)+":00 "+str(iTemp) +"\n")
                       i=i+1
                varHost=varHost+1 
            varAggr=varAggr+1
            file.close()
        varPod=varPod+1 

#cria rota outros pod
    varPod=1
    while varPod<=(k):
        varAggr=1
        while varAggr<=(k/2):
            file = open("s"+str(int(varAggr+(k/2)))+"c"+str(varPod)+".txt", 'a')          
            varPod2=1
            while varPod2<=k:
                if varPod2!=varPod:
                   file.write("table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10."+str(varPod2)+".0.0/16 => 08:00:00:"+str(varPod2).zfill(2)+":00:00 "+str(int((k/2)+1))+"  \n")            
                varPod2=varPod2+1 
            varAggr=varAggr+1
            file.close()
        varPod=varPod+1 

#cria rota outros pod backup
    varPod=1
    while varPod<=(k):
        varAggr=1
        while varAggr<=(k/2):
            file = open("s"+str(int(varAggr+(k/2)))+"c"+str(varPod)+".txt", 'a')          
            varPod2=1
            while varPod2<=k:
                if varPod2!=varPod:
                   file.write("table_add MyIngress.ipv4_lpm_forward_backup MyIngress.ipv4_forward_forward_backup 10."+str(varPod2)+".0.0/16 => 08:00:00:"+str(varPod2).zfill(2)+":00:00 "+str(int((k/2)+2))+" \n")            
                varPod2=varPod2+1 
            varAggr=varAggr+1
            file.close()
        varPod=varPod+1 



#cria rota backup para as redes
    varPod=1
    while varPod<=(k):
        varAggr=1
        while varAggr<=(k/2):
            file = open("s"+str(int(varAggr+(k/2)))+"c"+str(varPod)+".txt", 'a')          
            varPorta=1
            while varPorta<=k:
                file.write("mirroring_add "+str(varPorta)+" "+str(varPorta)+"\n")
                varPorta=varPorta+1 
            varAggr=varAggr+1
            file.close()
        varPod=varPod+1 

 
if __name__ == '__main__':
    main()
