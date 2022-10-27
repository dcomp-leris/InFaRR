/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

/* Define constants for types of packets */
#define PKT_INSTANCE_TYPE_NORMAL 0
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1
#define PKT_INSTANCE_TYPE_EGRESS_CLONE 2
#define PKT_INSTANCE_TYPE_COALESCED 3
#define PKT_INSTANCE_TYPE_INGRESS_RECIRC 4
#define PKT_INSTANCE_TYPE_REPLICATION 5
#define PKT_INSTANCE_TYPE_RESUBMIT 6

const bit<48> TESTE  = 1;
const bit<16> TYPE_IPV4 = 0x800;
const bit<8>  TYPE_TCP  = 6;
const bit<8>  TYPE_UDP  = 17;
const bit<8>  TYPE_ICMP  = 1;

const bit<1>  PORTA_DOWN  = 1;
const bit<1>  PORTA_UP  = 0;
const bit<1>  PIVO_FRR  = 1;
const bit<1>  NAO  = 0;
const bit<1>  SIM  = 1;

const bit<1>  REVALIDA  = 1;
const bit<1>  NAO_REVALIDA  = 0;
const bit<32>  NUMERO_FLUXOS = 100000;
const bit<32>  NUMERO_PORTAS = 4;
const bit<48>  TIME_OUT_GATILHO         =  500000;
const bit<48>  TIME_OUT_RECUPERA_FLUXO  =  100000;
const bit<48>  TIME_OUT_RECUPERA_ENLACE =  500000;
const bit<48>  TIME_OUT_VALIDA_CLONE    =  250000;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header tcp_t{
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<4>  res;
    bit<1>  cwr;
    bit<1>  ece;
    bit<1>  urg;
    bit<1>  ack;
    bit<1>  psh;
    bit<1>  rst;
    bit<1>  syn;
    bit<1>  fin;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> len;
    bit<16> checksum;
}

header icmp_t {
    bit<8> icmp_type;
    bit<8> icmp_code;
    bit<16> checksum;
    bit<16> identifier;
    bit<16> sequence_number;
    bit<64> timestamp;
}

struct metadata {
    /* empty */
}

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    tcp_t        tcp;
    udp_t        udp;
    icmp_t       icmp;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol){
            TYPE_ICMP: parse_icmp;
            TYPE_UDP: parse_udp;
            TYPE_TCP: parse_tcp;
            default: accept;
        }
    }
    state parse_tcp {
       packet.extract(hdr.tcp);
       transition accept;
    }
    
    state parse_udp {
      packet.extract(hdr.udp);
      transition accept;
    }

    state parse_icmp {
      packet.extract(hdr.icmp);
      transition accept;
    }

}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply {  }
}

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    register<bit<1>>(NUMERO_PORTAS) porta_status;
    register<bit<9>>(NUMERO_FLUXOS) fluxo_porta_entrada;
    register<bit<48>>(NUMERO_FLUXOS) fluxo_mac_entrada;
    register<bit<1>>(NUMERO_FLUXOS) fluxo_status;
    register<bit<48>>(NUMERO_FLUXOS) fluxo_tempo;
    register<bit<1>>(NUMERO_FLUXOS) fluxo_pivo_saida;
    register<bit<1>>(NUMERO_FLUXOS) clone_valida_fluxo;
    register<bit<16>>(NUMERO_PORTAS) SW_ID;                 
    // registra a porta thrift.... para troubleshooting
    register<bit<48>>(NUMERO_PORTAS) pacote_gatilho;                 

    action drop() {
        mark_to_drop(standard_metadata);
    }
    
    action fake_drop() {
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
	    hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
   }
   action ipv4_forward_backup(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.dstAddr = dstAddr;
    }
    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }
    table ipv4_lpm_backup {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            ipv4_forward_backup;
            drop;
            NoAction;

        }
        size = 1024;
        default_action = drop();
    }
    apply {
        
        bit<1> var_status_porta_saida;       
        bit<1> var_status_fluxo_saida;
        bit<48> var_fluxo_tempo;
        bit<48> var_hash_fluxo_porta_saida;
        bit<1> var_hash_fluxo_porta_entrada;
        bit<9> var_fluxo_porta_entrada;
        bit<1> var_fluxo_pivo_saida;
        bit<9> var_saida_primeira_rota;
        bit<1> var_clone_valida_fluxo;
        bit<1> var_drop;
        bit<16> varSW_ID;
        bit<48> var_pacote_gatilho;
        var_status_porta_saida = 0;        
        var_drop=NAO;
        
        var_status_fluxo_saida = 0;
        if (hdr.ipv4.isValid()) {
            if (hdr.ipv4.protocol==TYPE_ICMP){
                hash(var_hash_fluxo_porta_entrada,HashAlgorithm.crc32, (bit<32>)0, {hdr.ipv4.srcAddr, hdr.ipv4.dstAddr},(bit<32>)NUMERO_FLUXOS);                   
            } else if (hdr.ipv4.protocol==TYPE_TCP){
                hash(var_hash_fluxo_porta_entrada,HashAlgorithm.crc32, (bit<32>)0, {hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.tcp.srcPort, hdr.tcp.dstPort},(bit<32>)NUMERO_FLUXOS);
            } else if (hdr.ipv4.protocol==TYPE_UDP){
                hash(var_hash_fluxo_porta_entrada,HashAlgorithm.crc32, (bit<32>)0, {hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.udp.srcPort, hdr.udp.dstPort},(bit<32>)NUMERO_FLUXOS);
            } else {
                var_hash_fluxo_porta_entrada=0;
            }
            fluxo_porta_entrada.read(var_fluxo_porta_entrada,(bit<32>)var_hash_fluxo_porta_entrada);
            if (var_fluxo_porta_entrada == 0){
                fluxo_porta_entrada.write((bit<32>)var_hash_fluxo_porta_entrada,standard_metadata.ingress_port);
                fluxo_mac_entrada.write((bit<32>)var_hash_fluxo_porta_entrada,hdr.ethernet.srcAddr);
                var_fluxo_porta_entrada = standard_metadata.ingress_port;
            } 
            if (hdr.ipv4.ttl>0) {
                ipv4_lpm.apply();
                pacote_gatilho.read(var_pacote_gatilho,(bit<32>)standard_metadata.egress_spec);   
                if (((var_pacote_gatilho<=(bit<48>)hdr.tcp.seqNo)&&((var_pacote_gatilho*2)>(bit<48>)hdr.tcp.seqNo)&&(var_pacote_gatilho>0)) || 
                    ((((bit<48>)hdr.tcp.seqNo)==0)&&(var_pacote_gatilho<=(bit<48>)hdr.tcp.ackNo)&&((var_pacote_gatilho*2)>(bit<48>)hdr.tcp.ackNo)&&(var_pacote_gatilho>0))) {
                    porta_status.write((bit<32>)standard_metadata.egress_spec,PORTA_DOWN);
                }
                if ((((var_pacote_gatilho*2)<=(bit<48>)hdr.tcp.seqNo) && (var_pacote_gatilho>0)) ||
                    ((((bit<48>)hdr.tcp.seqNo)==0) && ((var_pacote_gatilho*2)<=(bit<48>)hdr.tcp.ackNo) && (var_pacote_gatilho>0))){
                    porta_status.write((bit<32>)standard_metadata.egress_spec,PORTA_UP);
                }
            
            } else {
                drop();
                var_drop=SIM;
            }
            porta_status.read(var_status_porta_saida,(bit<32>)standard_metadata.egress_spec);   
            if (hdr.ipv4.protocol==TYPE_ICMP){
                hash(var_hash_fluxo_porta_saida,HashAlgorithm.crc32, (bit<32>)0, {hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, standard_metadata.egress_spec},(bit<32>)NUMERO_FLUXOS);           
            } else if (hdr.ipv4.protocol==TYPE_TCP){
                hash(var_hash_fluxo_porta_saida,HashAlgorithm.crc32, (bit<32>)0, {hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.tcp.srcPort, hdr.tcp.dstPort, standard_metadata.egress_spec},(bit<32>)NUMERO_FLUXOS);           
            } else if (hdr.ipv4.protocol==TYPE_UDP){
                hash(var_hash_fluxo_porta_saida,HashAlgorithm.crc32, (bit<32>)0, {hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.udp.srcPort, hdr.udp.dstPort, standard_metadata.egress_spec},(bit<32>)NUMERO_FLUXOS); 
            } else {
                var_hash_fluxo_porta_saida =0;
            }   
            fluxo_status.read(var_status_fluxo_saida,(bit<32>)var_hash_fluxo_porta_saida); 
            if (standard_metadata.egress_spec == standard_metadata.ingress_port) {
                fluxo_status.write((bit<32>)var_hash_fluxo_porta_saida,PORTA_DOWN);
                fluxo_tempo.write((bit<32>)var_hash_fluxo_porta_saida,standard_metadata.ingress_global_timestamp);
                var_status_fluxo_saida=PORTA_DOWN;    
            } 
            if (var_status_fluxo_saida == PORTA_DOWN){
                fluxo_tempo.read(var_fluxo_tempo,(bit<32>)var_hash_fluxo_porta_saida); 
                clone_valida_fluxo.read(var_clone_valida_fluxo,(bit<32>)var_hash_fluxo_porta_saida); 

                if (var_clone_valida_fluxo == REVALIDA) {              
                        if (standard_metadata.egress_spec == standard_metadata.ingress_port) {
                            fluxo_tempo.write((bit<32>)var_hash_fluxo_porta_saida,standard_metadata.ingress_global_timestamp);
                            clone_valida_fluxo.write((bit<32>)var_hash_fluxo_porta_saida,NAO_REVALIDA);
                            drop();
                            var_drop = SIM;
                        } else 
                        if ((var_fluxo_tempo+TIME_OUT_RECUPERA_FLUXO+TIME_OUT_VALIDA_CLONE)<standard_metadata.ingress_global_timestamp) {
                            var_status_fluxo_saida = PORTA_UP;
                            fluxo_status.write((bit<32>)var_hash_fluxo_porta_saida,PORTA_UP);
                            clone_valida_fluxo.write((bit<32>)var_hash_fluxo_porta_saida,NAO_REVALIDA);
                            fluxo_pivo_saida.write((bit<32>)var_hash_fluxo_porta_saida,NAO);
                         }
                }
                if ((var_fluxo_tempo+TIME_OUT_RECUPERA_FLUXO)<standard_metadata.ingress_global_timestamp){
                    fluxo_pivo_saida.read(var_fluxo_pivo_saida,(bit<32>)var_hash_fluxo_porta_saida); 
                    if ((var_fluxo_pivo_saida == PIVO_FRR) && (var_status_porta_saida==PORTA_UP) && (var_clone_valida_fluxo == NAO_REVALIDA)){
                        clone_valida_fluxo.write((bit<32>)var_hash_fluxo_porta_saida,REVALIDA);
                        clone(CloneType.I2E,(bit<32>) standard_metadata.egress_spec);
                    } else if ((var_fluxo_pivo_saida != PIVO_FRR) && (var_status_porta_saida==PORTA_UP)){
                        var_status_fluxo_saida = PORTA_UP;
                        fluxo_status.write((bit<32>)var_hash_fluxo_porta_saida,PORTA_UP);
                    }
                }
            }
            var_saida_primeira_rota=standard_metadata.egress_spec;
            if  ((var_status_porta_saida==PORTA_DOWN) || (standard_metadata.egress_spec == standard_metadata.ingress_port) || (var_status_fluxo_saida==PORTA_DOWN)) {
                if (var_drop==NAO){
                    SW_ID.read(varSW_ID,1);
                    if ((varSW_ID!=9094) && (varSW_ID!=9099) && (varSW_ID!=9104) && (varSW_ID!=9109)){
                        ipv4_lpm_backup.apply();
                        pacote_gatilho.read(var_pacote_gatilho,(bit<32>)standard_metadata.egress_spec);   
                        if (((var_pacote_gatilho<=(bit<48>)hdr.tcp.seqNo)&&((var_pacote_gatilho*2)>(bit<48>)hdr.tcp.seqNo)&&(var_pacote_gatilho>0)) || 
                            ((((bit<48>)hdr.tcp.seqNo)==0)&&(var_pacote_gatilho<=(bit<48>)hdr.tcp.ackNo)&&((var_pacote_gatilho*2)>(bit<48>)hdr.tcp.ackNo)&&(var_pacote_gatilho>0))) {
                            porta_status.write((bit<32>)standard_metadata.egress_spec,PORTA_DOWN);
                        }
                        if ((((var_pacote_gatilho*2)<=(bit<48>)hdr.tcp.seqNo) && (var_pacote_gatilho>0)) ||
                            ((((bit<48>)hdr.tcp.seqNo)==0) && ((var_pacote_gatilho*2)<=(bit<48>)hdr.tcp.ackNo) && (var_pacote_gatilho>0))){
                            porta_status.write((bit<32>)standard_metadata.egress_spec,PORTA_UP);
                        }
                        porta_status.read(var_status_porta_saida,(bit<32>)standard_metadata.egress_spec);
                        if  ((var_status_porta_saida==PORTA_DOWN) || (standard_metadata.egress_spec == standard_metadata.ingress_port))  {
                            standard_metadata.egress_spec = (bit<9>)var_fluxo_porta_entrada;
                            fluxo_mac_entrada.read(hdr.ethernet.dstAddr,(bit<32>)var_hash_fluxo_porta_entrada);
                            fluxo_pivo_saida.write((bit<32>)var_hash_fluxo_porta_saida,NAO);
            
                        } else
                        if ((var_status_porta_saida==PORTA_UP) && (standard_metadata.ingress_port == var_saida_primeira_rota)){      
                            fluxo_pivo_saida.write((bit<32>)var_hash_fluxo_porta_saida,PIVO_FRR);
                        }
                    } else {
                        standard_metadata.egress_spec = (bit<9>)var_fluxo_porta_entrada;
                    }    
                }
                var_drop = NAO;
            }
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    
    apply {
        if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_INGRESS_CLONE) {
            hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
        }
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
     apply {
     update_checksum(
	    hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	          hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);
    }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
        packet.emit(hdr.icmp);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/
V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
