# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : result manages result of script execution
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.20 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import sys
import copy
import time
import inspect


import utils
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
        self.delay_trace_ctrl = []

    def trace_result(self, name, des):
        self.trace.trace_result(name, des)

    def get_time(self):
        return self.gtime.get_time()

    def get_assert_caller(self):
        CALL_DEPTH = 4
        lst = inspect.stack()
        dic = {}
        try :
            dic["file"]         = copy.copy(lst[CALL_DEPTH][1])
            dic["line"]         = copy.copy(lst[CALL_DEPTH][2])
            dic["function"]     = copy.copy(lst[CALL_DEPTH][3])
            dic["expression"]   = copy.copy(lst[CALL_DEPTH][4][0].strip(" \t\n"))
        finally:
            del lst
            return dic

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
        values = "%s != %s" % (utils.to_unicode(exp1), utils.to_unicode(exp2))
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
        # delay sending
        self.delay_trace_ctrl.append(des)


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
        except Exception, ex :
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
        except Exception, ex:
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


    def write_no_arg(self, key):
        sys.stdout.write("%s%s\n" % (key, ResultStdout.SEPARATOR))

    def write_one_arg(self, key, value):
        sys.stdout.write("%s%s%s\n" % (key, ResultStdout.SEPARATOR ,value))


    def write(self, opcode, arg):
        sys.stdout.write("%s%s%s\n" % (opcode, ResultStdout.SEPARATOR, arg.__str__()))


    @trace
    def script_start(self, des):
        self.write(ResultStdout.SCRIPT_START, des)
        for item in self.delay_trace_ctrl:
            self.write(ResultStdout.TRACE, item)

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
        self.delay_trace_ctrl.append(des)





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
        sstr = "%s\n" % self.name
        for k, v in self.counter.iteritems():
            sstr += "%s:%s\n" % (k, v)
        return sstr



class ResultScript:
    def __init__(self, name):
        self.name = name
        self.case = []
        self.trace = []

    def __str__(self):
        sstr = "%s\n" % self.name
        for cas in self.case:
            sstr += "%s\n" % cas.__str__()

        for item in self.trace:
            sstr += "TRACE:%s" % item

        return sstr






class ResultStandalone(Result):

    def __init__(self, trace):
        Result.__init__(self, trace)

        self.case = None
        self.result = []

    @trace
    def script_start(self, des):
        sys.stdout.write("Start running %s ...\n" % des["name"])
        for item in self.delay_trace_ctrl:
            sys.stdout.write("Trace : %s\n" % item)

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
        self.result[-1]["error_config"] += 1

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
        except Exception, ex:
            pass

    @trace
    def doc(self, des):
        import pydoc
        sys.stdout.write("\n")

        sys.stdout.write("Name : %s\n" % des[pydoc.KEY_NAME])
        sys.stdout.write("Type : %s\n" % des[pydoc.KEY_TYPE])
        sys.stdout.write("Doc :\n%s\n" % des[pydoc.KEY_DOC])



#    def trace_ctrl(self, des):
#        sys.stdout.write("Trace info : %s\n" % des.__str__())


def create(interface, mtrace):

    if   interface == "none" :
        return Result(mtrace)
    elif interface == "stdout" :
        return ResultStdout(mtrace)
    elif interface == "standalone" :
        return ResultStandalone(mtrace)
    else:
        assert False


