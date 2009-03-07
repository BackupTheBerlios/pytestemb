'''
Created on Mar 3, 2009

@author: jmb
'''

if __name__ == '__main__':
    pass



import wx



# Trace Level
# Same as "logging" module for interface
CRITICAL = 50
ERROR    = 40
WARNING  = 30
INFO     = 20
DEBUG    = 10
NOTSET   =  0


# ***************************************************
# wxEvent : EVT_CUSTOM_TRACE
# ***************************************************
EVT_CUSTOM_TRACE_ID = wx.NewId()

def EVT_CUSTOM_TRACE(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_TRACE_ID, func)    

class EventTrace(wx.PyEvent):
    def __init__(self, data , level):
        wx.PyEvent.__init__(self) 
        self.SetEventType(EVT_CUSTOM_TRACE_ID)
        self.m_propagationLevel = wx.EVENT_PROPAGATE_MAX
        self.data = data
        self.level = level
        
    def clone(self):
        return EventTrace(self.data, self.level)
    
    @staticmethod
    def create_critical(data):
        return EventTrace(data, CRITICAL)
    
    @staticmethod
    def create_error(data):
        return EventTrace(data, ERROR)
    
    @staticmethod
    def create_warning(data):
        return EventTrace(data, WARNING)
    
    @staticmethod
    def create_info(data):
        return EventTrace(data, INFO)
    
    @staticmethod
    def create_debug(data):
        return EventTrace(data, DEBUG)
    
    @staticmethod
    def create_notset(data):
        return EventTrace(data, NOTSET)

    



class LoggingFrame(wx.Panel):
    def __init__(self,parent, size = wx.Size(400,400)):
        
        wx.Panel.__init__(self, parent, -1, size=size)
        
        self.txtdis = wx.TextCtrl(self, -1, size=size, style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.txtdis.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        EVT_CUSTOM_TRACE(self, self.on_trace)
        
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.txtdis, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        
        cdb = wx.ColourDatabase()
        self.level = dict()
        self.level[CRITICAL]  = ("CRITICAL", wx.TextAttr(cdb.Find("RED")))
        self.level[ERROR]     = ("ERROR",    wx.TextAttr(cdb.Find("VIOLET RED")))
        self.level[WARNING]   = ("WARNING",  wx.TextAttr(cdb.Find("ORANGE")))
        self.level[INFO]      = ("INFO",     wx.TextAttr(cdb.Find("BLACK")))
        self.level[DEBUG]     = ("DEBUG",    wx.TextAttr(cdb.Find("BLUE")))
        self.level[NOTSET]    = ("NOTSET",   wx.TextAttr(cdb.Find("BLACK")))

        
        
        
    def on_trace(self, event):
        
        tl, style = self.level[event.level]
        
        self.txtdis.SetDefaultStyle(style)
        self.txtdis.AppendText("%s: %s\n" % (tl.ljust(10), event.data))




class TestFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):
        
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
    
        self.frm_log = LoggingFrame(self)
        
        self.but_debug    =  wx.Button(self, -1, "Log DEBUG",  (20, 20))
        self.but_info     =  wx.Button(self, -1, "Log INFO",   (20, 20))
        self.but_warning  =  wx.Button(self, -1, "Log WARNING",(20, 20))
        self.but_error    =  wx.Button(self, -1, "Log ERROR",  (20, 20))
        self.but_critical =  wx.Button(self, -1, "Log CRITICAL",  (20, 20))
        
        self.Bind(wx.EVT_BUTTON, self.on_but_debug,    self.but_debug)
        self.Bind(wx.EVT_BUTTON, self.on_but_info,     self.but_info)
        self.Bind(wx.EVT_BUTTON, self.on_but_warning,  self.but_warning)
        self.Bind(wx.EVT_BUTTON, self.on_but_error,    self.but_error)
        self.Bind(wx.EVT_BUTTON, self.on_but_critical, self.but_critical)
    


        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.but_debug)
        sizer_2.Add(self.but_info)
        sizer_2.Add(self.but_warning)
        sizer_2.Add(self.but_error)
        sizer_2.Add(self.but_critical)
        
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2,)
        sizer_1.Add(self.frm_log, 1, wx.EXPAND, 0)
        
        self.SetSizer(sizer_1)
        self.Layout()
     
    def on_but_debug(self, event):
        evt = EventTrace.create_debug("One debug log")
        self.frm_log.AddPendingEvent(evt)
        
    def on_but_info(self, event):
        evt = EventTrace.create_info("One info log")
        self.frm_log.AddPendingEvent(evt)

    def on_but_warning(self, event):
        evt = EventTrace.create_warning("One warning log")
        self.frm_log.AddPendingEvent(evt) 

    def on_but_error(self, event):
        evt = EventTrace.create_error("One error log")
        self.frm_log.AddPendingEvent(evt)

    def on_but_critical(self, event):
        evt = EventTrace.create_critical("One critical log")
        self.frm_log.AddPendingEvent(evt)  
    


class MyApp(wx.App):        

    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = TestFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        
        return 1




if __name__ == "__main__":

    App = MyApp(0)
    App.MainLoop()    
    
    
    
    
    