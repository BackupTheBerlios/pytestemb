# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : utils gathered some utils function
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.2 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import os
import sys












import codecs
import types


def to_unicode(instr):
    if type(instr) == types.UnicodeType:
        return instr
    else:
        return codecs.decode(instr, "utf-8")


def get_script_name():
    return os.path.splitext(os.path.split(sys.argv[0])[1])[0]



def str_dict(d):
    res = []
    for k,v in d.iteritems():
        l = u"'%s':'%s'" % (unicode(k), unicode(v))
        res.append(l)
    return u"{%s}" % ", ".join(res)






