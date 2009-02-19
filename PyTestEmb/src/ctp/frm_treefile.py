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

    
    
class TreefileFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):
        
        
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
  
        tree = wx.GenericDirCtrl(self, -1,  size=(160, 250), style=wx.DIRCTRL_SHOW_FILTERS,
                                filter="All files (*.*)|*.*|Python files (*.py)|*.py")
        
   

        


class MyApp(wx.App):        

    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = TreefileFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        
        return 1






if __name__ == "__main__":


    App = MyApp(0)
    App.MainLoop()    
    
    
    
    
    