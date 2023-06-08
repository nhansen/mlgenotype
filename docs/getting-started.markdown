---
layout: page
title: Calling genotypes
nav_order: 2
permalink: /getting-started/
---

# Calling genotypes

{: .warning }
> To use mlgenotype for creating a model and/or calling genotypes on actual sample BAM files, you'll first need to install both the SimSV snakemake package and the mlgenotype python module. See the section on [Installing mlgenotype]({{site.baseurl}}/installation) for instructions on installing these two packages.


The mlgenotype Python package can be used to train machine learning models to genotype any well-characterized structural variant, but first one needs to simulate short reads and calculate features for each of the possible genotypes.  sing unaligned short read data (fastq or bam-formatted files), as well as to predict genotypes for samples using whole genome short read datasets.

