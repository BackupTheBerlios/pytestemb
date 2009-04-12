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
import copy




# ***************************************************
# wxEvent : EVT_CUSTOM_RUN_SCRIPT
# ***************************************************
EVT_CUSTOM_RUN_SCRIPT_ID = wx.NewId()

def EVT_CUSTOM_RUN_SCRIPT(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_RUN_SCRIPT_ID, func)    

class EventRunScript(wx.PyEvent):
    def __init__(self, slist, config=None):
        wx.PyEvent.__init__(self) 
        self.SetEventType(EVT_CUSTOM_RUN_SCRIPT_ID)
        self.m_propagationLevel = wx.EVENT_PROPAGATE_MAX
        self.slist = copy.copy(slist)
        self.config = config
        
        
    def clone(self):
        evt = EventTrace(self.slist, self.config)
        return evt
    
 



    
    
    
    
    
    