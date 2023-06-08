---
layout: default
title: Home
nav_order: 1
description: "MLgenotype Introductory Page"
permalink: /
---

# MLgenotype: software for genotyping SVs using short read sequencing data

## About this project

Our efforts to use machine learning to classify known Alpha Thalassemia deletions using short read data
began in Dr. James Mullikin's Comparative Genomics Analysis Unit (CGAU) at NHGRI in 2018. In collaboration with members of Charles Rotimi's and Swee Lay Thein's groups at NIH, Dr. Mullikin's postdoctoral fellow Zhi Liu conducted a pilot project using convolutional neural networks (CNNs), and then two CGAU summer students, Gracelyn Hill and Jennifer Lin, built, trained, and tested machine learning models under the supervision of Dr. Nancy Hansen.

Our primary aim was to test the hypothesis that simulated short-read sequence data could sufficiently mimic real data in the vicinity of hard-to-map but variable regions of the genome, enabling us to train classifiers that are accurate in genotyping structural variants in real samples, even in the absence of large "known truth" datasets.

[Alpha thalassemia genotyping]({{site.baseurl}}/quickstart-alphathal/){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }

## Training classifiers to recognize large insertions and deletions

Software for genotyping large insertions and deletions using short read sequence data (e.g., reads less than a few hundred bases in length, like those produced by the Illumina platform) is often inaccurate due to inability to accurately map shorter reads in repetitive regions of a genome. Traditional variant detection software typically relies on accurate read mapping, and so performs better or worse on different variants, depending on their genomic context.

An alternative approach to genotyping known, large variation in a genome is to train machine learning classifiers to recognize features in short read sequence datasets that depend on a sample's variant genotype, but not on the specifics of how its reads align. Ideally, these features would be accurately captured by simulated read data, so that large amounts of training data could be generated even for rare variants.

The SimSV Snakemake-based software distribution allows users to generate simulated read features for genotypes of interest. With those features, users can train machine learning classifiers using the scripts distributed with the mlgenotype python module. Once a model has been trained, SimSV can then be used again to calculate features from actual samples' short read data, and those features can be used to predict those samples' genotypes.

[Training models]({{site.baseurl}}/training-models){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }

## Calling genotypes on short read fastq or BAM files

Once a model has been trained to recognize different genotypes for your variant of interest, the same SimSV Snakemake file can be used to generate features for sequence reads from actual samples. These features can then be used along with a previously-trained model to predict each sample's genotype.

[Calling genotypes]({{site.baseurl}}/getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }




