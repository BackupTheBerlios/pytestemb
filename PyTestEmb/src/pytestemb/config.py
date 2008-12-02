# -*- coding: UTF-8 -*-
###########################################################
# Project  : PyTestEmb                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 01/12/08                                     #
###########################################################


__version__ = "$Revision: 1.1 $"
__author__ = "$Author: octopy $"


import sys
import time

class ConfigutationError(Exception):
    "Error in configuration"
    pass





class Config:
    def __init__(self, trace):
        self.conf = {}
        self.trace = trace
        
    def trace_config(self, msg):
        self.trace.trace_msg(msg)
        
    def load_config(self):
        pass

    def get_config(self, key):
        return self.conf[key]
    
    
    def to_string(self):
        ret = ""
        for k,v in self.conf.items():
            ret = "%s = %s\n" % (k,v)
        return ret 
         




class ConfigStdin(Config):
    
    def __init__(self, trace):
        Config.__init__(self, trace)
        self.load_config()
        
        
    def add_line(self, line):
        try:
            k, v = line.split(":")
            self.conf[k] = v
        except :
            self.trace_config("Error line invalid : %s" % line)
        
    
    def load_config(self):
        
        #print sys.stdin.mode

        self.trace_config("CONFIG = STDIN")
        time.sleep(0.5)
        try:
            line = sys.stdin.readline()
            while line:
                line = line[:-1]
                if line == "END" : 
                    break
                else :
                    self.add_line(line)
                line = sys.stdin.readline()
        except Exception , ex:
            self.trace_config("CONFIG = Exception %s" % ex.__str__())
            
            
        self.trace_config(self.conf.__str__())
        
    
    
def create(interface, trace):    
    if   interface == "none" :
        return Config(trace)
    elif interface == "stdin" :
        return ConfigStdin(trace)
    else:
        assert False
    
    
    