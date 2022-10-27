#!/usr/bin/env python
import sys
import struct
import os
import time
import random

def main():
    #argumento 2 = numero repeticoes
    varPodSrc=1
    varPodDst=1
    varHostSrc=1
    varHostDst=1
    while varHostSrc<5:
        varPodSrc=1      
        while varPodSrc<5:
            varHostDst=1
            while varHostDst<5:
                varPodDst=1
                while varPodDst<5:

                    if len(sys.argv[2])==4:
                        vartemp=sys.argv[2]
                        varHostSrc=int(vartemp[0])
                        varPodSrc=int(vartemp[1])
                        varHostDst=int(vartemp[2])
                        varPodDst=int(vartemp[3])
                    # ignora os host pares dos pod e pro mesmo podre
                    if (varPodSrc!=varPodDst) and (varHostSrc%2==1) and (varHostDst%2==1):
                        file = open("teste.txt", 'w')
                        file.write(str(sys.argv[1])+str(sys.argv[3])+"-"+str(varHostSrc)+"-"+str(varPodSrc)+"-"+str(varHostDst)+"-"+str(varPodDst)+"\n")
                        file.close()
                    
                        file = open("/home/p4/FRRFTK4/P4/script_mininet."+str(sys.argv[3]),'w')
                        file.write("sh sleep 10 \n")
                        
                        if sys.argv[1] == "ufscar2":
                            file.write("sh /home/p4/FRRFTK4/pod-topo/nomeia_sw.sh \n")
                        
                        file.write("sh /home/p4/FRRFTK4/Control/gatilhodown-randomico \n")
                        file.write("xterm h"+str(varHostSrc)+"c"+str(varPodSrc)+" h"+str(varHostDst)+"c"+str(varPodDst)+" \n")
                        file.write("sh sleep 60 \n")
                        file.close()

                        file = open("/home/p4/FRRFTK4/Control/gatilhodown-randomico",'w')
                        file.write("cd /home/p4/FRRFTK4/Control/ \n")
                        
                        #se for codigo p4 limpo precisa rodar controller
                        if sys.argv[1] == "limpo" and sys.argv[3]!="0":
                            file.write("./clontroller.py & \n")
############################################################################
                        #um erro no core para acesso ao pod destino
                        if sys.argv[3] == "1" or sys.argv[3] == "2" or sys.argv[3] == "3":
                            if varHostSrc<=2:
                                #switch S1CORE
                                file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")              
                            else:
                                if varPodSrc==1 or varPodSrc==3:
                                    #switch S3CORE
                                    file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                    if varPodDst==1 or varPodDst==3:
                                        #s4c3
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta4down250.txt \n")
                                     
                                    elif varPodDst==2 or varPodDst==4:
                                        #s3c2 e s3c4
                                        file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                    
                                elif varPodSrc==2 or varPodSrc==4:
                                    #switch S2CORE
                                    file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                    if varPodDst==1 or varPodDst==3:
                                        #s3c1 s3c3
                                        file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta4down250.txt \n")
                                    elif varPodDst==2 or varPodDst==4:
                                        #s4c4
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                        
############################################################################
                        
                        #dois erro no core para acesso ao pod destino (rota principal e backup)
                        if sys.argv[3] == "2" or sys.argv[3] == "3":
                            if varHostSrc<=2:

                                if (varPodSrc==1 and varPodDst==4) or (varPodSrc==3 and varPodDst==2):
                                    #switch S3CORE porta secundaria
                                    file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                    file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                                                
                                #elif (varPodSrc==4 and varPodDst==2):
                                #    #switch S3CORE porta secundaria
                                #    file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                #    file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
 

                                else:
                                    if (varPodSrc==2 and varPodDst==1):
                                        #switch S2CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                        
                                    elif (varPodSrc==4 and varPodDst==3):
                                        #switch S2CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                        
                                    elif varPodDst==2 or varPodDst==4:
                                        #switch S2CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                                                    
                                    elif varPodDst==1 or varPodDst==3:
                                        #switch S3CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
############################################################################
                            else:
                                if varPodSrc==1 or varPodSrc==3:
                                                                   
                                    if (varPodSrc==1 and varPodDst==2):
                                        #switch S4CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                    
                                    
                                    elif (varPodSrc==3 and varPodDst==2) or (varPodSrc==2 and varPodDst==4) or (varPodSrc==4 and varPodDst==3) or (varPodSrc==1 and varPodDst==4):
                                        #switch S1CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                                                                              
                                    elif (varPodSrc==2 or varPodDst==1) and (varPodDst==1 or varPodDst==3):
                                        #switch S1CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")

                                    elif varPodDst==2 or varPodDst==4:
                                        #switch S4CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                    
                                    else:

                                        if varPodDst==1 or varPodDst==3:
                                            #switch S1CORE porta secundaria
                                            file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                            file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                                                    
                                        if varPodDst==2 or varPodDst==4:
                                            #switch S2CORE porta secundaria
                                            file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                            file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")

############################################################################
                                else:
                            
                                    if varPodSrc==4 and varPodDst==1:
                                        #switch S4CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                    
                                    elif (varPodSrc==2 and varPodDst==4) or (varPodSrc==4 and varPodDst==3) :
                                        #switch S1CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                        
                                    elif varPodSrc==2 and (varPodDst==3):
                                        #switch S4CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                    
                                    elif (varPodSrc==4 and varPodDst==2):
                                        #switch S1CORE porta secundaria
                                        file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                        file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")

                                    else:

                                        if varPodDst==1 or varPodDst==3:
                                            #switch S1CORE porta secundaria
                                            file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                            file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                                                    
                                        if varPodDst==2 or varPodDst==4:
                                            #switch S2CORE porta secundaria
                                            file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                            file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
    
                            
                            
                            #        file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")                                    
                            #        file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta4down250.txt \n")
                                
 
                        #dois erro no core para acesso ao pod destino (rota principal, secundario e terceario)
                        if sys.argv[3] == "3":
                            if varHostSrc<=2:
                                #switch S4CORE porta backup
                                file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta4down250.txt \n")

                                #switch S1CORE porta principal
#                                file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
#                                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                #switch S2CORE porta backup
#                                file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
#                                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta4down250.txt \n")
                            else:
# ************************************************

                                if varPodSrc==1 and (varPodDst==2 or varPodDst==4):
                                   #switch S2CORE porta tres
                                   file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                   file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                
                                elif varPodSrc==1 and (varPodDst==3):
                                   #switch S2CORE porta tres
                                   file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                   file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                
                                elif varPodSrc==2 and (varPodDst==1 or varPodDst==3):
                                   #switch S3CORE porta tres
                                   file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                   file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                

                                elif varPodSrc==2 and (varPodDst==4):
                                   #switch S3CORE porta tres
                                   file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                   file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                
                                elif varPodSrc==3 and (varPodDst==1):
                                   #switch S2CORE porta tres
                                   file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                   file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                                
                                
                                elif varPodSrc==3 and (varPodDst==2 or varPodDst==4 ):
                                   #switch S2CORE porta tres
                                   file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                   file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                
                                
                                elif varPodSrc==4 and varPodDst==2:
                                   #switch S3CORE porta tres
                                   file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                   file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                
                                elif varPodSrc==4 and (varPodDst==1 or varPodDst==3):
                                   #switch S3CORE porta tres
                                   file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                   file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                

                                elif varPodDst==1 or varPodDst==3:
                                    #switch S4CORE porta secundaria
                                    file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                    file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                                                                
                                elif varPodDst==2 or varPodDst==4:
                                    #switch S1CORE porta secundaria
                                    file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                                    file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")

 
                        file.close()
                        #vai chamar o bash m que executa o mininet
                        #argumento 1 = nome do teste
                        #argumento 3 = erro
                        
                        os.system("/home/p4/FRRFTK4/m "+str(sys.argv[1])+" "+str(sys.argv[3]))
                        time.sleep(random.randint(5,10))
                    
                    if len(sys.argv[2])==4:
                        varHostSrc=5
                        varPodSrc=5
                        varHostDst=5
                        varPodDst=5
                    varPodDst=varPodDst+1
                varHostDst=varHostDst+1    
            varPodSrc=varPodSrc+1
        varHostSrc=varHostSrc+1
              
            
            

if __name__ == '__main__':
    main()