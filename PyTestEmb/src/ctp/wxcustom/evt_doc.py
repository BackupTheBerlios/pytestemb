'''
Created on Mar 18, 2009

@author: jmb
'''



'''
Created on Mar 10, 2009

@author: jmb
'''


'''
Created on Mar 8, 2009

@author: jmb
'''



import wx
import copy








# ***************************************************
# wxEvent : EVT_CUSTOM_DOC
# ***************************************************
EVT_CUSTOM_DOC_ID = wx.NewId()

def EVT_CUSTOM_DOC(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_DOC_ID, func)    

class EventDoc(wx.PyEvent):
    def __init__(self, slist, config=None):
        wx.PyEvent.__init__(self) 
        self.SetEventType(EVT_CUSTOM_DOC_ID)
        self.m_propagationLevel = wx.EVENT_PROPAGATE_MAX
        self.slist = copy.copy(slist)
        self.config = config
        
    def clone(self):
        evt = EventTrace(self.slist, self.config)
        return evt
    
 



    
    
    
    
    
    