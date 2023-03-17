import os
for i in range(9090,9110):   
    print "simple_switch_CLI  --thrift-port "+str(i)+" < "+str(i)+".id"
    file = open(str(i)+".id", 'w')
    file.write("register_write SW_ID 1 "+str(i))
    file.close

    