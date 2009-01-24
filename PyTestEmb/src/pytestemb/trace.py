# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : trace manages trace coming from module and script execution
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.9 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"


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
    
    def trace_env(self, scope, data):
        pass




class TraceManager(Trace):
    def __init__(self):
        Trace.__init__(self)
        
        self.dictra = dict()

    def add_trace(self, name, tra):
        self.dictra[name] = tra
         
        
    def set_result(self, result):
        for tra in self.dictra.itervalues() :
            tra.set_result(result)
    
    def set_config(self, config):    
        for tra in self.dictra.itervalues() :
            tra.set_config(config)       
        
    def start(self):    
         for tra in self.dictra.itervalues() :
            tra.start()              
    
    def trace_script(self, msg):
         for tra in self.dictra.itervalues() :
            tra.trace_script(msg)              
    
    def trace_io(self, interface, data):
         for tra in self.dictra.itervalues() :
            tra.trace_io(interface, data)              
    
    def trace_result(self, name, des):
        for tra in self.dictra.itervalues() :
            tra.trace_result( name, des)               

    def trace_config(self, msg):
        for tra in self.dictra.itervalues() :
            tra.trace_config(msg)               
    
    def trace_env(self, scope, data):
        for tra in self.dictra.itervalues() :
            tra.trace_env(scope, data)               




    


class TraceOctopylog(Trace):
    
    def __init__(self):
        Trace.__init__(self)
        self.scope = {}   
           
    def start(self):    
        socketHandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        rootLogger = logging.getLogger("pytestemb")
        rootLogger.setLevel(logging.DEBUG)
        rootLogger.addHandler(socketHandler)
        
        des = dict({"octopylog":"pytestemb"})
        self.result.trace_ctrl(des)

    def trace_scope(self, scope, msg):
        try:
            self.scope[scope].info("%s" % msg)
        except:
            self.scope[scope] = logging.getLogger("pytestemb.%s" % scope)        
            self.scope[scope].info("%s" % msg)

    def trace_script(self, msg):
        self.trace_scope("script", msg)

    def trace_io(self, interface, data):
        self.trace_scope("io.%s" % interface, data)
    
    def trace_result(self, name, des):
        self.trace_scope("result", "%s : %s" % (name, des.__str__()))

    def trace_config(self, msg):
        self.trace_scope("config", msg)
        
    def trace_env(self, scope, data):
        self.trace_scope("env.%s" % scope, data)
     


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

    def trace_env(self, scope, data):
        sys.stdout.write("%s::%s" % (scope, data.__str__()))


from config import ConfigError


class TraceTxt(Trace):
    DEFAULT_DIR = "c:\\temp"
    def __init__(self):
        Trace.__init__(self)
        
    def start(self):
        # output path and filename for trace file
        try:
            pathfile = self.config.get_config("TRACE_PATH")
        except (ConfigError), (error):
            if not(os.path.lexists(TraceTxt.DEFAULT_DIR)):
                os.mkdir(TraceTxt.DEFAULT_DIR)
            pathfile = "%s\\" % TraceTxt.DEFAULT_DIR 
        pathfile += self.gen_file_name() 
        # create file
        des = dict({"file":pathfile})
        try :
            self.file = open(pathfile, 'w')          
        except (IOError) , (error):
            self.file = None
            des["error"] = error.__str__()
        self.result.trace_ctrl(des)
        # write header
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
        gtime = gtime.ljust(16)
        scope = scope.ljust(24)
        msg = msg.strip()       
        return "%s%s%s\n"  % (gtime, scope, msg)      
            
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

    def trace_env(self, scope, data):
        self.add_line(scope, data.__str__())     



def create(interface):
    tracemanager = TraceManager()
    for item in interface :
        if item == "octopylog":
            tracemanager.add_trace("octopylog", TraceOctopylog())
        elif item == "stdout":
            tracemanager.add_trace("stdout", TraceStdout())
        elif item == "txt":
            tracemanager.add_trace("txt", TraceTxt())
        else:
            assert False
    return tracemanager
    
    
    
    
    