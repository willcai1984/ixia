#!usr/bin/python
# Filename: ixia_config.py
# Function: connect ixia inter
# coding:utf-8
# Author: Well
# Example command: python ixia_connect.py -p '2/15 2/16'

#::ixia::interface_config
#[-arp_send_req                CHOICES 0 1]
#[-autonegotiation             CHOICES 0 1]
#[-clocksource                 CHOICES internal loop external]
#[-duplex                      CHOICES half full auto]
#[-framing                     CHOICES sonet sdh]
#[-gateway                     IPV4]
#[-ignore_link                 CHOICES 0 1 DEFAULT 0]
#[-interface_handle            ANY]
#[-intf_ip_addr                IP]
#[-intf_mode                   CHOICES atm pos_hdlc pos_ppp ethernet frame_relay1490 frame_relay2427 frame_relay_cisco srp srp_cisco rpr gfp ethernet_fcoe bert]
#[-ipv6_gateway                IP]
#[-ipv6_intf_addr              IP]
#[-ipv6_prefix_length]
#[-mode                        CHOICES config modify destroy]
#[-netmask                     IP]
#[-op_mode                     CHOICES loopback normal monitor sim_disconnect]
#[-phy_mode                    CHOICES copper fiber]
#-port_handle                  interface list
#[-rx_c2]
#[-rx_fcs                      CHOICES 16 32]
#[-rx_scrambling               CHOICES 0 1]
#[-speed                       CHOICES ether10 ether100 ether1000 oc3 oc12 oc48 oc192 ether10000wan ether10000lan ether40000lan ether100000lan ether40Gig ether100Gig auto]
#[-src_mac_addr]
#[-static_enable                    CHOICES 0 1 DEFAULT 0]
#[-static_atm_header_encapsulation  CHOICES llc_bridged_eth_fcs
#CHOICES llc_bridged_eth_no_fcs
#CHOICES llc_ppp
#CHOICES llc_routed_snap
#CHOICES vcc_mux_bridged_eth_fcs
#CHOICES vcc_mux_bridged_eth_no_fcs
#CHOICES vcc_mux_ppp
#CHOICES vcc_mux_routed
#DEFAULT llc_routed_snap]
#[-static_atm_range_count           NUMERICDEFAULT 0]
#[-static_dlci_count_mode           CHOICES fixed increment DEFAULT fixed]

import sys,argparse
from ixia import *

def ixia_interface_config(ixia_class,port_list,autonegotiation='1', speed='auto',duplex='auto',phy_mode='copper',op_mode='normal',mode='modify',enable_flow_control='1',flow_control_directed_addr='01:80:C2:00:00:01'):
    correct_port_list=''
    for port in port_list.split(','):
        correct_port_list=correct_port_list+str(port)+' '
    ixia_cli_list=['-port_handle', correct_port_list,\
                   '-autonegotiation', autonegotiation,\
                   '-speed', speed,\
                   '-duplex', duplex,\
                   '-phy_mode',phy_mode,\
                   '-op_mode',op_mode,\
                   '-mode',mode,\
                   '-enable_flow_control',enable_flow_control,\
                   '-flow_control_directed_addr',flow_control_directed_addr]
    ixia_interface_result = ixia_class.ixia_interface_config_via_list(ixia_cli_list)
    if ixia_interface_result:
        return ixia_class
    else:
        return None

parse = argparse.ArgumentParser(description='Configure IXIA interfaces')
parse.add_argument('-ixia_class', '--ixia_class', required=True, dest='ixia_class',
                    help='''IXIA class from login''')
parse.add_argument('-port_list', '--port_list', required=True, dest='port_list',
                    help='''Port-list such as '1/2/15,1/2/16' ''')

parse.add_argument('-autonegotiation', '--autonegotiation', required=False, default='1', choices=['0','1'], dest='autonegotiation',
                    help='autonegotiation status')

parse.add_argument('-speed', '--speed', required=False, default='auto', choices=['ether10', 'ether100', 'ether1000', 'ether10000wan', 'ether10000lan','auto'],dest='speed',
                    help='speed status')

parse.add_argument('-duplex', '--duplex', required=False, default='auto', choices=['half','full','auto'],dest='duplex',
                    help='duplex status')

parse.add_argument('-intf_mode', '--intf_mode', required=False, default='ethernet', dest='intf_mode',
                    help='The interface mode of the port-list')

parse.add_argument('-op_mode', '--op_mode', required=False, default='normal', choices=['loopback', 'normal', 'monitor', 'sim_disconnect'],dest='op_mode',
                    help='The operate you want to do of the port-list')

parse.add_argument('-phy_mode', '--phy_mode', required=False, default='copper', choices=['copper', 'fiber'],dest='phy_mode',
                    help='The phy mode you want to set of the port-list')

parse.add_argument('-transmit_mode', '--transmit_mode', required=False, default='advanced', choices=['advanced','stream','flow','echo'],dest='transmit_mode',
                    help='The transmit mode of the port-list')

parse.add_argument('-mode', '--mode', required=False, default='modify', choices=['modify','destroy'],dest='mode',
                    help='The configure mode of the port-list, destroy is cover the configure before')

parse.add_argument('-enable_flow_control', '--enable_flow_control', required=False, default='1', choices=['0','1'],dest='enable_flow_control',
                    help='The configure mode of the port-list, destroy is cover the configure before')

parse.add_argument('-flow_control_directed_addr', '--flow_control_directed_addr', required=False, default='01:80:C2:00:00:01',dest='flow_control_directed_addr',
                    help='The configure mode of the port-list, destroy is cover the configure before')



#parse.add_argument('-vlan', '--vlan', required=False, default=0, type=int, choices=[0,1],dest='vlan',
#                    help='Enable vlan mode or not')
#
#parse.add_argument('-vlan_id', '--vlan_id', required=False, default=0, type=int,dest='vlan_id',
#                    help='Enable vlan id value')
#
#parse.add_argument('-vlan_id_count', '--vlan_id_count', required=False, default=1, type=int,dest='vlan_id_count',
#                    help='The vlan id you want to create')
#
#parse.add_argument('-vlan_id_step', '--vlan_id_step', required=False, default=1, type=int,dest='vlan_id_step',
#                    help='The vlan step you want to increased')
#
#parse.add_argument('-vlan_tpid', '--vlan_tpid', required=False, default='0x8100', choices=['0x8100','0x88a8','0x9100','0x9200'],dest='vlan_tpid',
#                    help='The vlan step you want to increased')

#parse.add_argument('-arp_send_req', '--arp_send_req', required=False, default=1, type=int, choices=[0,1], dest='arp_send_req',
#                    help='arp send flag')
#
#parse.add_argument('-gateway', '--gateway', required=False, dest='gateway',
#                    help='The gateway of the port-list')
#
#parse.add_argument('-intf_ip_addr', '--intf_ip_addr', required=False, dest='intf_ip_addr',
#                    help='The ip address of the port-list')
#
#parse.add_argument('-netmask', '--netmask', required=False, dest='netmask',
#                    help='The netmask of the port-list')

#ixia::connect -reset -device %s -port_list %s -username %s -tcl_server %s
#port_list="2/15 2/16"

def main():
    args = parse.parse_args()
    ixia_class=args.ixia_class
    port_list=args.port_list
    autonegotiation=args.autonegotiation
    speed=args.speed
    duplex=args.duplex
    phy_mode=args.phy_mode
    op_mode=args.op_mode
    mode=args.mode
    enable_flow_control=args.enable_flow_control
    flow_control_directed_addr=args.flow_control_directed_addr
    ixia_interface_result = ixia_interface_config(ixia_class,port_list,autonegotiation,speed,duplex,phy_mode,op_mode,mode,enable_flow_control,flow_control_directed_addr)
    return ixia_interface_result

if __name__ == '__main__':
    try:
        ixia_connect_result = main()
    except Exception,e:
        print str(e)
    else:
        print 'Login IXIA successfully'