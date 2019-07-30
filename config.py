# -*- coding: utf8 -*-

from os import path, mkdir


'''
Parametros a ser dado pelo usuário
TODO: Fazer uma tela para configurar o caminho do listenerpath e startar a
app (hide no systray).
'''
pathImagesEntrada = path.expanduser("~/ImagensEntrada/")
pathImagesSaida = path.expanduser("~/ImagensSaida/")
pathImagesSaidaProcessadas = pathImagesSaida + "processadas/"
pathImagesSaidaRaw = pathImagesSaida + "raw/"
pathLog = path.expanduser("~/.rastreadorNuvens/")

databaseFile = pathLog + "rastreador.db3"
listenerTimer = 5
imgTime = 2
UltimasList = 10

if (not path.exists(pathImagesEntrada)):
    mkdir(pathImagesEntrada)
if (not path.exists(pathImagesSaida)):
    mkdir(pathImagesSaida)
if (not path.exists(pathImagesSaidaProcessadas)):
    mkdir(pathImagesSaidaProcessadas)
if (not path.exists(pathImagesSaidaRaw)):
    mkdir(pathImagesSaidaRaw)
if (not path.exists(pathLog)):
    mkdir(pathLog)
