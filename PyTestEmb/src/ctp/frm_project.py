# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.7 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"












import wx    

import data.rftree as rftree
import data.project as dpro

import wxcustom.evt_file as evt_file
import wxcustom.evt_run as evt_run   
    


import frm_controler as frm_controler


        
class ProjectFrame(wx.Panel):
    def __init__(self, *p, **pp):
        
        wx.Panel.__init__(self, *p, **pp)
        

    
        self.tree = wx.TreeCtrl(self,-1)
        self.tree.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnRightUp, self.tree)

        
        self.project = None
        self.log = None
        
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
        
        
    def OnRightUp(self, event):
        type = ["script", "campaign"]
        id = self.tree.GetSelection()
        node = self.tree.GetItemPyData(id)
        
        if node is None : return
        if type.count(node["type"]) != 1: return 
            
            
        type_menu = "script"
        
        menu = wx.Menu()
        if      node["type"] == "script" :
            item1 = menu.Append(wx.ID_ANY, "Run script")
            menu.AppendSeparator()
            item2 = menu.Append(wx.ID_ANY, "View script")
            self.Bind(wx.EVT_MENU, self.on_run_script,      item1)
            self.Bind(wx.EVT_MENU, self.on_view_script,     item2)            

        elif    node["type"] == "campaign" :
            item1 = menu.Append(wx.ID_ANY, "Run campaign")
            self.Bind(wx.EVT_MENU, self.on_run_campaign,      item1)
        else:
            assert False
        self.PopupMenu(menu)
        menu.Destroy()
        
    
    def on_run_campaign(self, event):
        id = self.tree.GetSelection()
        node = self.tree.GetItemPyData(id)
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
        id = self.tree.GetSelection()
        node = self.tree.GetItemPyData(id)
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
        id = self.tree.GetSelection()
        node = self.tree.GetItemPyData(id)
        assert node["type"] == "script"
        path = node["data"].str_absolute(self.project.get_base_path())
        self.log_debug(path)
        evt = evt_file.EventFileView.create_editor_py(path)
        self.post_event(evt)
    
    
#    def load_project(self, proj):
#        self.project = proj
#        self.update()
#        
#        l = proj.get_campaign_list_absolute("Campaign_02")
#        if l is not None:
#            for o in l:
#                print o
#        l = proj.get_pool_list_absolute()
#        if l is not None:
#            for o in l:
#                print o       
    
    
    
    
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
        tree_project = self.tree.AddRoot(self.project.name)
        
        self.tree.SetItemImage(tree_project, self.im_project, wx.TreeItemIcon_Normal)
    
    
        item_pool = self.tree.AppendItem(tree_project, "Script Pool")
        self.tree.SetItemImage(item_pool, self.im_pool, wx.TreeItemIcon_Normal)
        
        for node in self.project.scripts.root :
            self._add_node(item_pool, node)
            
                
        item_campaign = self.tree.AppendItem(tree_project, "Campaigns")
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


            


    def OnActivate(self, event):
        self.item = event.GetItem()
        script = self.tree.GetItemData(self.item)



class TestFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):
        
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        
        self.frm_project = ProjectFrame(self)
        
        
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
    
    
    
    
    