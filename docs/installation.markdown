---
layout: page
title: Installing mlgenotype
nav_order: 4
permalink: /installation/
---

# Installing the mlgenotype software

The easiest ways to install mlgenotype are from PyPi with Python's pip installer, or by using conda to install the bioconda mlgenotype package.

## Pip/PyPi

To install mlgenotype with Python's pip installer, first create a virtual environment. Then use pip install to install the latest version of mlgenotype:

python3 -m venv mlgeno_env
python3 -m pip install mlgenotype

## Conda
The mlgenotype package is also hosted on anaconda and available through the bioconda channel:

conda create -n mlgeno -c bioconda -c conda-forge mlgenotype
conda activate mlgeno
From github
If you prefer not to use a package manager, it also works to clone the github repository and run Python's setuptools installer:

git clone git://github.com/nhansen/mlgenotype
cd mlgenotype
python3 setup.py install
Note that installing from github requires you to first satisfy mlgenotype's software dependencies:

pandas >= 1.0
scikit-learn == 1.0.2

