# -*- coding: UTF-8 -*-
###########################################################
# Project  : PyTestEmb                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 01/12/08                                     #
###########################################################


__version__ = "$Revision: 1.6 $"
__author__ = "$Author: octopy $"


import sys
import copy
import inspect
import UserDict


class TestErrorFatal(Exception):
    "Fatal Error"
    pass






#def finspect():
#    lst = inspect.stack()
#    try :
#        
#        print lst[4][3]
##        for l in lst:
##            print "%s" % l.__str__()
#    finally:
#        del lst
#        






class Result:
    
    def __init__(self, trace):
        self.trace = trace
    
    def trace_result(self, msg):
        self.trace.trace_msg(msg)
    

    def get_assert_caller(self):
        CALL_DEPTH = 4
        lst = inspect.stack()
        dict = {}
        try :
            dict["file"] = copy.copy(lst[CALL_DEPTH][1])
            dict["line"] = copy.copy(lst[CALL_DEPTH][2])
            dict["function"] = copy.copy(lst[CALL_DEPTH][3])
            dict["expression"] = copy.copy(lst[CALL_DEPTH][4][0].strip(" \t\n"))           
        finally:
            del lst
            return dict
 
    def _assert_(self, exp, fatal, msg):
        if exp :
            info = {}
            info["info"] = msg
            self.assert_ok(info) 
        else :
            info = self.get_assert_caller()
            info["info"] = msg
            self.assert_ko(info)
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
 
    def assert_equal(self, exp1, exp2, msg):
        self._assert_((exp1 == exp2), False, msg)

    def assert_equal_fatal(self, exp1, exp2, msg):
        self._assert_((exp1 == exp2), True, msg)  

    def assert_notequal(self, exp1, exp2, msg):
        self._assert_((exp1 != exp2), False, msg)

    def assert_notequal_fatal(self, exp1, exp2, msg):
        self._assert_((exp1 != exp2), True, msg)  



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
    
    def case_start(self, name):
        pass
    
    def case_stop(self, name):
        pass

    def case_not_executed(self, name):
        pass
    
    def error_config(self, des):
        pass

    def error_io(self, des):
        pass
    
    def error_test(self, des):
        pass

    def warning(self, des):
        pass

    def assert_ok(self, des):
        pass
    
    def assert_ko(self, des):
        pass
        
    def py_exception(self, des):
        pass




def trace(func):
    """ call trace_result
     decorator function """
    def decorated(*args, **kwargs):
        # args[0] = self
        trace_func = args[0].trace_result
        #args[0].trace_result("%s" % func.func_name)
        # arg[1] = string or dict or no
        try:
            trace_func("%s : %s" % (func.func_name, args[1].__str__()))
        except :
            pass
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
    PY_EXCEPTION = "PY_EXCEPTION"

    
    def __init__(self, trace):
        Result.__init__(self, trace)
        
    def write_no_arg(self, key):
        sys.stdout.write("%s%s\n" % (key, ResultStdout.SEPARATOR))

    def write_one_arg(self, key, value):
        sys.stdout.write("%s%s%s\n" % (key, ResultStdout.SEPARATOR ,value))        
    
    
    def write(self, opcode, arg):
        sys.stdout.write("%s%s%s\n" % (opcode, ResultStdout.SEPARATOR, arg.__str__()))
        
    
    @trace
    def script_start(self, name):
        self.write(ResultStdout.SCRIPT_START, {"name":name})
 
    @trace   
    def script_stop(self, name):
        self.write(ResultStdout.SCRIPT_STOP, {"name":name})
    
    @trace    
    def setup_start(self):
        self.write(ResultStdout.SETUP_START, {})
    
    @trace
    def setup_stop(self):
        self.write(ResultStdout.SETUP_STOP, {})
 
    @trace   
    def cleanup_start(self):
        self.write(ResultStdout.CLEANUP_START, {})

    @trace
    def cleanup_stop(self):
        self.write(ResultStdout.CLEANUP_STOP, {})
    
    @trace    
    def case_start(self, name):
        self.write(ResultStdout.CASE_START, {"name":name})

    @trace    
    def case_stop(self, name):
        self.write(ResultStdout.CASE_STOP, {"name":name})

    @trace
    def case_not_executed(self, name):
        self.write(ResultStdout.CASE_NOTEXECUTED, {"name":name})
    
    @trace    
    def error_config(self, des):
        self.write(ResultStdout.ERROR_CONFIG, des)

    @trace    
    def error_io(self, des):
        self.write(ResultStdout.ERROR_IO, des)
    
    @trace
    def error_test(self, des):
        self.write(ResultStdout.ERROR_TEST, des)

    @trace
    def warning(self, des):
        self.write(ResultStdout.WARNING, des)

    @trace    
    def assert_ok(self, des):
        self.write(ResultStdout.ASSERT_OK, des)

    @trace    
    def assert_ko(self, des):
        self.write(ResultStdout.ASSERT_KO, des)
            
            
    @trace        
    def py_exception(self, des):
#        msg = ""
#        for sline in des["stack"] :
#            msg += "File \"%s\", line %d, in %s" % (sline["path"], sline["line"], sline["function"])
#            msg += "    %s\n" % (sline["code"])
#        msg += "%s" % des["exception"]
        self.write_one_arg(ResultStdout.PY_EXCEPTION, des)



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
        
    def add_result(self, kind, obj):
        """ add a result if limit is reach, the older result is remove """
        self.counter[kind].append(obj)
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
        obj.add_kind(ResultStdout.PY_EXCEPTION)        
        return obj
    
    
    def add_line(self, line):
        pos = line.find(ResultStdout.SEPARATOR)
        print line
        if pos == line[-1] :
            self.process(line, None)
        else :
            self.process(line[0:pos], line[pos+1:-1])



    def conv_dict(self, data):
        try:
            return UserDict.UserDict(eval(data))
        except Exception , error:
            print data
            raise error    
        
#import UserDict
# 
#value = "{'a':{'b':'c', 'd':'e'}}"
# 
#try:
#  a = UserDict.UserDict(eval(value))
#except:
#  print "Ce n'est pas un dictionnaire"

    
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
            dic = self.conv_dict(value)
            self.script[-1].case[-1].add_result(key, dic)

        


class ResultStandalone(Result):
    
    def __init__(self, trace):
        Result.__init__(self, trace)
        
        self.case = None
        self.result = [] 
    
    @trace  
    def script_start(self, name):
        sys.stdout.write("Start running %s ...\n" % name)
        
    
    def magical(self, data, size):
        return (len(data)-size)    
    
    def add_line(self, col1, col2):
        marge1 = (" " * (32-2-len(col1)))
        marge2 = (" " * (32-2-len(col2) ))
        sys.stdout.write("| %s%s| %s%s|\n"  % (col1, marge1, col2, marge2)) 
                 
    @trace     
    def script_stop(self, name):
        sys.stdout.write("End running %s\n" % name)
        
        test_ok = True
        
        sys.stdout.write("\n+%s+\n" % ("-"*63))
        for case in self.result :
            if case["assert_ko"] == 0 :
                self.add_line("Case \"%s\"" % case["case"], "ok")
            else :
                self.add_line("Case \"%s\"" % case["case"], "ko")
                test_ok = False
        sys.stdout.write("+%s+\n" % ("-"*63))        
        if test_ok :
            self.add_line("Script \"%s\"" % name , "OK")    
        else:
            self.add_line("Script \"%s\"" % name , "KO")
        sys.stdout.write("+%s+\n" % ("-"*63))
    
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
        sys.stdout.write("Case \"%s\" :\n" % name)
        
    @trace 
    def case_stop(self, name):
        pass

    @trace 
    def case_not_executed(self, name):
        pass
    
    @trace 
    def error_config(self, msg):
        self.result[-1]["error_config"]
    
    @trace    
    def error_io(self, des):
        pass
    
    @trace     
    def error_test(self, des):
        pass
    
    @trace 
    def warning(self, des):
        pass
 
    @trace    
    def assert_ok(self, des):
        #sys.stdout.write("%s\n" % des["info"])      
        self.result[-1]["assert_ok"] += 1
    
    @trace     
    def assert_ko(self, des):
        sys.stdout.write("    assert ko : %s\n" % des["info"])   
        self.result[-1]["assert_ko"] += 1

    @trace
    def py_exception(self, des):
        msg = "Exception :\n"
        for sline in des["stack"] :
            msg += "    File \"%s\", line %d, in %s\n" % (sline["path"], sline["line"], sline["function"])
            msg += "        %s\n" % (sline["code"])
        msg += "    %s" % (des["exception"])
        sys.stdout.write(msg)
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




    



        
        
        
 

    
    
   
        
    
    
    
    
    
    
    
    
    
    
    
    