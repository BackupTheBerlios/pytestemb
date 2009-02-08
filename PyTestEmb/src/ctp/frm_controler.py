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
import wx
import time
import threading


import logging
import logging.handlers


import results

import pytestemb.result as result


import project



LOG = logging.getLogger("ScriptRunner")




EVT_CUSTOM_STARTPROCESS_ID = wx.NewId()
EVT_CUSTOM_ENDSCRIPTS_ID = wx.NewId()


def EVT_CUSTOM_STARTPROCESS(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_STARTPROCESS_ID, func)

def EVT_CUSTOM_ENDSCRIPTS(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_ENDSCRIPTS_ID, func)


class EventStartProcess(wx.PyEvent):
    def __init__(self, pathfilename):
        wx.PyEvent.__init__(self) 
        self.pathfilename = pathfilename
        self.SetEventType(EVT_CUSTOM_STARTPROCESS_ID)
    def clone(self):
        return EventStartProcess(self.pathfilename)

class EventEndScript(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self) 
        self.SetEventType(EVT_CUSTOM_ENDSCRIPTS_ID)
    def clone(self):
        return EventEndScript()

def getScriptName(pathfilename):
    return os.path.splitext(os.path.split(pathfilename)[1])[0]      







# data dict
BASE_PATH       = 0
SCRIPT_LIST     = 1
CONFIG          = 2
TRACE           = 3
PYPATH          = 4

# trace config
TRACE_NONE          = 0
TRACE_OCTOPYLOG     = 1
TRACE_TXT           = 2
TRACE_OCTOPYLOG_TXT = 3
    
    

class DialogRunner(wx.Dialog):
    
    def __init__(self, data, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)
        
        LOG.info("Start init window")
        
        # get parameters
        self.data = data

        
        
        # create control  
        self.lstboxScript = wx.ListBox(self, -1,  size=wx.Size(400,200))
        self.activity = wx.Gauge(self, -1, size=wx.Size(400,30))
        self.start = wx.Button(self, -1,"Start")
        self.stop = wx.Button(self, -1, "Stop")
        self.close = wx.Button(self, -1, "Close")
        
        # layout
        self.__set_properties()
        self.__do_layout()
        
        # bind event
        self.Bind(wx.EVT_BUTTON, self.onStart, self.start)
        self.Bind(wx.EVT_BUTTON, self.onStop, self.stop)
        self.Bind(wx.EVT_BUTTON, self.onClose, self.close)
        self.Bind(wx.EVT_CLOSE,self.onDestroy)        
        
        # timer for activity gauge
        self.Bind(wx.EVT_TIMER, self.handler_timer)
        self.timer = wx.Timer(self)

        
        # process management
        self.process = None
        self.pid = None
        self.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)
        EVT_CUSTOM_STARTPROCESS(self, self.OnStartProcess)
        EVT_CUSTOM_ENDSCRIPTS(self, self.OnEndScripts)
        
        
        # scripts runner
        self.evtScriptRun = threading.Event()
        self.evtReaderRun = threading.Event()
        self.thdScriptRun = threading.Thread(target=self.thread_scripts_runner,  name="scripts_runner")
        
        self.results = results.Results()
        
        
        

        self.init_GUI()

        LOG.info("End Init window")
        


    def __set_properties(self):

        self.SetTitle("Script Runner")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("images\\cog_go.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)


    def __do_layout(self):

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add((400, 20), 0, 0, 0)
        sizer_1.Add(self.lstboxScript, 0, wx.ALL, 5)
        sizer_1.Add(self.activity, 0, wx.ALL, 5)
        sizer_1.Add((400, 20), 0, 0, 0)
        
        sizer_1.Add(self.start, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.stop, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.close, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
              
    
    def init_GUI(self):
        # init lstbox with scripts filename
        scriptName = []
        for script in  self.data[SCRIPT_LIST]:
            #scriptName.append(getScriptName(script))
            scriptName.append(script.str_relative())
        self.lstboxScript.InsertItems(scriptName, 0)
                
    
        
    def clean(self):
        LOG.info("Start clean")
        self.timer.Stop()
        self.stop_thread_scripts_runner()
        if self.process is not None:
            self.process.Kill(self.process.GetPid())
            self.process.CloseOutput()
            self.process = None
        LOG.info("Stop clean")        

            

    def handler_timer(self, event):
        self.activity.Pulse()


      
      
      
    def run_process(self, pathfilename):
        """ run a process 
        must be called in main thread """
        
        
        #scriptArgument = " --config=stdin --result=stdout"
        scriptArgument = " --config=stdin --result=stdout"
        if self.data[PYPATH] is not None:
            scriptArgument += " --path=%s" % (self.data[PYPATH])
        
        if  self.data[TRACE] == TRACE_NONE :
            scriptArgument += " --trace=none"
        elif  self.data[TRACE] == TRACE_OCTOPYLOG :
            scriptArgument += " --trace=octopylog"
        elif  self.data[TRACE] == TRACE_TXT :
            scriptArgument += " --trace=txt"    
        elif  self.data[TRACE] == TRACE_OCTOPYLOG_TXT :
            scriptArgument += " --trace=txt --trace=octopylog" 
        else:
            assert False
    

        interpretor = "python -u"
        cmd = interpretor + " " + pathfilename + scriptArgument
        self.pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)
        LOG.info("Start process : %s pid %s\n" % (cmd, self.pid))
        
        self.process.GetOutputStream().write("env : debug\n")
        self.process.GetOutputStream().write("serial : com1\n")
        self.process.GetOutputStream().write("case : case_01\n")
        self.process.GetOutputStream().write("case : case_02\n")
        self.process.GetOutputStream().write("END\n")        
        


    def OnProcessEnded(self, evt):
        """ call back when event """
        self.pid = None
        LOG.info("Process Ended pid:%s,  exitCode: %s\n" % \
                              (evt.GetPid(), evt.GetExitCode()))
        time.sleep(0.1)         # let some times to reader to finish reading
        self.evtReaderRun.set() # stop reader on process
        
        
    def update_result(self, script, resultstdoutreader):
        
        scriptres = results.ScriptRes(script)
        scriptres.import_resultstdoutreader(resultstdoutreader)    
        self.results.update(scriptres)

        
        



                
    def post_event_startprocess(self, pathfilename):
        evt = EventStartProcess(pathfilename)
        self.AddPendingEvent(evt)


    def post_event_endscripts(self):
        evt = EventEndScript()
        self.AddPendingEvent(evt)
        
        print self.results.__str__()
        self.results.save()
        
        

    def OnEndScripts(self, event):
        self.stop_Gauge_Activity()
        


    def OnStartProcess(self, event):
        self.process = wx.Process(self)
        self.process.Redirect()
        self.run_process(event.pathfilename)
    

    def start_Gauge_Activity(self):
        """ start the gauge activity
        Must be called by main thread """
        assert not(self.timer.IsRunning())
        self.timer.Start(100) 
        
        
    def stop_Gauge_Activity(self):
        """ stop the gauge activity (reset) """
        if self.timer.IsRunning() :
            self.timer.Stop()
            self.activity.SetValue(0)
                
            
    def start_thread_scripts_runner(self):
        """ start_thread_scripts_runner """
        self.evtScriptRun.clear()
        self.evtReaderRun.clear()       
        self.thdScriptRun.start()
        
           
    def stop_thread_scripts_runner(self):
        """ stop_thread_scripts_runner """
        if self.thdScriptRun.isAlive() :
            LOG.info("Thread is stopping ...")
            self.evtReaderRun.set()
            self.evtScriptRun.set()
            self.thdScriptRun.join()
            LOG.info("Thread is stopped")            
        else :
            LOG.info("Thread is already stopped")
        
    
    
    def thread_scripts_runner(self):  
        """ thread that run a list of scripts """
        LOG.info("Thread is running")
        for index, script in enumerate(self.data[SCRIPT_LIST]):
            self.lstboxScript.Select(index)
            self.evtReaderRun.clear()
            self.post_event_startprocess(script.str_absolute(self.data[BASE_PATH]))
            res = self.reader_process()
            self.lstboxScript.Deselect(index)
            self.update_result(script, res)
            if self.evtScriptRun.isSet() :
                break
        self.post_event_endscripts()
            
    
    
    def reader_process(self):
        
        resultstdoutreader = result.ResultStdoutReader()
        waiting = 0.05   
        while not(self.evtReaderRun.isSet()):
            if self.process is None:
                time.sleep(waiting) 
            stream = self.process.GetInputStream()
            if stream is None :
                #LOG.info("sleep : %f" % waiting)
                time.sleep(waiting) 
            else:
                while not(self.evtReaderRun.isSet()):
                    if stream.CanRead():
                        text = stream.readline()
                        LOG.info(text)
                        resultstdoutreader.add_line(text)
                    else:   
                        time.sleep(waiting)
                        
        self.process.CloseOutput()
        self.process.Destroy()
        self.process = None     
        return resultstdoutreader   
        #LOG.info("End reader")
                        

        
      
    def onStart(self, event):
        self.start_Gauge_Activity()
        self.start_thread_scripts_runner()

      
    def onStop(self, event):
        """ Stop script exection """
        LOG.info("Stop execution")
        self.process.CloseOutput()
        self.stop_thread_scripts_runner()  
        if self.pid is not None :
            LOG.info("Stop process ... by kill pid:%d" % self.pid)
            self.process.Kill(self.pid, wx.SIGKILL)
        
        

    def onClose(self, event): 
        self.EndModal(0)
        event.Skip()


    def onDestroy(self, event):
        #LOG.info("destroy")  
        #self.clean()
        self.EndModal(0)





if __name__ == "__main__":
    
    

    rootLogger = logging.getLogger("")
    rootLogger.setLevel(logging.DEBUG)
    socketHandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    rootLogger.addHandler(socketHandler)
        
    
    class MyApp(wx.App):
        def OnInit(self):
            
            
            
            proj = project.load_from_xml("C:\\CVS_LOCAL_ECLIPSE\\scripts\\project\\champ2\\champ2.xml")
            
            slist = proj.get_campaign_list_absolute("bluetooth_no_device")
            
            
            
            data = {}
            
            data[BASE_PATH] = proj.get_base_path()
            data[SCRIPT_LIST] = slist
            data[CONFIG] = None
            data[TRACE] = TRACE_OCTOPYLOG_TXT
            data[PYPATH] = "C:\\CVS_LOCAL_ECLIPSE\\scripts"
        
            

            

            wx.InitAllImageHandlers()
            dlg = DialogRunner(data, None, -1, "")
            dlg.ShowModal()
            return 1    
    

        
    App = MyApp(0)
    
    
    