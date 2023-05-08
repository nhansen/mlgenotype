# mlgenotype

This python package can be used to train machine learning models to genotype structural variants using unaligned short read data, as well as to predict genotypes for samples using whole genome short read datasets.

The software was written by Nancy Fisher Hansen, a staff scientist in the Computational and Statistical Genomics Branch of NHGRI, beginning with code written by Gracelyn Hill and Jennifer C Lin.  Nancy can be reached at nhansen@mail.nih.gov.

## Install

The easiest ways to install mlgenotype are from [PyPi](https://pypi.org/project/mlgenotype/) with Python's pip installer, or by using conda to install the [bioconda](https://bioconda.github.io/) mlgenotype package.

### Pip/PyPi

```
python3 -m venv mlgeno_env
python3 -m pip install mlgenotype
```

### Conda

```
conda create -n mlgeno mlgenotype
conda activate mlgeno
```

## From github:

```
git clone git://github.com/nhansen/mlgenotype
```

Note that installing from github requires you to first satisfy mlgenotype's software dependencies:

- pandas >= 1.0
- scikit-learn == 1.0.2


