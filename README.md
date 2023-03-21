InFaRR (In-network Fast ReRouting) is an algorithm for fast rerouting in programmable data planes. 

Implemented in P4, InFaRR is free of additional management headers (overheads) and network state management packets (hearbeats). 

InFaRR has four essential features not jointly found in other recovery mechanisms: Loop prevention, Pushback, Recognition and Restoration and Return to the main route. 

Tests in a Sandard Fat-Tree and AB Fat-Tree topology with failures in different scenarios showed positive results when compared to state-of-the-art algorithms in the literature. 

In scenarios in which the other algorithms were able to recover, InFaRR presented less time variation in packet delay when the Pushback, loop Prevention and Recognition and Restoration mechanisms was used, resulting in fewer hops when bypassing the failure. 

In scenarios with multiple failures, InFaRR successfully rerouted where the others algorithms in some cases looped. The unique mechanism for returning to the main route innovated in view of the possibility of verifying remote links in the data plane, making it possible to return to the main route without intervention from the control plane.

This directory contains the InfaRR source file and the Mininet files for building the FATTREE and ABFATREE environments for carrying out the tests.

The results obtained are displayed in the log files in the DATASET folder.

The source codes of the other algorithms used are available in the P4 folder.
