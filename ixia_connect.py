#!usr/bin/python
# Filename: ixia_connect.py
# Function: connect ixia
# coding:utf-8
# Author: Well
# Example command: python ixia_connect.py -p '2/15 2/16'

import sys,argparse,re
from ixia import *

def ixia_connect(port_list,device='10.155.33.216',username='wcai',tcl_server='10.155.30.164',reset=True):
    port_list=[re.sub('^\d+\/','',i) for i in port_list.split(',')]
    ###transfer to the format such as '2/15 2/16'
    correct_port_list=''
    for port in port_list:
        correct_port_list=correct_port_list+port+' '
    ixia_cli_list=['-device', device,\
                   '-port_list', correct_port_list,\
                   '-username', username,\
                   '-tcl_server', tcl_server]
    if reset:
        ixia_cli_list.append('-reset')
    ###set class
    ixia_class = ixia()
    ixia_connect_result=ixia_class.ixia_connect_via_list(ixia_cli_list)
    return ixia_class
#    print 'ixia_login_result is as blow',
#    print ixia_connect_result
#    ###example value {port_handle {{10 {{155 {{33 {{216 {{2/15 1/2/15} {2/16 1/2/16}}}}}}}}}}} {status 1}
#    ### port one 1/2/15 port two 1/2/16
#    ixia_login_status=re.search('status (\d+)',ixia_connect_result)
#    ### status == 1 login successfully and can execute cli
#    ### else print error and return none
#    if ixia_login_status:
#        if ixia_login_status.group(1) == 1:
#            print 'login successfully'
#            return ixia_class
#        elif ixia_login_status.group(1) == 0:
#            print 'login failed'
#            return ixia_login_status.group(1)
#    else:
#        print 'login failed'
#        return None


parse = argparse.ArgumentParser(description='Connect to IXIA and login some interfaces')
parse.add_argument('-device', '--device', required=False, default='10.155.33.216', dest='device',
                    help='Destination Server IP')

parse.add_argument('-port_list', '--port_list', required=True, dest='port_list',
                    help='IXIA port list you want to login, format 1/2/1,1/2/2')

parse.add_argument('-username', '--username', required=False, default='auto', dest='username',
                    help='Login Name')

parse.add_argument('-reset', '--reset', required=False, default=False,action='store_true', dest='reset',
                    help='enable reset mode')

parse.add_argument('-tcl_server', '--tcl_server', required=False, default='10.155.30.164', dest='tcl_server',
                    help='tcl server')


#ixia::connect -reset -device %s -port_list %s -username %s -tcl_server %s
#port_list="2/15 2/16"

def main():
    args = parse.parse_args() 
    device=args.device
    port_list=args.port_list
    username=args.username
    reset=args.reset
    tcl_server=args.tcl_server
    ixia_connect_result=ixia_connect(port_list,device,username,tcl_server,reset)
    return ixia_connect_result


if __name__ == '__main__':
    try:
        ixia_connect_result = ixia_connect()
    except Exception,e:
        print str(e)
    else:
        print 'Login process over, can goto next step now'