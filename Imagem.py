'''
Created on Oct 5, 2011

@author: guilherme
'''

from cv2 import *
from PIL import Image
import numpy
from bin.banco import Banco


class Imagem(object):
    Caminho = ""
    DiaJuliano = 0
    Ano = 0
    Aquisicao = ""
    Orbita = ""
    Sensor = ""
    Produto = ""
    ResolucaoEspacial = ""
    ResolucaoEspectral = ""
    data = None

    def __init__(self, caminho):
        self.Caminho = caminho
        self.db = Banco()
        self.ID = self.db.executeNonQuery("INSERT INTO imagens VALUES (null,'" + caminho.split("/")[-1] + "',datetime('" + self.caminho2datetime() + "'))")

    def Open(self, Caminho=None):
        if (not (Caminho is None)):
            self.Caminho = Caminho
        self.Carregar()

    def Carregar(self):
        self.data = imread(self.Caminho)
        if (self.data is None):
            self.data = Image.open(self.Caminho)
            self.data = numpy.asarray(self.data)
        canais = split(self.data)
        if (len(canais) == 1):
            canais = numpy.array(canais)[0]
            canais = (canais, canais, canais)
            self.data = merge(canais)

    def Save(self, caminho=None):
        if(caminho is not None):
            self.Caminho = caminho
        self.Descarregar()

    def caminho2datetime(self):
        caminho = self.Caminho.split("/")[-1]
        return "20" + caminho[:2] + "-" + caminho[2:4] + "-" + caminho[4:6] + " " + caminho[6:8] + ":" + caminho[8:10]

    def Descarregar(self):
        try:
            imwrite(self.Caminho, self.data)
        except:
            img = Image.fromarray(self.data)
            img.save(self.Caminho)

    def demarcarRoi(self, points):
        pass

    def recortarImagem(self, points):
        pass

    def __del__(self):
        pass
