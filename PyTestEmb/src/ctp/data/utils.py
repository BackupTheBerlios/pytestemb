# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : utils gathers all util function
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.2 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"





import os
import os.path



def split_fullpath(fullpath):
    """ fulltpath = path/filename.ext
        return (path, filename, ext)
     """
    path, filenameext = os.path.split(fullpath)
    filename, ext = os.path.splitext(filenameext)
    return (path, filename, ext.strip(".") )



def extract_relative(absolutepath1, absolutepath2):
    """ absolutepath1 = basepath
    absolutepath2 = basepath/subpath
    return (subpath)
    """
    len_1 = len(absolutepath1)
    len_2 = len(absolutepath2)
    if len_1 > len_2 :
        raise Exception("Incorrect base path")  
    if absolutepath1 != absolutepath2[:len_1]:
        raise Exception("Incorrect base path")  
    return absolutepath2[len_1:].strip(os.sep)
    
    
    
    
def cmp_string(str1, str2):
    """ function used for sorting """
    if str1 == str2 :
        return 0
    elif str1 > str2 :
        return 1
    else :
        return -1
    
    
    
    
    
XML_SIZE_INDENT = 4
XML_RETURN_CAR = u"\n"


def xml_indent(level):
    return (u" " * XML_SIZE_INDENT * level)
    
def xml_create_header():
    return u'<?xml version="1.0" encoding="UTF-8"?>%s' % XML_RETURN_CAR   

def xml_create_start_tag(level, name):
    return u"%s<%s>%s" % (xml_indent(level), name, XML_RETURN_CAR)

def xml_create_stop_tag(level, name):
    return u"%s</%s>%s" % (xml_indent(level), name, XML_RETURN_CAR)

def xml_create_property(level, name, value):
    return u"%s<%s>%s</%s>%s" % (xml_indent(level), name, value, name , XML_RETURN_CAR)    
    

