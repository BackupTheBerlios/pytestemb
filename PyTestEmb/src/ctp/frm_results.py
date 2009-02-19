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

import data.results as dres

class ResultFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):
        

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.tree = wx.TreeCtrl(self,-1)
        self.tree.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)
        
        self.project = None
        

 
        
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


        self.tree.SetImageList(il)
        self.il = il
        
    
    
        self.res = dres.Results()
        self.res.load()
        
                
        self.update()
        
        
        
        
        
    def __del__(self):
        pass
        #save_to_xml(self.project, "c:\\temp\\project.xml")
    

        


       
        

    
    

                
                
    
    
    
    
    def update(self):    
        # update gui
        self.tree.DeleteAllItems()
        
        # Root
        tree_result = self.tree.AddRoot("Results")
        self.tree.SetItemImage(tree_result, self.im_result, wx.TreeItemIcon_Normal)
        
        
        for k,scr in self.res.data.iteritems():
            
            item_script = self.tree.AppendItem(tree_result, scr.script.str_relative())
            status, param = scr.get_status()
            
            
            if status != dres.ST_EXEC_EXECUTED_NO_ERROR :
                self.tree.SetItemImage(item_script, self.im_script_warn, wx.TreeItemIcon_Normal)
                item_case = self.tree.AppendItem(item_script, "%s" % dres.SCRIPT_STATUS[status])
                if param is not None :
                    item_case = self.tree.AppendItem(item_script, "%s" % param)
            elif  status == dres.ST_EXEC_EXECUTED_NO_ERROR :
                #item_script = self.tree.AppendItem(tree_result, scr.script.str_relative())
                if scr.trace_info is None :
                    item_case = self.tree.AppendItem(item_script, "No trace" )
                else:
                    item_case = self.tree.AppendItem(item_script, "%s" % scr.trace_info )
                
                script_status = "ok"
                for k,cas in scr.cases.iteritems():
                    item_case = self.tree.AppendItem(item_script, cas.name)
                
                    case_status = "default" 
                    for k,res in cas.result.data.iteritems():
                        if res is not None:  
                            item_res = self.tree.AppendItem(item_case, "%s" % k )
                            if k == dres.RES_ASSERT_OK :
                                case_status = "ok"
                            else:
                                case_status = "ko"
                                script_status = "ko"                        
                            
                            for d in res:
                                for k,v in d.iteritems():
                                    item_l = self.tree.AppendItem(item_res, "%s :: %s" % (k.ljust(8),v) )  



                    if case_status == "default":
                        self.tree.SetItemImage(item_case, self.im_case, wx.TreeItemIcon_Normal)
                    elif case_status == "ok":
                        self.tree.SetItemImage(item_case, self.im_case_ok, wx.TreeItemIcon_Normal)
                    elif case_status == "ko":
                        self.tree.SetItemImage(item_case, self.im_case_ko, wx.TreeItemIcon_Normal)                   
          
                if script_status == "ok":
                    self.tree.SetItemImage(item_script, self.im_script_ok, wx.TreeItemIcon_Normal)
                elif script_status == "ko":
                    self.tree.SetItemImage(item_script, self.im_script_ko, wx.TreeItemIcon_Normal)
                                                                   
                
                #self.tree.SetItemImage(item_case, self.im_script_ko, wx.TreeItemIcon_Normal)           
            
        



    def OnActivate(self, event):
        self.item = event.GetItem()
        script = self.tree.GetItemData(self.item)


        


class MyApp(wx.App):        

    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = ResultFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        
        return 1




#    r = Results()
#
#    import project
#    
#    s = ScriptRes(project.Script("toto",[]))
#    s.cases[0] = CaseRes(u"name")
#    r.update(s)
#    r.save()
    


if __name__ == "__main__":


    App = MyApp(0)
    App.MainLoop()
    
    
        