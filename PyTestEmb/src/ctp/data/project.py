# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : project manages project aspect : files, scripts, campaign
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"






import utils
import os.path 


import utils
import rftree

    


SCRIPT_EXT = ".py"



class Project:
    
    def __init__(self, name="", absolutepath=""):
        self.name = name
        self.absolutepath = absolutepath
        self.campaigns = []
        self.scripts = rftree.RfTree()
        
    def get_base_path(self):
        return self.absolutepath
    
    
    def get_lst_scripts(self, sftree):
        lst = list()
        for script in  sftree.get_list_item():
            lst.append(Script(script[1], script[0]))
#            pathfilename = os.path.join(self.absolutepath, *(script[0]))
#            pathfilename = os.path.join(pathfilename, "%s%s" % ( , SCRIPT_EXT))
#            lst.append((script[0], script[1], pathfilename))
        return lst        

    def add_script_in_pool(self, script):
        self.scripts.add_item(script.get_path(), script.get_name())
  
    def add_script_in_campaign(self, name, script):
        for campaign in self.campaigns:
            if name == campaign.name :
                campaign.add_script(script)
                return
        
    def add_campaign(self, name):
        self.campaigns.append(Campaign(name))
            
            
    def delete_campaign(self, name):
        for campaign in self.campaigns:
            if name == campaign.name :
                self.campaigns.remove(campaign)
                return

    def remove_script_in_campaign(self, campaign, script):
        self.scripts.delete_item(script.path, script.name)
            
        
    def remove_script_in_pool(self, script):
        self.scripts.delete_item(script.path, script.name)
            
            
    def get_pool_list_absolute(self):      
        return self.get_lst_scripts(self.scripts)
  
            
                                  
    def get_campaign_list_absolute(self, name):      
        for campaign in self.campaigns:
            if name == campaign.name :
                return self.get_lst_scripts(campaign.scripts)


    def get_campaign_list_scripts(self, name):      
        for campaign in self.campaigns:
            if name == campaign.name :
                return self.get_lst_scripts(campaign.scripts)
                        
            
    def sort(self):
        self.campaigns.sort()
    
                                  
    def __str__(self):
        dis = ""
        dis = "Scripts\n" 
        dis += self.scripts.pprint()
        for campaign in self.campaigns:
            dis += campaign.__str__()                
        return dis
        
            
            
            
            
class Campaign:
    def __init__(self, name=""):
        self.scripts = rftree.RfTree()
        self.name = name
        
    def __cmp__(self, other):
        return utils.cmp_string(self.name, other.name)
    
#    def get_lst_scripts_absolute(self, base):
#        absolute = list()
#        for script in  self.scripts.get_list_item():
#            pathfilename = os.path.join(base, *(script[0]))
#            pathfilename = os.path.join(pathfilename, "%s%s" % (script[1] , SCRIPT_EXT))
#            absolute.append(pathfilename)
#        return absolute    
#        
#    def get_lst_scripts(self, base):
#        lst = list()
#        for script in  self.scripts.get_list_item():
#            pathfilename = os.path.join(base, *(script[0]))
#            pathfilename = os.path.join(pathfilename, "%s%s" % (script[1] , SCRIPT_EXT))
#            lst.append(script[0], script[1], pathfilename)
#        return lst  
            
    
    def add_script(self, script):
        self.scripts.add_item(script.get_path(), script.get_name())
        
    def __str__(self):
        dis = "Campaign : %s\n" % self.name
        dis += self.scripts.pprint()
        return dis
    

    
class Script:  
    def __init__(self, name, path):
        self._name = name
        self._path = path           
        
        
    def __hash__(self):
        return self.get_key()
        
    def __cmp__(self, other):
        if self.get_key() == other.get_key():
            return 0
        else:
            return 1
    
    def get_name(self):
        return self._name
    
    def get_path(self):
        return self._path
    
    def get_key(self):
        data = ""
        data = data.join(self._path)
        data = data.join(self._name)
        return hash(data)
        
        
        
        
          
    def str_absolute(self, base):
        if len(self._path) == 0:
            return os.path.join(base, "%s%s" % (self._name , SCRIPT_EXT))
        else:
            absolute = os.path.join(base, *(self._path))
            return os.path.join(absolute, "%s%s" % (self._name , SCRIPT_EXT))

    def str_relative(self):
        if len(self._path) == 0:
            return "%s%s" % (self._name , SCRIPT_EXT)
        else:
            absolute = os.path.join(*(self._path))
            return os.path.join(absolute, "%s%s" % (self._name , SCRIPT_EXT))
        
        
        
    @staticmethod
    def create_from_absolute_pathstr(base, file):
        s_absolutepath, filename, ext = utils.split_fullpath(file)
        relative = utils.extract_relative(base, s_absolutepath)
        relative = os.path.split(relative)
        return Script(filename, relative)

    @staticmethod
    def create_from_relative_pathlist(relative, name):
        return Script(name, relative)

    def __str__(self):
        return self.str_relative()
        
        
            
    
def _get_one_tag(element, tagname):
    try:
        if      len(element.getElementsByTagName(tagname)[0].childNodes) == 1 :  
            return element.getElementsByTagName(tagname)[0].childNodes[0].data
        elif    len(element.getElementsByTagName(tagname)[0].childNodes) == 0 :  
            return ""
        else:
            raise Exception
    except:
        raise Exception("Tag %s not found" % tagname)
    
    

XML_PATH_SEP = "\\"
    
    
    

    
def load_xml(filename):
    import xml.etree.ElementTree as et



    project = Project()    
    path,name, ext = utils.split_fullpath(filename)
    
    e = et.parse(filename)
    
    root = e.getroot()
    iter = root.getiterator()
    re = et.ElementTree()
    

#    for elt in root.get():
#        print elt.tag 
    
    child = root.getchildren()
    
    # Project Name
    if child[0].tag == "Name":
        project.name = child[0].text
    else :
        KeyError("No project name")
 
    # Script pool
    if child[1].tag == "Scripts":
        pass
    else :
        KeyError("No project name")   
    
    for camp in child[2:]:
        # Project Name
        if camp[0].tag == "Name":
            project.add_campaign(camp[0].text)
        else :
            KeyError("No campaign name")
        
        
        
    return project


    
    
def load_from_xml(filename):
    import xml.dom.minidom
    
    project = Project()    
    path,name, ext = utils.split_fullpath(filename)
    
    project.absolutepath = path

    try:
        dom1 = xml.dom.minidom.parse(filename)           
    except IOError :
        raise
        
    try:
        eltProject = dom1.getElementsByTagName("Project")   

        project.name = _get_one_tag(eltProject[0], "Name")
    
        eltScript =  eltProject[0].getElementsByTagName("Scripts")[0].getElementsByTagName("Script")
        for script in eltScript:
            name = _get_one_tag(script, "Name")
            path = _get_one_tag(script, "Path") 
            path_lst = path.split(XML_PATH_SEP)
            project.add_script_in_pool(Script(name, path_lst))
                       
        eltCampaign =  eltProject[0].getElementsByTagName("Campaign")
        for campaign in eltCampaign:
            campaignname = _get_one_tag(campaign, "Name")
            project.add_campaign(campaignname)
            eltScript =  campaign.getElementsByTagName("Script")
            for script in eltScript:
                name = _get_one_tag(script, "Name")
                path = _get_one_tag(script, "Path") 
                path_lst = path.split(XML_PATH_SEP)
                project.add_script_in_campaign(campaignname, (Script(name, path_lst)))
                    
    except (xml.dom.DOMException, IndexError):
        raise    
    
    dom1.unlink()
    
    project.sort()
    return project

        
        
        




    
    
    
def _create_script(level, name, path):
    data = u""
    data += utils.xml_create_start_tag(level, "Script")
    data += utils.xml_create_property(level+1, "Name", name)
    data += utils.xml_create_property(level+1, "Path", path)
    data += utils.xml_create_stop_tag(level, "Script")    
    return data    
    
    
def save_to_xml(proj, filename):
    import codecs
    
    data = u""
    data += utils.xml_create_header()   

    data += utils.xml_create_start_tag(0, "Project")
    data += utils.xml_create_property(1, "Name", proj.name)

    data += utils.xml_create_start_tag(1, "Scripts")
    for script in proj.scripts:
        data += _create_script(2, script.name, script.relativepath)
    data += utils.xml_create_stop_tag(1, "Scripts")    
    
    for campaign in proj.campaigns :
        data += utils.xml_create_start_tag(1, "Campaign")        
        data += utils.xml_create_property(2, "Name", campaign.name)
        for script in campaign.scripts:
            data += _create_script(2, script.name, script.relativepath)
        data += utils.xml_create_stop_tag(1, "Campaign") 
        
    data += utils.xml_create_stop_tag(0, "Project")

    file = codecs.open(filename, "w", "utf-8")
    file.write(data)
    file.close()
    




if __name__ == "__main__":
    
    
    p = load_xml("..\\..\\..\\test\\script\\project_01.xml")
    print p


#
#    s1 = Script("script", ["ddd"])
#
#
#
#    s2 = Script("script", ["ddd"])
#
#    print s1.__hash__()
#    print s2.__hash__()
#    
#    d = {}
#    d[s1] = "my"
#    d[s2] = "my"
#    
#    print d



    