# -*- coding: UTF-8 -*-
###########################################################
# Project  : PyTestEmb                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 01/12/08                                     #
###########################################################


__version__ = "$Revision: 1.4 $"
__author__ = "$Author: octopy $"



import sys




import trace
import valid
import result
import config






from optparse import OptionParser


interface = {}


INTERFACE_DEFAULT = 0
INTERFACE_LIST = 1

interface["config"] = (("none"),
                       ("none", "stdin"))
interface["result"] = (("standalone"),
                       ("none", "standalone" ,"stdout", "octopylog", "txt"))
interface["trace"] =  (("none"), 
                       ("none", "stdout", "octopylog", "txt"))


parser = OptionParser()
parser.add_option(  "-c", "--config",
                    action="store", type="string", dest="config", default=interface["config"][INTERFACE_DEFAULT],
                    help="set the interface for configuration, value can be : %s" % interface["config"][INTERFACE_LIST].__str__())
parser.add_option("-r", "--result",
                    action="store", type="string", dest="result", default=interface["result"][INTERFACE_DEFAULT],
                    help="set the interface for result, value can be : %s" % interface["result"][INTERFACE_LIST].__str__())
parser.add_option("-t", "--trace",
                    action="store", type="string", dest="trace", default=interface["trace"][INTERFACE_DEFAULT],
                    help="set the interface for trace, value can be : %s" % interface["trace"][INTERFACE_LIST].__str__()) 
parser.add_option("-p", "--path",
                    action="store", type="string", dest="path", default=None,
                    help="add path to python path") 


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
checker("trace", options.trace)


if options.path is not None:
    sys.path.append(options.path)


__trace__ = trace.create(options.trace)
__result__ = result.create(options.result, __trace__ )
__config__ = config.create(options.config, __trace__ )
__valid__ = valid.Valid(__config__, __result__, __trace__)





def set_setup(funcSetup):
    __valid__.set_setup(funcSetup)

def set_cleanup(funcCleanup):
    __valid__.set_cleanup(funcCleanup)

def add_test_case(funcCase):
    __valid__.add_test_case(funcCase)
    
def run_script():
    __valid__.run_script()

def raise_error(msg):
    __result__.error(msg)

def raise_warning(msg):
    __result__.warning(msg)
    
def assert_true(exp, msg):
    __result__.assert_true(exp, msg)
        
def assert_false(exp, msg):
    __result__.assert_false(exp, msg)
    
def assert_true_fatal(exp, msg):
    __result__.assert_true_fatal(exp, msg)
        
def assert_false_fatal(exp, msg):
    __result__.assert_false_fatal(exp, msg)
    
    
def assert_equal(exp1, exp2, msg):
    __result__.assert_equal(exp1, exp2, msg)    

def assert_equal_fatal(exp1, exp2, msg):
    __result__.assert_equal_fatal(exp1, exp2, msg) 

def assert_notequal(exp1, exp2, msg):
    __result__.assert_notequal(exp1, exp2, msg)    

def assert_notequal_fatal(exp1, exp2, msg):
    __result__.assert_notequal_fatal(exp1, exp2, msg)       
    
    
#def py_exception(exception, stack):
#    __result__.py_exception(exception, stack)    
    
def trace_msg(msg):
    __trace__.trace_msg(msg)
    


    
    
