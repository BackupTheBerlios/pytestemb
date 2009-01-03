# -*- coding: UTF-8 -*-
###########################################################
# Project  : PyTestEmb                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 01/12/08                                     #
###########################################################


__version__ = "$Revision: 1.4 $"
__author__ = "$Author: octopy $"


import os
import md5
import sys
import time

import logging
import logging.handlers

        
        
import gtime        





class Trace:
    def __init__(self):
        self.gtime = gtime.Gtime.create()
        self.result = None
        self.config = None
        
        
    def set_result(self, result):
        self.result = result
    
    def set_config(self, config):    
        self.config = config
        
    def start(self):    
        pass
    
    def trace_script(self, msg):
        pass
    
    def trace_io(self, interface, data):
        pass
    
    def trace_result(self, name, des):
        pass

    def trace_config(self, msg):
        pass

    


class TraceOctopylog(Trace):
    
    def __init__(self):
        Trace.__init__(self)
        
        socketHandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        rootLogger = logging.getLogger("pytestemb")
        rootLogger.setLevel(logging.DEBUG)
        rootLogger.addHandler(socketHandler)
        
        self.scope = {}   
           
           
    def start(self):    
        pass

    def trace_scope(self, scope, msg):
        try:
            self.scope[scope].info("%s" % msg)
        except:
            self.scope[scope] = logging.getLogger("pytestemb.%s" % scope)        
            self.scope[scope].info("%s" % msg)

    def trace_script(self, msg):
        self.trace_scope("script", msg)

    def trace_io(self, interface, data):
        self.trace_scope(interface, data)
    
    def trace_result(self, name, des):
        self.trace_scope("result", "%s : %s" % (name, des.__str__()))

    def trace_config(self, msg):
        self.trace_scope("config", msg)


class TraceStdout(Trace):
    
    def __init__(self):
        Trace.__init__(self)
        
        
    def trace_script(self, msg):
        sys.stdout.write("Script::%s" % msg)

    def trace_io(self, interface, data):
        sys.stdout.write("%s::%s" % (interface, data.__str__()))
    
    def trace_result(self, name, des):
        sys.stdout.write("%s::%s" % (name, des.__str__()))

    def trace_config(self, msg):
        sys.stdout.write("Config::%s" % msg)


class TraceTxt(Trace):
    
    def __init__(self):
        Trace.__init__(self)
        
     
    def start(self):
        
        pathfile = "c:\\temp\\" + self.gen_file_name()
        
        des = dict({"file":pathfile})
        try :
            self.file = open(pathfile, 'w')          
        except (IOError) , (error):
            self.file = None
            des["error"] = error.__str__()
            
        self.result.trace_info(des)
        self.add_header()         
        
        
    def gen_file_name(self):
        """ """
        m = md5.new()
        m.update(sys.argv[0])
        m.update(time.strftime("%d_%m_%Y_%H_%M_%S", self.gtime.start_date)) 
        name = os.path.splitext(os.path.split(sys.argv[0])[1])[0]      
        name += "_%s.log" % (m.hexdigest()[0:16].upper())
        return name
 
 
             
    def format(self, gtime, scope, msg):
        marge1 = (" " * (16-len(gtime)))
        marge2 = (" " * (24-len(scope) ))
        return "%s%s%s%s%s\n"  % (gtime, marge1, scope, marge2, msg)      
            
    def add_header(self):        
        if self.file is not None :
            dis = ""
            dis += "Script file    : %s\n" % sys.argv[0] 
            dis += "Date           : %s\n" % time.strftime("%d/%m/%Y %H:%M:%S", self.gtime.start_date)
            dis += "\n%s\n" % self.format("Time(s)", "Scope", "Info")
            self.file.write(dis)
           
            
            
    def add_line(self, scope, msg):
        if self.file is not None :
            gtime = "%.6f" % self.gtime.get_time()
            dis = self.format(gtime, scope, msg)
            self.file.write(dis)
        
    def trace_script(self, msg):
        self.add_line("Script", msg)

    def trace_io(self, interface, data):
        self.add_line(interface, data.__str__())
    
    def trace_result(self, name, des):
        self.add_line(name, des.__str__())

    def trace_config(self, msg):
        self.add_line("Config", msg)





def create(interface):
    
    if   interface == "none" :
        return Trace()
    elif interface == "octopylog":
        return TraceOctopylog()
    elif interface == "stdout":
        return TraceStdout()
    elif interface == "txt":
        return TraceTxt()    
    else:
        assert False
    
    
    
    
    