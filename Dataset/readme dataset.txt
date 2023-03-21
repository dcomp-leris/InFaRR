The logs of the tests performed are organized as follows:
1) All algorithms were tested in an error-free environment to create a comparison baseline. In this scenario there is no packet loss. The files are named as “algorithm name” + “0”.log.
2) The scenario with 1 error the files are named as “algorithm name” + “1”.log. Note that the “Control Plane” algorithm lost packets.

3) The scenario with 2 errors the files are named as “algorithm name” + “2”.log. Note that the “Control Plane” algorithm lost packets, rotor and static.

4) The scenario with 2 errors the files are named as “algorithm name” + “3”.log. Note that the “Control Plane” algorithm lost packets, rotor and static.

Data structure:
Each test package is made up of 750 packages, the failure simulation occurs between packages 250 and 500. The objective of the test is to map the network's convergence capacity and recovery after failure returns.
The 750 packets are sent sequentially, where the TCP_SEQ header is used to identify the packet (1-750)
Time: Time the packet was generated, information that will be sent in the packet payload
IP_SRC: Source IP, host where the packet was generated
IP_DST: Destination IP, host where the packet was received
IP_TTL: Number of hops the packet was routed
IP_LEN: Packet size
TCP_SEQ; Package Sequence Number
TIME_ORIGEM: Time of receipt of the packet at the destination host
TIME_DELTA: Calculation of packet transmission time
