'''
Created on Jan 25, 2012

@author: guilherme
'''
from threading import Event, Thread

class Interval(Thread):
    def __init__(self,funcao,interval,interations = -1):
        Thread.__init__(self)
        self.interval = interval
        self.funcao = funcao
        self.interations = interations
        self.finish = Event()
    def run(self):
        count = 0
        while (not self.finish.is_set() and (self.interations > count or self.interations <=0)):
            if not self.finish.is_set():
                self.funcao()
                count += 1
            self.finish.wait(self.interval)
    def stop(self):
        self.finish.set()