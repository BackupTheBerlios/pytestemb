# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : pannelRunner manages script execution
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.14 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




#import os
import time
import threading

#import logging
import logging.handlers


import wx

import pytestemb.parser as parser

import data.results as dres
import data.documentation as ddoc

import frm_logging




#LOG = logging.getLogger("ScriptRunner")




# ***************************************************
# wxEvent : EVT_CUSTOM_ENDSCRIPTS
# ***************************************************
EVT_CUSTOM_ENDSCRIPTS_ID = wx.NewId()

def EVT_CUSTOM_ENDSCRIPTS(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_ENDSCRIPTS_ID, func)    

class EventEndScript(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self) 
        self.SetEventType(EVT_CUSTOM_ENDSCRIPTS_ID)
    def clone(self):
        return EventEndScript()


# ***************************************************
# wxEvent : EVT_CUSTOM_ENDSCRIPTS
# *************************************************** 
EVT_CUSTOM_STARTPROCESS_ID = wx.NewId()

def EVT_CUSTOM_STARTPROCESS(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_STARTPROCESS_ID, func)

class EventStartProcess(wx.PyEvent):
    def __init__(self, pathfilename):
        wx.PyEvent.__init__(self) 
        self.pathfilename = pathfilename
        self.SetEventType(EVT_CUSTOM_STARTPROCESS_ID)
    def clone(self):
        return EventStartProcess(self.pathfilename)


# ***************************************************
# wxEvent : EVT_CUSTOM_EXECSTATUS
# *************************************************** 
EVT_CUSTOM_EXECSTATUS_ID = wx.NewId()

def EVT_CUSTOM_EXECSTATUS(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_EXECSTATUS_ID, func)

class EventExecStatus(wx.PyEvent):
    STATE_START = 0
    STATE_END = 1
    def __init__(self, status):
        wx.PyEvent.__init__(self) 
        self.status = status
        self.SetEventType(EVT_CUSTOM_EXECSTATUS_ID)
    def get_script(self):
        return self.status["name"]
    def is_state_start(self):
        return (self.status["state"] == EventExecStatus.STATE_START)
    def is_state_end(self):
        return (self.status["state"] == EventExecStatus.STATE_END)    
    def clone(self):
        return EventExecStatus(self.status)
    @staticmethod
    def create_start_script(script_name):
        status = {"name":script_name, "state":EventExecStatus.STATE_START}
        return EventExecStatus(status)
    @staticmethod
    def create_end_script(script_name):
        status = {"name":script_name, "state":EventExecStatus.STATE_END}
        return EventExecStatus(status)
               




# On linux
PY_EXE_RET_CODE_OK              = 0
PY_EXE_RET_CODE_ERROR_SYNTAX    = 1
PY_EXE_RET_CODE_ERROR_FILE      = 2



# data dict
BASE_PATH       = 0
SCRIPT_LIST     = 1
CONFIG          = 2
TRACE           = 3
PYPATH          = 4
RUN_TYPE        = 5
PYINTER         = 6

# trace config
TRACE_NONE          = 0
TRACE_OCTOPYLOG     = 1
TRACE_TXT           = 2
TRACE_OCTOPYLOG_TXT = 3

# run type
RUN_SCRIPT = 0
RUN_DOC    = 1

    
    
STYLE_AUTO_START_CLOSE  = 0
STYLE_DEFAULT           = 1


RET_CODE_OK         = 0
RET_CODE_ERROR      = 1
RET_CODE_USER_ABORT = 2


class DialogRunner(wx.Dialog):
    
    def __init__(self, data, style=STYLE_DEFAULT, *args, **kwds):
        
        
        # init wx.Dialog
        if   style == STYLE_DEFAULT:
            kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        elif style == STYLE_AUTO_START_CLOSE:
            kwds["style"] = wx.THICK_FRAME 
        else :
            assert False
        wx.Dialog.__init__(self, *args, **kwds)
        

        
        # get parameters
        self.data = data
        self.style = style

        self.log        = None
        self.docs       = None
        self.results    = None        
        self.start      = None
        self.stop       = None
        

        if   style == STYLE_DEFAULT:
            self.SetTitle("Script Runner")
            self.start = wx.Button(self, -1,"Start")
            self.stop = wx.Button(self, -1, "Stop") 
        elif style == STYLE_AUTO_START_CLOSE:
            self.stop = wx.Button(self, -1, "Stop")
        else :
            assert False
            

        # bind event
        if self.stop is not None :
            self.Bind(wx.EVT_BUTTON, self.onStop, self.stop)  
        if self.start is not None :
            self.Bind(wx.EVT_BUTTON, self.onStart, self.start)

        self.Bind(wx.EVT_CLOSE, self.onClose)        
        
        # timer for activity gauge
#        self.Bind(wx.EVT_TIMER, self.handler_timer)
#        self.timer = wx.Timer(self)

        
        # process management
        self.process = None
        self.pid = None
        self.exit_code = None
        
        self.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)
        EVT_CUSTOM_STARTPROCESS(self, self.OnStartProcess)
        EVT_CUSTOM_ENDSCRIPTS(self, self.OnEndScripts)
        EVT_CUSTOM_EXECSTATUS(self, self.on_execstatus)
        
        
        # scripts runner
        self.evtScriptRun = threading.Event()
        self.evtReaderRun = threading.Event()
        self.thdScriptRun = threading.Thread(target=self.thread_scripts_runner,  name="scripts_runner")

        
        
        if      self.data[RUN_TYPE] == RUN_SCRIPT :
            self.results = dres.Results("tmp_controler")
        elif    self.data[RUN_TYPE] == RUN_DOC :
            self.docs = ddoc.Documentation()
        else :
            raise Exception("No type run define")        
        
    
            # create control  
        self.lstboxScript = wx.ListBox(self, -1,  size=wx.Size(400,200))
        self.lstboxScript.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.activity = wx.Gauge(self, -1, size=wx.Size(400,30))
        
    
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add((400, 20), 0, 0, 0)
        sizer_1.Add(self.lstboxScript, 0, wx.ALL, 5)
        sizer_1.Add(self.activity, 0, wx.ALL, 5)
        sizer_1.Add((400, 20), 0, 0, 0)
        
        
        
        if self.start is not None :
            sizer_1.Add(self.start, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        if self.stop is not None :
            sizer_1.Add(self.stop, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5) 

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
    
        self.init_GUI()
        
        
        
        # Start
        if   style == STYLE_DEFAULT:
            pass
        elif style == STYLE_AUTO_START_CLOSE:
            self.start_running_script()
        else :
            assert False
        
        
        
    def get_result(self):
        return self.results
    
    def get_doc(self):
        return self.docs
        
    def set_log(self, log):
        self.log = log
        self.log_info("log enable")
        
    def log_debug(self, data):
        if self.log is not None :
            self.log.log_debug(data)
        
    def log_info(self, data):
        if self.log is not None :
            self.log.log_info(data)

    def log_error(self, data):
        if self.log is not None :
            self.log.log_error(data)



    def init_GUI(self):
        # init lstbox with scripts filename
        scriptName = []
        for script in  self.data[SCRIPT_LIST]:
            scriptName.append(script.str_relative())
        self.lstboxScript.InsertItems(scriptName, 0)
        self.activity.SetRange(len(scriptName))

            
      
    def run_process(self, pathfilename):
        """ run a process 
        must be called in main thread """
        
        #scriptArgument = " --config=stdin --result=stdout"
        scriptArgument = " --config=none --result=stdout"
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
    
        if self.data[RUN_TYPE] == RUN_DOC :
            scriptArgument += " --doc" 


        interpretor = self.data[PYINTER] + " -u"
        
        cmd = interpretor + " " + pathfilename + scriptArgument
        
        self.exit_code = None
        self.pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)
        self.log_debug("Process cmd : %s" % cmd)
        self.log_debug("Process pid : %s" % self.pid)
        
#        self.process.GetOutputStream().write("env : debug\n")
#        self.process.GetOutputStream().write("serial : com1\n")
#        self.process.GetOutputStream().write("case : case_01\n")
#        self.process.GetOutputStream().write("case : case_02\n")
#        self.process.GetOutputStream().write("END\n")        
        
        
    def on_execstatus(self, evt):

        n = self.lstboxScript.FindString(evt.get_script())
        if      evt.is_state_start():
            self.lstboxScript.Select(n)
        elif    evt.is_state_end():
            self.lstboxScript.Deselect(n)
            
            self.activity.SetValue(n+1) 
        else:
            assert False
        



    def OnProcessEnded(self, evt):
        """ call back when event """
        self.pid = None
        
        self.log_debug("Process Ended")
        self.log_debug("Process pid : %s" % evt.GetPid())
        self.log_debug("Process exitcode : %s" % evt.GetExitCode())
        self.exit_code = evt.GetExitCode()
        self.evtReaderRun.set() # stop reader on process
        
        
        
        
    def update_result(self, script, sdoutreader):
        
        if      self.data[RUN_TYPE] == RUN_SCRIPT :
            scriptres = dres.ScriptRes(script)
            if self.exit_code == PY_EXE_RET_CODE_OK :
                scriptres.import_resultstdoutreader(sdoutreader)    
            elif self.exit_code ==  PY_EXE_RET_CODE_ERROR_FILE:
                param = "python: can't open file \"%s\""  % script.str_absolute(self.data[BASE_PATH])
                scriptres.set_status(dres.ST_EXEC_EXECUTED_FILE_ERROR, param )
            elif self.exit_code ==  PY_EXE_RET_CODE_ERROR_SYNTAX:
                param = "SyntaxError: invalid syntax"
                scriptres.set_status(dres.ST_EXEC_EXECUTED_PY_ERROR, param)        
            else :
                scriptres.set_status(dres.ST_EXEC_EXECUTED_FILE_ERROR)
            self.results.update(scriptres)
        
        elif    self.data[RUN_TYPE] == RUN_DOC :
            scriptdoc = ddoc.ScriptDoc(script)
            if self.exit_code == PY_EXE_RET_CODE_OK :
                scriptdoc.import_doctstdoutreader(sdoutreader)    
            elif self.exit_code ==  PY_EXE_RET_CODE_ERROR_FILE:
                param = "python: can't open file \"%s\""  % script.str_absolute(self.data[BASE_PATH])
                scriptdoc.set_status(ddoc.ST_PARSE_FILE_ERROR, param )
            elif self.exit_code ==  PY_EXE_RET_CODE_ERROR_SYNTAX:
                param = "SyntaxError: invalid syntax"
                scriptdoc.set_status(ddoc.ST_PARSE_PY_ERROR, param)        
            else :
                scriptdoc.set_status(ddoc.ST_PARSE_FILE_ERROR) 
            self.docs.update(scriptdoc)
        else :
            raise Exception("No type run define")


                
    def post_event_startprocess(self, pathfilename):
        evt = EventStartProcess(pathfilename)
        self.AddPendingEvent(evt)


    def post_event_endscripts(self):
        evt = EventEndScript()
        self.AddPendingEvent(evt)        
        

    def OnEndScripts(self, event):
        
        self.log_info("end script running")   
        if   self.style == STYLE_DEFAULT:
            self.log_debug("nop")  
        elif self.style == STYLE_AUTO_START_CLOSE:
            self.log_debug("EndModal(RET_CODE_OK)")  
            self.EndModal(RET_CODE_OK)
        else :
            assert False
            
        

    def OnStartProcess(self, event):
        self.log_debug("OnStartProcess")   
        self.process = wx.Process(self)
        self.process.Redirect()
        self.run_process(event.pathfilename)
    

    def start_thread_scripts_runner(self):
        """ start_thread_scripts_runner """
        self.evtScriptRun.clear()
        self.evtReaderRun.clear()       
        self.thdScriptRun.start()
        
           
    def stop_thread_scripts_runner(self):
        """ stop_thread_scripts_runner """
        if self.thdScriptRun.isAlive() :
            self.log_debug("Thread is stopping ...")
            self.evtReaderRun.set()
            self.evtScriptRun.set() 
            self.thdScriptRun.join()
            self.log_debug("Thread is stopped")            
        else :
            self.log_debug("Thread is already stopped")
    
    

    def thread_scripts_runner(self):  
        """ thread that run a list of scripts """
        self.log_debug("Thread is running")
        
        for index, script in enumerate(self.data[SCRIPT_LIST]):
            # update GUI
            self.AddPendingEvent(EventExecStatus.create_start_script(script.str_relative()))
            # run script
            self.evtReaderRun.clear()
            self.post_event_startprocess(script.str_absolute(self.data[BASE_PATH]))
            res = self.reader_process()
            
            if self.evtScriptRun.isSet() :
                self.log_debug("Break thread loop")
                return            
            
            self.process.Destroy()
            self.process = None            

            # update GUI and result
            self.AddPendingEvent(EventExecStatus.create_end_script(script.str_relative()))
            self.update_result(script, res)
            # Stop script execution
            if self.evtScriptRun.isSet() :
                self.log_debug("Break thread loop")
                return
        self.post_event_endscripts()
            
    
    
    def reader_process(self):
        
        if      self.data[RUN_TYPE] == RUN_SCRIPT :
            stdoutreader = parser.ResultStdoutReader()
        elif    self.data[RUN_TYPE] == RUN_DOC :
            stdoutreader = parser.DocStdoutReader()
        else :
            raise Exception("No type run define")
        
        
        try :
            waiting = 0.05   
            while not(self.evtReaderRun.isSet()):
                if self.process is None:
                    time.sleep(waiting) 
                    continue
                stream = self.process.GetInputStream()
                if stream is None :
                    #LOG.info("sleep : %f" % waiting)
                    time.sleep(waiting) 
                else:
                    while       not(self.evtReaderRun.isSet())\
                            or  stream.CanRead():
                        if stream.CanRead():
                            text = stream.readline()
                            #LOG.info(text)
                            stdoutreader.add_line(text)
                        else:   
                            time.sleep(waiting)                    

        except Exception, ex:
            self.log_debug("%s : %s" % (ex.__class__.__name__, ex.__str__()))
            raise ex
        #self.process = None     
        self.log_debug("end stdoutreader")
        return stdoutreader   
                        

    def start_running_script(self):
        self.start_thread_scripts_runner()
      
    def onStart(self, event):
        self.start_running_script()
        
      
    def onStop(self, event):
        self.stop_script_running()

        if   self.style == STYLE_DEFAULT:
            pass
        elif self.style == STYLE_AUTO_START_CLOSE:
            
            time.sleep(1)
            self.log_debug("EndModal(RET_CODE_USER_ABORT)")
            self.EndModal(RET_CODE_USER_ABORT)
        else :
            assert False
            


       
        
        
    def stop_script_running(self):
        """ Stop script exection """    
        self.log_debug("stop script running")
    
        try:
            self.process.CloseOutput()
            self.stop_thread_scripts_runner() 
            self.process.Detach()   
#            self.process.Destroy()
            self.process = None                   
           
        except Exception, ex :
            self.log_debug("%s : %s" % (ex.__class__.__name__, ex.__str__()))
         
         
        if self.pid is not None:
            try :
                self.log_debug("Stop process ... by kill pid:%d" % self.pid)
                
                ret = wx.Process.Kill(self.pid, wx.SIGKILL)
                if    ret == wx.KILL_OK :
                    self.log_debug("Process kill success")
                elif  ret == wx.KILL_NO_PROCESS :
                    self.log_debug("No process existing")
                else :
                    self.log_error("Error killing process, try manually : name=\"python\", pid=%d " % self.pid)    
            except Exception, ex:
                self.log_debug("%s : %s" % (ex.__class__.__name__, ex.__str__()))
                self.log_error("Error during process killing")    
        else:
            self.log_debug("Process seems ended")

    
    def close_dialog(self):
        
        if self.thdScriptRun.isAlive() :
            self.stop_script_running()
            self.log_debug("EndModal(RET_CODE_USER_ABORT)")
            self.EndModal(RET_CODE_USER_ABORT)
        else: 
            self.log_debug("EndModal(RET_CODE_OK)")
            self.EndModal(RET_CODE_OK)        
    
                
        
    def onClose(self, event):
        self.close_dialog()







if __name__ == "__main__":
    
    import data.project as dproj

#    rootLogger = logging.getLogger("")
#    rootLogger.setLevel(logging.DEBUG)
#    socketHandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
#    rootLogger.addHandler(socketHandler)
#        
    
    class MyApp(wx.App):
        def OnInit(self):
   
   
            #import os.path
        
            proj = dproj.load_xml(os.path.realpath("../../test/script/project_01.xml")) 
            #proj = dproj.load_xml(os.path.realpath("C:\\CVS_LOCAL_ECLIPSE\\scripts\\project\\champ2\\champ2.xml"))
            #slist = proj.get_campaign_list_scripts("Campaign_Infinite_Loop")
            #slist = proj.get_campaign_list_scripts("Campaign_Infinite_Loop")
            slist = proj.get_pool_list_absolute()
               
            data = {}
            
            data[BASE_PATH] = proj.get_base_path()
            data[SCRIPT_LIST] = slist
            data[CONFIG] = None
            data[TRACE] = TRACE_OCTOPYLOG
            #data[PYPATH] = "c:\\CVS_LOCAL_ECLIPSE\\scripts"
            data[PYPATH] = None
            #data[RUN_TYPE] = RUN_SCRIPT
            data[RUN_TYPE] = RUN_SCRIPT
            

            style = STYLE_AUTO_START_CLOSE
            
            
            
            log = frm_logging.LoggingStdout()
            
            wx.InitAllImageHandlers()
            dlg = DialogRunner(data, style, None, -1, "")
            dlg.set_log(log)
            dlg.ShowModal()
            
            res = dlg.get_result()
            
            res.save("result.dbm")
            
            print dlg.GetReturnCode()
            return 1    
    

        
    App = MyApp(0)
    
    
    