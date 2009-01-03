



import time


class Gtime():

    __single = None
    
    def __init__(self):
        Gtime.__single = self       
        
        self.start_date = time.localtime()
        self.start_clock = time.clock()
        
    def get_time(self):
        return (time.clock() - self.start_clock)
    
    @staticmethod
    def create():
        if Gtime.__single is None :
            return Gtime()
        else:
            return Gtime.__single
        
        
        
        
        