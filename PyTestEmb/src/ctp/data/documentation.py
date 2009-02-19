# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"


import project
import utils

class Documentation:
    def __init__(self, name=""):
        self.name = name
        self.data = dict()
        
        
    def add_script(self, scriptdoc):
        self.data[scriptdoc.script.get_key()] = scriptdoc
        
        
    def get_sorted_key_list(self):
        l = list()
        for k,v in self.data.iteritems():
            l.append(v)
        l.sort()
        return l
    

    def __iter__(self):
        l = self.data.values()
        l.sort()
        return l 
        
        
        
class ScriptDoc:
    def __init__(self, script):
        self.script = script
             
    def __cmp__(self, other):
        return utils.cmp_string(self.script.str_relative(), other.script.str_relative())


class DocData:
    def __init__(self):
        self.fields = dict()
        

    

#
#fields = {}
#
#current = None
#
#for line in data2.splitlines(False):
#
#    line = line.strip(" ")
#
#    if line.startswith("@"):
#
#        current,sep,data = line.partition("::")
#
#        if sep != "::":
#
#            assert False
#
#        current = current.strip(" @\t")
#
#        data = data.strip(" \t")
#
#        fields[current] = []
#
#        fields[current].append(data)
#
#    else :
#
#        if current is not None :
#
#            data = line.strip(" \t")
#
#            fields[current].append(data)
#
#        else:
#
#            assert False
#
# 
#
# 
#
#for k,v in fields.iteritems():
#
#    print k
#
#    for item in v:
#
#        print "\t%s" % item





if __name__ == "__main__":
    
    
    s1 = project.Script("script_01", ["path01","path02"])
    s2 = project.Script("script_02", ["path01","path02"])
    s3 = project.Script("script_03", ["path01","path02"])

    
    d = Documentation()
    d.add_script(ScriptDoc(s1))
    d.add_script(ScriptDoc(s2))
    d.add_script(ScriptDoc(s3))


    for s in d:
        print d.script

  
        
        
        