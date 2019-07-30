#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on Jan 25, 2012

@author: guilherme
'''
from os import listdir
from threading import Thread, Event
from cv2 import threshold, split, THRESH_BINARY, waitKey, imshow
from os import rename, remove
import time
from bin import config
from bin.Interval import Interval
from bin.Rastreador import Rastreador
from bin.Imagem import Imagem

'''
Podemos transformar isso numa classe
'''
rastreador = Rastreador()
UltimasImg = []


def Reader():
    for arq in listdir(config.pathImagesEntrada):
        '''
        TODO: Verificar no banco ao inves da pasta de saida....
        '''
        if (not (arq in listdir(config.pathImagesSaidaProcessadas))):
            print("Analisando: " + arq)
            starttime = time.clock()
            img = Imagem(config.pathImagesEntrada + arq)
            img.Carregar()
            binaria = threshold(split(img.data)[0], 180, 255, THRESH_BINARY)[1]
            waitKey(1000)
            rastreador.updateModel(binaria, img.ID)
            rastreador.drawContour(img.data)
            UltimasImg.append(img)
            img.Save(config.pathImagesSaidaProcessadas + arq)
            rename(config.pathImagesEntrada + arq, config.pathImagesSaidaRaw + arq)
            print ("Tempo de analise: " + str(time.clock() - starttime))
        else:
            remove(config.pathImagesEntrada + arq)
'''
Só serve para ficar visualizando a imagem na tela
Na aplicação final, ficará mandando para a viw...
'''


class Player(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.finish = Event()

    def run(self):
        while not self.finish.is_set():
            if len(UltimasImg) == 0:
                time.sleep(config.listenerTimer)
            else:
                if len(UltimasImg) > config.UltimasList:
                    UltimasImg.pop(0)
                if len(UltimasImg):
                    for imagem in UltimasImg:
                        imshow("win", imagem.data)
                        waitKey(10)
                        self.finish.wait(config.imgTime)

    def stop(self):
        self.finish.set()

t = Interval(Reader, config.listenerTimer)
r = Player()

t.start()
r.start()

r.join()
