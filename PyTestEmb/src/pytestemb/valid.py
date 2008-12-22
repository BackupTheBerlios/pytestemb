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
import copy
import os.path
import inspect



import result
import trace

sys.stderr = sys.stdout




def getScriptName():
    try:
        return os.path.splitext(os.path.split(sys.argv[0])[1])[0]      
    except:
        return "error_script_filename" 



class Valid:
    def __init__(self, config, result, trace):
        self.config = config
        self.result = result
        self.trace = trace
        self.setup = self._nothing_
        self.cleanup = self._nothing_
        self.case = []
        self.name = getScriptName()
    
    def _nothing_(self):
        pass

    def set_setup(self, funcSetup):
        self.setup = funcSetup

    def set_cleanup(self, funcCleanup):
        self.cleanup = funcCleanup

    def add_test_case(self, funcCase):
        self.case.append(funcCase)
    
    def script_need_run(self, name):
        return True
    
    
    def run_script(self):
        self.result.script_start(self.name)
        try:
            # Setup
            self.result.setup_start()
            self.run_try(self.setup)
            self.result.setup_stop()
            # Case
            for acase in self.case :
                name = acase.func_name
                self.result.case_start(name)
                if self.script_need_run(name):
                    self.run_case(acase)
                else :
                    pass
                self.result.case_stop(name)
            # Cleanup
            self.result.cleanup_start()
            self.run_try(self.cleanup)
            self.result.cleanup_stop()
        except:
            raise
        self.result.script_stop(self.name)
        
    
    def run_try(self, func):  
        try:
            func()
        except result.TestErrorFatal:
            pass  
        except (Exception), (error):
            self.inspect_traceback(error)            

    def run_case(self, case):
        try:
            case()
            return True
        except result.TestErrorFatal:
            return True
        except (Exception), (error):
            self.inspect_traceback(error)
            return False
            
        
        
        
    def inspect_traceback(self, exception):
        CALL_DEPTH = 1
        traceback = inspect.trace()
        stack = []
        try:
            for index in range(CALL_DEPTH, len(traceback)):
                stack.append({})
                stack[-1]["path"]      = copy.copy(traceback[index][1])
                stack[-1]["line"]      = copy.copy(traceback[index][2])
                stack[-1]["function"]  = copy.copy(traceback[index][3])
                stack[-1]["code"]      = copy.copy(traceback[index][4][0].strip("\n"))     
        finally:
            del traceback
            
        self.result.py_exception(exception.__str__(), stack)
            




