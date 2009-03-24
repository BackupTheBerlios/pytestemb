#!/usr/bin/env python
"""
wxPython Technical Support Wizard (sort of).

Usage: wxsupportwiz.wxAddExceptHook('http://host.com/error.php')

- what happens if this is run when unconnected to the net?
- would be nice if the user could optionally enter some information about the problem, though of course I don't want it to get so complex that the user just cancels it

This sends the data using a CGI instead of by email because there's no guarantee that the user has setup an email account with MAPI.
Or I could always just bring up the user's web browser to a form already partially filled out.
The CGI could automatically match the error data to answers to already solved problems and suggest those.
So the whole wizard should probably be on the web.
For FAQs, could record how popular each answer is and then shown links to the top N answers.

can see XatXesizerDoc.cpp for a MAPI example. useful only for automatically including the user's email address
x automatically getting the user's email address seems hard, and what if there are multiple accounts, or none?

- sending the program's log would be nice to send too

The more work you postpone in your wxPython app until the wxWindows event loop has started, the more errors this will be able to catch.

If the cgi prints a line, this will assume it's a url and try to point the user's web browser to it. So you could, eg, popup help on the problem.

Having an exception occur in your exception handler is annoying.
"""

__author__ = 'Patrick Roberts'
__copyright__ = 'Copyright 2004 Patrick Roberts'
__license__ = 'Python'
__version__ = '1.0'

import os, platform, sys, time, traceback



import wx


def get_last_traceback(tb):
    while tb.tb_next:
        tb = tb.tb_next
    return tb


def format_namespace(d, indent=''):#    '):
    return '\n'.join(['%s%s: %s' % (indent, k, repr(v)[:10000]) for k, v in d.iteritems()])


ignored_exceptions = [] # a problem with a line in a module is only reported once per session

def add_exception_hook(path_log, app_version='[No version]'):#, ignored_exceptions=[]):
    """
    wxMessageBox can't be called until the app's started
    - It would be nice if this used win32 directly, and didn't depend on wx being started, cuz that can't handle initial errors. Maybe have a temporary initial error handler that just uses a standard windows message dlg, then switch once wx is going.
    """
    
    filename = os.path.join(path_log, "exception.log")
    
    def handle_exception(e_type, e_value, e_traceback):
        traceback.print_exception(e_type, e_value, e_traceback) # this is very helpful when there's an exception in the rest of this func
        last_tb = get_last_traceback(e_traceback)
        ex = (last_tb.tb_frame.f_code.co_filename, last_tb.tb_frame.f_lineno)
        if ex not in ignored_exceptions:
            ignored_exceptions.append(ex)
            ##message = "An uncaught error occurred.\n\nDo you mind if an error report is sent to %s?"
            #message = "Do you mind if an error report is sent to %s?"
            #message
            #if wx.MessageBox(message % urlparse.urlparse(cgi_url)[1], 'Uncaught Error', wx.OK|wx.CANCEL|wx.ICON_ERROR) == wx.OK:
            #print 'woof', `wx.GetTextFromUser('x')` # badly returns '' on cancel
            
            wx.MessageBox("Python exception raised\nWrite log in \"%s\"" % filename)
            
            #dlg = wx.TextEntryDialog(None, "Do you mind if an error report is sent to %s?\n\nIf you want to be contacted when a solution is found, please enter your e-mail address:" % "dd", 'Uncaught Error', '', wx.OK|wx.CANCEL) #|wx.ICON_ERROR) -- can use that style only with wx.MessageBox
            #result = dlg.ShowModal()
            #email_addr = dlg.GetValue()
           # dlg.Destroy()
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

            busy = wx.BusyCursor()
                
            
                
            f = open(filename, "w")
                
                
#            for k,v in info.iteritems():
#                f.write("%s:: %s\n" % (k.ljust(16),v))

            order = ['app-title', 
                    'app-version', 
                    'wx-version', 
                    'wx-platform', 
                    'python-version', 
                    'platform', 
                    'date' ,
                    'cwd',
                    'e-type',
                    'e-value',      ]
            for k in order:            
                f.write("%s:: %s\n" % (k.ljust(16),info[k]))

            
            
            try : 
            
                k = "traceback"
                f.write("%s::\n" % (k.ljust(16)))
                f.write("%s%s\n" % (" ".ljust(19),info[k].replace("\n", "\n".ljust(19))))
                
                
                k = "locals"
                f.write("%s::\n" % (k.ljust(16)))
                f.write("%s%s\n" % (" ".ljust(19),info[k].replace("\n", "\n".ljust(19))))
           
    
                k = "self"
                f.write("%s::\n" % (k.ljust(16)))
                f.write("%s%s\n" % (" ".ljust(19),info[k].replace("\n", "\n".ljust(19))))
            except Exception, ex :
                f.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                f.write("Exception in the exception handler\n")
                f.write("%s\n" % ex.__str__())
                f.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                
                
            
            f.close()
        

            del busy


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

    add_exception_hook("/tmp", "version_test")
    App = MyApp(0)
    App.MainLoop()    
    





