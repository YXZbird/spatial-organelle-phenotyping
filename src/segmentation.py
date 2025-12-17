import numpy as np
from dataclasses import asdict
from skimage.filters import threshold_otsu
from skimage.morphology import disk, binary_closing, binary_opening, remove_small_objects
from skimage.measure import label, regionprops
from skimage.segmentation import watershed
from scipy import ndimage as ndi

def threshold_image(img2d: np.ndarray, method: str = "otsu", percentile: float = 99.0) -> np.ndarray:
    img2d = img2d.astype(np.float32)
    if img2d.max() <= 0:
        return np.zeros_like(img2d, dtype=bool)
    if method == "otsu":
        thr = threshold_otsu(img2d)
    elif method == "percentile":
        thr = np.percentile(img2d, percentile)
    else:
        raise ValueError(f"Unknown threshold_method: {method}")
    return img2d > thr

def segment_nuclei(dapi2d: np.ndarray,
                   threshold_method: str = "otsu",
                   percentile: float = 99.0,
                   min_area: int = 200,
                   max_area: int | None = None,
                   closing_radius: int = 2,
                   opening_radius: int = 1,
                   split_touching: bool = True,
                   distance_transform_sigma: float = 1.0,
                   min_peak_distance: int = 8) -> np.ndarray:
    """
    Returns labeled nuclei mask (0=background, 1..N nuclei).
    """
    mask = threshold_image(dapi2d, method=threshold_method, percentile=percentile)

    if closing_radius and closing_radius > 0:
        mask = binary_closing(mask, disk(closing_radius))
    if opening_radius and opening_radius > 0:
        mask = binary_opening(mask, disk(opening_radius))

    mask = remove_small_objects(mask, min_size=max(1, int(min_area)))

    if not split_touching:
        lab = label(mask)
        return _filter_by_area(lab, min_area=min_area, max_area=max_area)

    # Split touching nuclei: distance transform + watershed
    dist = ndi.distance_transform_edt(mask)
    if distance_transform_sigma and distance_transform_sigma > 0:
        dist = ndi.gaussian_filter(dist, sigma=distance_transform_sigma)

    # Local maxima markers
    footprint = np.ones((min_peak_distance, min_peak_distance), dtype=bool)
    peaks = (dist == ndi.maximum_filter(dist, footprint=footprint)) & (dist > 0)
    markers = label(peaks)

    lab = watershed(-dist, markers, mask=mask)
    lab = _filter_by_area(lab, min_area=min_area, max_area=max_area)
    return lab

def _filter_by_area(lab: np.ndarray, min_area: int, max_area: int | None) -> np.ndarray:
    out = np.zeros_like(lab, dtype=np.int32)
    nid = 1
    for r in regionprops(lab):
        a = r.area
        if a < min_area:
            continue
        if max_area is not None and a > max_area:
            continue
        out[lab == r.label] = nid
        nid += 1
    return out

def count_nuclei(lab: np.ndarray) -> int:
    return int(lab.max())

def nuclei_centroids(lab: np.ndarray) -> np.ndarray:
    """
    Return centroids array of shape (N,2) with (row, col).
    """
    cents = []
    for r in regionprops(lab):
        cents.append(r.centroid)
    return np.array(cents, dtype=np.float32)
