# -*- coding: UTF-8 -*-
###########################################################
# Project  : PyTestEmb                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 01/12/08                                     #
###########################################################


__version__ = "$Revision: 1.2 $"
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
    """ call trace_result
     decorator function """
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
        sys.stdout.write("%s%s\n" % (key, ResultStdout.SEPARATOR))

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
        self.write_no_arg(ResultStdout.CLEANUP_STOP)
    
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




class ResultCounter:
    """ class to count result
    a limit is implemented (usefull for test instanciate for endurance )
    counter works as cyclic after limit is reach
    """
    def __init__(self, name="", limit=1000):
        self.name = name
        self.limit = limit
        self.counter = {}
        
    def set_not_executed(self):
        self.counter = None
        
    def add_kind(self, kind):
        self.counter[kind] = []    
        
    def add_result(self, kind, msg):
        """ add a result if limit is reach, the older result is remove """
        self.counter[kind].append(msg)
        if len(self.counter[kind]) > self.limit :
            self.counter[kind].pop(0)
    def get_counter(self):
        return self.counter

    def __str__(self):
        str = "%s\n" % self.name
        for k, v in self.counter.iteritems():
            str += "%s:%s\n" % (k, v)
        return str       



class ResultScript:
    def __init__(self, name):
        self.name = name
        self.case = []
    
    def __str__(self):
        str = "%s\n" % self.name
        for cas in self.case:
            str += "%s\n" % cas.__str__()
        return str


class ResultStdoutReader:
    
    def __init__(self):
        self.script = []
        
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
        
    def __str__(self):
        str = ""
        for scr in self.script:
            str += "%s\n" % scr.__str__()
        return str
    

    def create_resultcounter(self):
        obj = ResultCounter()
        obj.add_kind(ResultStdout.ERROR_CONFIG)
        obj.add_kind(ResultStdout.ERROR_IO)
        obj.add_kind(ResultStdout.ERROR_TEST)
        obj.add_kind(ResultStdout.WARNING)
        obj.add_kind(ResultStdout.ASSERT_OK)
        obj.add_kind(ResultStdout.ASSERT_KO)
        return obj
    
    
    def add_line(self, line):
        pos = line.find(ResultStdout.SEPARATOR)
        print line
        if pos == line[-1] :
            self.process(line, None)
        else :
            self.process(line[0:pos], line[pos+1:-1])


    
    def process(self, key, value):
        print "key=%s value=%s" % (key, value)
        
        # SCRIPT_START
        if      key == ResultStdout.SCRIPT_START :
            self.check_started(not(self.script_started))
            self.script.append(ResultScript(value))
            self.script_started = True
        # SCRIPT_STOP
        elif    key == ResultStdout.SCRIPT_STOP :
            self.check_started(self.script_started)
            self.script_started = False
        # SETUP_START, CLEANUP_START, CASE_START
        elif        key == ResultStdout.SETUP_START\
                or  key == ResultStdout.CLEANUP_START\
                or  key == ResultStdout.CASE_START :
            self.check_started(not(self.case_started))
            if key == ResultStdout.SETUP_START :
                value = "setup"
            if key == ResultStdout.CLEANUP_START:
                value = "cleanup"
            obj = self.create_resultcounter()
            obj.name = value
            self.script[-1].case.append(obj)
            self.case_started = True
        # SETUP_STOP, CLEANUP_STOP, CASE_STOP
        elif        key == ResultStdout.SETUP_STOP\
                or  key == ResultStdout.CLEANUP_STOP\
                or  key == ResultStdout.CASE_STOP :
            self.check_started(self.case_started)
            self.case_started = False
        # CASE_NOTEXECUTED
        elif    key == ResultStdout.CASE_NOTEXECUTED :
            self.check_started(not(self.case_started))
            obj = self.create_resultcounter()
            obj.set_not_executed()
            obj.name = value
            self.script[-1].case.append(obj)
        # CASE_XX
        else :
            self.check_started(self.case_started)
            self.script[-1].case[-1].add_result(key, value)

        


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




    



        
        
        
 

    
    
   
        
    
    
    
    
    
    
    
    
    
    
    
    