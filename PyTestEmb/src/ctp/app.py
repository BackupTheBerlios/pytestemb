# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.3 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"


import wx
import wx.grid
import wx.html
import wx.aui


import wxcustom.evt_file as evt_file
import wxcustom.editor_py as editor_py

import frm_logging
import frm_project
import frm_results




TRACE_DEBUG = True


ID_MENU_PROJECT_OPEN = wx.NewId()
ID_MENU_PROJECT_REFRESH = wx.NewId()









ID_CreateTree = wx.NewId()
#ID_CreateGrid = wx.NewId()
ID_CreateLog = wx.NewId()
#ID_GridContent = wx.NewId()
ID_LogContent = wx.NewId()
ID_TreeContent = wx.NewId()
ID_SizeReportContent = wx.NewId()
ID_CreatePerspective = wx.NewId()
ID_CopyPerspective = wx.NewId()


ID_Settings = wx.NewId()
ID_About = wx.NewId()
ID_FirstPerspective = ID_CreatePerspective+1000









class PyAUIFrame(wx.Frame):
    
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        
        
 
        self.ctrl = { "log"     :     None,
                      "project" :     None,
                      "result"  :     None,
                      "mdi"    :      None,}

        
    
        evt_file.EVT_CUSTOM_FILE_VIEW(self, self.on_file_view)
        
        
        self.SetTitle("Control Test - PyTestEmb")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("images/Crystal_Clear_action_run.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)       
        
        
        
        
        
        
        
        
        # tell FrameManager to manage this frame        
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        
        self._perspectives = []
        self.n = 0
        self.x = 0
        

        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

        project_menu = wx.Menu()
        project_menu.Append(ID_MENU_PROJECT_OPEN,     "Open ...")
        project_menu.Append(ID_MENU_PROJECT_REFRESH,  "Refresh")
        self.Bind(wx.EVT_MENU, self.on_menu_project_open, id=ID_MENU_PROJECT_OPEN)
        self.Bind(wx.EVT_MENU, self.on_menu_refresh, id=ID_MENU_PROJECT_REFRESH)
    
           
           
        help_menu = wx.Menu()
        help_menu.Append(ID_About, "About...")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)      
        
        
        mb.Append(file_menu,    "File")
        mb.Append(project_menu, "Project")
        mb.Append(help_menu,    "Help")
        
        
        
        
        
        
        
        
        
        
        
        
        
        self.SetMenuBar(mb)

        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("Welcome To wxPython!", 1)

        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))



        tb2 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb2.SetToolBitmapSize(wx.Size(16,16))
        tb2_bmp1 = wx.ArtProvider_GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.Realize()
 

                      
        self._mgr.AddPane(self.CreateProjectCtrl(), wx.aui.AuiPaneInfo().
                          Name("project").Caption("Project").
                          Left().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))
                      

        self._mgr.AddPane(self.CreateLogCtrl(), wx.aui.AuiPaneInfo().
                          Name("log").Caption("Log").
                          Bottom().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))

                
        
        self._mgr.AddPane(self.Create_MDI(), wx.aui.AuiPaneInfo().Name("mdi").
                          CenterPane())     




        self._mgr.AddPane(tb2, wx.aui.AuiPaneInfo().
                          Name("tb2").Caption("Toolbar 2").
                          ToolbarPane().Top().Row(1).
                          LeftDockable(False).RightDockable(False))


        # make some default perspectives

        self._mgr.GetPane("tbvert").Hide()
        
        perspective_all = self._mgr.SavePerspective()
        
        all_panes = self._mgr.GetAllPanes()
        
        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()
                
#        self._mgr.GetPane("tb1").Hide()
#        self._mgr.GetPane("tb5").Hide()
        self._mgr.GetPane("project").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("log").Show().Bottom().Layer(0).Row(0).Position(0)


        perspective_default = self._mgr.SavePerspective()

        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

#        self._mgr.GetPane("tb1").Hide()
#        self._mgr.GetPane("tb5").Hide()
#        self._mgr.GetPane("tbvert").Show()
#        self._mgr.GetPane("grid_content").Show()

        self._mgr.GetPane("project").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("log").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("mdi").Show()

        perspective_vert = self._mgr.SavePerspective()
        
        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(perspective_vert)

#        self._mgr.GetPane("tbvert").Hide()
#        self._mgr.GetPane("grid_content").Hide()

        # "commit" all changes made to FrameManager   
        self._mgr.Update()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show How To Use The Closing Panes Event
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        


        

        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)



    
        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective,
                  id2=ID_FirstPerspective+1000)
        
    
        self.log_info("Application is ready")
        
        
    def log_info(self, data):
        evt = frm_logging.EventTrace.create_info(data)
        self.ctrl["log"].AddPendingEvent(evt)

    def log_debug(self, data):
        if TRACE_DEBUG :
            evt = frm_logging.EventTrace.create_debug(data)
            self.ctrl["log"].AddPendingEvent(evt)





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
        except :
            wx.MessageBox("Error reading File : %s" % path)
            return
            
        
        ctrl = self.ctrl["mdi"]
        page = editor_py.Editor_py(ctrl, -1, style = wx.NO_FULL_REPAINT_ON_RESIZE)
        page.SetText(t)
        ctrl.AddPage(page, "PyEditor")




    def OnPaneClose(self, event):

        caption = event.GetPane().caption

        if caption in ["Tree Pane", "Dock Manager Settings", "Fixed Pane"]:
            msg = "Are You Sure You Want To Close This Pane?"
            dlg = wx.MessageDialog(self, msg, "AUI Question",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                event.Veto()
            dlg.Destroy()
        

    def OnClose(self, event):
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()


    def OnExit(self, event):
        self.Close()

    def OnAbout(self, event):
        self.log_debug("OnAbout")
        msg = "Beta"
        dlg = wx.MessageDialog(self, msg, "About Control Tower PytestEmb",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()        


    def on_menu_project_open(self, event):
        self.log_debug("on_menu_project_open")
        self.ctrl["project"].open_and_load_xml()
    
    
    def on_menu_refresh(self, event):
        self.log_debug("on_menu_refresh")
        self.ctrl["project"].refresh_xml()


  
        

    def GetDockArt(self):

        return self._mgr.GetArtProvider()


    def DoUpdate(self):

        self._mgr.Update()


    def OnEraseBackground(self, event):

        event.Skip()


    def OnSize(self, event):

        event.Skip()


    def OnSettings(self, event):

        # show the settings pane, and float it
        floating_pane = self._mgr.GetPane("settings").Float().Show()

        if floating_pane.floating_pos == wx.DefaultPosition:
            floating_pane.FloatingPosition(self.GetStartPosition())

        self._mgr.Update()



    def OnUpdateUI(self, event):

        flags = self._mgr.GetFlags()
        eid = event.GetId()
        
        if eid == ID_NoGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_NONE)

        elif eid == ID_VerticalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_VERTICAL)

        elif eid == ID_HorizontalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_HORIZONTAL)

        elif eid == ID_AllowFloating:
            event.Check((flags & wx.aui.AUI_MGR_ALLOW_FLOATING) != 0)

        elif eid == ID_TransparentDrag:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_DRAG) != 0)

        elif eid == ID_TransparentHint:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_HINT) != 0)

        elif eid == ID_VenetianBlindsHint:
            event.Check((flags & wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT) != 0)

        elif eid == ID_RectangleHint:
            event.Check((flags & wx.aui.AUI_MGR_RECTANGLE_HINT) != 0)

        elif eid == ID_NoHint:
            event.Check(((wx.aui.AUI_MGR_TRANSPARENT_HINT |
                          wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT |
                          wx.aui.AUI_MGR_RECTANGLE_HINT) & flags) == 0)

        elif eid == ID_HintFade:
            event.Check((flags & wx.aui.AUI_MGR_HINT_FADE) != 0);

        elif eid == ID_NoVenetianFade:
            event.Check((flags & wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE) != 0);


        
    def OnRestorePerspective(self, event):

        self._mgr.LoadPerspective(self._perspectives[event.GetId() - ID_FirstPerspective])


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




    def CreateLogCtrl(self):
        ctrl = frm_logging.LoggingFrame(self, -1, wx.Point(0, 0), wx.Size(150, 90) )
        self.ctrl["log"] = ctrl
        return ctrl

    def CreateProjectCtrl(self):
        ctrl = frm_project.ProjectFrame(self, -1, wx.Point(0, 0), wx.Size(300, 400) )
        ctrl.set_log(self)
        self.ctrl["project"] = ctrl
        return ctrl






    def Create_MDI(self):
        ctrl = wx.aui.AuiNotebook(self, -1,  size=(640,480),\
                                          style=wx.DEFAULT_FRAME_STYLE, pos=wx.DefaultPosition  )
        self.ctrl["mdi"] = ctrl
        return ctrl
        
#        page = wx.TextCtrl(ctrl, -1, "", style=wx.TE_MULTILINE)
#        
#        ctrl.AddPage(page, "Welcome0")
        
#        
#        import pyeditor
#        page = pyeditor.PythonSTC(ctrl, -1, style = wx.NO_FULL_REPAINT_ON_RESIZE)
#
#        ctrl.AddPage(page, "Welcome1")      
#        
#        
        
                      
        



# -- wx.SizeReportCtrl --
# (a utility control that always reports it's client size)

class SizeReportCtrl(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, mgr=None):

        wx.PyControl.__init__(self, parent, id, pos, size, wx.NO_BORDER)
            
        self._mgr = mgr

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        
        size = self.GetClientSize()
        s = ("Size: %d x %d")%(size.x, size.y)

        dc.SetFont(wx.NORMAL_FONT)
        w, height = dc.GetTextExtent(s)
        height = height + 3
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)
        dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2))
        
        if self._mgr:
        
            pi = self._mgr.GetPane(self)
            
            s = ("Layer: %d")%pi.dock_layer
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*1))
           
            s = ("Dock: %d Row: %d")%(pi.dock_direction, pi.dock_row)
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*2))
            
            s = ("Position: %d")%pi.dock_pos
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*3))
            
            s = ("Proportion: %d")%pi.dock_proportion
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*4))
        

    def OnEraseBackground(self, event):
        # intentionally empty
        pass        
    

    def OnSize(self, event):
    
        self.Refresh()
        event.Skip()
    

ID_PaneBorderSize = wx.ID_HIGHEST + 1
ID_SashSize = ID_PaneBorderSize + 1
ID_CaptionSize = ID_PaneBorderSize + 2
ID_BackgroundColor = ID_PaneBorderSize + 3
ID_SashColor = ID_PaneBorderSize + 4
ID_InactiveCaptionColor =  ID_PaneBorderSize + 5
ID_InactiveCaptionGradientColor = ID_PaneBorderSize + 6
ID_InactiveCaptionTextColor = ID_PaneBorderSize + 7
ID_ActiveCaptionColor = ID_PaneBorderSize + 8
ID_ActiveCaptionGradientColor = ID_PaneBorderSize + 9
ID_ActiveCaptionTextColor = ID_PaneBorderSize + 10
ID_BorderColor = ID_PaneBorderSize + 11
ID_GripperColor = ID_PaneBorderSize + 12
    









class MyApp(wx.App):        

    
    
    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = PyAUIFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        return 1







if __name__ == "__main__":

    # start app
    App = MyApp(0)
    App.MainLoop()    



