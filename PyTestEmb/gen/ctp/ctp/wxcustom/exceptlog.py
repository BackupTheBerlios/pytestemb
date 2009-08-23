# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : pannelRunner manages script execution
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"





import os
import sys
import time
import platform
import traceback



import wx


def get_last_traceback(tb):
    while tb.tb_next:
        tb = tb.tb_next
    return tb


def format_namespace(d, indent=''):
    return '\n'.join(['%s%s: %s' % (indent, k, repr(v)[:10000]) for k, v in d.iteritems()])


ignored_exceptions = [] 

def add_exception_hook(path_log, app_version, app_support):
    filename = os.path.join(path_log, "exception.log")
    
    def handle_exception(e_type, e_value, e_traceback):
        traceback.print_exception(e_type, e_value, e_traceback)
        last_tb = get_last_traceback(e_traceback)
        ex = (last_tb.tb_frame.f_code.co_filename, last_tb.tb_frame.f_lineno)
        if ex not in ignored_exceptions:
            ignored_exceptions.append(ex)
        
            instruction = "An exception was raised, but not catch by the application\n"
            instruction += "A report will be generated : %s\n" % filename
            instruction += "\nTo help developement team, you can :\n"
            instruction += " 1. Add a quick description of the action or/and configuration that results to an exception\n"
            instruction += " 2. Send an email with log report to : %s\n" % app_support
            instruction += "\nQuick description :"
            dlg = wx.TextEntryDialog(None, instruction, "Exception","",  wx.OK)
            result = dlg.ShowModal()
            user = dlg.GetValue()
            dlg.Destroy()
            info = {
                    'app-title' : wx.GetApp().GetAppName(), # app_title
                    'app-version' : app_version,
                    'wx-version' : wx.VERSION_STRING,
                    'wx-platform' : wx.Platform,
                    'python-version' : platform.python_version(), #sys.version.split()[0],
                    'platform' : platform.platform(),
                    'e-type' : e_type,
                    'e-value' : e_value,
                    'date' : time.ctime(),
                    'cwd' : os.getcwd(),
                    "user" : user
                    }
            if e_traceback:
                info['traceback'] = ''.join(traceback.format_tb(e_traceback)) + '%s: %s' % (e_type, e_value)
                last_tb = get_last_traceback(e_traceback)
                exception_locals = last_tb.tb_frame.f_locals # the locals at the level of the stack trace where the exception actually occurred
                info['locals'] = format_namespace(exception_locals)
                if 'self' in exception_locals:
                    info['self'] = format_namespace(exception_locals['self'].__dict__)
            if sys.platform == 'win32':
                import win32api
                info['user-name'] = win32api.GetUserName()
                
            
                
            f = open(filename, "w")
            
            
            order = ['app-title', 
                    'app-version', 
                    'wx-version', 
                    'wx-platform', 
                    'python-version', 
                    'platform', 
                    'date' ,
                    'cwd',
                    'e-type',
                    'e-value',   
                    "user"   ]
            for k in order:            
                f.write("%s:: %s\n" % (k.ljust(16),info[k]))

            
            k = "traceback"
            if info.has_key(k):
                f.write("%s::\n" % (k.ljust(16)))
                f.write("%s%s\n" % (" ".ljust(19),info[k].replace("\n", "\n".ljust(19))))
                
            k = "locals"
            if info.has_key(k):
                f.write("%s::\n" % (k.ljust(16)))
                f.write("%s%s\n" % (" ".ljust(19),info[k].replace("\n", "\n".ljust(19))))
           
            k = "self"
            if info.has_key(k):
                f.write("%s::\n" % (k.ljust(16)))
                f.write("%s%s\n" % (" ".ljust(19),info[k].replace("\n", "\n".ljust(19))))

            f.close()
        


    sys.excepthook = lambda *args: wx.CallAfter(handle_exception, *args) # this callafter may be unnecessary since it looks like threads ignore sys.excepthook; could have all a thread's code be contained in a big try clause (possibly by subclassing Thread and replacing run())
















class TestFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):
        
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        
        
        self.but_exception    =  wx.Button(self, -1, "Exception",  (20, 20))
        
        self.Bind(wx.EVT_BUTTON, self.on_but_exception,    self.but_exception)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.but_exception)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2,)
        
        self.SetSizer(sizer_1)
        self.Layout()
     
     
     
    def on_but_exception(self, event):
        raise Exception("exception test")
        pass




class MyApp(wx.App):        

    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = TestFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        
        return 1

    


if __name__ == "__main__":

    add_exception_hook("/tmp", "version_test", "support@test.com")
    App = MyApp(0)
    App.MainLoop()    
    





