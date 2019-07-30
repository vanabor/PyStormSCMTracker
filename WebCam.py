# -*- coding: utf8 -*-   
'''
Created on Jan 5, 2012

@author: guilherme
'''
from cv2 import *
import numpy
from random import *
from bin.Rastreador import Rastreador

def find_connected_comp(mask,poly=1,perimScale=4,num=None,bbs=None,centers=None):
    mask = morphologyEx(mask, MORPH_OPEN , numpy.array(0))
    mask = morphologyEx(mask, MORPH_CLOSE ,numpy.array(0))
    c = findContours(numpy.array(binaria,numpy.uint8), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)[0]
    q = (mask.shape[0]+mask.shape[1])/perimScale
    out = []
    for co in range(len(c)):
        leng =  arcLength(c[co], False)
        if (leng>q):
            out.append(approxPolyDP(c[co], 2, False))
    mask -= mask
    fillPoly(mask, out, (255,255,255))
    return mask
'''
contours = []
ids = 1
'''
thChroma = 285
def onChange(value):
    global thChroma
    thChroma = value
namedWindow("Camera")
createTrackbar("chromaKey", "Camera", thChroma, 350, onChange)
cam = VideoCapture(0)
rastreador = Rastreador()


while(waitKey(33)<0):
    if(cam.grab()):
        img = cam.retrieve()[1]
        
        bgr = split(img)
        bgr[0] = bitwise_not(bgr[0])
        bgr[2] = bitwise_not(bgr[2])
        binaria = numpy.array(bgr[0],numpy.float32)+numpy.array(bgr[1],numpy.float32)
        binaria = threshold(binaria, thChroma, 255, THRESH_BINARY)[1]
        binaria = find_connected_comp(binaria)
        imshow("binaria", binaria)
        
        rastreador.updateModel(binaria,"")
        rastreador.drawContour(img)
                    
        imshow("Camera", img)


