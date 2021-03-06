# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : parser manages parsing of stdout result
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.3 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import result
import UserDict



class StdoutReader:
    
    def __init__(self):
        self.script_started = False 
        self.case_started = False
        
    def new_script(self):
        self.script_started = False 
        self.case_started = False
        
    def check_started(self, state):
        if state :
            return
        else :
            raise Exception   
        
    
    def add_line(self, line):
        pos = line.find(result.ResultStdout.SEPARATOR)
        if pos == line[-1] :
            self.process(line, None)
        else :
            self.process(line[0:pos], line[pos+1:-1])


    def conv_dict(self, data):
        try:
            return UserDict.UserDict(eval(data))
        except Exception , error:
            raise error    
    
    def process(self, key, value):
        pass



class ResultStdoutReader(StdoutReader):
    
    def __init__(self):
        StdoutReader.__init__(self)
        self.script = []


    def __str__(self):
        str = ""
        for scr in self.script:
            str += "%s\n" % scr.__str__()
        return str
    

    def create_resultcounter(self):
        obj = result.ResultCounter()
        obj.add_kind(result.ResultStdout.ERROR_CONFIG)
        obj.add_kind(result.ResultStdout.ERROR_IO)
        obj.add_kind(result.ResultStdout.ERROR_TEST)
        obj.add_kind(result.ResultStdout.WARNING)
        obj.add_kind(result.ResultStdout.ASSERT_OK)
        obj.add_kind(result.ResultStdout.ASSERT_KO)
        obj.add_kind(result.ResultStdout.PY_EXCEPTION)        
        return obj
    
    
    
    def process(self, key, value):
        #print "key=%s value=%s" % (key, value)
        
        # SCRIPT_START
        if      key == result.ResultStdout.SCRIPT_START :
            self.check_started(not(self.script_started))
            self.script.append(result.ResultScript(value))
            self.script_started = True
        # SCRIPT_STOP
        elif    key == result.ResultStdout.SCRIPT_STOP :
            self.check_started(self.script_started)
            self.script_started = False
        # SETUP_START, CLEANUP_START, CASE_START
        elif        key == result.ResultStdout.SETUP_START\
                or  key == result.ResultStdout.CLEANUP_START\
                or  key == result.ResultStdout.CASE_START :
            self.check_started(not(self.case_started))
            if      key == result.ResultStdout.SETUP_START :
                value = "setup"
            elif    key == result.ResultStdout.CLEANUP_START:
                value = "cleanup"
            else :
                dic = self.conv_dict(value)
                value = dic["name"]
                
            obj = self.create_resultcounter()
            obj.name = value
            self.script[-1].case.append(obj)
            self.case_started = True
        # SETUP_STOP, CLEANUP_STOP, CASE_STOP
        elif        key == result.ResultStdout.SETUP_STOP\
                or  key == result.ResultStdout.CLEANUP_STOP\
                or  key == result.ResultStdout.CASE_STOP :
            self.check_started(self.case_started)
            self.case_started = False
        # CASE_NOTEXECUTED
        elif    key == result.ResultStdout.CASE_NOTEXECUTED :
            self.check_started(not(self.case_started))
            obj = self.create_resultcounter()
            obj.set_not_executed()
            obj.name = value
            self.script[-1].case.append(obj)
        # TRACE
        elif    key == result.ResultStdout.TRACE :
            self.check_started(self.script_started)
            self.script[-1].trace.append(self.conv_dict(value))
        # CASE_XX
        elif        key == result.ResultStdout.ERROR_CONFIG\
                or  key == result.ResultStdout.ERROR_IO\
                or  key == result.ResultStdout.ERROR_TEST\
                or  key == result.ResultStdout.WARNING\
                or  key == result.ResultStdout.ASSERT_OK\
                or  key == result.ResultStdout.ASSERT_KO\
                or  key == result.ResultStdout.PY_EXCEPTION :
            self.check_started(self.case_started)
            dic = self.conv_dict(value)
            self.script[-1].case[-1].add_result(key, dic)
        else :
            pass
            #print "key=%s value=%s" % (key, value)
            
            



class DocStdoutReader(StdoutReader):
    
    def __init__(self):
        StdoutReader.__init__(self)
        self.data = []
        
    def __str__(self):
        str = ""
        return str
    
    
    def process(self, key, value):
        # DOC
        if  key == result.ResultStdout.DOC :
            self.data.append(self.conv_dict(value))
        else:
            pass
            #print "key=%s value=%s" % (key, value)
            
            
            
            