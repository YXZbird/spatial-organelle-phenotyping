# Image-based Spatial Phenotyping Pipeline

A reproducible pipeline for cell-level spatial phenotyping from multichannel
microscopy images, combining interpretable feature extraction with exploratory
machine learning analysis.

---

## Overview

This project implements a modular, notebook-driven workflow for analyzing
organelle spatial organization at the single-cell level. The pipeline focuses
on **interpretable spatial features** rather than end-to-end prediction, and
is designed to minimize information leakage while maximizing biological clarity.

### Key characteristics

- Cell-first spatial feature extraction  
- Explicit nucleus–cell assignment  
- Strict separation between data processing and analysis  
- Conservative, interpretable machine learning  
- Emphasis on reproducibility and transparency  

---

## Pipeline structure

The analysis is organized into three sequential notebooks:

01 → 02 → 03


### 01. Tile-level QC and preprocessing

Visual inspection and parameter tuning to ensure segmentation quality and
signal integrity at the image-tile level.

### 02. Cell-level spatial feature extraction

Segmentation of cells and nuclei, nucleus-to-cell assignment, classification
of mono- vs multi-nuclear cells, and extraction of biologically interpretable
spatial features.

### 03. Exploratory machine learning analysis

Assessment of whether extracted spatial features distinguish experimental
conditions (e.g. treated vs untreated) using Random Forest classifiers under
strict tile-level cross-validation.

> **Important**  
> Machine learning analyses are exploratory and interpretable.  
> No predictive performance claims are made.

---

## Repository layout

image-based-phenotyping-pipeline/
├─ notebooks/ # Analysis notebooks (01–03)
├─ src/ # Reusable core modules
├─ data/ # Input images and derived metadata
├─ figures/ # Automatically generated figures
└─ README.md # This file


Each subdirectory contains its own `README.md` describing scope, structure,
and interpretation.

---

## Core concepts

### Cell-first analysis

Cells are segmented independently of experimental condition. All spatial
features are computed **without access to treated/untreated labels**.

### Spatial feature design

Features are defined to capture:

- Radial distribution of organelle signal  
- Perinuclear enrichment  
- Intensity heterogeneity  
- Inter-organelle spatial coupling  

All features are deterministic and biologically interpretable.

### Leakage-aware evaluation

Experimental condition labels are encoded at the **tile level**. Machine
learning analyses use stratified group cross-validation to prevent information
leakage across tiles.

---

## Data and outputs

### Input

- Multichannel TIFF image tiles  
- Experimental condition encoded at folder (tile) level  

### Outputs

- Cell-level feature tables (`.csv`)  
- QC figures  
- Exploratory statistical and machine learning visualizations  

All outputs are generated automatically by the notebooks and saved to
structured directories.

The included toy dataset (treated / untreated TIFF tiles) is provided solely for pipeline testing and demonstration purposes.
---

## Reproducibility

- All parameters are centralized and explicitly logged.  
- Random seeds are fixed where applicable.  
- Results are reproducible given identical input data and environment.  

---

## Scope and limitations

- The pipeline is intended for method development and exploratory analysis.  
- The provided dataset is a small-scale example.  
- Machine learning results reflect feature separability under the current
  sample size and should not be over-interpreted.  

---

## Intended use

This project is suitable for:

- Methodological development in spatial cell biology  
- Teaching or demonstration of leakage-aware machine learning analysis  
- Extension to larger or more complex imaging datasets  

It is **not** intended as a turnkey predictive model.

---

## Acknowledgements

This pipeline was developed to support research into spatial organization of
intracellular organelles and nucleus-associated phenotypes, with an emphasis
on interpretability and reproducible analysis.
