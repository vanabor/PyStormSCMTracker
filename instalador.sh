#!/bin/bash

versao=`lsb_release -c | awk '{print $2}'`

if [ ! "$versao" = "natty" ] && [ ! "$versao" = "oneiric" ] && [ ! "$versao" = "quantal" ]; then
	echo "Desculpe, mas o software não está disponivel para esta versão de SO" 
	sleep 3
	exit 1
elif [ "`whoami`" = "root" ]; then
	echo " "
	echo "====================================================================="
	echo " Esse script não deve ser rodado com a permissão de sudo!"
	echo "====================================================================="
	sleep 3
	exit 1
else
	echo " "
	echo "=========================Rastreador de nuvens 0.3========================="
	echo " Durante a execução deste script, pode lhe ser solicitado acesso de root."
	echo "=========================================================================="
fi


echo "Removendo possiveis versões antigas..."
if [ "$versao" = "natty" ]; then
	sudo apt-get -y remove libopencv-dev python-opencv python-numpy > /dev/null
else
	sudo apt-get -y remove libcv-dev python-opencv python-numpy > /dev/null
fi

rm ~/.rastreadorNuvens/ -R  > /dev/null
rm ~/ImagensEntrada/ -R  > /dev/null
rm ~/ImagensSaida/ -R  > /dev/null

echo "Adicionando repositórios..."
echo " "
sudo add-apt-repository -y ppa:gijzelaar/cuda  > /dev/null
sudo add-apt-repository -y ppa:gijzelaar/opencv2.3 > /dev/null
echo " "

echo "Atualizando o sistema..."
sudo apt-get update > /dev/null

echo "Instalando pré-requisitos..."
if [ "$versao" = "natty" ]; then
	sudo apt-get -y install libopencv-dev python-opencv python-numpy > /dev/null
else
	sudo apt-get -y install libcv-dev python-opencv python-numpy > /dev/null
fi

echo "Fornecendo permissão para execução..."
sudo chmod +x * -R

echo "Criando diretórios..."
mkdir ~/.rastreadorNuvens/ -p -m 777
mkdir ~/ImagensEntrada/ -p -m 777
mkdir ~/ImagensSaida/processadas/ -p -m 777
mkdir ~/ImagensSaida/raw/ -p -m 777

echo "Criando banco de dados SQLite..."
cp rastreador.db3 ~/.rastreadorNuvens/

