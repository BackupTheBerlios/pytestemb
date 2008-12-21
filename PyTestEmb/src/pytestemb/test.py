

import inspect


def finspect():
    lst = inspect.stack()
    try :
        for l in lst:
            print "%s" % l.__str__()
    finally:
        del lst
        
        
def func1():
    func2()

def func2():
    func3()
    
def func3():
    finspect()
    
    
    
func1()