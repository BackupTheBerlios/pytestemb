# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.13 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import os


import wx

import data.rftree as rftree
import data.project as dpro
import data.utils as dutils

import wxcustom.evt_file as evt_file
import wxcustom.evt_run as evt_run
import wxcustom.evt_doc as evt_doc


import frm_logging
import frm_controler



class ProjectFrame(wx.Panel):

    POOL_SCRIPT = 0
    CAMPAIGN    = 1

    def __init__(self, config, *p, **pp):

        wx.Panel.__init__(self, *p, **pp)


        # Tree control
        self.tree = wx.TreeCtrl(self,-1)
        self.tree.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnItemMenu, self.tree)

        self.configuration = {"trace"   :frm_controler.TRACE_OCTOPYLOG_TXT,
                              "path"    :""}

        # Configuration
        self.config = config
        self.configuration["path"] = self.config.Read("PYTHON_PATH", "")
        self.configuration["trace"] = self.config.ReadInt("TRACE", frm_controler.TRACE_OCTOPYLOG_TXT)


        self.project    = None
        self.log        = None
        self.sel_item   = None
        self.path       = None


        # image list for tree control
        self.il = wx.ImageList(16, 16)
        self.im_script          = self.il.Add( wx.Bitmap("images/script.png", wx.BITMAP_TYPE_PNG))
        self.im_wrench          = self.il.Add( wx.Bitmap("images/wrench.png", wx.BITMAP_TYPE_PNG))
        self.im_folder_wrench   = self.il.Add( wx.Bitmap("images/folder_wrench.png", wx.BITMAP_TYPE_PNG))
        self.im_newspaper       = self.il.Add( wx.Bitmap("images/newspaper.png", wx.BITMAP_TYPE_PNG))
        self.im_tick            = self.il.Add( wx.Bitmap("images/tick.png", wx.BITMAP_TYPE_PNG))
        self.im_cross           = self.il.Add( wx.Bitmap("images/cross.png", wx.BITMAP_TYPE_PNG))
        self.im_folder_link     = self.il.Add( wx.Bitmap("images/folder_link.png", wx.BITMAP_TYPE_PNG))
        self.im_pool            = self.il.Add( wx.Bitmap("images/database.png", wx.BITMAP_TYPE_PNG))
        self.im_folder          = self.il.Add( wx.Bitmap("images/folder_database.png", wx.BITMAP_TYPE_PNG))
        self.im_project         = self.il.Add( wx.Bitmap("images/application_view_tile.png", wx.BITMAP_TYPE_PNG))
        self.im_campaigns       = self.il.Add( wx.Bitmap("images/chart_organisation.png", wx.BITMAP_TYPE_PNG))
        self.im_campaign        = self.il.Add( wx.Bitmap("images/database_table.png", wx.BITMAP_TYPE_PNG))
        self.tree.SetImageList(self.il)

        # sizer
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.tree, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()



    def finish(self):
        self.log_debug("Save configuration")
        self.log_debug("PYTHON_PATH   :: %s" % self.configuration["path"])
        self.log_debug("TRACE         :: %d" % self.configuration["trace"])
        self.config.Write("PYTHON_PATH", self.configuration["path"])
        self.config.WriteInt("TRACE", self.configuration["trace"])



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


    def new_project(self):

        intruction = "Please enter the name of project :"
        dlg = wx.TextEntryDialog(self, instruction, "New project ...", "Python")
        dlg.SetValue("project_name")

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            self.log_debug("Entered project name : %s" % name)
            self.project = dpro.Project(name)
            self.update_tree()
        else :
            self.log_debug("Canceled")

        dlg.Destroy()


    def save_xml(self):
        if self.path is not None:
            self.save_file_xml(self.path)


    def open_and_load_xml(self):

        wildcard = "Project file (*.xml)|*.xml|All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, message="Choose a file",
            #"defaultDir=os.getcwd(),
            defaultDir="../../test/script/",
            defaultFile="",
            wildcard=wildcard,
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




    def save_file_xml(self, filename):
        self.log_info("Save project : \"%s\"" % filename)
        dpro.save_to_xml(self.project, filename)



    def load_xml(self, filename):
        self.log_info("Load project : \"%s\"" % filename)
        self.project = dpro.load_xml(filename)
        self.project.sort()
        self.update_tree()



    def OnItemMenu(self, event):
        type = ["root_pool","root_campaign","script", "campaign", "configuration"]
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
        if      node["type"] == "script" \
            and node["parent_type"] == ProjectFrame.POOL_SCRIPT :
            item1 = menu.Append(wx.ID_ANY, "Run script")
            item2 = menu.Append(wx.ID_ANY, "Doc script")
            menu.AppendSeparator()
            item3 = menu.Append(wx.ID_ANY, "View script")
            menu.AppendSeparator()
            item4 = menu.Append(wx.ID_ANY, "Add script in campaign ...")
            item5 = menu.Append(wx.ID_ANY, "Add script from files ...")
            menu.AppendSeparator()
            item6 = menu.Append(wx.ID_ANY, "Remove script from pool")

            self.Bind(wx.EVT_MENU, self.on_run_script,                  item1)
            self.Bind(wx.EVT_MENU, self.on_doc_script,                  item2)
            self.Bind(wx.EVT_MENU, self.on_view_script,                 item3)
            self.Bind(wx.EVT_MENU, self.on_add_script_in_campaign,      item4)
            self.Bind(wx.EVT_MENU, self.on_add_script_from_files,       item5)
            self.Bind(wx.EVT_MENU, self.on_remove_script_from_pool,     item6)

        elif      node["type"] == "script" \
            and node["parent_type"] == ProjectFrame.CAMPAIGN :
            item1 = menu.Append(wx.ID_ANY, "Run script")
            item2 = menu.Append(wx.ID_ANY, "Doc script")
            menu.AppendSeparator()
            item3 = menu.Append(wx.ID_ANY, "View script")
            menu.AppendSeparator()
            item4 = menu.Append(wx.ID_ANY, "Remove script from campaign")

            self.Bind(wx.EVT_MENU, self.on_run_script,                  item1)
            self.Bind(wx.EVT_MENU, self.on_doc_script,                  item2)
            self.Bind(wx.EVT_MENU, self.on_view_script,                 item3)
            self.Bind(wx.EVT_MENU, self.on_remove_script_from_campaign, item4)

        elif    node["type"] == "campaign" :
            item1 = menu.Append(wx.ID_ANY, "Run campaign")
            item2 = menu.Append(wx.ID_ANY, "Doc campaign")
            menu.AppendSeparator()
            item3 = menu.Append(wx.ID_ANY, "New campaign ...")
            menu.AppendSeparator()
            item4 = menu.Append(wx.ID_ANY, "Remove campaign")

            self.Bind(wx.EVT_MENU, self.on_run_campaign,      item1)
            self.Bind(wx.EVT_MENU, self.on_doc_campaign,      item2)
            self.Bind(wx.EVT_MENU, self.on_new_campaign,      item3)
            self.Bind(wx.EVT_MENU, self.on_remove_campaign,      item4)

        elif    node["type"] == "root_pool" :
            item1 = menu.Append(wx.ID_ANY, "Add script from files ...")
            self.Bind(wx.EVT_MENU, self.on_add_script_from_files,      item1)

        elif    node["type"] == "root_campaign" :
            item1 = menu.Append(wx.ID_ANY, "New campaign ...")
            self.Bind(wx.EVT_MENU, self.on_new_campaign,      item1)

        elif   node["type"] == "configuration" :
            item1 = menu.Append(wx.ID_ANY, "Edit ...")
            self.Bind(wx.EVT_MENU, self.on_edit_config,      item1)
        else:
            assert False
        self.PopupMenu(menu)
        menu.Destroy()



    def on_edit_config(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "configuration"
        self.log_debug("on_edit_config")
        dlg = DialogConfiguration(self.configuration, self, -1, "")
        dlg.set_log(self)
        dlg.ShowModal()
        ret = dlg.GetReturnCode()
        dlg.Destroy()

        if ret == DIALOG_RET_DONE :
            self.update_tree()




    def on_remove_campaign(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "campaign"
        self.log_debug("on_remove_campaign")

        campaign = node["data"]

        question = """Confirm removing campaign ?
        campaign : "%s" """ % (campaign)
        dlg = wx.MessageDialog(self, question,
                               'Remove campaign ...',
                               wx.CANCEL|wx.OK | wx.ICON_QUESTION )
        ret = dlg.ShowModal()
        dlg.Destroy()

        if ret ==  wx.ID_OK :
            self.log_debug("OK")
            self.log_debug("Remove \"%s\" " % ( campaign))
            self.project.remove_campaign(campaign)
            self.update_tree()
        else :
            self.log_debug("Cancel")


    def on_remove_script_from_campaign(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        self.log_debug("on_remove_script_from_campaign")

        script = node["data"]
        campaign = node["parent_name"]


        question = """Confirm removing script ?
        script : "%s"
        campaign : "%s" """ % (script.get_name(),campaign)
        dlg = wx.MessageDialog(self, question,
                               'Remove script ...',
                               wx.CANCEL|wx.OK | wx.ICON_QUESTION )
        ret = dlg.ShowModal()
        dlg.Destroy()

        if ret ==  wx.ID_OK :
            self.log_debug("OK")
            self.log_debug("Remove \"%s\" from \"%s\"" % (script.get_name(), campaign))
            self.project.remove_script_in_campaign(campaign, script)
            self.update_tree()
        else :
            self.log_debug("Cancel")



    def on_remove_script_from_pool(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        self.log_debug("on_remove_script_from_pool")

        script = node["data"]


        question = """Confirm removing script ?
        script : "%s" """ % (script.get_name())
        dlg = wx.MessageDialog(self, question,
                               'Remove script ...',
                               wx.CANCEL|wx.OK | wx.ICON_QUESTION )
        ret = dlg.ShowModal()
        dlg.Destroy()

        if ret ==  wx.ID_OK :
            self.log_debug("OK")
            self.log_debug("Remove \"%s\"" % (script.get_name()))
            self.project.remove_script_in_pool(script)
            self.update_tree()
        else :
            self.log_debug("Cancel")





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

        dlg = DialogAddScriptFiles(self.project, self, -1, "")
        dlg.set_log(self)
        dlg.ShowModal()
        ret = dlg.GetReturnCode()
        dlg.Destroy()

        if ret == DIALOG_RET_DONE  :
            self.update_tree()



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

        if ret == DIALOG_RET_DONE  :
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
        config[frm_controler.PYPATH]    = self.configuration["path"]
        config[frm_controler.TRACE]     = frm_controler.TRACE_NONE
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
        config[frm_controler.PYPATH]    = self.configuration["path"]
        config[frm_controler.TRACE]     = frm_controler.TRACE_NONE
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
        config[frm_controler.PYPATH]    = self.configuration["path"]
        config[frm_controler.TRACE]     = self.configuration["trace"]
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
        config[frm_controler.PYPATH]    = self.configuration["path"]
        config[frm_controler.TRACE]     = self.configuration["trace"]

        evt = evt_run.EventRunScript(slist, config)
        self.post_event(evt)



    def on_view_script(self, event):
        node = self.tree.GetItemPyData(self.sel_item)
        assert node["type"] == "script"
        path = node["data"].str_absolute(self.project.get_base_path())
        self.log_debug(path)
        evt = evt_file.EventFileView.create_editor_py(path)
        self.post_event(evt)


    def _add_node(self, item, node, parent):

        data = {}
        data["parent_type"] = parent["type"]
        data["parent_name"] = parent["name"]

        if node.is_behavior(rftree.B_FILE) :

            item_ = self.tree.AppendItem(item, node.key)
            data["type"] = "script"
            data["data"] = node.data

            self.tree.SetPyData(item_, data)
            self.tree.SetItemImage(item_, self.im_script, wx.TreeItemIcon_Normal)

        if node.is_behavior(rftree.B_DIR) :
            item_ = self.tree.AppendItem(item, node.key)

            data["type"] = "directory"
            data["data"] = None

            self.tree.SetPyData(item_, data)

            self.tree.SetItemImage(item_, self.im_folder, wx.TreeItemIcon_Normal)
            for n in node:
                self._add_node(item_, n, parent)

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

        # Local config
        item_config = self.tree.AppendItem(item_root, "Local Config")
        self.tree.SetPyData(item_config, {"type":"configuration", "data":None})
        self.tree.SetItemImage(item_config, self.im_wrench, wx.TreeItemIcon_Normal)

        item_config_trace = self.tree.AppendItem(item_config, "Trace")
        self.tree.SetPyData(item_config_trace, {"type":"configuration", "data":None})
        self.tree.SetItemImage(item_config_trace, self.im_newspaper, wx.TreeItemIcon_Normal)

        item_config_txt = self.tree.AppendItem(item_config_trace, "TXT")
        self.tree.SetPyData(item_config_txt, {"type":"configuration", "data":None})

        item_config_octopy = self.tree.AppendItem(item_config_trace, "OCTOPYLOG")
        self.tree.SetPyData(item_config_octopy, {"type":"configuration", "data":None})


        if      self.configuration["trace"] == frm_controler.TRACE_OCTOPYLOG_TXT :
            self.tree.SetItemImage(item_config_txt, self.im_tick, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(item_config_octopy, self.im_tick, wx.TreeItemIcon_Normal)
        elif    self.configuration["trace"] == frm_controler.TRACE_NONE :
            self.tree.SetItemImage(item_config_txt, self.im_cross, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(item_config_octopy, self.im_cross, wx.TreeItemIcon_Normal)
        elif    self.configuration["trace"] == frm_controler.TRACE_TXT :
            self.tree.SetItemImage(item_config_txt, self.im_tick, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(item_config_octopy, self.im_cross, wx.TreeItemIcon_Normal)
        elif    self.configuration["trace"] == frm_controler.TRACE_OCTOPYLOG :
            self.tree.SetItemImage(item_config_txt, self.im_cross, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(item_config_octopy, self.im_tick, wx.TreeItemIcon_Normal)
        else :
            self.tree.SetItemImage(item_config_txt, self.im_cross, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(item_config_octopy, self.im_cross, wx.TreeItemIcon_Normal)

        item_config_path = self.tree.AppendItem(item_config, "Python Path")
        self.tree.SetPyData(item_config_path, {"type":"configuration", "data":None})
        self.tree.SetItemImage(item_config_path, self.im_folder_wrench, wx.TreeItemIcon_Normal)

        path = self.configuration["path"]
        item_ = self.tree.AppendItem(item_config_path, path)
        self.tree.SetPyData(item_, {"type":"configuration", "data":None})
        self.tree.SetItemImage(item_, self.im_folder_link, wx.TreeItemIcon_Normal)


        # script pool
        item_pool = self.tree.AppendItem(item_root, "Script Pool")
        self.tree.SetPyData(item_pool, {"type":"root_pool", "data":None})
        self.tree.SetItemImage(item_pool, self.im_pool, wx.TreeItemIcon_Normal)

        for node in self.project.scripts.root :
            parent = {}
            parent["type"] = ProjectFrame.POOL_SCRIPT
            parent["name"] = None

            self._add_node(item_pool, node, parent)


        item_campaign = self.tree.AppendItem(item_root, "Campaigns")
        self.tree.SetPyData(item_campaign, {"type":"root_campaign", "data":None})
        self.tree.SetItemImage(item_campaign, self.im_campaigns, wx.TreeItemIcon_Normal)


        # campaign
        for campaign in self.project.campaigns :

            item_ = self.tree.AppendItem(item_campaign, campaign.name)
            self.tree.SetPyData(item_, {"type":"campaign", "data":campaign.name})
            self.tree.SetItemImage(item_, self.im_campaign, wx.TreeItemIcon_Normal)

            for node in campaign.scripts.root :
                parent = {}
                parent["type"] = ProjectFrame.CAMPAIGN
                parent["name"] = campaign.name

                self._add_node(item_, node, parent)

#            for script in campaign.get_lst_scripts():
#                item__ = self.tree.AppendItem(item_, "%s.py" % script.get_relativepath())
#                self.tree.SetPyData(item__, copy.copy(script))

        self.tree.Expand(item_root)
        self.tree.Expand(item_pool)
        self.tree.Expand(item_campaign)






DIALOG_RET_CANCELED = 0
DIALOG_RET_DONE     = 1



class DialogConfiguration(wx.Dialog):

    LOG_CONFIG_TXT = ("txt", "octopylog")

    def __init__(self, configuration, *args, **kwds):


        self.configuration = configuration

        kwds["size"] = size=(400,400)

        wx.Dialog.__init__(self, *args, **kwds)

        self.SetTitle("Configuration")

        self.save = wx.Button(self, -1,"Save")
        self.cancel = wx.Button(self, -1, "Cancel")

        self.directory = wx.Button(self, -1, "Directory")

        self.Bind(wx.EVT_BUTTON, self.on_save, self.save)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel)
        self.Bind(wx.EVT_BUTTON, self.on_directory, self.directory)
        self.Bind(wx.EVT_CLOSE, self.on_close)



        self.txt_trace = wx.StaticText(self, -1, "Trace(s) :", (20, 10))
        self.txt_directory = wx.StaticText(self, -1, "Python Directory :", (20, 10))
        self.txt_path = wx.TextCtrl(self, -1, "",size=(300,20))
        self.txt_path.SetEditable(False)


        # create control
        self.lstbox = wx.CheckListBox(self, -1, (80, 50), wx.DefaultSize, DialogConfiguration.LOG_CONFIG_TXT)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)


        sizer_1.Add((400, 1), 0, 0, 0)
        sizer_1.Add(self.txt_trace, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.lstbox, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        #sizer_1.Add((400, 20), 0, 0, 0)

        sizer_1.Add(self.txt_directory, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.directory, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.txt_path, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_2, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        #sizer_1.Add((400, 20), 0, 0, 0)


        sizer_3.Add(self.save, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.cancel, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_3, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()


        self.txt_path.SetValue(self.configuration["path"])

        if self.configuration["trace"] == frm_controler.TRACE_OCTOPYLOG_TXT :
            self.lstbox.Check(0, True)
            self.lstbox.Check(1, True)
        if self.configuration["trace"] == frm_controler.TRACE_OCTOPYLOG :
            self.lstbox.Check(1,True)
        if self.configuration["trace"] == frm_controler.TRACE_TXT :
            self.lstbox.Check(0,True)



    def set_log(self, log):
        self.log = log

    def log_debug(self, data):
        if self.log is not None :
            self.log.log_debug(data)

    def log_info(self, data):
        if self.log is not None :
            self.log.log_info(data)


    def on_directory(self, event):

        _style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        dlg = wx.DirDialog(self, "Choose a directory:", _style)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.log_info("Path selected : %s"  % path)
            self.txt_path.SetValue(path)
            
        dlg.Destroy()


    def on_save(self, event):
        self.log_debug("on_save")

        self.configuration["path"] =  self.txt_path.GetValue()

        if      self.lstbox.IsChecked(0)\
            and self.lstbox.IsChecked(1):
            self.configuration["trace"] = frm_controler.TRACE_OCTOPYLOG_TXT
        elif  self.lstbox.IsChecked(1):
            self.configuration["trace"] = frm_controler.TRACE_OCTOPYLOG
        elif  self.lstbox.IsChecked(0):
            self.configuration["trace"] = frm_controler.TRACE_TXT
        else :
            self.configuration["trace"] = frm_controler.TRACE_NONE

        self.EndModal(DIALOG_RET_DONE)


    def on_cancel(self, event):
        self.log_debug("on_cancel")
        self.EndModal(DIALOG_RET_CANCELED)

    def on_close(self, event):
        self.log_debug("on_close")
        self.EndModal(DIALOG_RET_CANCELED)





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
            self.EndModal(DIALOG_RET_DONE)


    def on_cancel(self, event):
        self.log_debug("on_cancel")
        self.EndModal(DIALOG_RET_CANCELED)

    def on_close(self, event):
        self.log_debug("on_close")
        self.EndModal(DIALOG_RET_CANCELED)





class DialogAddScriptFiles(wx.Dialog):

    def __init__(self, project, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)

        self.project = project
        self.scripts = []

        self.SetTitle("Add Script files ...")

        self.select = wx.Button(self, -1, "Select Script(s)")
        self.add    = wx.Button(self, -1,"Add Script(s)")
        self.cancel = wx.Button(self, -1, "Cancel")

        self.Bind(wx.EVT_BUTTON, self.on_select, self.select)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.add)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel)

        self.Bind(wx.EVT_CLOSE, self.on_close)


        # create control
        self.lstbox_script = wx.ListBox(self, -1,  size=wx.Size(300,200))
        self.lstbox_script.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        #sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)


        sizer_1.Add((400, 20), 0, 0, 0)

        sizer_1.Add(self.select, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add((400, 20), 0, 0, 0)
        sizer_1.Add(self.lstbox_script, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        #sizer_1.Add(sizer_2)
        sizer_1.Add((400, 20), 0, 0, 0)
        sizer_3.Add(self.add, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.cancel, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_3, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)


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



    def on_add(self, event):
        self.log_debug("on_add")

        for script in self.scripts:
            self.project.add_script_in_pool(script)
            self.log_debug("Add script : %s" % script.str_relative())

        self.EndModal(DIALOG_RET_DONE)


    def on_select(self, event):
        self.log_debug("on_select")

        wildcard = "Python file (*.py)|*.py|All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.project.get_base_path(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )


        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()

            for path in paths:
                try :
                    self.scripts.append(dpro.Script.create_from_absolute_pathstr(self.project.get_base_path(), path))
                    self.lstbox_script.Append(self.scripts[-1].str_relative())
                except :
                    msg = "Error script : %s\nIt must be a subpath of : %s" % (path, self.project.get_base_path() )
                    dlg = wx.MessageDialog(self, msg, 'Error script ...', wx.OK | wx.ICON_ERROR )
                    dlg.ShowModal()
                    dlg.Destroy()
                    break
        dlg.Destroy()


    def on_cancel(self, event):
        self.log_debug("on_cancel")
        self.EndModal(DIALOG_RET_CANCELED)

    def on_close(self, event):
        self.log_debug("on_close")
        self.EndModal(DIALOG_RET_CANCELED)




class TestFrame(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)


        wxconf = wx.Config("TestFrame_project")

        self.frm_project = ProjectFrame(wxconf, self)

        log = frm_logging.LoggingStdout()
        self.frm_project.set_log(log)

        # create menu
        mb = wx.MenuBar()
        file_menu = wx.Menu()

        file_menu.Append(wx.ID_NEW,     "New")
        file_menu.Append(wx.ID_OPEN,    "Open ...")
        file_menu.Append(wx.ID_SAVE,    "Save")
        file_menu.Append(wx.ID_EXIT,    "Exit")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "About...")

        mb.Append(file_menu, "File")
        mb.Append(help_menu, "Help")

        self.SetMenuBar(mb)


        self.Bind(wx.EVT_MENU, self.on_new, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.on_open_xml, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_save_xml, id=wx.ID_SAVE)

    def on_new(self, event):
        self.frm_project.new_project()

    def on_open_xml(self, event):
        self.frm_project.open_and_load_xml()

    def on_save_xml(self, event):
        self.frm_project.save_xml()






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

    # clean
    wxconf = wx.Config("TestFrame_project")
    wxconf.DeleteAll()



