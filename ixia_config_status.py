#!usr/bin/python
# Filename: ixia_config_status.py
# Function: configure interface and get status
# coding:utf-8
# Author: Well
# Example command: python ixia_config_status.py -port_list '1/2/1,1/2/2' -username 'wcai' -autonegotiation 1 -speed ether1000 -duplex full -reset

import sys, argparse, re, time
from ixia import *
def sleep (mytime=1):
    time.sleep(mytime)

def ixia_connect(port_list, device='10.155.33.216', username='wcai', tcl_server='10.155.30.164', reset=True):
    port_list = [re.sub('^\d+\/', '', i) for i in port_list.split(',')]
    ###transfer to the format such as '2/15 2/16'
    correct_port_list = ''
    for port in port_list:
        correct_port_list = correct_port_list + port + ' '
    ixia_cli_list = ['-device', device, \
                   '-port_list', correct_port_list, \
                   '-username', username, \
                   '-tcl_server', tcl_server]
    if reset:
        ixia_cli_list.append('-reset')
    ###set class
    ixia_class = ixia()
    ixia_connect_result = ixia_class.ixia_connect_via_list(ixia_cli_list)
    print 'ixia_connect_result is %s' % ixia_connect_result
    return ixia_class

def ixia_interface_config(ixia_class, port_list, autonegotiation='1', speed='auto', duplex='auto', phy_mode='copper', op_mode='normal', mode='modify', enable_flow_control='1', flow_control_directed_addr='01:80:C2:00:00:01'):
    correct_port_list = ''
    for port in port_list.split(','):
        correct_port_list = correct_port_list + str(port) + ' '
    ixia_cli_list = ['-port_handle', correct_port_list, \
                   '-autonegotiation', autonegotiation, \
                   '-speed', speed, \
                   '-duplex', duplex, \
                   '-phy_mode', phy_mode, \
                   '-op_mode', op_mode, \
                   '-mode', mode, \
                   '-enable_flow_control', enable_flow_control, \
                   '-flow_control_directed_addr', flow_control_directed_addr]
    ixia_interface_result = ixia_class.ixia_interface_config_via_list(ixia_cli_list)
    print 'ixia_interface_result is %s' % ixia_interface_result
    return ixia_class

def get_info_via_ixia_stats(ixia_stats_result):
    inter_info_list = re.findall('\{\d/.*?portCpuMemory \d+\}', ixia_stats_result)
    inter_reg = re.compile('(\d/\d/\d)')
    speed_reg = re.compile('intf_speed (.*?)\}')
    duplex_reg = re.compile('duplex (.*?)\}')
    link_reg = re.compile('link (\d+)')
    for inter_info in inter_info_list:
        if inter_reg.search(inter_info):
            print 'Port:%s;' % inter_reg.search(inter_info).group(1),
        if speed_reg.search(inter_info):
            print 'Speed:%s;' % speed_reg.search(inter_info).group(1),
        if duplex_reg.search(inter_info):
            print 'Duplex:%s;' % duplex_reg.search(inter_info).group(1),
        if link_reg.search(inter_info):
            if link_reg.search(inter_info).group(1)=='1':
                print 'Link:up\n'
            elif link_reg.search(inter_info).group(1)=='0':
                print 'Link:down\n'
            else:
                print 'Link:%s\n' % link_reg.search(inter_info).group(1)
                                
def ixia_interface_stats(ixia_class, port_list):
    correct_port_list = ''
    for port in port_list.split(','):
        correct_port_list = correct_port_list + str(port) + ' '
    ixia_cli_list = ['-port_handle', correct_port_list]
    ixia_stats_result = ixia_class.ixia_interface_stats_via_list(ixia_cli_list)
    ###{1/2/1 {{intf_type ethernet} {framing {}} {card_name {10/100/1000 LSM XMVDC16}} {port_name {10/100/1000 Base T}} {tx_frames 0} {rx_frames 937} {elapsed_time 3.10} {rx_collisions 0} {total_collisions 0} {duplex full} {intf_speed 100} {fcs_errors 0} {late_collisions 0} {link 1} {portCpuMemory 1024}}} {status 1}
    ixia_info_print = get_info_via_ixia_stats(ixia_stats_result)
    print 'ixia_stats_result is %s' % ixia_stats_result 
    return ixia_class

parse = argparse.ArgumentParser(description='Configure IXIA interfaces')
parse.add_argument('-device', '--device', required=False, default='10.155.33.216', dest='device',
                    help='Destination Server IP')

parse.add_argument('-port_list', '--port_list', required=True, dest='port_list',
                    help='IXIA port list you want to login, format 1/2/1,1/2/2')

parse.add_argument('-username', '--username', required=False, default='auto', dest='username',
                    help='Login Name')

parse.add_argument('-reset', '--reset', required=False, default=False, action='store_true', dest='reset',
                    help='enable reset mode')

parse.add_argument('-tcl_server', '--tcl_server', required=False, default='10.155.30.164', dest='tcl_server',
                    help='tcl server')

parse.add_argument('-autonegotiation', '--autonegotiation', required=False, default='1', choices=['0', '1'], dest='autonegotiation',
                    help='autonegotiation status')

parse.add_argument('-speed', '--speed', required=False, default='auto', choices=['ether10', 'ether100', 'ether1000', 'ether10000wan', 'ether10000lan', 'auto'], dest='speed',
                    help='speed status')

parse.add_argument('-duplex', '--duplex', required=False, default='auto', choices=['half', 'full', 'auto'], dest='duplex',
                    help='duplex status')

parse.add_argument('-intf_mode', '--intf_mode', required=False, default='ethernet', dest='intf_mode',
                    help='The interface mode of the port-list')

parse.add_argument('-op_mode', '--op_mode', required=False, default='normal', choices=['loopback', 'normal', 'monitor', 'sim_disconnect'], dest='op_mode',
                    help='The operate you want to do of the port-list')

parse.add_argument('-phy_mode', '--phy_mode', required=False, default='copper', choices=['copper', 'fiber'], dest='phy_mode',
                    help='The phy mode you want to set of the port-list')

parse.add_argument('-transmit_mode', '--transmit_mode', required=False, default='advanced', choices=['advanced', 'stream', 'flow', 'echo'], dest='transmit_mode',
                    help='The transmit mode of the port-list')

parse.add_argument('-mode', '--mode', required=False, default='destroy', choices=['modify', 'destroy'], dest='mode',
                    help='The configure mode of the port-list, destroy is cover the configure before')

parse.add_argument('-enable_flow_control', '--enable_flow_control', required=False, default='1', choices=['0', '1'], dest='enable_flow_control',
                    help='The configure mode of the port-list, destroy is cover the configure before')

parse.add_argument('-flow_control_directed_addr', '--flow_control_directed_addr', required=False, default='01:80:C2:00:00:01', dest='flow_control_directed_addr',
                    help='The configure mode of the port-list, destroy is cover the configure before')


def main():
    args = parse.parse_args()
    device = args.device
    username = args.username
    reset = args.reset
    tcl_server = args.tcl_server
    port_list = args.port_list
    autonegotiation = args.autonegotiation
    speed = args.speed
    duplex = args.duplex
    phy_mode = args.phy_mode
    op_mode = args.op_mode
    mode = args.mode
    enable_flow_control = args.enable_flow_control
    flow_control_directed_addr = args.flow_control_directed_addr
    ixia_login_result=ixia_connect(port_list,device,username,tcl_server,reset)
    ixia_config_result=ixia_interface_config(ixia_login_result, port_list, autonegotiation, speed, duplex, phy_mode, op_mode, mode, enable_flow_control, flow_control_directed_addr)
    print 'Sleep 5s for interface autonegotiation'
    sleep(5)
    ixia_status_result=ixia_interface_stats(ixia_config_result,port_list)
    return ixia_status_result

if __name__ == '__main__':
    try:
        ixia_connect_result = main()
    except Exception, e:
        print str(e)
    else:
        print 'IXIA process is over'
