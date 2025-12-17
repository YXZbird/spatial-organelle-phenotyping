# src – Core analysis modules

This directory contains the core Python modules that implement the reusable
components of the image-based spatial phenotyping pipeline.

The code in this directory is designed to be imported and executed by the
analysis notebooks in `notebooks/`.

---

## Design principles

- Modular and reusable functions.
- Clear separation between configuration, preprocessing, segmentation,
  feature computation, and visualization.
- No hard-coded dataset paths or experimental labels.
- Deterministic behavior given fixed parameters and random seeds.

---

## Module overview

### `config.py`

**Purpose**
- Centralized configuration container for the pipeline.

**Contents**
- Path definitions (data, metadata, figures).
- Channel mappings and preview settings.
- Segmentation and preprocessing parameters.

**Notes**
- All tunable parameters are exposed here to avoid scattering constants
  across notebooks.
- Notebooks should modify configuration values, not internal module logic.

---

### `io_utils.py`

**Purpose**
- Input/output utilities for image and filesystem handling.

**Contents**
- Multichannel TIFF loading.
- Directory creation and path safety checks.

**Notes**
- No preprocessing or normalization is performed at this stage.
- All image arrays are returned in a consistent `(C, Y, X)` format.

---

### `preprocess.py`

**Purpose**
- Low-level image preprocessing utilities.

**Contents**
- Intensity normalization.
- Gamma correction.
- Gaussian smoothing.

**Notes**
- Preprocessing functions are intentionally minimal and composable.
- Applied selectively depending on downstream segmentation requirements.

---

### `segmentation.py`

**Purpose**
- Image segmentation primitives.

**Contents**
- Nucleus segmentation from DAPI.
- Morphological post-processing.
- Optional splitting of touching objects.

**Notes**
- Segmentation functions operate purely on image data and parameters.
- No assumptions are made about experimental condition or cell class.

---

### `features.py`

**Purpose**
- Computation of biologically interpretable spatial features.

**Contents**
- Radial distance-based metrics.
- Perinuclear enrichment measures.
- Intensity heterogeneity descriptors.
- Inter-organelle coupling metrics.

**Notes**
- Feature definitions are deterministic and cell-centric.
- Functions are designed to be composable and easily extended.

---

### `viz.py`

**Purpose**
- Visualization utilities for QC and exploratory analysis.

**Contents**
- RGB rendering from multichannel images.
- Boundary overlays for segmentation QC.

**Notes**
- Visualization is intended for qualitative assessment only.
- No analysis logic is embedded in plotting functions.

---

## Scope and limitations

- Modules in this directory are not intended to be a general-purpose library.
- The focus is clarity, reproducibility, and interpretability rather than
  maximal performance.
- Machine learning models are implemented in notebooks, not in `src/`,
  to maintain a clear separation between data processing and analysis logic.

---

## Reproducibility

- All functions are deterministic given identical inputs and parameters.
- Randomness, where applicable, is controlled at the notebook level.

