import numpy as np
from skimage.exposure import rescale_intensity
from skimage.filters import gaussian

def apply_gamma(img: np.ndarray, gamma: float) -> np.ndarray:
    """
    Gamma correction on float [0,1] scale; returns float32.
    """
    img = img.astype(np.float32)
    if img.max() > img.min():
        x = rescale_intensity(img, in_range="image", out_range=(0.0, 1.0)).astype(np.float32)
        x = np.power(x, gamma).astype(np.float32)
        return x
    return np.zeros_like(img, dtype=np.float32)

def smooth(img: np.ndarray, sigma: float) -> np.ndarray:
    if sigma is None or sigma <= 0:
        return img.astype(np.float32)
    return gaussian(img.astype(np.float32), sigma=sigma, preserve_range=True).astype(np.float32)

def to_uint16(img: np.ndarray) -> np.ndarray:
    img = img.astype(np.float32)
    if img.max() > img.min():
        out = rescale_intensity(img, in_range="image", out_range=(0, 65535))
    else:
        out = np.zeros_like(img)
    return out.astype(np.uint16)

def channel_signal_for_thresholding(cyx: np.ndarray, use_channel: int | None) -> np.ndarray:
    """
    Build a 2D signal image used for thresholding or QC.
    """
    if use_channel is None:
        return cyx.max(axis=0).astype(np.float32)
    return cyx[int(use_channel)].astype(np.float32)
