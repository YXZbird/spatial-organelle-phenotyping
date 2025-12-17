import numpy as np
from skimage.exposure import rescale_intensity
from skimage.color import label2rgb

def to_u8(img2d: np.ndarray) -> np.ndarray:
    x = img2d.astype(np.float32)
    if x.max() > x.min():
        x = rescale_intensity(x, in_range="image", out_range=(0, 255))
    else:
        x = np.zeros_like(x)
    return x.astype(np.uint8)

def make_rgb(cyx: np.ndarray, rgb_channels=(1,2,0)) -> np.ndarray:
    r, g, b = rgb_channels
    rgb = np.stack([to_u8(cyx[r]), to_u8(cyx[g]), to_u8(cyx[b])], axis=-1)
    return rgb

def overlay_nuclei_on_rgb(rgb: np.ndarray, nuclei_lab: np.ndarray, alpha: float = 0.35) -> np.ndarray:
    """
    nuclei_lab: labeled mask
    """
    return (label2rgb(nuclei_lab, image=rgb, alpha=alpha, bg_label=0) * 255).astype(np.uint8)
