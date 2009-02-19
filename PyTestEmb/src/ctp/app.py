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
import wx.grid
import wx.html
import wx.aui


ID_CreateTree = wx.NewId()
ID_CreateGrid = wx.NewId()
ID_CreateText = wx.NewId()
ID_CreateHTML = wx.NewId()
ID_CreateSizeReport = wx.NewId()
ID_GridContent = wx.NewId()
ID_TextContent = wx.NewId()
ID_TreeContent = wx.NewId()
ID_HTMLContent = wx.NewId()
ID_SizeReportContent = wx.NewId()
ID_CreatePerspective = wx.NewId()
ID_CopyPerspective = wx.NewId()

ID_TransparentHint = wx.NewId()
ID_VenetianBlindsHint = wx.NewId()
ID_RectangleHint = wx.NewId()
ID_NoHint = wx.NewId()
ID_HintFade = wx.NewId()
ID_AllowFloating = wx.NewId()
ID_NoVenetianFade = wx.NewId()
ID_TransparentDrag = wx.NewId()
ID_AllowActivePane = wx.NewId()
ID_NoGradient = wx.NewId()
ID_VerticalGradient = wx.NewId()
ID_HorizontalGradient = wx.NewId()

ID_Settings = wx.NewId()
ID_About = wx.NewId()
ID_FirstPerspective = ID_CreatePerspective+1000







class PyAUIFrame(wx.Frame):
    
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        
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

        view_menu = wx.Menu()
        view_menu.Append(ID_CreateText, "Create Text Control")
        view_menu.Append(ID_CreateHTML, "Create HTML Control")
        view_menu.Append(ID_CreateTree, "Create Tree")
        view_menu.Append(ID_CreateGrid, "Create Grid")
        view_menu.Append(ID_CreateSizeReport, "Create Size Reporter")
        view_menu.AppendSeparator()
        view_menu.Append(ID_GridContent, "Use a Grid for the Content Pane")
        view_menu.Append(ID_TextContent, "Use a Text Control for the Content Pane")
        view_menu.Append(ID_HTMLContent, "Use an HTML Control for the Content Pane")
        view_menu.Append(ID_TreeContent, "Use a Tree Control for the Content Pane")
        view_menu.Append(ID_SizeReportContent, "Use a Size Reporter for the Content Pane")    
           
        options_menu = wx.Menu()
        options_menu.AppendRadioItem(ID_TransparentHint, "Transparent Hint")
        options_menu.AppendRadioItem(ID_VenetianBlindsHint, "Venetian Blinds Hint")
        options_menu.AppendRadioItem(ID_RectangleHint, "Rectangle Hint")
        options_menu.AppendRadioItem(ID_NoHint, "No Hint")
        options_menu.AppendSeparator();
        options_menu.AppendCheckItem(ID_HintFade, "Hint Fade-in")
        options_menu.AppendCheckItem(ID_AllowFloating, "Allow Floating")
        options_menu.AppendCheckItem(ID_NoVenetianFade, "Disable Venetian Blinds Hint Fade-in")
        options_menu.AppendCheckItem(ID_TransparentDrag, "Transparent Drag")
        options_menu.AppendCheckItem(ID_AllowActivePane, "Allow Active Pane")
        options_menu.AppendSeparator();
        options_menu.AppendRadioItem(ID_NoGradient, "No Caption Gradient")
        options_menu.AppendRadioItem(ID_VerticalGradient, "Vertical Caption Gradient")
        options_menu.AppendRadioItem(ID_HorizontalGradient, "Horizontal Caption Gradient")
        options_menu.AppendSeparator();
        options_menu.Append(ID_Settings, "Settings Pane")

        self._perspectives_menu = wx.Menu()
        self._perspectives_menu.Append(ID_CreatePerspective, "Create Perspective")
        self._perspectives_menu.Append(ID_CopyPerspective, "Copy Perspective Data To Clipboard")
        self._perspectives_menu.AppendSeparator()
        self._perspectives_menu.Append(ID_FirstPerspective+0, "Default Startup")
        self._perspectives_menu.Append(ID_FirstPerspective+1, "All Panes")
        self._perspectives_menu.Append(ID_FirstPerspective+2, "Vertical Toolbar")

        help_menu = wx.Menu()
        help_menu.Append(ID_About, "About...")
        
        mb.Append(file_menu, "File")
        mb.Append(view_menu, "View")
        mb.Append(self._perspectives_menu, "Perspectives")
        mb.Append(options_menu, "Options")
        mb.Append(help_menu, "Help")
        
        self.SetMenuBar(mb)

        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("Welcome To wxPython!", 1)

        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))

        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(48,48))
        tb1.AddLabelTool(101, "Test", wx.ArtProvider_GetBitmap(wx.ART_ERROR))
        tb1.AddSeparator()
        tb1.AddLabelTool(102, "Test", wx.ArtProvider_GetBitmap(wx.ART_QUESTION))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_WARNING))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.Realize()

        tb2 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb2.SetToolBitmapSize(wx.Size(16,16))
        tb2_bmp1 = wx.ArtProvider_GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddSeparator()
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddSeparator()
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.AddLabelTool(101, "Test", tb2_bmp1)
        tb2.Realize()
 

        # add a bunch of panes
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test1").Caption("Pane Caption").Top().
                          CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test2").Caption("Client Size Reporter").
                          Bottom().Position(1).CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test3").Caption("Client Size Reporter").
                          Bottom().CloseButton(True).MaximizeButton(True))
     
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test4").Caption("Pane Caption").
                          Left().CloseButton(True).MaximizeButton(True))
                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test5").Caption("Pane Caption").
                          Right().CloseButton(True).MaximizeButton(True))
                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test6").Caption("Client Size Reporter").
                          Right().Row(1).CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test7").Caption("Client Size Reporter").
                          Left().Layer(1).CloseButton(True).MaximizeButton(True))
                      
        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().
                          Name("test8").Caption("Tree Pane").
                          Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test9").Caption("Min Size 200x100").
                          BestSize(wx.Size(200,100)).MinSize(wx.Size(200,100)).
                          Bottom().Layer(1).CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().
                          Name("test10").Caption("Text Pane").
                          Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
                                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test11").Caption("Fixed Pane").
                          Bottom().Layer(1).Position(2).Fixed().CloseButton(True).MaximizeButton(True))



        # create some center panes

        self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().Name("grid_content").
                          CenterPane().Hide())

        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().Name("tree_content").
                          CenterPane().Hide())
                      
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().Name("sizereport_content").
                          CenterPane().Hide())

        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().Name("text_content").
                          CenterPane().Hide())
        
        self._mgr.AddPane(self.Create_MDI(), wx.aui.AuiPaneInfo().Name("html_content").
                          CenterPane())        

                                
        # add the toolbars to the manager
                        
        self._mgr.AddPane(tb1, wx.aui.AuiPaneInfo().
                          Name("tb1").Caption("Big Toolbar").
                          ToolbarPane().Top().
                          LeftDockable(False).RightDockable(False))

        self._mgr.AddPane(tb2, wx.aui.AuiPaneInfo().
                          Name("tb2").Caption("Toolbar 2").
                          ToolbarPane().Top().Row(1).
                          LeftDockable(False).RightDockable(False))
                      
 
                      
        self._mgr.AddPane(wx.Button(self, -1, "Test Button"),
                          wx.aui.AuiPaneInfo().Name("tb5").
                          ToolbarPane().Top().Row(2).Position(1).
                          LeftDockable(False).RightDockable(False))

        # make some default perspectives

        self._mgr.GetPane("tbvert").Hide()
        
        perspective_all = self._mgr.SavePerspective()
        
        all_panes = self._mgr.GetAllPanes()
        
        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()
                
        self._mgr.GetPane("tb1").Hide()
        self._mgr.GetPane("tb5").Hide()
        self._mgr.GetPane("test8").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("test10").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("html_content").Show()

        perspective_default = self._mgr.SavePerspective()

        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

        self._mgr.GetPane("tb1").Hide()
        self._mgr.GetPane("tb5").Hide()
        self._mgr.GetPane("tbvert").Show()
        self._mgr.GetPane("grid_content").Show()
        self._mgr.GetPane("test8").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("test10").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("html_content").Show()

        perspective_vert = self._mgr.SavePerspective()
        
        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(perspective_vert)

        self._mgr.GetPane("tbvert").Hide()
        self._mgr.GetPane("grid_content").Hide()

        # "commit" all changes made to FrameManager   
        self._mgr.Update()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show How To Use The Closing Panes Event
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        
        self.Bind(wx.EVT_MENU, self.OnCreateTree, id=ID_CreateTree)
        self.Bind(wx.EVT_MENU, self.OnCreateGrid, id=ID_CreateGrid)
        self.Bind(wx.EVT_MENU, self.OnCreateText, id=ID_CreateText)
        
        self.Bind(wx.EVT_MENU, self.OnCreateSizeReport, id=ID_CreateSizeReport)
        self.Bind(wx.EVT_MENU, self.OnCreatePerspective, id=ID_CreatePerspective)
        self.Bind(wx.EVT_MENU, self.OnCopyPerspective, id=ID_CopyPerspective)

        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowFloating)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_RectangleHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_HintFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentDrag)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowActivePane)
        
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_NoGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_VerticalGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_HorizontalGradient)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=ID_Settings)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_GridContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_TreeContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_TextContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_SizeReportContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_HTMLContent)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)

        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_RectangleHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HintFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowFloating)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentDrag)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowActivePane)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VerticalGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HorizontalGradient)

    
        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective,
                  id2=ID_FirstPerspective+1000)


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

        msg = "wx.aui Demo\n" + \
              "An advanced window management library for wxWidgets\n" + \
              "(c) Copyright 2005-2006, Kirix Corporation"
        dlg = wx.MessageDialog(self, msg, "About wx.aui Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()        


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


    def OnGradient(self, event):

        gradient = 0

        if event.GetId() == ID_NoGradient:
            gradient = wx.aui.AUI_GRADIENT_NONE
        elif event.GetId() == ID_VerticalGradient:
            gradient = wx.aui.AUI_GRADIENT_VERTICAL
        elif event.GetId() == ID_HorizontalGradient:
            gradient = wx.aui.AUI_GRADIENT_HORIZONTAL

        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE, gradient)
        self._mgr.Update()


    def OnManagerFlag(self, event):

        flag = 0
        eid = event.GetId()

        if eid in [ ID_TransparentHint, ID_VenetianBlindsHint, ID_RectangleHint, ID_NoHint ]:
            flags = self._mgr.GetFlags()
            flags &= ~wx.aui.AUI_MGR_TRANSPARENT_HINT
            flags &= ~wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
            flags &= ~wx.aui.AUI_MGR_RECTANGLE_HINT
            self._mgr.SetFlags(flags)

        if eid == ID_AllowFloating:
            flag = wx.aui.AUI_MGR_ALLOW_FLOATING
        elif eid == ID_TransparentDrag:
            flag = wx.aui.AUI_MGR_TRANSPARENT_DRAG
        elif eid == ID_HintFade:
            flag = wx.aui.AUI_MGR_HINT_FADE
        elif eid == ID_NoVenetianFade:
            flag = wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        elif eid == ID_AllowActivePane:
            flag = wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE
        elif eid == ID_TransparentHint:
            flag = wx.aui.AUI_MGR_TRANSPARENT_HINT
        elif eid == ID_VenetianBlindsHint:
            flag = wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
        elif eid == ID_RectangleHint:
            flag = wx.aui.AUI_MGR_RECTANGLE_HINT
        
        self._mgr.SetFlags(self._mgr.GetFlags() ^ flag)


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

                


    def OnCreatePerspective(self, event):

        dlg = wx.TextEntryDialog(self, "Enter a name for the new perspective:", "AUI Test")
        
        dlg.SetValue(("Perspective %d")%(len(self._perspectives)+1))
        if dlg.ShowModal() != wx.ID_OK:
            return
        
        if len(self._perspectives) == 0:
            self._perspectives_menu.AppendSeparator()
        
        self._perspectives_menu.Append(ID_FirstPerspective + len(self._perspectives), dlg.GetValue())
        self._perspectives.append(self._mgr.SavePerspective())


    def OnCopyPerspective(self, event):

        s = self._mgr.SavePerspective()
        
        if wx.TheClipboard.Open():
        
            wx.TheClipboard.SetData(wx.TextDataObject(s))
            wx.TheClipboard.Close()
        
    def OnRestorePerspective(self, event):

        self._mgr.LoadPerspective(self._perspectives[event.GetId() - ID_FirstPerspective])


    def GetStartPosition(self):

        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))
        
        return wx.Point(pt.x + x, pt.y + x)


    def OnCreateTree(self, event):
        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Tree Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(150, 300)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateGrid(self, event):
        self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().
                          Caption("Grid").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()



    def OnCreateText(self, event):
        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Text Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateSizeReport(self, event):
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Client Size Reporter").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnChangeContentPane(self, event):

        self._mgr.GetPane("grid_content").Show(event.GetId() == ID_GridContent)
        self._mgr.GetPane("text_content").Show(event.GetId() == ID_TextContent)
        self._mgr.GetPane("tree_content").Show(event.GetId() == ID_TreeContent)
        self._mgr.GetPane("sizereport_content").Show(event.GetId() == ID_SizeReportContent)
        self._mgr.GetPane("html_content").Show(event.GetId() == ID_HTMLContent)
        self._mgr.Update()


    def CreateTextCtrl(self):

        text = ("This is text box %d")%(self.n + 1)

        return wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)



    def CreateGrid(self):

        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),
                            wx.NO_BORDER | wx.WANTS_CHARS)
        
        grid.CreateGrid(50, 20)

        return grid


    def CreateTreeCtrl(self):

        tree = wx.GenericDirCtrl(self, -1,  size=(160, 250), style=wx.DIRCTRL_SHOW_FILTERS,
                                filter="All files (*.*)|*.*|Python files (*.py)|*.py")

#        tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
#                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        
        return tree


    def CreateSizeReportCtrl(self, width=80, height=80):

        ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition,
                              wx.Size(width, height), self._mgr)
        return ctrl


    def Create_MDI(self):
        ctrl = wx.aui.AuiNotebook(self, -1,  size=(640,480),\
                                          style=wx.DEFAULT_FRAME_STYLE, pos=wx.DefaultPosition  )
        
        page = wx.TextCtrl(ctrl, -1, "", style=wx.TE_MULTILINE)
        ctrl.AddPage(page, "Welcome0")
        
#        
#        import pyeditor
#        page = pyeditor.PythonSTC(ctrl, -1, style = wx.NO_FULL_REPAINT_ON_RESIZE)
#
#        ctrl.AddPage(page, "Welcome1")      
#        
#        
        
                      
        return ctrl



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
    




#----------------------------------------------------------------------

#class TestPanel(wx.Panel):
#    def __init__(self, parent, log):
#        self.log = log
#        wx.Panel.__init__(self, parent, -1)
#        b = wx.Button(self, -1, "Show the wx.aui Demo Frame", (50,50))
#        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
#
#    def OnButton(self, evt):
#        frame = PyAUIFrame(self, wx.ID_ANY, "wx.aui wxPython Demo", size=(750, 590))
#        frame.Show()
#
##----------------------------------------------------------------------
#
#def runTest(frame, nb, log):
#    win = TestPanel(nb, log)
#    return win

#----------------------------------------------------------------------





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



