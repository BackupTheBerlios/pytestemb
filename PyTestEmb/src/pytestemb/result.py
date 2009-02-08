# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : result manages result of script execution
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.15 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import sys
import copy
import time
import inspect
import UserDict


import gtime


class TestErrorFatal(Exception):
    "Fatal Error"
    pass







class Result:
    
    def __init__(self, trace):
        self.trace = trace

        self.start_date = time.localtime()
        self.start_clock = time.clock()
        
        self.gtime = gtime.Gtime.create()
    
    def trace_result(self, name, des):
        self.trace.trace_result(name, des)
        
    def get_time(self):
        return self.gtime.get_time()

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
 
    def _assert_(self, exp, fatal, des, values=""):
        if exp :
            self.assert_ok(des)
        else :
            info = self.get_assert_caller()
            des["values"] = values
            des.update(info)
            self.assert_ko(des)
            if fatal :
                raise TestErrorFatal
        
    def fail(self, des):
        self._assert_(False, False, des)
    
    def fail_fatal(self, des):
        self._assert_(False, True, des)
        
    def assert_true(self, exp, des):
        values = "%s" % exp
        self._assert_(exp, False, des, values)
        
    def assert_false(self, exp, des):
        values = "%s" % exp
        self._assert_(not(exp), False, des, values)         
    
    def assert_true_fatal(self, exp, des):
        values = "%s" % exp
        self._assert_(exp, True, des, values)
        
    def assert_false_fatal(self, exp, des):
        values = "%s" % exp
        self._assert_(not(exp), True, des, values)   
 
    def assert_equal(self, exp1, exp2, des):
        values = "%s != %s" % (exp1, exp2)
        self._assert_((exp1 == exp2), False, des, values)

    def assert_equal_fatal(self, exp1, exp2, des):
        values = "%s != %s" % (exp1, exp2)
        self._assert_((exp1 == exp2), True, des, values)  

    def assert_notequal(self, exp1, exp2, des):
        values = "%s != %s" % (exp1, exp2)
        self._assert_((exp1 != exp2), False, des, values)

    def assert_notequal_fatal(self, exp1, exp2, des):
        values = "%s != %s" % (exp1, exp2)
        self._assert_((exp1 != exp2), True, des, values)  



    def script_start(self, des):
        pass

    def script_stop(self, des):
        pass
    
    def setup_start(self):
        pass
    
    def setup_stop(self):
        pass
 
    def cleanup_start(self):
        pass

    def cleanup_stop(self):
        pass
    
    def case_start(self, des):
        pass
    
    def case_stop(self, des):
        pass

    def case_not_executed(self, des):
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
    
    def doc(self, des):
        pass
    
    def trace_ctrl(self, des):
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
            trace_func(func.func_name, args[1])
        except :
            pass
        result = func(*args, **kwargs)
        return result
    return decorated


def stamp(func):
    """ add time stamp """
    def decorated(*args, **kwargs):
        # args[0] = self
        stamp = args[0].get_time()
        try:
            args[1]["time"] = stamp
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
    TRACE = "TRACE"
    DOC = "DOC"

    
    def __init__(self, trace):
        Result.__init__(self, trace)
        self.delay_trace_ctrl = None
        
    def write_no_arg(self, key):
        sys.stdout.write("%s%s\n" % (key, ResultStdout.SEPARATOR))

    def write_one_arg(self, key, value):
        sys.stdout.write("%s%s%s\n" % (key, ResultStdout.SEPARATOR ,value))        
    
    
    def write(self, opcode, arg):
        sys.stdout.write("%s%s%s\n" % (opcode, ResultStdout.SEPARATOR, arg.__str__()))
        
    
    @trace
    def script_start(self, des):
        self.write(ResultStdout.SCRIPT_START, des)
        if self.delay_trace_ctrl is not None:
            self.write(ResultStdout.TRACE, self.delay_trace_ctrl)

    @trace   
    def script_stop(self, des):
        self.write(ResultStdout.SCRIPT_STOP, des)
    
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

    @stamp     
    @trace    
    def case_start(self, des):
        self.write(ResultStdout.CASE_START, des)

    @stamp 
    @trace    
    def case_stop(self, des):
        self.write(ResultStdout.CASE_STOP, des)

    @stamp 
    @trace
    def case_not_executed(self, des):
        self.write(ResultStdout.CASE_NOTEXECUTED, des)

    @stamp     
    @trace    
    def error_config(self, des):
        self.write(ResultStdout.ERROR_CONFIG, des)

    @stamp 
    @trace    
    def error_io(self, des):
        self.write(ResultStdout.ERROR_IO, des)

    @stamp     
    @trace
    def error_test(self, des):
        self.write(ResultStdout.ERROR_TEST, des)

    @stamp 
    @trace
    def warning(self, des):
        self.write(ResultStdout.WARNING, des)

    @stamp 
    @trace    
    def assert_ok(self, des):
        self.write(ResultStdout.ASSERT_OK, des)
        
    @stamp 
    @trace    
    def assert_ko(self, des):
        self.write(ResultStdout.ASSERT_KO, des)
    
    @stamp                    
    @trace        
    def py_exception(self, des):
        self.write(ResultStdout.PY_EXCEPTION, des)

    @trace           
    def doc(self, des):
        self.write(ResultStdout.DOC, des)


    def trace_ctrl(self, des):
        # delay sending
        self.delay_trace_ctrl = des
        




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
        self.trace = None
    
    def __str__(self):
        str = "%s\n" % self.name
        for cas in self.case:
            str += "%s\n" % cas.__str__()
        if self.trace is not None:
            str += "TRACE:%s" % self.trace
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
            if      key == ResultStdout.SETUP_START :
                value = "setup"
            elif    key == ResultStdout.CLEANUP_START:
                value = "cleanup"
            else :
                dic = self.conv_dict(value)
                value = dic["name"]
                
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
        # TRACE
        elif    key == ResultStdout.TRACE :
            self.check_started(self.script_started)
            self.script[-1].trace = self.conv_dict(value)
        # CASE_XX
        elif        key == ResultStdout.ERROR_CONFIG\
                or  key == ResultStdout.ERROR_IO\
                or  key == ResultStdout.ERROR_TEST\
                or  key == ResultStdout.WARNING\
                or  key == ResultStdout.ASSERT_OK\
                or  key == ResultStdout.ASSERT_KO\
                or  key == ResultStdout.PY_EXCEPTION :
            self.check_started(self.case_started)
            dic = self.conv_dict(value)
            self.script[-1].case[-1].add_result(key, dic)
        else :
            print "key=%s value=%s" % (key, value)
        


class ResultStandalone(Result):
    
    def __init__(self, trace):
        Result.__init__(self, trace)
        
        self.case = None
        self.result = [] 
    
    @trace  
    def script_start(self, des):
        sys.stdout.write("Start running %s ...\n" % des["name"])
        
    
    def magical(self, data, size):
        return (len(data)-size)    
    
    def add_line(self, col1, col2):
        col1 = col1.ljust(60)
        col2 = col2.ljust(32)
        sys.stdout.write("| %s| %s|\n"  % (col1, col2)) 
                 
    @trace     
    def script_stop(self, des):
        sys.stdout.write("End running %s\n" % des["name"])
        
        test_ok = True
        
        sys.stdout.write("\n+%s+\n" % ("-"*95))
        for case in self.result :
            if case["assert_ko"] == 0 :
                self.add_line("Case \"%s\"" % case["case"], "ok")
            else :
                self.add_line("Case \"%s\"" % case["case"], "ko")
                test_ok = False
        sys.stdout.write("+%s+\n" % ("-"*95))        
        if test_ok :
            self.add_line("Script \"%s\"" % des["name"] , "OK")    
        else:
            self.add_line("Script \"%s\"" % des["name"] , "KO")
        sys.stdout.write("+%s+\n" % ("-"*95))
    
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
  
    @stamp
    @trace   
    def case_start(self, des):
        self.result.append({"case":des["name"]}) 
        self.result[-1]["assert_ok"] = 0
        self.result[-1]["assert_ko"] = 0
        sys.stdout.write("Case \"%s\" :\n" % des["name"])
        
    @stamp    
    @trace 
    def case_stop(self, des):
        pass

    @stamp
    @trace 
    def case_not_executed(self, des):
        pass
    
    @stamp
    @trace 
    def error_config(self, des):
        self.result[-1]["error_config"]

    @stamp
    @trace    
    def error_io(self, des):
        pass
    
    @stamp
    @trace     
    def error_test(self, des):
        pass

    @stamp    
    @trace 
    def warning(self, des):
        pass
 
    @stamp
    @trace    
    def assert_ok(self, des):  
        self.result[-1]["assert_ok"] += 1
    
    @stamp
    @trace     
    def assert_ko(self, des):
        sys.stdout.write("    assert ko\n")
        sys.stdout.write("        + function   : \"%s\"\n" % des["function"])  
        if des.has_key("msg"):
            sys.stdout.write("        + message    : \"%s\"\n" % des["msg"])       
        sys.stdout.write("        + expression : \"%s\"\n" % des["expression"])
        sys.stdout.write("        + values     : \"%s\"\n" % des["values"])
        loc = "    File \"%s\", line %d, in %s\n" % (des["file"], des["line"], des["function"])
        sys.stdout.write("%s\n" % loc)
        self.result[-1]["assert_ko"] += 1

    @stamp
    @trace
    def py_exception(self, des):
        dis = "Exception \n"
        for sline in des["stack"] :
            dis += "    File \"%s\", line %d, in %s\n" % (sline["path"], sline["line"], sline["function"])
            dis += "        %s\n" % (sline["code"])
        dis += "    %s\n" % (des["exception_class"])
        dis += "    %s\n" % (des["exception_info"])
        sys.stdout.write(dis)
        
        try :
            self.result[-1]["assert_ko"] += 1
        except :
            pass
 
    @trace           
    def doc(self, des):
        dis = "%s :: %s\n" % (des["type"], des["name"])
        dis += "%s\n" % des["doc"] 
        sys.stdout.write(dis)
        
        
        
    def trace_ctrl(self, des):
        sys.stdout.write("Trace info : %s\n" % des.__str__())
        

def create(interface, trace):
    
    if   interface == "none" :
        return Result(trace)
    elif interface == "stdout" :
        return ResultStdout(trace)
    elif interface == "standalone" :
        return ResultStandalone(trace)
    else:
        assert False


