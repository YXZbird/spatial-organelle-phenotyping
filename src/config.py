from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple

# =====================================================
# Robust project root detection (DO NOT CHANGE IN NOTEBOOKS)
# =====================================================
# This file must be located at: <PROJECT_ROOT>/src/config.py
_THIS_FILE = Path(__file__).resolve()

if _THIS_FILE.parent.name != "src":
    raise RuntimeError(
        f"config.py must live in a 'src/' directory, got {_THIS_FILE.parent}"
    )

PROJECT_ROOT = _THIS_FILE.parent.parent

# Hard sanity check
if not (PROJECT_ROOT / "data").exists():
    raise RuntimeError(
        f"Resolved PROJECT_ROOT={PROJECT_ROOT}, but 'data/' not found. "
        "Repository structure is inconsistent."
    )

# =====================================================
# Paths (single source of truth)
# =====================================================
@dataclass
class Paths:
    toy_images_dir: Path = PROJECT_ROOT / "data" / "toy_data" / "images"
    toy_metadata_dir: Path = PROJECT_ROOT / "data" / "toy_data" / "metadata"
    figures_dir: Path = PROJECT_ROOT / "figures"


# =====================================================
# Preprocessing parameters
# =====================================================
@dataclass
class PreprocessParams:
    apply_gamma: bool = True
    gamma: float = 0.9
    gaussian_sigma: float = 1.0


# =====================================================
# Nucleus segmentation parameters
# =====================================================
@dataclass
class NucleusSegParams:
    dapi_channel: int = 0

    threshold_method: str = "otsu"     # "otsu" or "percentile"
    percentile: float = 99.0

    min_area: int = 200
    max_area: Optional[int] = None
    closing_radius: int = 2
    opening_radius: int = 1

    split_touching: bool = True
    distance_transform_sigma: float = 1.0
    min_peak_distance: int = 8


# =====================================================
# Radial coupling / spatial feature parameters
# =====================================================
@dataclass
class CouplingParams:
    channel_a: int = 1
    channel_b: int = 2
    n_radial_bins: int = 12
    max_radius_px: Optional[int] = None


# =====================================================
# RGB preview parameters (visualisation only)
# =====================================================
@dataclass
class PreviewRGB:
    rgb_channels: Tuple[int, int, int] = (1, 2, 0)


# =====================================================
# Unified pipeline configuration
# =====================================================
@dataclass
class PipelineConfig:
    paths: Paths = Paths()
    preprocess: PreprocessParams = PreprocessParams()
    nucleus: NucleusSegParams = NucleusSegParams()
    coupling: CouplingParams = CouplingParams()
    preview: PreviewRGB = PreviewRGB()
