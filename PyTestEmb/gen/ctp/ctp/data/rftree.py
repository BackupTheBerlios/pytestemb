# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : rftree for relative file tree
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import copy

import utils


# Behavior definition for node
B_ROOT  = "root"
B_DIR   = "directory"
B_FILE  = "file"



class Node:
    def __init__(self, key=None, data=None, behavior=None):
        self.lst_node = list()
        self.key = key
        self.data = data
        self.behavior = behavior
                
    def is_behavior(self, behavior):
        return (self.behavior==behavior)
    
    def add_node(self, node):
        self.lst_node.append(node)
        
    def delete_node(self, key, behavior):
        for node in self.lst_node:
            if      (node.key == key)\
                and (node.behavior == behavior):
                self.lst_node.remove(node)
                return True
        return False
    
    def set_data(self, data):
        self.data = data
        
    def get_data(self):
        return self.data
        
    def find_node(self, key, behavior):
        for node in self.lst_node:
            if      (node.key == key)\
                and (node.behavior == behavior):
                return node
        return None
    
    def sort(self):
        self.lst_node.sort()

    def __iter__(self):
        return self.lst_node.__iter__()                

    def __cmp__(self, other):
        assert False

    def __str__(self):
        return "Node \"%s\"" % self.key 




class Directory(Node):
    def __init__(self, name, path):
        Node.__init__(self, name, path, B_DIR)
        
    def __str__(self):
        return "Directory \"%s\"" % self.key 

    def __cmp__(self, other):
        if self.behavior != other.behavior :
            return -1
        else:
            return utils.cmp_string(self.key, other.key)
       
    

    
           
       
       
        
        
class File(Node):
    def __init__(self, name, data):
        Node.__init__(self, name, data, B_FILE)    
    
    def __str__(self):
        return "File \"%s\"" % self.key     

    def __cmp__(self, other):
        if self.behavior != other.behavior :
            return 1
        else:
            return utils.cmp_string(self.key, other.key)



class RfTree:
    def __init__(self):
        self.root = Node("root", None, B_ROOT)
        
    def get_rootnode(self):
        return self.root
    
    def _iter_sort(self, node):
        for n in node.lst_node:
            self._iter_sort(n)
            n.sort()
            
    def sort(self):
        self.root.sort()
        self._iter_sort(self.root) 
   
    
    def add_item(self, pathname, filename=None, data=None):
        """ pathname = list of directory """
        parent = self.root
        child = self.root
        
        for directory in pathname:
            child = parent.find_node(directory, B_DIR)
            if child is None :
                child = Directory(directory, pathname[:pathname.index(directory)])
                parent.add_node(child)  
            parent = child
            
        if filename is not None:
            child.add_node(File(filename, data))    


    def delete_item(self, pathname, filename=None):
        """ pathname = list of directory """
        parent = self.root
        child = self.root
        last = self.root
        
        for directory in pathname:
            parent = last
            child = parent.find_node(directory, B_DIR)
            if child is None :
                raise Exception()
            last = child

        if filename is None :
            parent.delete_node(child.key, B_DIR)
        else:
            child.delete_node(filename, B_FILE)




    def _get_list_item(self, node, lst, path):
        for n in node:
            if      n.is_behavior(B_DIR):
                path.append(n.key)
                self._get_list_item(n, lst, path)
                path.remove(n.key)
            if n.is_behavior(B_FILE) :
                lst.append((copy.copy(path), n.key))
        return lst  


    def get_list_item(self):
        lst = list() 
        path = list()
        return self._get_list_item(self.root, lst, path)
        
        
    
    def _pprint_node(self, node, depth=0):
        dis = ""
        for n in node:
            if      n.is_behavior(B_DIR) \
                or  n.is_behavior(B_ROOT):
                dis += "<D> %s%s\n" % ((" "*depth), n.key)
                dis += self._pprint_node(n, (depth+4))
            if n.is_behavior(B_FILE) :
                dis += "<F> %s%s\n" % ((" "*depth), n.key)  
        return dis  
    
    

    
    def pprint(self):
        """ pretty print """
        return self._pprint_node(self.root)
                        
        

        
        
            

        

if __name__ == "__main__":
    
    
    tree = RfTree()
    
    tree.add_item([], "devicelist")
    
    tree.add_item(["bluetooth"], "devicelist")
    tree.add_item(["bluetooth","fkt"], "devicelist")
    tree.add_item(["bluetooth","fkt"], "removedevice")
    tree.add_item(["bluetooth","fkt"], "adddevice")
    tree.add_item(["telephone"], "allocate")
    tree.add_item(["telephone"])
    tree.add_item(["diagjob"])

    tree.pprint()
    
    tree.sort()
    
    print tree.pprint()
    
    
    for l in tree.get_list_item():
        print l
    
    
#    tree.delete_item(["bluetooth"],"devicelist")
#    tree.pprint()


    pass





