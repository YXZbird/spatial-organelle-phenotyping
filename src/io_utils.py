from pathlib import Path
from typing import List
import numpy as np
import tifffile as tiff


# ------------------------------------------------------------
# Project root resolution
# ------------------------------------------------------------
def get_project_root() -> Path:
    """
    Return the project root directory.
    Assumes this file lives in <project_root>/src/io_utils.py
    """
    return Path(__file__).resolve().parents[1]


# ------------------------------------------------------------
# Listing toy-data tiles
# ------------------------------------------------------------
def list_toy_tiles(
    toy_images_dir: str | Path,
    pattern_prefix: str = "tile_",
    recursive: bool = True
) -> List[str]:
    """
    Discover multi-channel TIFF tiles in the toy data directory.

    Features:
    - Interprets relative paths with respect to project root
    - Supports .tif / .tiff (case-insensitive)
    - Optional recursive search
    - Excludes RGB preview files (*_RGB.png)
    - Returns sorted list of absolute file paths (as strings)

    Parameters
    ----------
    toy_images_dir : str or Path
        Directory containing toy image tiles (relative to project root or absolute).
    pattern_prefix : str
        Filename prefix to match (default: 'tile_').
    recursive : bool
        Whether to search subdirectories recursively.

    Returns
    -------
    List[str]
        Sorted list of tile file paths.
    """
    project_root = get_project_root()
    base = Path(toy_images_dir)

    # Resolve relative paths against project root
    if not base.is_absolute():
        base = (project_root / base).resolve()
    else:
        base = base.resolve()

    if not base.exists():
        return []

    exts = {".tif", ".tiff"}
    iterator = base.rglob("*") if recursive else base.glob("*")

    tiles = []
    for p in iterator:
        if not p.is_file():
            continue

        # extension check (case-insensitive)
        if p.suffix.lower() not in exts:
            continue

        # exclude RGB previews
        if p.name.lower().endswith("_rgb.png"):
            continue

        # optional filename prefix
        if pattern_prefix and not p.name.startswith(pattern_prefix):
            continue

        tiles.append(str(p))

    return sorted(tiles)


# ------------------------------------------------------------
# Reading / writing multi-channel TIFF
# ------------------------------------------------------------
def read_multichannel_tif(path: str | Path) -> np.ndarray:
    """
    Read a TIFF file and return an array of shape (C, Y, X).

    Accepts:
    - (Y, X) single-channel → converted to (1, Y, X)
    - (C, Y, X) multi-channel

    Raises an error for unsupported shapes.
    """
    arr = tiff.imread(str(path))
    arr = np.asarray(arr)

    if arr.ndim == 2:
        return arr[None, ...]  # (1, Y, X)

    if arr.ndim == 3:
        return arr  # assume (C, Y, X)

    raise ValueError(f"Unsupported TIFF shape {arr.shape} in file {path}")


def save_multichannel_tif(path: str | Path, cyx: np.ndarray) -> None:
    """
    Save a (C, Y, X) array as a multi-channel TIFF.
    """
    cyx = np.asarray(cyx)
    if cyx.ndim != 3:
        raise ValueError("save_multichannel_tif expects array of shape (C, Y, X)")
    tiff.imwrite(str(path), cyx, photometric="minisblack")


# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------
def ensure_dir(path: str | Path) -> None:
    """
    Create directory if it does not exist.
    """
    Path(path).mkdir(parents=True, exist_ok=True)
