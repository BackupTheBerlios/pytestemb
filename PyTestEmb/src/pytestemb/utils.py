# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : utils gathered some utils function
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import os
import sys






def get_script_name():
    return os.path.splitext(os.path.split(sys.argv[0])[1])[0]      
 
 
 
 
 
 
 
 
 
 
 
 
 
 