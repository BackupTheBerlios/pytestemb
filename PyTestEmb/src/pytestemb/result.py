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


class TestErrorFatal(Exception):
    "Fatal Error"
    pass



class Result:
    
    def __init__(self, trace):
        self.trace = trace
    
    def trace_result(self, msg):
        self.trace.trace_msg(msg)
    

    def get_assert_caller(self):
        pass
 
    def _assert_(self, exp, fatal ,msg):
        if exp :
            self.assert_ok(msg) 
        else :
            self.get_assert_caller()
            self.assert_ko(msg)
            if fatal : 
                raise TestErrorFatal
        
    def fail(self, msg=""):
        self._assert_(False, False, msg)
    
    def fail_fatal(self, msg=""):
        self._assert_(False, True, msg)
        
    def assert_true(self, exp, msg):
        self._assert_(exp, False, msg)
        
    def assert_false(self, exp, msg):
        self._assert_(not(exp), False, msg)           
    
    def assert_true_fatal(self, exp, msg):
        self._assert_(exp, True, msg)
        
    def assert_false_fatal(self, exp, msg):
        self._assert_(not(exp), True, msg)   
 
  

    def script_start(self, name):
        pass
    
    def script_stop(self, name):
        pass
    
    def setup_start(self):
        pass

    def setup_stop(self):
        pass
       
    
    
    def cleanup_start(self):
        pass

    def cleanup_stop(self):
        pass
    
    
    def case_not_executed(self, name):
        pass
    
    def case_start(self, name):
        pass   
    
    def case_stop(self, name):
        pass   


    def error_config(self, msg):
        pass
    
    def error_io(self, msg):
        pass
    
    def error(self, msg):
        pass

    def warning(self, msg):
        pass
    
    def assert_ok(self, msg):
        pass
    
    def assert_ko(self, msg):
        pass








def trace(func):
    """The time_this decorator"""
    def decorated(*args, **kwargs):
        args[0].trace_result("%s" % func.func_name)
        result = func(*args, **kwargs)
        return result
    return decorated


class ResultStdout(Result):
    SEPARATOR = "="
    SCRIPT_START = "SCRIPT_START"
    SCRIPT_STOP = "SCRIPT_STOP" 
    SETUP_START = "SETUP_START"
    SETUP_STOP = "SETUP_STOP" 
    CLEANUP_START = "CLEANUP_START"
    CLEANUP_STOP = "CLEANUP_STOP"         
    CASE_START = "CASE_START"
    CASE_STOP = "CASE_STOP"  
    CASE_NOTEXECUTED = "CASE_NOTEXECUTED"
    ERROR_CONFIG = "ERROR_CONFIG" 
    ERROR_IO = "ERROR_IO"
    ERROR_TEST = "ERROR_TEST"
    WARNING = "WARNING"
    ASSERT_OK = "ASSERT_OK"
    ASSERT_KO = "ASSERT_KO"

    
    def __init__(self, trace):
        Result.__init__(self, trace)
        
    def write_no_arg(self, key):
        sys.stdout.write("%s\n" % key)

    def write_one_arg(self, key, value):
        sys.stdout.write("%s%s%s\n" % (key, ResultStdout.SEPARATOR ,value))        
    
    @trace
    def script_start(self, name):
        self.write_one_arg(ResultStdout.SCRIPT_START, name)
 
    @trace   
    def script_stop(self, name):
        self.write_one_arg(ResultStdout.SCRIPT_STOP, name)
    
    @trace    
    def setup_start(self):
        self.write_no_arg(ResultStdout.SETUP_START)
    
    @trace
    def setup_stop(self):
        self.write_no_arg(ResultStdout.SETUP_STOP)
 
    @trace   
    def cleanup_start(self):
        self.write_no_arg(ResultStdout.CLEANUP_START)

    @trace
    def cleanup_stop(self):
        self.write_no_arg(ResultStdout.CLEANUP_START)
    
    @trace    
    def case_start(self, name):
        self.write_one_arg(ResultStdout.CASE_START, name)

    @trace    
    def case_stop(self, name):
        self.write_one_arg(ResultStdout.CASE_STOP, name)

    @trace
    def case_not_executed(self, name):
        self.write_one_arg(ResultStdout.CASE_NOTEXECUTED, name)
    
    @trace    
    def error_config(self, msg):
        self.write_one_arg(ResultStdout.ERROR_CONFIG, msg)

    @trace    
    def error_io(self, msg):
        self.write_one_arg(ResultStdout.ERROR_IO, msg)
    
    @trace
    def error_test(self, msg):
        self.write_one_arg(ResultStdout.ERROR_TEST, msg)

    @trace
    def warning(self, msg):
        self.write_one_arg(ResultStdout.WARNING, msg)

    @trace    
    def assert_ok(self, msg):
        self.write_one_arg(ResultStdout.ASSERT_OK, msg)

    @trace    
    def assert_ko(self, msg):
        self.write_one_arg(ResultStdout.ASSERT_KO, msg)




class ResultScript:
    def __init__(self):
        self.name = ""
        self.case = []


class ResultStdoutReader:
    def __init__(self):
        self.script = []
    
    def clear(self):
        self.script = []
    
    def add_line(self, line):
        pos = line.find(ResultStdout.SEPARATOR)
        if pos == -1 :
            self.no_arg(line)
        else :
            self.one_arg(line[0:pos-1], line[pos+1:])

    def no_arg(self, key):
        pass
    
    def one_arg(self, key, value):
        pass



class ResultStandalone(Result):
    
    def __init__(self, trace):
        Result.__init__(self, trace)
        
        self.case = None
        self.result = [] 
    
    @trace  
    def script_start(self, name):
        sys.stdout.write("Start running %s ...\n" % name)
        
    @trace     
    def script_stop(self, name):
        sys.stdout.write("End running %s\n" % name)
        
        test_ok = True
        
        for case in self.result :
            if case["assert_ko"] == 0 :
                sys.stdout.write("Case %s : ok\n" % case["case"])
            else :
                sys.stdout.write("Case %s : ko\n" % case["case"])
                test_ok = False
        if test_ok :
            sys.stdout.write("Test OK\n")     
        else:
            sys.stdout.write("Test KO\n")
    
    @trace    
    def setup_start(self):
        pass
    
    @trace 
    def setup_stop(self):
        pass

    @trace     
    def cleanup_start(self):
        pass

    @trace 
    def cleanup_stop(self):
        pass
  
      
    @trace   
    def case_start(self, name):
        self.result.append({"case":name}) 
        self.result[-1]["assert_ok"] = 0
        self.result[-1]["assert_ko"] = 0
        
    @trace 
    def case_stop(self, name):
        pass

    @trace 
    def case_not_executed(self, name):
        pass
    
    @trace 
    def error_config(self, msg):
        pass
        self.result[-1]["error_config"]
    
    @trace    
    def error_io(self, msg):
        pass
    
    @trace     
    def error_test(self, msg):
        pass
    
    @trace 
    def warning(self, msg):
        pass
 
    @trace    
    def assert_ok(self, msg):
        self.result[-1]["assert_ok"] += 1
    
    @trace     
    def assert_ko(self, msg):
        self.result[-1]["assert_ko"] += 1


def create(interface, trace):
    
    if   interface == "none" :
        return Result(trace)
    elif interface == "stdout" :
        return ResultStdout(trace)
    elif interface == "standalone" :
        return ResultStandalone(trace)
    else:
        assert False




    



        
        
        
 

    
    
   
        
    
    
    
    
    
    
    
    
    
    
    
    