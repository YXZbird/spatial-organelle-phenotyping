# Notebooks overview

This directory contains a three-stage analysis pipeline for image-based,
cell-level spatial phenotyping and exploratory machine learning analysis.

The notebooks are designed to be executed sequentially.

---

## 01_tile_qc_and_preprocessing.ipynb

**Purpose**
- Visual quality control and preprocessing at the image-tile level.
- Verify channel integrity, signal quality, and segmentation plausibility.

**Key operations**
- Load multichannel microscopy tiles.
- Generate RGB previews and boundary overlays.
- Tune segmentation-related parameters.
- Save QC figures for manual inspection.

**Output**
- QC figures saved to `figures/`
- No quantitative feature tables are generated at this stage.

---

## 02_cell_level_spatial_features.ipynb

**Purpose**
- Extract biologically interpretable, cell-level spatial features.

**Key operations**
- Segment cells using combined organelle channels.
- Segment nuclei from DAPI.
- Assign nuclei to cells and classify cells as mono- or multi-nuclear.
- Quantify spatial features describing radial distribution, perinuclear enrichment,
  intensity heterogeneity, and inter-organelle coupling.

**Output**
- Cell-level feature table:
  `data/toy_data/metadata/toy_cell_spatial_features__*.csv`
- QC figures illustrating segmentation and labeling.

---

## 03_ml_cell_vs_condition.ipynb

**Purpose**
- Exploratory machine learning analysis to assess whether spatial features
  distinguish experimental conditions (treated vs untreated).

**Key operations**
- Train Random Forest classifiers using cell-level features only.
- Enforce strict tile-level separation using stratified group cross-validation.
- Evaluate performance using out-of-fold predictions and confusion matrices.
- Identify informative features via Gini and permutation importance.
- Visualize feature space using UMAP or PCA (for intuition only).

**Output**
- Confusion matrices and feature-importance plots saved to `figures/`.
- No new feature tables are generated.

---

## Notes

- The pipeline is designed to minimize information leakage.
- Machine learning analyses are exploratory and interpretable;
  no predictive claims are made.

