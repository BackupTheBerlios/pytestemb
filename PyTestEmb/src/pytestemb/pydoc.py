# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : pydoc manages doc extraction from script
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import sys
import copy
import os.path
import inspect



def getScriptName():
    try:
        return os.path.splitext(os.path.split(sys.argv[0])[1])[0]      
    except:
        return "error_script_filename" 



class Pydoc:
    
    def __init__(self, config, result):
        self.config = config
        self.result = result
        
    
    def set_doc(self, doc):
        des = dict()
        des["type"] = "script"
        des["name"] = getScriptName()
        if doc is None :
            des["doc"] = ""
        else:
            des["doc"] = Pydoc.clean(doc)
        self.result.doc(des)
        
        
    def set_setup(self, funcSetup):
        self._function(funcSetup)
    
    def set_cleanup(self, funcCleanup):
        self._function(funcCleanup)
    
    def add_test_case(self, funcCase):
        self._function(funcCase)
        
    
    def _function(self, func):
        des = dict()
        des["type"] = "case"
        des["name"] = func.func_name
        if func.__doc__ is None :
            des["doc"] = ""
        else:
            des["doc"] = Pydoc.clean(func.__doc__)
        self.result.doc(des)
    
    @staticmethod
    def clean(doc):
        res = ""
        doc = doc.strip(" \n")
        for line in doc.splitlines():
            res += "%s\n" % line.strip(" \t")
        return res.strip("\n")
        
        
        
        
    
           