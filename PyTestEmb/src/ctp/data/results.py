# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.4 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import copy
import time
import shelve


import pytestemb.result as result



# RES_TYPE
RES_ERROR_CONFIG    = result.ResultStdout.ERROR_CONFIG   
RES_ERROR_IO        = result.ResultStdout.ERROR_IO   
RES_ERROR_TEST      = result.ResultStdout.ERROR_TEST
RES_WARNING         = result.ResultStdout.WARNING 
RES_ASSERT_OK       = result.ResultStdout.ASSERT_OK
RES_ASSERT_KO       = result.ResultStdout.ASSERT_KO
RES_PY_EXCEPTION    = result.ResultStdout.PY_EXCEPTION
 



class Results:
    
    def __init__(self):
        self.data = dict()
        
    def save(self, filename):
        s = shelve.open(filename, writeback=True)
        try:
            for k,v in self.data.iteritems():
                s[str(k)] = v
        finally:
            s.close()
            
    def load(self, filename):
        s = shelve.open(filename, writeback=False)
        try:      
            for k,v in s.iteritems():
                self.data[k] = v 
        finally:
            s.close()
        

    def update(self, ScriptRes):    
        self.data[ScriptRes.script.get_key()] = ScriptRes


    def __str__(self):
        dis = ""
        for script in self.data.itervalues():
            dis += "%s\n" % script
        return dis




class Res:
    field = [RES_ERROR_CONFIG,
             RES_ERROR_IO,
             RES_ERROR_TEST,
             RES_WARNING,
             RES_ASSERT_OK,
             RES_ASSERT_KO,
             RES_PY_EXCEPTION]
    
    def __init__(self):
        self.data = dict.fromkeys(Res.field, None)
        
        
        
        
    def is_ones(self, res_type):
        return (self.data[res_type] is not None)
    
    def get_lst_of_ones(self, res_type):
        return self.data[res_type]
    
    
    @staticmethod
    def create_from_resultcounter(rescount):
        res = Res()
        for k,v in rescount.counter.iteritems():
            if      v is None\
                or len(v) == 0 :
                continue
            else:
                res.data[k] = copy.copy(v)
        return res
    
    
    def __str__(self):
        dis = ""
        for k, v in self.data.iteritems():
            dis += "%s:%s\n" % (k, v)
        return dis    
        
       




class CaseRes:
    def __init__(self, name):
        self.name = name
        self.result = Res()

#    def get_dict(self):
#        d = dict()
#        d["name"] = self.name
#        d["result"] = dict()
#        return d

    def __hash__(self):
        return hash(self.name)
        
    def __cmp__(self, other):
        if self.__hash__() == other.__hash__():
            return 0
        else:
            return 1
        
    @staticmethod
    def create_from_resultcounter(rescount):
        case = CaseRes(rescount.name)        
        case.result = Res.create_from_resultcounter(rescount)
        return case
        
    def __str__(self):
        return "%s\n%s" % (self.name, self.result)

    
    
    
ST_EXEC_NOT_YET_EXECUTED    = 0
ST_EXEC_EXECUTED_NO_ERROR   = 1
ST_EXEC_EXECUTED_FILE_ERROR = 2
ST_EXEC_EXECUTED_PY_ERROR   = 3
ST_EXEC_EXECUTED_INT_ERROR  = 4

    
    
SCRIPT_STATUS = {   ST_EXEC_NOT_YET_EXECUTED    : "Script has not been executed",\
                    ST_EXEC_EXECUTED_NO_ERROR   : "Script executed, no error",\
                    ST_EXEC_EXECUTED_FILE_ERROR : "Script executed, error : problem with script file",\
                    ST_EXEC_EXECUTED_PY_ERROR   : "Script executed, error : python error",
                    ST_EXEC_EXECUTED_INT_ERROR  : "Script executed, error : internal error",}    
    
        

class ScriptRes:
    
    
    def __init__(self, script):
        self.script = script
        self.start_time     = None
        self.stop_time      = None
        self.trace_info     = None
        self.status         = None
        self.cases = dict()
        self.set_status(ST_EXEC_NOT_YET_EXECUTED)
    
    
#    def get_dict(self):
#        d = dict()
#        d["start_time"] = self.start_time
#        d["stop_time"]  = self.stop_time
#        d["trace_info"] = self.trace_info
#        d["status"]     = self.status
#        d["cases"]      = dict()
#        for k,v in self.cases.iteritems():
#            d["cases"][k] = v.get_dict()
#        return d
        
  
    def stamp_start(self):
        self.start_time = time.localtime()
    
    def stamp_stop(self):
        self.stop_time = time.localtime()

    def get_key(self):
        pass
    
    def get_status(self):
        return self.status
    
    def set_status(self, status, param=None):
        self.status = [status, param]
    
    def import_resultstdoutreader(self, resreader):
        if len(resreader.script) < 1 :
            self.set_status(ST_EXEC_EXECUTED_INT_ERROR)
        else:
            self.set_status(ST_EXEC_EXECUTED_NO_ERROR)
        #name = resreader.script[0].name
            trace = resreader.script[0].trace
            self.trace_info = trace
            for index, rcase in  enumerate(resreader.script[0].case):
                case = CaseRes.create_from_resultcounter(rcase)
                self.cases[index] = case
        

    def __str__(self):
        dis = "*****\n%s\n" % self.script.get_name()
        for k, v in self.cases.iteritems():
            dis += "%s" % v     
        return dis 






