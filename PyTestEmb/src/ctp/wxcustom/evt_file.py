# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.2 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"





import wx



VIEW_RESULT     = 0
VIEW_EDITOR_PY  = 1
VIEW_EDITOR_TXT = 2




# ***************************************************
# wxEvent : EVT_CUSTOM_FILE_VIEW
# ***************************************************
EVT_CUSTOM_FILE_VIEW_ID = wx.NewId()

def EVT_CUSTOM_FILE_VIEW(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_FILE_VIEW_ID, func)    

class EventFileView(wx.PyEvent):
    def __init__(self, path, view):
        wx.PyEvent.__init__(self) 
        self.SetEventType(EVT_CUSTOM_FILE_VIEW_ID)
        self.m_propagationLevel = wx.EVENT_PROPAGATE_MAX
        self.path = path
        self.view = view
        
        
    def clone(self):
        evt = EventTrace(self.path, self.view)
        return evt
    
    @staticmethod
    def create_result(path):
        return EventFileView(data, VIEW_RESULT)
    
    @staticmethod
    def create_editor_py(path):
        return EventFileView(path, VIEW_EDITOR_PY)
    
    @staticmethod
    def create_editor_txt(path):
        return EventFileView(path, VIEW_EDITOR_TXT)    



    
    
    
    
    
    