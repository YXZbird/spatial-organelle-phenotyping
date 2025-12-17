import numpy as np

def radial_distance_map(center_rc: tuple[float, float], shape: tuple[int, int]) -> np.ndarray:
    rr, cc = np.indices(shape)
    r0, c0 = center_rc
    return np.sqrt((rr - r0) ** 2 + (cc - c0) ** 2).astype(np.float32)

def organelle_perinuclear_ratio(signal2d: np.ndarray, center_rc: tuple[float, float],
                                r_inner: float = 20.0, r_outer: float = 80.0) -> float:
    """
    Ratio of signal within r_inner vs in annulus (r_inner..r_outer).
    Toy-friendly metric for center vs periphery bias.
    """
    d = radial_distance_map(center_rc, signal2d.shape)
    inner = signal2d[d <= r_inner]
    ann = signal2d[(d > r_inner) & (d <= r_outer)]
    if ann.size == 0 or ann.mean() <= 0:
        return float("nan")
    return float(inner.mean() / ann.mean())

def radial_profile(signal2d: np.ndarray, center_rc: tuple[float, float],
                   n_bins: int = 12, max_radius: float | None = None) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns (bin_centers, mean_intensity_per_bin)
    """
    sig = signal2d.astype(np.float32)
    d = radial_distance_map(center_rc, sig.shape)
    if max_radius is None:
        max_radius = float(d.max())
    edges = np.linspace(0.0, max_radius, n_bins + 1)
    prof = np.zeros(n_bins, dtype=np.float32)
    for i in range(n_bins):
        m = (d >= edges[i]) & (d < edges[i+1])
        prof[i] = sig[m].mean() if np.any(m) else np.nan
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers, prof

def distribution_coupling(profile_a: np.ndarray, profile_b: np.ndarray) -> float:
    """
    A simple, interpretable coupling score based on cosine similarity of radial profiles.
    Not pixel-wise colocalisation; distribution-level coupling.
    """
    a = np.asarray(profile_a, dtype=np.float32)
    b = np.asarray(profile_b, dtype=np.float32)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return float("nan")
    a = a[m] - np.nanmean(a[m])
    b = b[m] - np.nanmean(b[m])
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return float("nan")
    return float(np.dot(a, b) / (na * nb))

def within_cell_heterogeneity(signal2d: np.ndarray, mask: np.ndarray | None = None) -> float:
    """
    Toy heterogeneity metric: coefficient of variation (CV) within mask (or full field if mask None).
    """
    sig = signal2d.astype(np.float32)
    if mask is not None:
        sig = sig[mask.astype(bool)]
    if sig.size < 10:
        return float("nan")
    mu = float(np.mean(sig))
    sd = float(np.std(sig))
    if mu <= 0:
        return float("nan")
    return float(sd / mu)
