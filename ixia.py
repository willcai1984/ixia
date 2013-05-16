#!/usr/bin/python
# coding: utf-8
# Author: Well
import Tkinter
def debug(mesage, is_debug=True):
    if mesage and is_debug:
        print 'DEBUG',
        print mesage

###build_cmd via set ('1','2','3'...)
def build_cmd(*args):
    cmd = ''
    for arg in args:
        cmd = cmd + arg + ' '
    print cmd
    return cmd
###build_cmd via list ([1,2,3])
def build_cmd_list(ixia_flag, arg_list):
    cmd = ixia_flag+' '
    for arg in arg_list:
        cmd = cmd + arg + ' '
    print cmd
    return cmd 

class ixia(object):
    def __init__(self):
        self.tclsh =Tkinter.Tcl()
        self.tclsh.eval("package require Ixia")
    def ixia_connect_via_list(self,arg_list):
        cmd =build_cmd_list('ixia::connect', arg_list)
        return self.tclsh.eval(cmd)
    def ixia_interface_config_via_list(self,arg_list):
        cmd =build_cmd_list('ixia::interface_config', arg_list)
        return self.tclsh.eval(cmd)
    def ixia_interface_stats_via_list(self,arg_list):
        cmd =build_cmd_list('ixia::interface_stats', arg_list)
        return self.tclsh.eval(cmd)
