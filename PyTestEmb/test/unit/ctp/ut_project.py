# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : unit test for result module
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import sys
import unittest

import ctp.data.project as project

        


class Test_Script(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_create_from_absolute_pathstr_1(self):
        script = project.Script.create_from_absolute_pathstr("/home/testor", "/home/testor/script.py")
    
        self.assertEqual(script.get_name(), "script")
        self.assertEqual(script.get_path(), [])
        

    def test_create_from_absolute_pathstr_2(self):
        script = project.Script.create_from_absolute_pathstr("/home/testor", "/home/testor/dir_1/script.py")
    
        self.assertEqual(script.get_name(), "script")
        self.assertEqual(script.get_path(), ["dir_1"])
        
        
    def test_create_from_absolute_pathstr_3(self):
        script = project.Script.create_from_absolute_pathstr("/home/testor", "/home/testor/dir_1/dir_2/script.py")
    
        self.assertEqual(script.get_name(), "script")
        self.assertEqual(script.get_path(), ["dir_1", "dir_2"])
        
               
        
        
if __name__ == '__main__':
    unittest.main()







