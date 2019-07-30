'''
Created on Dec 16, 2011

@author: guilherme
'''
from cv2 import *
class ProvedorImages(object):
    capture = None
    def __init__(self):
        self.capture = VideoCapture(0)
    def next(self):
        if self.capture.grab():
            return self.capture.retrieve(); 