#!usr/bin/python
# Filename: ixia_config.py
# Function: connect ixia inter
# coding:utf-8
# Author: Well
# Example command: python ixia_connect.py -p '2/15 2/16'

import sys,argparse,re
from ixia import *

def get_info_via_ixia_stats(ixia_stats_result):
    inter_info_list=re.findall('\{\d/.*?portCpuMemory \d+\}',ixia_stats_result)
    inter_reg=re.compile('(\d/\d/\d)')
    speed_reg=re.compile('intf_speed (\d+)')
    duplex_reg=re.compile('duplex (\w+)')
    link_reg=re.compile('link (\d+)')
    for inter_info in inter_info_list:
        if inter_reg.search(inter_info):
            print 'Port: %s' % inter_reg.search(inter_info).group(1),
        if speed_reg.search(inter_info):
            print 'Speed: %s' % speed_reg.search(inter_info).group(1),
        if duplex_reg.search(inter_info):
            print 'Duplex: %s' % duplex_reg.search(inter_info).group(1),
        if link_reg.search(inter_info):
            if link_reg.search(inter_info).group(1) == 1:
                print 'Link: up'
            elif link_reg.search(inter_info).group(1) == 0:
                print 'Link: down'
def ixia_interface_stats(ixia_class,port_list):
    correct_port_list=''
    for port in port_list.split(','):
        correct_port_list=correct_port_list+str(port)+' '
    ixia_cli_list=['-port_handle', correct_port_list]
    ixia_stats_result = ixia_class.ixia_interface_stats_via_list(ixia_cli_list)
    ###{1/2/1 {{intf_type ethernet} {framing {}} {card_name {10/100/1000 LSM XMVDC16}} {port_name {10/100/1000 Base T}} {tx_frames 0} {rx_frames 937} {elapsed_time 3.10} {rx_collisions 0} {total_collisions 0} {duplex full} {intf_speed 100} {fcs_errors 0} {late_collisions 0} {link 1} {portCpuMemory 1024}}} {status 1}
    ixia_info_print=get_info_via_ixia_stats(ixia_stats_result)
    return ixia_class
#    if ixia_stats_result:
#        return ixia_class
#    else:
#        return None

parse = argparse.ArgumentParser(description='Configure IXIA interfaces')
parse.add_argument('-ixia_class', '--ixia_class', required=True, dest='ixia_class',
                    help='''IXIA class from login''')
parse.add_argument('-port_list', '--port_list', required=True, dest='port_list',
                    help='''Port-list such as '1/2/15,1/2/16' ''')


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
    ixia_interface_result = ixia_interface_stats(ixia_class,port_list)
    return ixia_interface_result

if __name__ == '__main__':
    try:
        ixia_connect_result = main()
    except Exception,e:
        print str(e)
    else:
        print 'Login IXIA successfully'