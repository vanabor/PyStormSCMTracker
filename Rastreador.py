# -*- coding: utf8 -*- 
'''
Created on Jan 22, 2012

@author: guilherme
'''
import numpy
from bin.Nuvem import Nuvem
from random import randrange
from cv2 import *

class Rastreador(object):
    contours = []
    def __init__(self):
        self.contours = []
    
    def updateModel(self,binaria,imagem):
        c = findContours(numpy.array(binaria,numpy.uint8), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)[0]
        for cNew in c:
            hit = []
            for cOld in self.contours:
                if (cOld.isHit(cNew)):
                    cOld.addHit(cNew)
                    hit.append(cOld)
            nHits = len(hit)
            if (nHits == 0):
                #print("Novo!")
                newNuvem = Nuvem()
                newNuvem.setShape(binaria.shape)
                newNuvem.addHit(cNew)
                newNuvem.cor = [randrange(0,256),randrange(0,256),randrange(0,256)]
                self.contours.append(newNuvem)
            elif nHits > 1:
                #print("Novo! Agrupar!!")
                newNuvem = Nuvem()
                newNuvem.setShape(binaria.shape)
                newNuvem.addHit(cNew)
                newNuvem.cor = [randrange(0,256),randrange(0,256),randrange(0,256)]
                self.contours.append(newNuvem)
                for cOld in hit:
                    cOld.close()
                    newNuvem.formacao.append(cOld.ID)
                    self.contours.remove(cOld)
        for cOld in self.contours:
            if (cOld.countHits() == 0):
                #print("Delete: "+str(cOld.ID))
                cOld.close()
                self.contours.remove(cOld)
                
        contoursNew = []
        contoursRemove = []
        
        for cOld in self.contours:
            if (cOld.countHits() == 1):
                cOld.updateContour(imagem)
            else:
                for cNew in cOld.Hits:
                    #print("Novo!")
                    newNuvem = Nuvem()
                    newNuvem.setShape(binaria.shape)
                    newNuvem.addHit(cNew)
                    newNuvem.cor = [randrange(0,256),randrange(0,256),randrange(0,256)]
                    newNuvem.formacao.append(cOld.ID)
                    newNuvem.updateContour(imagem)
                    newNuvem.cleanHits()
                    contoursNew.append(newNuvem)
                cOld.close()
                contoursRemove.append(cOld)
            cOld.cleanHits()
        
        for cOld in contoursRemove:
            self.contours.remove(cOld)
        self.contours += contoursNew

    def drawContour(self,img):
        for c in self.contours:
            if (c.contour != None):
                '''
                if(c.centre != []):
                    help(ellipse)
                    ellipse(img, c.centre[-1], c.axes[-1], c.angle[-1], 0, 360, c.cor)
                '''
                fillPoly(img, [c.contour], c.cor)
                if (c.centroid != (None,None)):
                    circle(img, c.centroid, 5, [255,255,255],-1)
            else:
                print("Contour: ")
                print (c.contour)
            
    
    