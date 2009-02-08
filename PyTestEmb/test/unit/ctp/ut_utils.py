# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : unit test for result utils
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import unittest

import gui.utils as utils





    

class Test_split_fullpath(unittest.TestCase):
    def setUp(self):
        pass
    
    
    
    def test_case_nominal(self):
        path, file, ext =  utils.split_fullpath("c:\\temp\\file.xml")
        self.assertEqual(path,"c:\\temp")
        self.assertEqual(file,"file")
        self.assertEqual(ext,"xml")
 
    def test_case_noext(self):
        path, file, ext = utils.split_fullpath("c:\\temp\\file")        
        self.assertEqual(path,"c:\\temp")
        self.assertEqual(file,"file")
        self.assertEqual(ext,"")
                
    def test_case_nofile(self):
        path, file, ext = utils.split_fullpath("c:\\temp\\.xml")             
        self.assertEqual(path,"c:\\temp")
        self.assertEqual(file,"")
        self.assertEqual(ext,"xml")
                
    def test_case_nopath(self):
        path, file, ext = utils.split_fullpath("file.xml")    
        self.assertEqual(path,"")
        self.assertEqual(file,"file")
        self.assertEqual(ext,"xml")
        
        
        
        
class Test_extract_sub(unittest.TestCase):
    def setUp(self):
        pass
    

    def test_case_nominal(self):
        path_1 = "c:\\project" 
        path_2 = "c:\\project\\script\\001"
        relative = utils.extract_relative(path_1, path_2)
        self.assertEqual(relative, "script\\001")


    def test_case_equal(self):
        path_1 = "c:\\project" 
        path_2 = "c:\\project"
        relative = utils.extract_relative(path_1, path_2)
        self.assertEqual(relative, "")
        





class Test_utils(unittest.TestCase):
    def setUp(self):
        pass

#    def test_case_nominal(self):
#        camp = utils.Campaign("camp", "c:\\temp\\project")
#        camp.add_script("c:\\temp\\project\\script_01\\script_01.py")
#        camp.add_script("c:\\temp\\project\\script_01\\script_02.py")
#        camp.add_script("c:\\temp\\project\\script_02\\script_01.py")
#        
#        list_relative = camp.get_list_relative()
#        list_absolute = camp.get_list_absolute()
#        
#        
#        self.assertEqual(list_relative, ["script_01\\script_01.py",\
#                                         "script_01\\script_02.py",\
#                                         "script_02\\script_01.py"])
#        
#        self.assertEqual(list_absolute, ["c:\\temp\\project\\script_01\\script_01.py",\
#                                         "c:\\temp\\project\\script_01\\script_02.py",\
#                                         "c:\\temp\\project\\script_02\\script_01.py"])
#
#        
#        
        
        
        
                        
if __name__ == '__main__':
    unittest.main()







