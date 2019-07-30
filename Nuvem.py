'''
Created on Jan 6, 2012

@author: guilherme
'''

from cv2 import *
import numpy
import bin.config
from bin.banco import Banco

class Nuvem(object):
    
    def __init__(self):
        self.__shape = None
        self.contour = None
        self.Hits = []
        self.ID = None
        self.cor = None
        self.formacao = []
        self.x=0
        self.y=0
        self.area = 0
        self.centre =[]
        self.axes = []
        self.angle = []
        self.centroid = (None,None) 
        self.imagems = []
        self.db = Banco()
    
    
    def getWindowName(self):
        ret = str(self.ID)
        if (len(self.formacao) != 0):
            ret += "("
            for con in range(len(self.formacao)):
                ret += str(self.formacao[con])
                if (con+1 != len(self.formacao)):
                    ret += ","
            ret += ")"
        ret += " Contour"
        return ret
            
    def close(self):
        destroyWindow(self.getWindowName())
        
    def setShape(self,newShape):
        self.__shape = (newShape[0],newShape[1],1)
        
    def getShape(self):
        return self.__shape
    
    def updateContour(self,imagem):
        if (self.ID == None):
            self.ID = int(self.db.executeNonQuery("INSERT INTO nuvem VALUES(null)"))
            for formada in self.formacao:
                self.db.executeNonQuery("INSERT INTO nuvem_formacao VALUES("+str(self.ID)+","+str(formada)+")")
        if (self.countHits() == 1):
            self.contour = self.Hits[0]
            self.imagems = [imagem]
            self.area = contourArea(self.contour)*16
            m = moments(self.contour)
            if (m['m00'] != 0.0):
                self.centroid = (int(m['m10']/m['m00']),int(m['m01']/m['m00']))
            else:
                self.centroid = (None,None)
            if len(self.contour) >5:
                centre,axes,angle = fitEllipse(self.contour)
                self.centre = centre
                self.axes = axes
                self.angle = angle
            else:
                self.centre = (None,None)
                self.axes = (None,None)
                self.angle = None
            self.db.executeNonQuery("INSERT INTO imagem_nuvem VALUES (null,"+
                               str(imagem)+
                               ","+str(self.ID)+
                               ","+str(self.centroid[0] or "null")+
                               ","+str(self.centroid[1] or "null")+
                               ","+str(self.centre[0] or "null")+
                               ","+str(self.centre[1] or "null")+
                               ","+str(self.angle or "null")+
                               ","+str(self.axes[0] or "null")+
                               ","+str(self.axes[1] or "null")+
                               ","+str(self.area or "null")+
                               ")")
    def addHit(self,contour):
        self.Hits.append(numpy.copy(contour))
        
    def cleanHits(self):
        self.Hits = []
        
    def countHits(self):
        return len(self.Hits)

    def isHit(self,newContours):
        if (self.contour == None):
            return False
        img = numpy.zeros(self.__shape,numpy.uint8)
        imgNew = numpy.zeros(self.__shape,numpy.uint8)
        fillPoly(img, [self.contour], (255,255,255))
        fillPoly(imgNew, [newContours], (255,255,255))
        img = bitwise_and(img, imgNew)
        imgNew = numpy.copy(img)
        rects = findContours(img, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)[0]
        if (len(rects) != 0):
            return True
        else:
            return False
    def __del__(self):
        pass
        '''
        arq = open(config.pathImagesSaidaNuvens+str(self.ID)+".txt","w")
        arq.write("Nuvem ID:\t"+str(self.ID)+"\n")
        arq.write("Imagens:\t"+str(self.imagems)+"\n")
        arq.write("Formacao:\t"+str(self.formacao)+"\n")
        arq.write("Area:\t"+str(self.area)+"\n")
        arq.write("Centroid:\t"+str(self.centroid)+"\n")
        arq.write("Centro da elipse:\t"+str(self.centre)+"\n")
        arq.write("Angulo da elipse:\t"+str(self.angle)+"\n")
        arq.write("Eixos da elipse:\t"+str(self.axes)+"\n")
        arq.close()
        '''