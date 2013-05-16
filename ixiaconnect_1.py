#!usr/bin/python
# Filename: ixiaconnect.py
# Function: connect ixia
# coding:utf-8
# Author: Well
# Example command: 

import Tkinter
tclsh =Tkinter.Tcl()
tclsh.eval("package require Ixia")
test_name='well'
chassisIP='10.155.33.216'
serverIP='10.155.30.164'
ipV4_port_list="2/15 2/16"
ipV4_ixia_list="1.1.1.2 1.1.1.1"
ipV4_gateway_list="1.1.1.1 1.1.1.2"
ipV4_netmask_list="255.255.255.0 255.255.255.0"
ipV4_mac_list="0000.debb.0001 0000.debb.0002"
ipV4_version_list="4 4"
ipV4_autoneg_list="1 1"
ipV4_duplex_list="full full"
ipV4_speed_list="ether1000 ether1000"

tclsh.eval("set connect_status [ixia::connect -reset -device %s -port_list %s -username %s -tcl_server %s]" % (chassisIP,ipV4_port_list,test_name,serverIP))


#% puts $connect_status
#{
#port_handle {{10 {{155 {{33 {{    216 {{2/15 1/2/15} {2/16 1/2/16}}}}}}}}}}
#}
#
#{
#status 1
#}
#
#set port_one [keylget connect_status port_handle.$chassisIP.[lindex $ipV4_port_list 0]]
#
#1/2/15
#
#set port_two [keylget connect_status port_handle.$chassisIP.[lindex $ipV4_port_list 1]]
#
#1/2/16
#
#set port_handle [list $port_one $port_two]
#
#1/2/15 1/2/16