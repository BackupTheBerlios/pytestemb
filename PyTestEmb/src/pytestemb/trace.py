# -*- coding: UTF-8 -*-
###########################################################
# Project  : PyTestEmb                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 01/12/08                                     #
###########################################################


__version__ = "$Revision: 1.1 $"
__author__ = "$Author: octopy $"



import sys


class Trace:
    def __init__(self):
        pass

    def trace_msg(self, msg):
        pass



class TraceOctopylog(Trace):
    
    def __init__(self):
        Trace.__init__(self)
        
        import logging
        import logging.handlers
        socketHandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        rootLogger = logging.getLogger("")
        rootLogger.setLevel(logging.DEBUG)
        rootLogger.addHandler(socketHandler)
        self.logger = logging.getLogger("pyvalid")

    def __del__(self):
        pass

    def trace_msg(self, msg):
        self.logger.info("%s\n" % msg)




class TraceStdout(Trace):
    
    def __init__(self):
        Trace.__init__(self)
        

    def trace_msg(self, msg):
        sys.stdout.write("%s\n" % msg)





def create(interface):
    
    if   interface == "none" :
        return Trace()
    elif interface == "octopylog":
        return TraceOctopylog()
    elif interface == "stdout":
        return TraceStdout()
    else:
        assert False
    
    
    
    
    