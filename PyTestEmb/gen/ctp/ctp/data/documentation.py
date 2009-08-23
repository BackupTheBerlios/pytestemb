# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : -
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import copy
import shelve


import project
import utils




class Documentation:
    def __init__(self, name=""):
        self.name = name
        self.data = dict()
        
    def save(self, filename):
        s = shelve.open(filename, writeback=True)
        try:
            # erase
            for k,v in s.iteritems():
                del s[k]                
            # save
            for k,v in self.data.iteritems():
                d = dict()
                d["status"]  = (v.get_status()[0] == ST_PARSE_DOC_NO_ERROR, v.get_status()[1])
                d["doc"]  = v.data
                d["name"] = v.script.get_name()
                d["path"] = v.script.get_path()
                s[str(k)] = d
        finally:
            s.close()


    def load(self, filename):
        s = shelve.open(filename, writeback=False)
        try:
            for k,v in s.iteritems():
                self.data[k] = v
        finally:
            s.close()

    def update(self, scriptdoc):
        self.data[scriptdoc.script.get_key()] = scriptdoc


    def get_sorted_key_list(self):
        l = list()
        for k,v in self.data.iteritems():
            l.append(v)
        l.sort()
        return l



    def __str__(self):
        dis = ""
        for script in self.data.itervalues():
            dis += "%s\n" % script
        return dis







ST_PARSE_NOT_YET_PARSE   = 0
ST_PARSE_DOC_NO_ERROR    = 1
ST_PARSE_FILE_ERROR      = 2
ST_PARSE_PY_ERROR        = 3
ST_PARSE_INT_ERROR       = 4
ST_PARSE_FORMAT_ERROR    = 5


SCRIPT_STATUS = {   ST_PARSE_NOT_YET_PARSE   : "Script has not been parse",\
                    ST_PARSE_DOC_NO_ERROR    : "Script parsed, no error",\
                    ST_PARSE_FILE_ERROR      : "Script parsed, error : problem with script file",\
                    ST_PARSE_PY_ERROR        : "Script parsed, error : python error",\
                    ST_PARSE_INT_ERROR       : "Script parsed, error : internal error",\
                    ST_PARSE_FORMAT_ERROR    : "Script parsed, error : format error"}


class ScriptDoc:
    def __init__(self, script):
        self.script = script

        self.set_status(ST_PARSE_NOT_YET_PARSE)
        self.data = list()


    def get_status(self):
        return self.status

    def set_status(self, status, param=None):
        self.status = [status, param]


    def import_doctstdoutreader(self, resreader):
        self.data = copy.copy(resreader.data)
        self.set_status(ST_PARSE_DOC_NO_ERROR)

    def __cmp__(self, other):
        return utils.cmp_string(self.script.str_relative(), other.script.str_relative())





if __name__ == "__main__":
    

    d = Documentation()
    
    d.load("doc.dbm")
    
    
    print "%s" % d 
    





