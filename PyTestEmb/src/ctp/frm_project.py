# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"












import wx    

import data.rftree as rftree
import data.project as dpro

    
    
class ProjectFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):
        

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.tree = wx.TreeCtrl(self,-1)
        
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)
        
        self.project = None
        
        
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnRightUp, self.tree)
 
        
        il = wx.ImageList(16, 16)
        self.im_script      = il.Add( wx.Bitmap("images/script.png", wx.BITMAP_TYPE_PNG))
        self.im_pool        = il.Add( wx.Bitmap("images/database.png", wx.BITMAP_TYPE_PNG))
        self.im_folder      = il.Add( wx.Bitmap("images/folder_database.png", wx.BITMAP_TYPE_PNG))
        self.im_project     = il.Add( wx.Bitmap("images/application_view_tile.png", wx.BITMAP_TYPE_PNG))
        
        
        self.im_campaigns    = il.Add( wx.Bitmap("images/chart_organisation.png", wx.BITMAP_TYPE_PNG))
        
        self.im_campaign    = il.Add( wx.Bitmap("images/database_table.png", wx.BITMAP_TYPE_PNG))


        self.tree.SetImageList(il)
        self.il = il
        
    
        
        
                
        proj = dpro.load_from_xml("C:\\CVS_Local\\PyTestEmb\\test\\project_01.xml")
        self.load_project(proj)
        
        
        
        
        
        
        
    def OnRightUp(self, event):
        
        menu = wx.Menu()

        item1 = menu.Append(wx.ID_ANY, "New Campaign")
        menu.AppendSeparator()
        item2 = menu.Append(wx.ID_ANY, "Add script to a Campaign")
        item3 = menu.Append(wx.ID_ANY, "Add script to Pool")
        menu.AppendSeparator()
        item4 = menu.Append(wx.ID_ANY, "Remove script")
        



        self.Bind(wx.EVT_MENU, self.OnItemNewCampaign, item1)
        self.Bind(wx.EVT_MENU, self.OnItemAddScriptCampaign, item2)
        self.Bind(wx.EVT_MENU, self.OnItemAddScriptPool, item3)
        self.Bind(wx.EVT_MENU, self.OnRemoveScript, item4)
        #self.Bind(wx.EVT_MENU, self.OnRemoveCampaign, item5)
        
        self.PopupMenu(menu)
        menu.Destroy()
        

        
        
        
    def OnItemNewCampaign(self, event):
        self.project.add_campaign("test")
        self.update()

    def OnItemAddScriptCampaign(self, event):
        pass

    def OnItemAddScriptPool(self, event):
        pass

    def OnRemoveScript(self, event):
        pass

        
        
        
        #self.import_scripts_from_directory()
        
    def __del__(self):
        pass
        #save_to_xml(self.project, "c:\\temp\\project.xml")
    
    def load_project(self, proj):
        self.project = proj
        self.update()
        
        l = proj.get_campaign_list_absolute("Campaign_02")
        if l is not None:
            for o in l:
                print o
        l = proj.get_pool_list_absolute()
        if l is not None:
            for o in l:
                print o       
    
    
    
    
    def _add_node(self, item, node):
        
        
        if node.is_behavior(rftree.B_FILE) :
            item_ = self.tree.AppendItem(item, node.key)

            self.tree.SetItemImage(item_, self.im_script, wx.TreeItemIcon_Normal)          
            
        if node.is_behavior(rftree.B_DIR) : 
            item_ = self.tree.AppendItem(item, node.key)
            self.tree.SetItemImage(item_, self.im_folder, wx.TreeItemIcon_Normal)
            for n in node:
                self._add_node(item_, n)               
        
#        if node.is_behavior(ftree.B_ROOT) :
#            item_ = self.tree.AppendItem(item, node.key)
#            self.tree.SetItemImage(item_, self.im_root, wx.TreeItemIcon_Normal)
#            for n in node:
#                self._add_node(item_, n)
                
                
                
    
    
    def update(self):    
        # update gui
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
            self.tree.SetItemImage(item_, self.im_campaign, wx.TreeItemIcon_Normal)
            
            for node in campaign.scripts.root :
                self._add_node(item_, node)
            
#            for script in campaign.get_lst_scripts():
#                item__ = self.tree.AppendItem(item_, "%s.py" % script.get_relativepath())
#                self.tree.SetPyData(item__, copy.copy(script))


    def import_scripts_from_directory(self):

        ignore_path = ["CVS", "data", "environement"]
        ignore_file = ["__init__.py"]
        
        extention = ".py"
    
        lst_files = list()
    
        import os
        path = "C:\\CVS_LOCAL_ECLIPSE\\scripts\\project\\champ2"
        for root, dirs, files in os.walk(path, topdown=True):
            
            for p in ignore_path:
                if p in dirs:
                    #print "remove : %s" % p
                    dirs.remove(p)  # don't visit CVS directories       
            for f in files:
                if os.path.splitext(f)[1] == extention :
                    if f in ignore_file :
                        continue
                    lst_files.append("%s\\%s" % (root, f))  
                    #print lst_files[-1]
                    
        for f in lst_files:
            self.project.add_script_file_in_scripts(f)
        self.update()
            


    def OnActivate(self, event):
        self.item = event.GetItem()
        script = self.tree.GetItemData(self.item)


        


class MyApp(wx.App):        

    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = ProjectFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        
        return 1






if __name__ == "__main__":


    App = MyApp(0)
    App.MainLoop()    
    
    
    
    
    