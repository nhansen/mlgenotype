#.. image:: images/bioconda.png

**mlgenotype** lets you train random forest classifiers to recognize
structural variant genotypes in a sample's unaligned whole genome
sequencing reads. Once a classifier has been trained to genotype
a large deletion, insertion, or other more complex variant, users
can convert fastq- and bam-formatted whole genome sequences to feature
sets with the `mlgenofeatures <https://github.com/nhansen/mlgenofeatures>`
Snakemake workflow, and use those features, the model, and the mlgenotype
software to predict genotypes for samples.

Overview
========

Package distributions
---------------------

* `PyPi <https://pypi.org/project/mlgenotype/>`

Contributors
------------

* `Nancy F. Hansen <https://github.com/nhansen>`_
* Gracelyn Hill_
* Jennifer Lin_

Table of contents
=================

.. toctree::
   :includehidden:
   :maxdepth: 1

   faqs
   contributor/index
   developer/index
   tutorials/index


.. _conda: https://conda.io/en/latest/index.html
.. _`repository of recipes`: https://github.com/bioconda/bioconda-recipes
.. _`build system`: https://github.com/bioconda/bioconda-utils
.. _`repository of packages`: https://anaconda.org/bioconda/
.. _`conda package`: https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html
.. _`BioContainer`: https://biocontainers.pro
.. _`Quay.io`: https://quay.io/organization/biocontainers
