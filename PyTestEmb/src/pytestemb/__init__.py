# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : __init__ manages command line option and interface with other modules
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.19 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"





VERSION_STRING = "1.2.4"



import sys
import types



import trace
import valid
import result
import config
import pydoc
import pexception




from optparse import OptionParser





interface = {}


INTERFACE_DEFAULT = 0
INTERFACE_LIST = 1

interface["config"] = (("none"),
                       ("none", "stdin"))
interface["result"] = (("standalone"),
                       ("none", "standalone", "stdout"))
interface["trace"] =  ([], 
                       ("none", "octopylog", "txt"))


parser = OptionParser()
parser.add_option(  "-c", "--config",
                    action="store", type="string", dest="config", default=interface["config"][INTERFACE_DEFAULT],
                    help="set the interface for configuration, value can be : %s" % interface["config"][INTERFACE_LIST].__str__())
parser.add_option("-r", "--result",
                    action="store", type="string", dest="result", default=interface["result"][INTERFACE_DEFAULT],
                    help="set the interface for result, value can be : %s" % interface["result"][INTERFACE_LIST].__str__())
parser.add_option("-t", "--trace",
                    action="append", type="string", dest="trace", default=interface["trace"][INTERFACE_DEFAULT],
                    help="set the interface for trace, value can be : %s" % interface["trace"][INTERFACE_LIST].__str__()) 
parser.add_option("-p", "--path",
                    action="store", type="string", dest="path", default=None,
                    help="add path to python path") 
parser.add_option("-d", "--doc",
                    action="store_true", dest="doc", default=False,
                    help="add path to python path") 
parser.add_option("-v", "--version",
                    action="store_true", dest="ver", default=False,
                    help="version of software") 




def checker(name, value):
    for line in interface[name][INTERFACE_LIST] :
        if line == value:
            break
    else :
        parser.error("Interface %s is not valid, see --help" % value)


(options, args) = parser.parse_args()


if args != []:
    parser.error("Argument invalid %s " % args.__str__())
checker("config", options.config)
checker("result", options.result)
for item in options.trace:
    checker("trace", item)


if options.path is not None:
    sys.path.append(options.path)


if options.ver :
    sys.stdout.write("pytestemb\n")
    sys.stdout.write("Version   : %s\n" % VERSION_STRING)
    sys.stdout.write("Copyright : %s\n" % __copyright__)
    sys.stdout.write("Copyright : %s\n" % __license__)
    sys.stdout.write("Contact   : %s\n" % __email__)
    sys.exit(0)




__trace__   = None
__result__  = None
__config__  = None
__valid__   = None
__pydoc__   = None






if options.doc :
    # doc generation   
    __trace__   = trace.create(options.trace) 
    __result__  = result.create(options.result, __trace__ )
    __config__  = config.create(options.config, __trace__ )
    __pydoc__   = pydoc.Pydoc(None, __result__)
else :
    # test execution
    __trace__   = trace.create(options.trace)
    __result__  = result.create(options.result, __trace__ )
    __config__  = config.create(options.config, __trace__ )
    __valid__   = valid.Valid(__config__, __result__)


__trace__.set_result(__result__)
__trace__.set_config(__config__)
__trace__.start()
    
__config__.start()


    
def set_doc(doc):
    """ set script doc for doc generation """
    if options.doc :
        __pydoc__.set_doc(doc)


def set_setup(func_setup):
    """ 
    @function           : set_setup(func_setup)
    @param func_setup   : (function) a test case function
    @return             : None     
    @summary            : add a setup function to the script
    """   
    if options.doc :
        __pydoc__.set_setup(func_setup)
    else :
        __valid__.set_setup(func_setup)

def set_cleanup(func_cleanup):
    """ 
    @function           : set_cleanup(func_cleanup)
    @param func_cleanup : (function) a test case function
    @return             : None     
    @summary            : add a cleanup function to the script
    """    
    if options.doc :
        __pydoc__.set_cleanup(func_cleanup)
    else :
        __valid__.set_cleanup(func_cleanup)



def add_test_case(func_case):
    """ 
    @function       : add_test_case(func_case)
    @param func_case: (function) a test case function
    @return         : None     
    @summary        : add a test case to the script
    """  
    if options.doc :
        __pydoc__.add_test_case(func_case)
    else :
        __valid__.add_test_case(func_case)

    
def run_script():
    """ 
    @function       : run_script()
    @return         : None     
    @summary        : start the run of script
    @warning        : - 
    """         
    if options.doc :
        pass
    else :
        __valid__.run_script()
        
    


def _create_des_(msg):
    if msg is None :
        return {}
    elif not(isinstance(msg, types.StringTypes)):
        raise pexception.PytestembError("Msg must be a string")
    else:
        return dict({"msg":"%s" % msg})



def assert_true(exp, msg=None):
    """ 
    @function       : assert_true(exp, msg=None)
    @param exp      : (boolean) expression that we expect "True" value
    @param msg      : (string) message string describing the goal of assertion 
    @return         : None     
    @summary        : assert a "True" value
    """
    __result__.assert_true(exp, _create_des_(msg))
 
        
def assert_false(exp, msg=None):
    """ 
    @function       : assert_false(exp, msg=None)
    @param exp      : (boolean) expression that we expect "False" value
    @param msg      : (string) message string describing the goal of assertion 
    @return         : None     
    @summary        : assert a "False" value
    """
    __result__.assert_false(exp, _create_des_(msg))
    
    
def assert_true_fatal(exp, msg=None):
    """ 
    @function       : assert_true_fatal(exp, msg=None)
    @param exp      : (boolean) expression that we expect "True" value
    @param msg      : (string) message string describing the goal of assertion 
    @return         : None     
    @summary        : assert a "True" value, if assertion is False execution of test case is finished
    """
    __result__.assert_true_fatal(exp, _create_des_(msg))
    
        
def assert_false_fatal(exp, msg=None):
    """ 
    @function       : assert_false_fatal(exp, msg=None)
    @param exp      : (boolean) expression that we expect "False" value
    @param msg      : (string) message string describing the goal of assertion 
    @return         : None     
    @summary        : assert a "False" value, if assertion is False execution of test case is finished
    """    
    __result__.assert_false_fatal(exp, _create_des_(msg))
    
    
def assert_equal(exp1, exp2, msg=None):
    """ 
    @function       : assert_equal(exp1, exp2, msg=None)
    @param exp1     : (object) expression1
    @param exp2     : (object) expression2
    @param msg      : (string) message string describing the goal of assertion 
    @return         : None     
    @summary        : assert that exp1 is equal to exp2
    """    
    __result__.assert_equal(exp1, exp2, _create_des_(msg))    


def assert_equal_fatal(exp1, exp2, msg=None):
    """ 
    @function       : assert_equal_fatal(exp1, exp2, msg=None)
    @param exp1     : (object) expression1
    @param exp2     : (object) expression2
    @param msg      : (string) message string describing the goal of assertion 
    @return         : None     
    @summary        : assert that exp1 is equal to exp2, if assertion is False execution of test case is finished
    """    
    __result__.assert_equal_fatal(exp1, exp2, _create_des_(msg)) 



def assert_notequal(exp1, exp2, msg=None):
    """ 
    @function       : assert_notequal(exp1, exp2, msg=None)
    @param exp1     : (object) expression1
    @param exp2     : (object) expression2
    @param msg      : (string) message string describing the goal of assertion 
    @return         : None     
    @summary        : assert that exp1 is not equal to exp2
    """        
    __result__.assert_notequal(exp1, exp2, _create_des_(msg))
    
    
        

def assert_notequal_fatal(exp1, exp2, msg=None):
    """ 
    @function       : assert_notequal(exp1, exp2, msg=None)
    @param exp1     : (object) expression1
    @param exp2     : (object) expression2
    @param msg      : (string) message string describing the goal of assertion 
    @return         : None     
    @summary        : assert that exp1 is not equal to exp2, if assertion is False execution of test case is finished
    """        
    __result__.assert_notequal_fatal(exp1, exp2, _create_des_(msg))       
    


def warning(msg=None):
    """ 
    @function       : warning(msg=None)
    @param msg      : (string) message string describing the warning
    @return         : None     
    @summary        : generate a warning
    """     
    __result__.warning(_create_des_(msg))

def fail(msg=None):
    """ 
    @function       : fail(msg=None)
    @param msg      : (string) message string describing the warning
    @return         : None     
    @summary        : generate a fail
    """     
    __result__.fail(_create_des_(msg))

def fail_fatal(msg=None):
    """ 
    @function       : fail_fatal(msg=None)
    @param msg      : (string) message string describing the warning
    @return         : None     
    @summary        : generate a fail and execution of test case is finished
    """     
    __result__.fail_fatal(_create_des_(msg))




def trace_env(scope, data):
    """ 
    @function       : trace_env(scope, data)
    @param scope    : (string) string that refer the scope
    @param data     : (string) string to trace
    @return         : None     
    @summary        : trace data towards environment trace type
    """     
    __trace__.trace_env(scope, data)

def trace_io(interface, data):
    """ 
    @function       : trace_io(interface, data)
    @param interface: (string) string that refer the interface
    @param data     : (string) string to trace
    @return         : None     
    @summary        : trace data towards io trace type
    """         
    __trace__.trace_io(interface, data)


def trace_script(msg):
    """ 
    @function       : trace_script(msg)
    @param msg      : (string) message to trace
    @return         : None     
    @summary        : trace message, for script application
    """      
    __trace__.trace_script(msg)
    
    
def config_get(key):
    """ 
    @function       : config_get(key)
    @param key      : (string) key of configuration parameter
    @return         : value of parameter     
    @summary        : get a parameter by a kay value
    """      
    return __config__.get_config(key)










__api__ = [ set_setup,
            set_cleanup,
            add_test_case,
            run_script,
            assert_true,
            assert_false,
            assert_true_fatal,
            assert_false_fatal,
            assert_equal,
            assert_equal_fatal,
            assert_notequal,
            assert_notequal_fatal,
            warning,
            fail,
            fail_fatal,            
            trace_env,
            trace_io,
            trace_script,
            config_get,]

