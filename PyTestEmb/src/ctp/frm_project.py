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

import data.rftree as rftree
import data.project as dpro

    
    
class ProjectFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):
        
        
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.tree = wx.TreeCtrl(self,-1)
        self.tree.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnRightUp, self.tree)

        
        self.project = None
        
        
        self.il = wx.ImageList(16, 16)
        self.im_script      = self.il.Add( wx.Bitmap("images/script.png", wx.BITMAP_TYPE_PNG))
        self.im_pool        = self.il.Add( wx.Bitmap("images/database.png", wx.BITMAP_TYPE_PNG))
        self.im_folder      = self.il.Add( wx.Bitmap("images/folder_database.png", wx.BITMAP_TYPE_PNG))
        self.im_project     = self.il.Add( wx.Bitmap("images/application_view_tile.png", wx.BITMAP_TYPE_PNG))        
        self.im_campaigns   = self.il.Add( wx.Bitmap("images/chart_organisation.png", wx.BITMAP_TYPE_PNG))
        self.im_campaign    = self.il.Add( wx.Bitmap("images/database_table.png", wx.BITMAP_TYPE_PNG))
        self.tree.SetImageList(self.il)
        
    
        
        
        
    def load_xml(self, filename):
        
        self.project = dpro.load_xml(filename)
        self.project.sort()
        self.update_tree()
        
        
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
  

    def OnItemAddScriptCampaign(self, event):
        pass

    def OnItemAddScriptPool(self, event):
        pass

    def OnRemoveScript(self, event):
        pass

    
    
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
            self.tree.SetItemImage(item_, self.im_campaign, wx.TreeItemIcon_Normal)
            
            for node in campaign.scripts.root :
                self._add_node(item_, node)
            
#            for script in campaign.get_lst_scripts():
#                item__ = self.tree.AppendItem(item_, "%s.py" % script.get_relativepath())
#                self.tree.SetPyData(item__, copy.copy(script))


            


    def OnActivate(self, event):
        self.item = event.GetItem()
        script = self.tree.GetItemData(self.item)


        


class MyApp(wx.App):        

    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = ProjectFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        
        import os.path
        frameMain.load_xml(os.path.realpath("..\\..\\test\\script\\project_01.xml"))
        return 1






if __name__ == "__main__":


    App = MyApp(0)
    App.MainLoop()    
    
    
    
    
    