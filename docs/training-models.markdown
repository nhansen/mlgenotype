---
layout: page
title: Training models
nav_order: 3
permalink: /training-models/
---

# Training random forest models

{: .warning }
> To use mlgenotype for creating a model and/or calling genotypes on actual sample BAM files, you'll first need to install both the SimSV snakemake package and the mlgenotype python module. See the section on [Installing mlgenotype]({{site.baseurl}}/installation) for instructions on installing these two packages.

The mlgenotype Python package can be used to train machine learning models to genotype any well-characterized structural variant, but first you'll need to simulate short reads and calculate features from them for each of the possible genotypes.  sing unaligned short read data (fastq or bam-formatted files), as well as to predict genotypes for samples using whole genome short read datasets.

