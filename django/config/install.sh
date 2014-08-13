#!/bin/bash

#Bash stop if some command fails
set -e 
set -o pipefail

#Install dependencies programs
wget https://pypi.python.org/packages/source/s/setuptools/setuptools-1.1.6.tar.gz#md5=ee82ea53def4480191061997409d2996
tar -xvf setuptools-1.1.6.tar.gz
cd setuptools-1.1.6
python ez_setup.py
easy_install pip

#Install django
pip install -U django==1.5.4
pip install pillow
