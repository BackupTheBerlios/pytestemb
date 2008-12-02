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
import os.path



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

    def run_case(self, case):
        try:
            case()
        except result.TestErrorFatal:
            pass
        




