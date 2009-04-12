# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.11 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"





import wx

import data.results as dres




class ResultFrame(wx.Panel):
    def __init__(self, name, *p, **pp):

        wx.Panel.__init__(self, *p, **pp)

        self.tree = wx.TreeCtrl(self,-1)
        self.tree.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)

        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnItemMenu, self.tree)


        il = wx.ImageList(16, 16)
        self.im_script      = il.Add( wx.Bitmap("images/script.png", wx.BITMAP_TYPE_PNG))
        self.im_pool        = il.Add( wx.Bitmap("images/database.png", wx.BITMAP_TYPE_PNG))
        self.im_folder      = il.Add( wx.Bitmap("images/folder_database.png", wx.BITMAP_TYPE_PNG))
        self.im_project     = il.Add( wx.Bitmap("images/application_view_tile.png", wx.BITMAP_TYPE_PNG))

        self.im_script_ko   = il.Add( wx.Bitmap("images/script_delete.png", wx.BITMAP_TYPE_PNG))
        self.im_script_warn = il.Add( wx.Bitmap("images/script_error.png", wx.BITMAP_TYPE_PNG))
        self.im_script_ok   = il.Add( wx.Bitmap("images/script_go.png", wx.BITMAP_TYPE_PNG))

        self.im_result   = il.Add( wx.Bitmap("images/table_multiple.png", wx.BITMAP_TYPE_PNG))

        self.im_case_ok   = il.Add( wx.Bitmap("images/bullet_green.png", wx.BITMAP_TYPE_PNG))
        self.im_case_ko   = il.Add( wx.Bitmap("images/bullet_red.png", wx.BITMAP_TYPE_PNG))
        self.im_case   = il.Add( wx.Bitmap("images/bullet_purple.png", wx.BITMAP_TYPE_PNG))
        
        self.il = il
        self.tree.SetImageList(il)
        
        self.lst_res   = list()
        self.lst_dest  = list()
        self.sel_item  = None
        self.log       = None
        self.path      = None
        
        self.wildcard_dbm = "Project file (*.dbm)|*.dbm|All files (*.*)|*.*"
        self.wildcard_csv = "Csv file (*.csv)|*.csv|All files (*.*)|*.*"

        
        self.res = dres.Results(name)
        self.update()
        
        # toolbar
        tsize = (16,16)
        self.tb1 = wx.ToolBar(self, -1)
        self.tb1.SetToolBitmapSize(tsize)
        
        
        bmp_new = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        bmp_save = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        bmp_saveas = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
        bmp_open = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        bmp_export_csv = wx.Bitmap("images/page_white_c.png", wx.BITMAP_TYPE_PNG)
        id_new = wx.NewId()
        id_save = wx.NewId()
        id_saveas = wx.NewId()
        id_open = wx.NewId()
        id_export_csv = wx.NewId()
        
        
    
        self.tb1.AddLabelTool(id_new,       "New",          bmp_new,)
        self.tb1.AddSeparator()
        self.tb1.AddLabelTool(id_open,      "Open",         bmp_open)
        self.tb1.AddLabelTool(id_save,      "Save",         bmp_save)
        self.tb1.AddLabelTool(id_saveas,    "Save As",      bmp_saveas)
        self.tb1.AddSeparator()
        self.tb1.AddLabelTool(id_export_csv,"Export csv",   bmp_export_csv)
        
        
        self.tb1.SetToolShortHelp(id_new,       "New result")
        self.tb1.SetToolShortHelp(id_open,      "Open a result")
        self.tb1.SetToolShortHelp(id_save,      "Save curent result")
        self.tb1.SetToolShortHelp(id_saveas,    "Save As curent result")
        self.tb1.SetToolShortHelp(id_export_csv,"Export to csv")
        
        self.Bind(wx.EVT_TOOL, self.on_tool_new,    id=id_new)
        self.Bind(wx.EVT_TOOL, self.on_tool_open,   id=id_open)
        self.Bind(wx.EVT_TOOL, self.on_tool_save,   id=id_save)
        self.Bind(wx.EVT_TOOL, self.on_tool_saveas, id=id_saveas)
        self.Bind(wx.EVT_TOOL, self.on_tool_csv,    id=id_export_csv)

        
        self.tb1.Realize()



        # sizer
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.tb1, 0, wx.ALL, 2)
        sizer_1.Add(self.tree, 1, wx.ALL| wx.EXPAND, 2)

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        
        
        

    def set_log(self, log):
        self.log = log

    def log_debug(self, data):
        if self.log is not None :
            self.log.log_debug(data)

    def log_info(self, data):
        if self.log is not None :
            self.log.log_info(data)


    def on_tool_new(self, event):
        self.log_debug("on_tool_new")


    def on_tool_open(self, event):
        self.log_debug("on_tool_open")

        self.load_and_update()
        
        
    def on_tool_save(self, event):
        self.log_debug("on_tool_save")
        
        self.res.save(self.path)
        
        
    def on_tool_saveas(self, event):
        self.log_debug("on_tool_saveas")
        dlg = wx.MessageDialog(self, "To do", 'To Do', wx.OK | wx.ICON_EXCLAMATION )
        ret = dlg.ShowModal()
        dlg.Destroy()
               
    def on_tool_csv(self, event):
        self.log_debug("on_tool_csv")     
        self.save_export_csv()
        

    def add_result_dest(self, resultframe):

        if len(self.lst_dest) < 2 :
            self.lst_dest.append((resultframe.res.name, resultframe))
        else :
            raise Exception("Result dest limit to 2")


    def remove_result_dest(self, name):
        for i,v in enumerate(self.lst_dest):
            if v[0] == name:
                del self.lst_dest[i]


    def update_in_dest(self, script_res, name):
        for i,v in enumerate(self.lst_dest):
            if v[0] == name:
                v[1].res.update(script_res)
                v[1].update()



    def OnItemMenu(self, event):
        type = ["root", "script", "info"]
        item = event.GetItem()
        self.log_debug("OnItemMenu item=\"%s\"" % self.tree.GetItemText(item))

        self.sel_item = item

        node = self.tree.GetItemPyData(self.sel_item)

        if node is None :
            self.sel_item = None
            return
        if type.count(node["type"]) != 1:
            self.sel_item = None

        menu = wx.Menu()
        if      node["type"] == "root" :
            item1 = menu.Append(wx.ID_ANY, "Export csv ...")
            self.Bind(wx.EVT_MENU, self.on_export_csv,      item1)

            if len(self.lst_dest) > 0 :
                sm = wx.Menu()
                for k in self.lst_dest:
                    itemA = sm.Append(wx.ID_ANY, k[0])
                    self.Bind(wx.EVT_MENU, self.on_update_all_result,      itemA)
                menu.AppendSeparator()
                menu.AppendMenu(wx.ID_ANY, "Update all results ...", sm)

        elif    node["type"] == "script" :
            item1 = menu.Append(wx.ID_ANY, "Remove")
            self.Bind(wx.EVT_MENU, self.on_remove_result,      item1)

            if len(self.lst_dest) > 0 :
                sm = wx.Menu()
                for k in self.lst_dest:
                    itemA = sm.Append(wx.ID_ANY, k[0])
                    self.Bind(wx.EVT_MENU, self.on_update_result,      itemA)
                menu.AppendSeparator()
                menu.AppendMenu(wx.ID_ANY, "Update result ...", sm)


        elif    node["type"] == "info" :
            return
        else:
            assert False
        self.PopupMenu(menu)
        menu.Destroy()




    def on_update_all_result(self, event):

        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "root"
        self.log_debug("on_update_all_result")

        for k,r in self.res.data.iteritems():
            self.update_in_dest(r, self.lst_dest[0][0])
                
        for k in self.res.data.keys():
            self.remove_result(k)
        self.update()  



    def on_update_result(self, event):

        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        self.log_debug("on_update_result")

        k = node["data"]

        self.update_in_dest(self.res.data[k], self.lst_dest[0][0])
        self.remove_result(k)
        self.update()  



    def on_export_csv(self, event):
        self.save_export_csv()


    def on_remove_result(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        self.log_debug("on_remove_campaign")

        k = node["data"]
        self.remove_result(k)
        self.update()  



    def remove_result(self, key):
        del self.res.data[key]
            


    def load_and_update(self):
        import os

        dlg = wx.FileDialog(
            self, message="Choose a file",
            #"defaultDir=os.getcwd(),
            defaultDir="",
            defaultFile="",
            wildcard=self.wildcard_dbm,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
        else :
            self.path = None
        dlg.Destroy()

        self.log_debug("FileDialog = \"%s\"" % self.path)

        if self.path is not None :
            self.load_dbm(self.path)



    def refresh_dbm(self):
        if self.path is not None:
            self.load_dbm(self.path)



    def load_dbm(self, filename):
        self.log_info("Load result : \"%s\"" % filename)

        self.res.load(filename)
        self.update()


    def update_res(self, res):
        self.res = res
        self.update()


    def add_lst_res(self, path, script, case, res):
        self.lst_res.append((path, script, case, res))

    def clearlst_res(self):
        self.lst_res = list()



    def export_csv_lst_res(self, filename):
        self.log_debug("Export csv = \"%s\"" % filename)
        try :
            f = open(filename, "w")
            for l in self.lst_res:
                f.write("%s\n" % (";".join(l)))
            f.close()
            self.log_debug("Export success")
        except :
            raise



    def save_export_csv(self):
        import os


        wildcard = "Csv file (*.csv)|*.csv|"     \
           "All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, message="Choose a file",
            #"defaultDir=os.getcwd(),
            defaultDir="",
            defaultFile="",
            wildcard=self.wildcard_csv,
            style=wx.SAVE | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        else :
            path = None
        dlg.Destroy()

        self.log_debug("FileDialog = \"%s\"" % path)

        if path is not None :
            self.export_csv_lst_res(path)






    def update(self):
        # update gui

        self.clearlst_res()

        self.tree.DeleteAllItems()

        item_root = self.tree.AddRoot(self.res.name)
        self.tree.SetPyData(item_root, {"type":"root", "data":None})
        self.tree.SetItemImage(item_root, self.im_result, wx.TreeItemIcon_Normal)

        for k,scr in self.res.data.iteritems():

            item_script = self.tree.AppendItem(item_root, scr.script.get_name())
            self.tree.SetPyData(item_script, {"type":"script", "data":k})

            status, param = scr.get_status()

            if status != dres.ST_EXEC_EXECUTED_NO_ERROR :
                self.tree.SetItemImage(item_script, self.im_script_warn, wx.TreeItemIcon_Normal)
                item_case = self.tree.AppendItem(item_script, "%s" % dres.SCRIPT_STATUS[status])
                self.tree.SetPyData(item_case, {"type":"info", "data":k})
                if param is not None :
                    item_case = self.tree.AppendItem(item_script, "%s" % param)
                    self.tree.SetPyData(item_case, {"type":"info", "data":k})
            elif  status == dres.ST_EXEC_EXECUTED_NO_ERROR :
                

                item_file = self.tree.AppendItem(item_script, "file" )
                self.tree.SetPyData(item_file, {"type":"info", "data":k})                  
                
                item_ = self.tree.AppendItem(item_file, "name     : \"%s.py\"" % scr.script.get_name())
                item_ = self.tree.AppendItem(item_file, "relative : \"%s\"" % scr.script.str_relative())
               
                
                item_trace = self.tree.AppendItem(item_script, "trace" )
                self.tree.SetPyData(item_, {"type":"info", "data":k})  
                
                for item in scr.trace_info:
                    item_ = self.tree.AppendItem(item_trace, "%s" % item )
                    self.tree.SetPyData(item_, {"type":"info", "data":k})                    
                


                script_status = "ok"
                for k,cas in scr.cases.iteritems():
                    item_case = self.tree.AppendItem(item_script, cas.name)
                    self.tree.SetPyData(item_case, {"type":"info", "data":k})

                    case_status = "default"
                    for k,res in cas.result.data.iteritems():
                        if res is not None:
                            item_res = self.tree.AppendItem(item_case, "%s" % k )
                            self.tree.SetPyData(item_case, {"type":"info", "data":k})
                            if k == dres.RES_ASSERT_OK :
                                case_status = "ok"
                            else:
                                case_status = "ko"
                                script_status = "ko"

                            for d in res:
                                for k,v in d.iteritems():
                                    jsize = 16
                                    item_l = self.tree.AppendItem(item_res, "%s :: %s" % (k.ljust(jsize),v) )
                                    self.tree.SetPyData(item_case, {"type":"info", "data":k})


                    if case_status == "default":
                        self.tree.SetItemImage(item_case, self.im_case, wx.TreeItemIcon_Normal)
                    elif case_status == "ok":
                        self.add_lst_res("/".join(scr.script.get_path()),scr.script.get_name(),cas.name,"OK")
                        self.tree.SetItemImage(item_case, self.im_case_ok, wx.TreeItemIcon_Normal)
                    elif case_status == "ko":
                        self.add_lst_res("/".join(scr.script.get_path()),scr.script.get_name(),cas.name,"KO")
                        self.tree.SetItemImage(item_case, self.im_case_ko, wx.TreeItemIcon_Normal)

                if script_status == "ok":
                    self.tree.SetItemImage(item_script, self.im_script_ok, wx.TreeItemIcon_Normal)
                elif script_status == "ko":
                    self.tree.SetItemImage(item_script, self.im_script_ko, wx.TreeItemIcon_Normal)

                #self.tree.SetItemImage(item_case, self.im_script_ko, wx.TreeItemIcon_Normal)
        self.tree.Expand(item_root)

    def OnActivate(self, event):
        self.item = event.GetItem()
        script = self.tree.GetItemData(self.item)




class TestFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.frm_result1 = ResultFrame("TestResult1", self, -1,)
        self.frm_result2 = ResultFrame("TestResult2", self, -1)


        self.frm_result1.add_result_dest(self.frm_result2)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.frm_result1, 1, wx.EXPAND, 0)
        sizer_1.Add(self.frm_result2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

        self.SetSize(wx.Size(500,500))

        # create menu
        mb = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN,        "Open ...")
        file_menu.Append(wx.ID_DUPLICATE,   "Export csv ...")
        file_menu.Append(wx.ID_EXIT,        "Exit")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "About...")

        mb.Append(file_menu, "File")
        mb.Append(help_menu, "Help")

        self.SetMenuBar(mb)


        self.Bind(wx.EVT_MENU, self.on_open_xml, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_export_csv, id=wx.ID_DUPLICATE)




    def on_open_xml(self, event):
        self.frm_result1.load_and_update()

    def on_export_csv(self, event):
        self.frm_result1.save_export_csv()




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




