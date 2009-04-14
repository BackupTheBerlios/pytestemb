# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.17 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"

import wx
import wx.grid
import wx.html
import wx.aui

import wx.lib.flatnotebook as fnb


import sys
import os.path

import data.utils

import wxcustom.evt_file as evt_file
import wxcustom.evt_run as evt_run
import wxcustom.evt_doc as evt_doc
import wxcustom.exceptlog as exceptlog
import wxcustom.editor_py as editor_py

import frm_logging
import frm_project
import frm_results
import frm_controler


APP_NAME     = "Control Test"
APP_VERSION  = "1.0.1"



# TRACE_DEBUG :
#  True   = Debug Trace Activate
#  False  = Debug Trace DeActivate
TRACE_DEBUG     = True
# EXCEPT_DEBUG :
# True    = std.err for exception output
# False   = GUI exception handler
EXCEPT_DEBUG    = True



ID_PROJECT_NEW = wx.NewId()
ID_PROJECT_OPEN = wx.NewId()
ID_PROJECT_SAVE = wx.NewId()
ID_PROJECT_SAVEAS = wx.NewId()

ID_ABOUT = wx.NewId()





def get_app_path():
    return os.path.split(sys.argv[0])[0]



class PyAUIFrame(wx.Frame):

    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.path = dict()
        self.path["app_path"] = get_app_path()
        self.path["stack_file"] = os.path.join(self.path["app_path"], "stack.dbm")
        self.path["global_file"] = os.path.join(self.path["app_path"], "global.dbm")


        self.ctrl = { "log"     :     None,
                      "project" :     None,
                      "result"  :     None,
                      "mdi"     :     None,
                      "res_glo" :     None,
                      "res_sta" :     None}


        # Custom event from view
        evt_file.EVT_CUSTOM_FILE_VIEW(self, self.on_file_view)
        evt_run.EVT_CUSTOM_RUN_SCRIPT(self, self.on_run_script)
        evt_doc.EVT_CUSTOM_DOC(self,        self.on_run_doc)


        # Application Title & Icon
        self.SetTitle("Control Test - PyTestEmb")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("images/weather_lightning.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        # Configuration application
        self.wxconf = wx.Config(APP_NAME.replace(" ", "_"))


        # tell FrameManager to manage this frame
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self._perspectives = []
        self.n = 0
        self.x = 0

        # Menu
        mb = wx.MenuBar()
        self.SetMenuBar(mb)
        # Menu File
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        mb.Append(file_menu,    "File")

        # Menu project
        project_menu = wx.Menu()
        project_menu.Append(ID_PROJECT_NEW,    "New ...")
        project_menu.Append(ID_PROJECT_OPEN,   "Open ..")
        project_menu.Append(ID_PROJECT_SAVE,   "Save")
        project_menu.Append(ID_PROJECT_SAVEAS, "Save As ..")
        self.Bind(wx.EVT_MENU, self.on_menu_project_new,    id=ID_PROJECT_NEW)
        self.Bind(wx.EVT_MENU, self.on_menu_project_open,   id=ID_PROJECT_OPEN)
        self.Bind(wx.EVT_MENU, self.on_menu_project_save,   id=ID_PROJECT_SAVE)
        self.Bind(wx.EVT_MENU, self.on_menu_project_saveas, id=ID_PROJECT_SAVEAS)
        mb.Append(project_menu, "Project")
        # Menu Help
        help_menu = wx.Menu()
        help_menu.Append(ID_ABOUT, "About...")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_ABOUT)
        mb.Append(help_menu,    "Help")
        
        


        # Status Bar
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("", 1)

        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))



        self._mgr.AddPane(self.create_project_ctrl(), wx.aui.AuiPaneInfo().
                          Name("project").Caption("Project").
                          Left().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))


        self._mgr.AddPane(self.create_log_ctrl(), wx.aui.AuiPaneInfo().
                          Name("log").Caption("Log").
                          Bottom().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))


        self._mgr.AddPane(self.create_tool_ctrl(), wx.aui.AuiPaneInfo().Name("mdi").
                          CenterPane())

        self._mgr.AddPane(self.create_toolbar_ctrl(), wx.aui.AuiPaneInfo().
                          Name("tb").Caption("Toolbar").
                          ToolbarPane().Top().Row(1).
                          LeftDockable(False).RightDockable(False))


        # make some default perspectives

        self._mgr.GetPane("tbvert").Hide()

        perspective_all = self._mgr.SavePerspective()

        all_panes = self._mgr.GetAllPanes()

        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()


        self._mgr.GetPane("project").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("log").Show().Bottom().Layer(0).Row(0).Position(0)


        perspective_default = self._mgr.SavePerspective()

        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

        self._mgr.GetPane("project").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("log").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("mdi").Show()

        perspective_vert = self._mgr.SavePerspective()

        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(perspective_vert)


        # "commit" all changes made to FrameManager
        self._mgr.Update()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show How To Use The Closing Panes Event
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)



        self.Bind(wx.EVT_MENU, self.OnExit,     id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout,    id=ID_ABOUT)


        self.Maximize()

        self.log_info("Application is ready")





    def log_info(self, data):
        evt = frm_logging.EventTrace.create_info(data)
        self.ctrl["log"].AddPendingEvent(evt)

    def log_debug(self, data):
        if TRACE_DEBUG :
            evt = frm_logging.EventTrace.create_debug(data)
            self.ctrl["log"].AddPendingEvent(evt)

    def log_error(self, data):
        evt = frm_logging.EventTrace.create_error(data)
        self.ctrl["log"].AddPendingEvent(evt)


    def on_run_script(self, event):

        slist = event.slist
        config = event.config

        self.log_info("Run %d script(s)" % len(slist))

        self.log_debug("Base path : \"%s\"" % config[frm_controler.BASE_PATH])
        for s in slist:
            self.log_debug(s.str_relative())

            
        config[frm_controler.SCRIPT_LIST]   = slist
        config[frm_controler.CONFIG]        = None
        config[frm_controler.RUN_TYPE]      = frm_controler.RUN_SCRIPT
        
        # Create runner
        style=frm_controler.STYLE_AUTO_START_CLOSE
        dlg = frm_controler.DialogRunner(config, style, None, -1, "")
        dlg.set_log(self)
        dlg.ShowModal()
        ret = dlg.GetReturnCode()
        if    ret == frm_controler.RET_CODE_OK :
            self.log_info("Running scripts success")
        elif  ret == frm_controler.RET_CODE_ERROR :
            self.log_error("Running scripts error")
        elif ret == frm_controler.RET_CODE_USER_ABORT :
            self.log_error("Running scripts user abortion")
        else :
            assert False
        
        res = dlg.get_result()
        res.save(self.path["stack_file"])

        dlg.Destroy()
        
        # update view
        self.ctrl["res_sta"].update_res(res)




    def on_run_doc(self, event):

        slist = event.slist
        config = event.config

        self.log_info("Run %d script(s)" % len(slist))

        self.log_debug("Base path : \"%s\"" % config[frm_controler.BASE_PATH])
        for s in slist:
            self.log_debug(s.str_relative())

        config[frm_controler.SCRIPT_LIST]   = slist
        config[frm_controler.CONFIG]        = None
        config[frm_controler.RUN_TYPE]      = frm_controler.RUN_DOC
        
        # Create runner
        style=frm_controler.STYLE_AUTO_START_CLOSE
        dlg = frm_controler.DialogRunner(config, style, None, -1, "")
        dlg.set_log(self)
        dlg.ShowModal()
        ret = dlg.GetReturnCode()
        if    ret == frm_controler.RET_CODE_OK :
            self.log_info("Gen doc success")
        elif  ret == frm_controler.RET_CODE_ERROR :
            self.log_error("Gen doc error")
        elif ret == frm_controler.RET_CODE_USER_ABORT :
            self.log_error("Gen doc user abortion")
        else :
            assert False

        res = dlg.get_result()

        dlg.Destroy()




    def on_file_view(self, event):

        if    event.view == evt_file.VIEW_EDITOR_PY :
            self.log_debug("evt_file.VIEW_EDITOR_PY")
            self.create_view_editor_py(event.path)
        elif  event.view == evt_file.VIEW_EDITOR_TXT :
            self.log_debug("evt_file.VIEW_EDITOR_TXT")
        elif  event.view == evt_file.VIEW_RESULT :
            self.log_debug("evt_file.VIEW_RESULT")
        else:
            assert False


    def create_view_editor_py(self, path):

        # read file
        try:
            import codecs
            fileObj = codecs.open( path, "r", "utf-8" )
            t = fileObj.read()
        except Exception, exc :
            self.log_error("Error reading File : %s" % path)
            self.log_debug("Exception : %s" % exc.__str__())
            wx.MessageBox("Error reading File : %s" % path)
            return

        ctrl = self.ctrl["mdi"]
        page = editor_py.Editor_py(ctrl, -1, style = wx.FULL_REPAINT_ON_RESIZE)
        page.SetText(t)

        s_absolutepath, filename, ext = data.utils.split_fullpath(path)
        ctrl.AddPage(page, "%s.%s" % (filename, ext))




    def OnPaneClose(self, event):
        assert False
#        caption = event.GetPane().caption
#
#        if caption in ["Tree Pane", "Dock Manager Settings", "Fixed Pane"]:
#            msg = "Are You Sure You Want To Close This Pane?"
#            dlg = wx.MessageDialog(self, msg, "AUI Question",
#                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
#
#            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
#                event.Veto()
#            dlg.Destroy()


    def OnClose(self, event):
        self.log_debug("OnClose")
        
        
        msg = "Are you sure you want to close application"
        dlg = wx.MessageDialog(self, msg, self.GetTitle(),
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        ret = dlg.ShowModal()
        dlg.Destroy() 
        
        if ret in [wx.ID_NO, wx.ID_CANCEL]:
            return
        else:
            self.ctrl["project"].finish()
            self._mgr.UnInit()
            del self._mgr
            self.Destroy()


    def OnExit(self, event):
        self.log_debug("OnExit")
        self.Close()

    def OnAbout(self, event):
        self.log_debug("OnAbout")
        
        from wx.lib.wordwrap import wordwrap
        import platform
        import pytestemb

        description = "Control Test is a script manager\n"
        description += "\n PyTestEmb-version : %s\n" % pytestemb.VERSION_STRING
        description += "\n WX-version : %s" % wx.VERSION_STRING
        description += "\n WX-plateform : %s" % wx.Platform
        description += "\n Python-version : %s" % platform.python_version()
        description += "\n Plateform : %s" % platform.platform(terse=True)
        description += "\n"
        
        info = wx.AboutDialogInfo()
        info.Name = APP_NAME
        info.Version = APP_VERSION
        info.Copyright = "GNU GENERAL PUBLIC LICENSE v3"
        info.Description = wordwrap(description, 350, wx.ClientDC(self))
        info.WebSite = ("http://developer.berlios.de/projects/pytestemb/", "berlios home page")
        info.Developers = [ "Jean-Marc Beguinet" ]
        
        licenseText = "GNU GENERAL PUBLIC LICENSE v3\n"
        licenseText += "Please report to :\n"
        licenseText += "http://www.gnu.org/licenses/licenses.html"
        info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        wx.AboutBox(info)
        


    def on_menu_project_open(self, event):
        self.log_debug("on_menu_project_open")
        self.ctrl["project"].open_and_load_xml()

    def on_menu_project_new(self, event):
        self.log_debug("on_menu_project_new")
        dlg = wx.MessageDialog(self, "To do", 'To Do', wx.OK|wx.ICON_EXCLAMATION )
        ret = dlg.ShowModal()
        dlg.Destroy()
        #self.ctrl["project"].new_project()
                
    def on_menu_project_save(self, event):
        self.log_debug("on_menu_project_save")
        self.ctrl["project"].save_xml()
                
    def on_menu_project_saveas(self, event):
        self.log_debug("on_menu_project_saveas")
        dlg = wx.MessageDialog(self, "To do", 'To Do', wx.OK|wx.ICON_EXCLAMATION )
        ret = dlg.ShowModal()
        dlg.Destroy()

    def GetDockArt(self):
        return self._mgr.GetArtProvider()

    def DoUpdate(self):
        self._mgr.Update()

    def OnEraseBackground(self, event):
        event.Skip()


    def OnSize(self, event):
        event.Skip()



    def GetStartPosition(self):
        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))
        return wx.Point(pt.x + x, pt.y + x)


    def OnChangeContentPane(self, event):
#        self._mgr.GetPane("grid_content").Show(event.GetId() == ID_GridContent)
#        self._mgr.GetPane("log_content").Show(event.GetId() == ID_LogContent)
#        self._mgr.GetPane("tree_content").Show(event.GetId() == ID_TreeContent)
        self._mgr.Update()



    def create_log_ctrl(self):
        ctrl = frm_logging.LoggingFrame(self, -1, wx.Point(0, 0), wx.Size(150, 100) )
        self.ctrl["log"] = ctrl
        return ctrl

    def create_project_ctrl(self):
        ctrl = frm_project.ProjectFrame(self.wxconf, self, -1, wx.Point(0, 0), wx.Size(500, 500) )
        ctrl.set_log(self)
        self.ctrl["project"] = ctrl
        return ctrl




    def create_tool_ctrl(self):

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        self.Freeze()

        # Main FlatNoteBook
        bookStyle = fnb.FNB_ALLOW_FOREIGN_DND
        bookStyle |= fnb.FNB_NO_X_BUTTON
        bookStyle |= fnb.FNB_NODRAG
        ctrl = fnb.FlatNotebook(self, wx.ID_ANY, style=bookStyle)

        
        # Global result view
        res_glo = frm_results.ResultFrame("Global", ctrl)
        res_glo.set_log(self)
        res_glo.path = self.path["global_file"]
        self.ctrl["res_glo"] = res_glo
        ctrl.AddPage(res_glo, "Global Result")

        # Stack result view
        res_sta = frm_results.ResultFrame( "Stack",ctrl)
        res_sta.set_log(self)
        res_sta.add_result_dest(res_glo)
        self.ctrl["res_sta"] = res_sta
        ctrl.AddPage(res_sta    ,  "Stack Result")

        # Document AuiNoteBook
        _style = wx.DEFAULT_FRAME_STYLE
        mdi = wx.aui.AuiNotebook(self, -1, size=(640,480), style=_style, pos=wx.DefaultPosition) 
        self.ctrl["mdi"] = mdi
        ctrl.AddPage(mdi,  "Document")

        self.Thaw()
        #mainSizer.Layout()
        self.SendSizeEvent()
        
        self.ctrl["fnb"] = ctrl
        return ctrl


    def create_toolbar_ctrl(self):
        
        tsize = wx.Size(16,16)
        bmp_new     = wx.ArtProvider.GetBitmap(wx.ART_NEW,          wx.ART_TOOLBAR, tsize)
        bmp_save    = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,    wx.ART_TOOLBAR, tsize)
        bmp_saveas  = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
        bmp_open    = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,    wx.ART_TOOLBAR, tsize)
        
        toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        toolbar.SetToolBitmapSize(tsize)

        toolbar.AddLabelTool(ID_PROJECT_NEW,   "New",      bmp_new)
        toolbar.AddLabelTool(ID_PROJECT_OPEN,  "Open",     bmp_open)
        toolbar.AddLabelTool(ID_PROJECT_SAVE,  "Save",     bmp_save)
        toolbar.AddLabelTool(ID_PROJECT_SAVEAS,"SaveAs",   bmp_saveas)
        toolbar.AddSeparator()
    
        toolbar.SetToolShortHelp(ID_PROJECT_NEW,       "New project")
        toolbar.SetToolShortHelp(ID_PROJECT_OPEN,      "Open project")
        toolbar.SetToolShortHelp(ID_PROJECT_SAVE,      "Save project")
        toolbar.SetToolShortHelp(ID_PROJECT_SAVEAS,    "Save As project")
        
        toolbar.Realize()
        return toolbar





class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = PyAUIFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        return 1




if __name__ == "__main__":

    if not(EXCEPT_DEBUG) :
        exceptlog.add_exception_hook(get_app_path(), APP_VERSION, __email__)

    App = MyApp(0)
    App.MainLoop()



