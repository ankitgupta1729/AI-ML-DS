"""Turn phone photos of notebook pages into clean, scanner-like page images.

For each photo:

1. **Orientation.** Photos taken sideways are turned upright; the caller says
   how many quarter turns each photo needs (see ``rotate``).
2. **Paper.** The notebook paper is the large bright, unsaturated region; the
   bedsheet and table around it are found.
3. **Level.** The photo is rotated by the paper's small tilt so the page
   stands straight, then cropped to the paper. Nothing on the paper is cut
   off: a neighbouring page that was in the shot stays in.
4. **Whiten.** Dividing by a blurred estimate of the paper (lighting and
   shadows) turns the paper white and keeps the ink, including coloured ink.
5. **Background.** Everything outside the paper is blanked to white.

The handwriting itself is never altered beyond this tone correction.
"""
from __future__ import annotations

import cv2
import numpy as np

VERSION = "1"  # bump when the output of process() changes (invalidates cached pages)
WORK = 1000  # long side used for detection


def _scale(img: np.ndarray, long_side: int) -> tuple[np.ndarray, float]:
    h, w = img.shape[:2]
    f = long_side / max(h, w)
    return cv2.resize(img, (round(w * f), round(h * f)), interpolation=cv2.INTER_AREA), f


def paper_mask(bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    purple = (h > 115) & (h < 170) & (s > 18)  # the lilac bedsheet, even where it is pale
    mask = ((s < 42) & (v > 110) & ~purple).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    # a wide opening removes the white squares of the checked bedsheet
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45)))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask)
    if n <= 1:
        return mask
    big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    out = (labels == big).astype(np.uint8) * 255
    # fill holes (dense handwriting, diagrams)
    cnts, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(out)
    cv2.drawContours(filled, cnts, -1, 255, -1)
    return filled


def whiten(bgr: np.ndarray) -> np.ndarray:
    """Even out lighting: paper becomes white, ink keeps its colour."""
    out = np.empty_like(bgr)
    k = max(31, (min(bgr.shape[:2]) // 12) | 1)
    for ch in range(3):
        c = bgr[..., ch]
        bg = cv2.medianBlur(cv2.dilate(c, np.ones((7, 7), np.uint8)), k)
        norm = cv2.divide(c, bg, scale=255)
        out[..., ch] = norm
    # gentle contrast: lift paper to white, deepen ink a little
    lut = np.clip((np.arange(256) - 40) * 255.0 / 200, 0, 255) ** 1.0
    lut = np.clip(255 * (lut / 255) ** 1.25, 0, 255).astype(np.uint8)
    return cv2.LUT(out, lut)


def clear_cloth(bgr: np.ndarray, outside: np.ndarray) -> np.ndarray:
    """Blank the background: everything outside the paper, plus bedsheet.

    ``outside`` marks pixels known to lie off the paper. Purple bedsheet
    regions are removed only where they touch that area or the image border,
    so ink in the middle of the page (including blue or violet pen) is never
    touched.
    """
    out = bgr.copy()
    out[outside] = 255
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    cloth = ((hsv[..., 0] > 118) & (hsv[..., 0] < 172) & (hsv[..., 1] > 30) & ~outside).astype(np.uint8)
    cloth = cv2.morphologyEx(cloth, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(cloth)
    h, w = cloth.shape
    near_out = cv2.dilate(outside.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    for i in range(1, n):
        x, y, bw, bh, area = stats[i]
        if area < 0.002 * h * w:
            continue
        region = labels == i
        if x == 0 or y == 0 or x + bw >= w or y + bh >= h or (region & near_out).any():
            out[cv2.dilate(region.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0] = 255
    return out


def rotate(bgr: np.ndarray, quarter_turns: int) -> np.ndarray:
    return np.rot90(bgr, k=quarter_turns % 4).copy()


def process(bgr: np.ndarray, quarter_turns: int = 0) -> tuple[np.ndarray, dict]:
    """Return the cleaned page image and a dict describing what was done.

    Nothing written on the paper is cropped: the result keeps the convex hull
    of *all* the paper in the photo, with a margin, so a neighbouring page that
    was in the shot stays too. The photo is only levelled (small rotation),
    never warped, and only the background around the paper is blanked.
    """
    bgr = rotate(bgr, quarter_turns)
    small, f = _scale(bgr, WORK)
    mask = paper_mask(small)
    pts = cv2.findNonZero(mask)
    hull = np.zeros_like(mask)
    cv2.drawContours(hull, [cv2.convexHull(pts)], -1, 255, -1)
    margin = max(9, WORK // 50) | 1
    hull = cv2.dilate(hull, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (margin, margin)))
    (_, _), (rw, rh), angle = cv2.minAreaRect(pts)
    angle = (angle + 45) % 90 - 45  # OpenCV versions differ in range; keep the small tilt
    h0, w0 = bgr.shape[:2]
    rot = cv2.getRotationMatrix2D((w0 / 2, h0 / 2), angle, 1.0)
    level = cv2.warpAffine(bgr, rot, (w0, h0), flags=cv2.INTER_CUBIC, borderValue=(255, 255, 255))
    keep = cv2.resize(hull, (w0, h0), interpolation=cv2.INTER_NEAREST)
    keep = cv2.warpAffine(keep, rot, (w0, h0), flags=cv2.INTER_NEAREST, borderValue=0)
    ys, xs = np.nonzero(keep)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    page, keep = level[y0:y1, x0:x1], keep[y0:y1, x0:x1]
    out = clear_cloth(whiten(page), keep == 0)
    return out, {"rotated": quarter_turns % 4, "angle": round(float(angle), 1),
                 "size": (int(x1 - x0), int(y1 - y0))}
