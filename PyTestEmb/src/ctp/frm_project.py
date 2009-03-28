# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.9 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"












import wx

import data.rftree as rftree
import data.project as dpro

import wxcustom.evt_file as evt_file
import wxcustom.evt_run as evt_run
import wxcustom.evt_doc as evt_doc


import frm_logging
import frm_controler



class ProjectFrame(wx.Panel):
    def __init__(self, *p, **pp):

        wx.Panel.__init__(self, *p, **pp)



        self.tree = wx.TreeCtrl(self,-1)
        self.tree.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnItemMenu, self.tree)



        self.project = None
        self.log = None

        self.sel_item = None

        self.il = wx.ImageList(16, 16)
        self.im_script      = self.il.Add( wx.Bitmap("images/script.png", wx.BITMAP_TYPE_PNG))
        self.im_pool        = self.il.Add( wx.Bitmap("images/database.png", wx.BITMAP_TYPE_PNG))
        self.im_folder      = self.il.Add( wx.Bitmap("images/folder_database.png", wx.BITMAP_TYPE_PNG))
        self.im_project     = self.il.Add( wx.Bitmap("images/application_view_tile.png", wx.BITMAP_TYPE_PNG))
        self.im_campaigns   = self.il.Add( wx.Bitmap("images/chart_organisation.png", wx.BITMAP_TYPE_PNG))
        self.im_campaign    = self.il.Add( wx.Bitmap("images/database_table.png", wx.BITMAP_TYPE_PNG))
        self.tree.SetImageList(self.il)

        self.path = None
        self.wildcard = "Project file (*.xml)|*.xml|"     \
           "All files (*.*)|*.*"



        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.tree, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()


    def post_event(self, evt):
        self.GetParent().AddPendingEvent(evt)


    def set_log(self, log):
        self.log = log


    def log_debug(self, data):
        if self.log is not None :
            self.log.log_debug(data)

    def log_info(self, data):
        if self.log is not None :
            self.log.log_info(data)



    def open_and_load_xml(self):
        import os

        dlg = wx.FileDialog(
            self, message="Choose a file",
            #"defaultDir=os.getcwd(),
            defaultDir="../../test/script/",
            defaultFile="",
            wildcard=self.wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
        else :
            self.path = None
        dlg.Destroy()

        self.log_debug("FileDialog = \"%s\"" % self.path)

        if self.path is not None :
            self.load_xml(self.path)


    def refresh_xml(self):
        if self.path is not None:
            self.load_xml(self.path)



    def load_xml(self, filename):
        self.log_info("Load project : \"%s\"" % filename)
        self.project = dpro.load_xml(filename)
        self.project.sort()
        self.update_tree()



    def OnItemMenu(self, event):
        type = ["root_pool","root_campaign","script", "campaign"]
        item = event.GetItem()
        self.log_debug("OnItemMenu item=\"%s\"" % self.tree.GetItemText(item))

        self.sel_item = item


        node = self.tree.GetItemPyData(self.sel_item)

        if node is None :
            self.sel_item = None
            return
        if type.count(node["type"]) != 1:
            self.sel_item = None
            return


        type_menu = "script"

        menu = wx.Menu()
        if      node["type"] == "script" :
            item1 = menu.Append(wx.ID_ANY, "Run script")
            item2 = menu.Append(wx.ID_ANY, "Doc script")
            menu.AppendSeparator()
            item3 = menu.Append(wx.ID_ANY, "View script")
            menu.AppendSeparator()
            item4 = menu.Append(wx.ID_ANY, "Add script in campaign ...")
            item5 = menu.Append(wx.ID_ANY, "Add script from files ...")

            self.Bind(wx.EVT_MENU, self.on_run_script,                  item1)
            self.Bind(wx.EVT_MENU, self.on_doc_script,                  item2)
            self.Bind(wx.EVT_MENU, self.on_view_script,                 item3)
            self.Bind(wx.EVT_MENU, self.on_add_script_in_campaign,      item4)
            self.Bind(wx.EVT_MENU, self.on_add_script_from_files,       item5)
            
        elif    node["type"] == "campaign" :
            item1 = menu.Append(wx.ID_ANY, "Run campaign")
            item2 = menu.Append(wx.ID_ANY, "Doc campaign")
            menu.AppendSeparator()
            item3 = menu.Append(wx.ID_ANY, "New campaign ...")
            
            self.Bind(wx.EVT_MENU, self.on_run_campaign,      item1)
            self.Bind(wx.EVT_MENU, self.on_doc_campaign,      item2)
            self.Bind(wx.EVT_MENU, self.on_new_campaign,      item3)
            

        elif    node["type"] == "root_pool" :
            item1 = menu.Append(wx.ID_ANY, "Add script from files ...")
            self.Bind(wx.EVT_MENU, self.on_add_script_from_files,      item1)
            
        elif    node["type"] == "root_campaign" : 
            item1 = menu.Append(wx.ID_ANY, "New campaign ...")
            self.Bind(wx.EVT_MENU, self.on_new_campaign,      item1)
        else:
            assert False
        self.PopupMenu(menu)
        menu.Destroy()
        
        

    def on_new_campaign(self, event):
        self.log_debug("on_new_campaign")

        
        dlg = wx.TextEntryDialog(
                self, "Please enter the name of campaign :",
                'New campaign ...', 'Python')

        dlg.SetValue("campaign_name")

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            self.log_debug("Entered campaign name : %s" % name)
            
            # check campaign does not 
            campaignlist = []
            for campaign in self.project.campaigns :
                campaignlist.append(campaign.name)
            
            if campaignlist.count(name) > 0 :
                wx.MessageBox("This campaign name already exist")
            else:       
                self.project.add_campaign(name)
                self.update_tree()
                self.log_debug("New campaign added : %s" % name)
            
        else :
            self.log_debug("Canceled")

        dlg.Destroy()
        

    def on_add_script_from_files(self, event):
        self.log_debug("on_add_script_from_files")        
        

    def on_add_script_in_campaign(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        self.log_debug("Add script in campaign : \"%s\"" % node["data"])
        
        
        script = node["data"]
        dlg = DialogAddScriptInCampaign(self.project, script, self, -1, "")
        dlg.set_log(self)
        dlg.ShowModal()
        ret = dlg.GetReturnCode()   
        dlg.Destroy()
        
        if ret > 0 :
            self.update_tree()
        
        



    def on_doc_campaign(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "campaign"
        self.log_debug("Run Doc Campaign : \"%s\"" % node["data"])
        # EventRunScript
        slist = list()
        for script in self.project.get_campaign_list_scripts(node["data"]):
            slist.append(script)
        config = dict()
        config[frm_controler.BASE_PATH] = self.project.get_base_path()
        evt = evt_doc.EventDoc(slist, config)
        self.post_event(evt)


    def on_doc_script(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        self.log_debug("Run Doc Script : \"%s\"" % node["data"].get_name())
        # EventRunScript
        slist = list()
        slist.append(node["data"])
        config = dict()
        config[frm_controler.BASE_PATH] = self.project.get_base_path()
        evt = evt_doc.EventDoc(slist, config)
        self.post_event(evt)





    def on_run_campaign(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "campaign"
        self.log_debug("Run Campaign : \"%s\"" % node["data"])
        # EventRunScript
        slist = list()
        for script in self.project.get_campaign_list_scripts(node["data"]):
            slist.append(script)
        config = dict()
        config[frm_controler.BASE_PATH] = self.project.get_base_path()
        evt = evt_run.EventRunScript(slist, config)
        self.post_event(evt)


    def on_run_script(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        self.log_debug("Run Script : \"%s\"" % node["data"].get_name())
        # EventRunScript
        slist = list()
        slist.append(node["data"])
        config = dict()
        config[frm_controler.BASE_PATH] = self.project.get_base_path()
        evt = evt_run.EventRunScript(slist, config)
        self.post_event(evt)



    def on_view_script(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        path = node["data"].str_absolute(self.project.get_base_path())
        self.log_debug(path)
        evt = evt_file.EventFileView.create_editor_py(path)
        self.post_event(evt)









    def _add_node(self, item, node):

        if node.is_behavior(rftree.B_FILE) :

            item_ = self.tree.AppendItem(item, node.key)
            self.tree.SetPyData(item_, {"type":"script", "data":node.data})
            self.tree.SetItemImage(item_, self.im_script, wx.TreeItemIcon_Normal)

        if node.is_behavior(rftree.B_DIR) :
            item_ = self.tree.AppendItem(item, node.key)

            self.tree.SetPyData(item_, {"type":"directory", "data":None})

            self.tree.SetItemImage(item_, self.im_folder, wx.TreeItemIcon_Normal)
            for n in node:
                self._add_node(item_, n)

#        if node.is_behavior(ftree.B_ROOT) :
#            item_ = self.tree.AppendItem(item, node.key)
#            self.tree.SetItemImage(item_, self.im_root, wx.TreeItemIcon_Normal)
#            for n in node:
#                self._add_node(item_, n)





    def update_tree(self):

        if self.project is None:
            return

        self.tree.DeleteAllItems()
        item_root = self.tree.AddRoot(self.project.name)

        self.tree.SetItemImage(item_root, self.im_project, wx.TreeItemIcon_Normal)


        item_pool = self.tree.AppendItem(item_root, "Script Pool")
        self.tree.SetPyData(item_pool, {"type":"root_pool", "data":None})
        self.tree.SetItemImage(item_pool, self.im_pool, wx.TreeItemIcon_Normal)

        for node in self.project.scripts.root :
            self._add_node(item_pool, node)


        item_campaign = self.tree.AppendItem(item_root, "Campaigns")
        self.tree.SetPyData(item_campaign, {"type":"root_campaign", "data":None})
        self.tree.SetItemImage(item_campaign, self.im_campaigns, wx.TreeItemIcon_Normal)

        for campaign in self.project.campaigns :


            item_ = self.tree.AppendItem(item_campaign, campaign.name)
            self.tree.SetPyData(item_, {"type":"campaign", "data":campaign.name})
            self.tree.SetItemImage(item_, self.im_campaign, wx.TreeItemIcon_Normal)

            for node in campaign.scripts.root :
                self._add_node(item_, node)

#            for script in campaign.get_lst_scripts():
#                item__ = self.tree.AppendItem(item_, "%s.py" % script.get_relativepath())
#                self.tree.SetPyData(item__, copy.copy(script))



        self.tree.Expand(item_root)
        self.tree.Expand(item_pool)
        self.tree.Expand(item_campaign)






class DialogAddScriptInCampaign(wx.Dialog):
    
    def __init__(self, project, script, *args, **kwds):
        
        
        wx.Dialog.__init__(self, *args, **kwds)
        
        
        self.project = project
        self.script = script
        

        self.SetTitle("Add Script \"%s\" in Campaign ..." %  script.get_name())
        
        self.add = wx.Button(self, -1,"Add")
        self.cancel = wx.Button(self, -1, "Cancel") 
    
        self.Bind(wx.EVT_BUTTON, self.on_add, self.add)  
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel)

        self.Bind(wx.EVT_CLOSE, self.on_close)        
        
        
    
        # create control  
        self.campaign = wx.ListBox(self, -1,  size=wx.Size(300,200))
        self.campaign.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.Bind(wx.EVT_LISTBOX, self.on_listbox, self.campaign)



        self.lstbox_script = wx.ListBox(self, -1,  size=wx.Size(300,200))
        self.lstbox_script.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        
        
    
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
    
        
        sizer_1.Add((400, 20), 0, 0, 0)
        
        sizer_2.Add(self.campaign, 0, wx.ALL, 5)
        sizer_2.Add(self.lstbox_script, 0, wx.ALL, 5)
        
        sizer_1.Add(sizer_2)
        
        sizer_1.Add((400, 20), 0, 0, 0)
        
        sizer_3.Add(self.add, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.cancel, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5) 
        
        sizer_1.Add(sizer_3, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        
        
        self.sel_campaign = None
        
        # update list
        campaignlist = []
        for campaign in self.project.campaigns :
            campaignlist.append(campaign.name)
        self.campaign.InsertItems(campaignlist, 0)


    def set_log(self, log):
        self.log = log


    def log_debug(self, data):
        if self.log is not None :
            self.log.log_debug(data)

    def log_info(self, data):
        if self.log is not None :
            self.log.log_info(data)
            
    
    
    def fill_script(self, campaign):
        
        slist = list()
        for script in self.project.get_campaign_list_scripts(campaign):
            slist.append(script.get_name())       
        
        self.lstbox_script.Clear()
        self.lstbox_script.InsertItems(slist, 0)
        
        
        
            
    def on_listbox(self, event):
        self.log_debug("on_listbox")
        
        name = event.GetString()
        self.sel_campaign = name
        self.log_debug("Campaign : %s" % name)
        self.fill_script(name)
        
        
        
    
        
    def on_add(self, event):
        self.log_debug("on_add")
        
        
        if      self.sel_campaign is None :
            wx.MessageBox("Please select a campaign")
        elif    self.lstbox_script.GetItems().count(self.script.get_name()) > 0 :
            info = "Script \"%s\" already in campaign \"%s\"" % (self.script.get_name(),self.sel_campaign) 
            wx.MessageBox(info)
            self.log_debug(info)
        else:
            self.project.add_script_in_campaign(self.sel_campaign, self.script)
            wx.MessageBox("Added")
            self.EndModal(1)
        
    
    def on_cancel(self, event):
        self.log_debug("on_cancel")
        self.EndModal(0)

    def on_close(self, event):
        self.log_debug("on_close")
        self.EndModal(0)




class TestFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.frm_project = ProjectFrame(self)


        log = frm_logging.LoggingStdout()
        self.frm_project.set_log(log)

        # create menu
        mb = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN,    "Open ...")
        file_menu.Append(wx.ID_REFRESH, "Refresh ...")
        file_menu.Append(wx.ID_EXIT,    "Exit")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "About...")

        mb.Append(file_menu, "File")
        mb.Append(help_menu, "Help")

        self.SetMenuBar(mb)


        self.Bind(wx.EVT_MENU, self.on_open_xml, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_refresh_xml, id=wx.ID_REFRESH)


    def on_open_xml(self, event):
        self.frm_project.open_and_load_xml()

    def on_refresh_xml(self, event):
        self.frm_project.refresh_xml()




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



