#!/usr/bin/env python3
"""Redraw the plots and sketches of the handwritten notebook as SVG figures.

    python tools/notes-to-pdf/plotfigs.py            # writes foundations/04.Theory/Notes/digital/figures/*.svg

Each function reproduces one sketch from the notebook (the docstring names the
notebook page). Output is deterministic (fixed random seeds, no SVG ids/dates).
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Ellipse  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "foundations", "04.Theory", "Notes", "digital", "figures")
ACC, ACC2, INK, MUT, WARM = "#7c3aed", "#c4b5fd", "#0f172a", "#64748b", "#f59e0b"
plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 10, "axes.edgecolor": MUT, "axes.labelcolor": INK,
    "xtick.color": MUT, "ytick.color": MUT, "axes.spines.top": False, "axes.spines.right": False,
    "svg.hashsalt": "notes", "svg.fonttype": "none", "figure.dpi": 100,
})
FIGS = []


def fig(fn):
    FIGS.append(fn)
    return fn


def save(f, name):
    f.savefig(os.path.join(OUT, name + ".svg"), bbox_inches="tight", pad_inches=0.08, metadata={"Date": None})
    plt.close(f)


def bare(ax):
    ax.set_xticks([])
    ax.set_yticks([])


@fig
def knn():
    """p3: KNN — 6 neighbours of the query (4 ○, 2 ●) inside a circle."""
    f, ax = plt.subplots(figsize=(4.2, 3))
    q = np.array([0, 0])
    inner_o = [(-0.9, 0.3), (-0.4, 0.75), (0.5, 0.55), (0.9, -0.1)]
    inner_f = [(-0.2, -0.8), (0.6, -0.65)]
    outer_o = [(-2.2, 1.6), (-1.4, 1.7), (2.0, 0.4), (2.3, -0.6)]
    outer_f = [(-2.3, -0.9), (1.7, 0.95), (2.0, 1.4), (1.6, -1.2)]
    ax.add_patch(Ellipse(q, 3.2, 2.6, fill=False, ec=ACC, lw=1.5, ls="--"))
    for x, y in inner_o + outer_o:
        ax.scatter(x, y, s=60, facecolor="white", edgecolor=INK, lw=1.3, zorder=3)
    for x, y in inner_f + outer_f:
        ax.scatter(x, y, s=60, color=INK, zorder=3)
    ax.scatter(*q, s=110, marker="s", color=WARM, ec=INK, zorder=4)
    ax.text(-0.2, -0.45, "query x", fontsize=9, color="#b45309", ha="center")
    ax.text(0, -1.75, r"$P(\circ\mid x)=4/6,\;\; P(\bullet\mid x)=2/6\;\Rightarrow\;x$ is labelled $\circ$",
            ha="center", fontsize=9, color=INK)
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(-2.0, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "knn")


@fig
def regression_line():
    """p4: regression — data points and the line of regression."""
    f, ax = plt.subplots(figsize=(3.8, 2.6))
    rng = np.random.default_rng(1)
    x = np.linspace(0.5, 9.5, 14)
    y = 0.6 * x + 1 + rng.normal(0, 0.6, x.size)
    ax.scatter(x, y, s=22, color=ACC, zorder=3, label="data points")
    b, a = np.polyfit(x, y, 1)
    xx = np.array([0, 10])
    ax.plot(xx, a + b * xx, color=INK, lw=1.6, label="line of regression")
    ax.set_xlabel("X (independent variable)")
    ax.set_ylabel("Y (dependent variable)")
    bare(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    save(f, "regression-line")


@fig
def sigmoid():
    """p4: logistic regression — S-curve between y = 0 and y = 1."""
    f, ax = plt.subplots(figsize=(3.8, 2.4))
    z = np.linspace(-7, 7, 300)
    ax.plot(z, 1 / (1 + np.exp(-z)), color=ACC, lw=2)
    for yv in (0, 1):
        ax.axhline(yv, color=MUT, lw=0.8, ls="--")
        ax.text(-7, yv + 0.04, f"y = {yv}", fontsize=8, color=MUT)
    ax.text(2.2, 0.55, "S-curve: predicted y\nlies within 0 and 1", fontsize=8.5, color=INK)
    ax.set_ylim(-0.12, 1.15)
    bare(ax)
    ax.set_xlabel("x")
    ax.set_ylabel("ŷ")
    save(f, "sigmoid")


@fig
def column_space():
    """p5: Ax maps x into the plane spanned by the columns a1, a2 of A."""
    f, ax = plt.subplots(figsize=(4.2, 2.9))
    plane = np.array([[0, 0], [3.2, 0], [4.2, 1.3], [1.0, 1.3]])
    ax.fill(plane[:, 0], plane[:, 1], color="#ede9fe", ec=ACC, lw=1.2)
    o = np.array([1.2, 0.35])
    for v, lab in (((2.6, 0.45), "$a_1$"), ((2.0, 1.05), "$a_2$")):
        ax.annotate("", v, o, arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.5))
        ax.text(v[0] + 0.05, v[1] + 0.02, lab, color=ACC, fontsize=11)
    ax.annotate("", (2.2, 2.6), o, arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5))
    ax.text(2.25, 2.62, "$x$ (not in the plane)", fontsize=9.5, color=INK)
    ax.annotate("", (3.1, 0.9), (2.2, 2.55),
                arrowprops=dict(arrowstyle="-|>", color=WARM, lw=1.3, ls="--", connectionstyle="arc3,rad=-0.3"))
    ax.text(3.15, 1.6, "$A$ rotates $x$\ninto the plane", fontsize=9, color="#b45309")
    ax.text(0.15, 0.12, "column space of $A$", fontsize=8.5, color=MUT)
    ax.set_xlim(-0.1, 4.6)
    ax.set_ylim(-0.1, 3.0)
    ax.axis("off")
    save(f, "column-space")


@fig
def rank_factorisation():
    """p6: rank(M) = k  =>  M (m x n) = C (m x k) . R (k x n)."""
    f, ax = plt.subplots(figsize=(4.6, 1.8))
    from matplotlib.patches import Rectangle
    boxes = [((0, 0), 2.0, 1.6, "M", "m × n"), ((3.0, 0), 0.7, 1.6, "C", "m × k"), ((4.1, 0.9), 2.0, 0.7, "R", "k × n")]
    for (x, y), w, h, lab, dim in boxes:
        ax.add_patch(Rectangle((x, y), w, h, fc="#ede9fe", ec=ACC, lw=1.4))
        ax.text(x + w / 2, y + h / 2, lab, ha="center", va="center", fontsize=13, fontweight="bold", color=INK)
        ax.text(x + w / 2, y - 0.25, dim, ha="center", fontsize=8.5, color=MUT)
    ax.text(2.5, 0.8, "=", fontsize=16, ha="center", va="center", color=INK)
    ax.text(3.9, 1.25, "·", fontsize=18, ha="center", va="center", color=INK)
    ax.text(3.1, -0.75, "rank factorisation (used in recommender systems)", ha="center", fontsize=8, color=MUT)
    ax.set_xlim(-0.2, 6.3)
    ax.set_ylim(-0.95, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "rank-factorisation")


@fig
def level_curves():
    """p6: level curves x1^2 + x2^2 = k; the gradient is normal to them."""
    f, ax = plt.subplots(figsize=(3.2, 3.0))
    t = np.linspace(0, 2 * np.pi, 200)
    for r in (0.5, 1.0, 1.5, 2.0):
        ax.plot(r * np.cos(t), r * np.sin(t), color=ACC, lw=1.1, alpha=0.4 + r / 5)
    p = np.array([1.5 * np.cos(0.7), 1.5 * np.sin(0.7)])
    ax.annotate("", p * 1.45, p, arrowprops=dict(arrowstyle="-|>", color=WARM, lw=1.8))
    ax.text(*(p * 1.48 + [0.05, 0]), r"$\nabla f(x)$", fontsize=10, color="#b45309")
    ax.scatter(*p, s=14, color=INK, zorder=3)
    ax.axhline(0, color=MUT, lw=0.6)
    ax.axvline(0, color=MUT, lw=0.6)
    ax.text(2.55, -0.25, "$x_1$", color=MUT)
    ax.text(0.1, 2.5, "$x_2$", color=MUT)
    ax.set_xlim(-2.4, 2.8)
    ax.set_ylim(-2.4, 2.8)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "level-curves")


@fig
def convex_function():
    """p8: a convex function lies below the chord between x1 and x2."""
    f, ax = plt.subplots(figsize=(3.6, 2.6))
    x = np.linspace(-1.6, 1.6, 200)
    ax.plot(x, x ** 2, color=ACC, lw=2)
    x1, x2, th = -1.2, 1.4, 0.45
    x3 = th * x1 + (1 - th) * x2
    ax.plot([x1, x2], [x1 ** 2, x2 ** 2], color=WARM, lw=1.4)
    ax.scatter([x1, x2], [x1 ** 2, x2 ** 2], color=WARM, zorder=3, s=18)
    ax.vlines(x3, x3 ** 2, th * x1 ** 2 + (1 - th) * x2 ** 2, color=INK, lw=1, ls=":")
    ax.scatter([x3, x3], [x3 ** 2, th * x1 ** 2 + (1 - th) * x2 ** 2], color=INK, s=14, zorder=3)
    for xv, lab in ((x1, "$x_1$"), (x3, "$x_3$"), (x2, "$x_2$")):
        ax.text(xv, -0.38, lab, ha="center", color=INK)
    ax.text(0.0, 2.45, r"$\theta f(x_1)+(1-\theta)f(x_2)\;\geq\;f(x_3)$", fontsize=8.5, color=INK, ha="center")
    ax.set_ylim(-0.5, 2.7)
    ax.axhline(0, color=MUT, lw=0.6)
    ax.axis("off")
    save(f, "convex-function")


@fig
def bias_variance():
    """p14: prediction error vs model complexity (training and test sample)."""
    f, ax = plt.subplots(figsize=(4.6, 2.9))
    c = np.linspace(0.3, 9.7, 200)
    train = 7.5 * np.exp(-0.33 * c) + 0.4
    test = train + 0.06 * (c - 1.5) ** 2 + 0.4
    ax.plot(c, train, color=MUT, lw=1.8, label="training sample")
    ax.plot(c, test, color=ACC, lw=2, label="test sample")
    m = c[np.argmin(test)]
    ax.axvline(m, color=INK, lw=0.8, ls=":")
    ax.text(m + 0.15, 0.25, "$m^*$", color=INK)
    ax.text(1.0, 6.9, "high bias\nlow variance", fontsize=8.5, color=INK)
    ax.text(7.2, 6.4, "low bias\nhigh variance", fontsize=8.5, color=INK)
    ax.set_xlabel("model complexity (e.g. tree size)  →  high")
    ax.set_ylabel("prediction error")
    bare(ax)
    ax.set_ylim(0, 8.6)
    ax.legend(frameon=False, fontsize=8, loc="lower left", bbox_to_anchor=(0.02, 0.02))
    save(f, "bias-variance")


@fig
def pca_components():
    """p14/16: correlated data with its 1st and 2nd principal components."""
    f, ax = plt.subplots(figsize=(3.6, 2.8))
    rng = np.random.default_rng(7)
    pts = rng.multivariate_normal([0, 0], [[3, 1.6], [1.6, 1.3]], 90)
    ax.scatter(pts[:, 0], pts[:, 1], s=10, color=ACC2, ec=ACC, lw=0.4)
    w, v = np.linalg.eigh(np.cov(pts.T))
    for k, lab in ((1, "1st principal component"), (0, "2nd principal component")):
        d = v[:, k] * (3.6 if k else 2.0)
        d = d if d[1] > 0 else -d
        ax.annotate("", d, (0, 0), annotation_clip=False,
                    arrowprops=dict(arrowstyle="-|>", color=INK if k else WARM, lw=2))
        ax.text(d[0] + (0.15 if k else -0.15), d[1] + 0.1, lab, fontsize=8.5, color=INK if k else "#b45309",
                ha="left" if k else "right", zorder=5, bbox=dict(fc="white", ec="none", alpha=0.9, pad=1))
    ax.set_xlim(-6, 7)
    ax.set_ylim(-3.2, 3.6)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "pca-components")


@fig
def pca_projection():
    """p16: projection of x_k onto the line through m with direction e."""
    f, ax = plt.subplots(figsize=(4.2, 2.6))
    m = np.array([0.0, 0.0])
    e = np.array([np.cos(0.25), np.sin(0.25)])
    xk = np.array([3.0, 1.9])
    a = e @ (xk - m)
    xh = m + a * e
    ax.plot(*np.c_[m - 0.6 * e, m + 4.3 * e], color=MUT, lw=1)
    ax.annotate("", m + e, m, arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2))
    ax.text(*(m + 1.0 * e + [0.0, -0.32]), "$e$", color=ACC, fontsize=11)
    ax.annotate("", xk, m, arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.plot(*np.c_[xk, xh], color=WARM, lw=1.4, ls="--")
    ax.scatter(*np.c_[m, xk, xh], color=[INK, INK, ACC], s=22, zorder=3)
    ax.text(*(m + [-0.15, -0.35]), "$m$", fontsize=11)
    ax.text(*(xk + [0.1, 0.05]), "$x_k$", fontsize=11)
    ax.text(*(xh + [0.05, -0.38]), r"$\hat{x}_k = m + \alpha_k e$", fontsize=10, color=ACC)
    ax.text(*((xk + xh) / 2 + [0.12, 0]), "$d$ (projection error)", fontsize=9, color="#b45309")
    ax.text(*(m + 0.5 * a * e + [-0.2, 0.15]), r"$\alpha_k$", fontsize=10, color=INK)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "pca-projection")


@fig
def pca_vs_fld():
    """p18: two classes separable in 2-D overlap after projecting onto the PCA direction."""
    f, (a1, a2) = plt.subplots(1, 2, figsize=(5.4, 2.4), gridspec_kw={"width_ratios": [1, 1.25]})
    rng = np.random.default_rng(2)
    c1 = rng.normal([0, 0], [0.35, 1.4], (25, 2))
    c2 = rng.normal([1.7, 0], [0.3, 1.4], (25, 2))
    c1 = np.c_[np.clip(c1[:, 0], -0.7, 0.7), c1[:, 1]]
    c2 = np.c_[np.clip(c2[:, 0], 1.05, 2.4), c2[:, 1]]
    a1.scatter(*c1.T, marker="s", s=16, facecolor="white", ec=ACC, lw=1)
    a1.scatter(*c2.T, marker="o", s=16, facecolor="white", ec=WARM, lw=1)
    a1.annotate("", (0.85, 3.3), (0.85, -3.3), annotation_clip=False,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    a1.text(0.95, 2.6, "PCA\ndirection", fontsize=8, color=INK)
    a1.annotate("", (2.6, -3.6), (-1.0, -3.6), annotation_clip=False,
                arrowprops=dict(arrowstyle="-|>", color="#16a34a", lw=1.2))
    a1.text(-1.0, -4.3, "FLD direction", fontsize=8, color="#16a34a")
    a1.set_title("2-D data (two classes)", fontsize=9, color=INK, pad=12)
    a1.set_xlim(-1.2, 2.9)
    a1.set_ylim(-4.5, 3.6)
    a1.axis("off")
    a2.axhline(0.6, color=MUT, lw=0.8)
    a2.scatter(c1[:, 1], np.full(25, 0.6), marker="s", s=14, facecolor="white", ec=ACC)
    a2.scatter(c2[:, 1], np.full(25, 0.6), marker="o", s=14, facecolor="white", ec=WARM)
    a2.text(0, 0.85, "projected on PCA: non-separable", ha="center", fontsize=8, color=INK)
    a2.axhline(0, color=MUT, lw=0.8)
    a2.scatter(c1[:, 0] * 2.0 - 1.7, np.zeros(25), marker="s", s=14, facecolor="white", ec=ACC)
    a2.scatter(c2[:, 0] * 2.0 - 1.7, np.zeros(25), marker="o", s=14, facecolor="white", ec=WARM)
    a2.text(0, 0.22, "projected on FLD: separable", ha="center", fontsize=8, color="#16a34a")
    a2.set_ylim(-0.4, 1.2)
    a2.axis("off")
    save(f, "pca-vs-fld")


@fig
def clusters():
    """p21: intra-cluster distances minimised, inter-cluster distances maximised."""
    f, ax = plt.subplots(figsize=(3.8, 2.8))
    rng = np.random.default_rng(4)
    cents = np.array([[0, 2.2], [3.2, 2.6], [1.8, 0]])
    marks = ["s", "o", "^"]
    for c, mk in zip(cents, marks, strict=True):
        p = c + rng.normal(0, 0.28, (7, 2))
        ax.add_patch(Ellipse(c, 1.6, 1.4, fill=False, ec=ACC, lw=1.2))
        ax.scatter(*p.T, marker=mk, s=18, facecolor="white", ec=INK, lw=0.9)
    for i, j in ((0, 1), (1, 2), (0, 2)):
        ax.annotate("", cents[j], cents[i], arrowprops=dict(arrowstyle="<->", color=WARM, lw=1, shrinkA=30, shrinkB=30))
    ax.text(1.0, 3.35, "inter-cluster distances\nare maximised", fontsize=8, color="#b45309", ha="center")
    ax.text(-0.9, 0.6, "intra-cluster\ndistances are\nminimised", fontsize=8, color=ACC)
    ax.set_xlim(-1.3, 4.3)
    ax.set_ylim(-1.0, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "clusters")


@fig
def dendrogram():
    """p22: hierarchical clustering — a dendrogram (tree-like structure)."""
    f, ax = plt.subplots(figsize=(3.8, 2.4))
    # (left, right, height) merges over leaves 0..5 placed at x = 0..5
    xs = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
    hs = {k: 0 for k in xs}
    merges = [(0, 1, 1.0), (2, 3, 1.4), (6, 7, 2.6), (4, 5, 0.8), (8, 9, 4.0)]
    nid = 6
    for a, b, h in merges:
        ax.plot([xs[a], xs[a], xs[b], xs[b]], [hs[a], h, h, hs[b]], color=ACC, lw=1.6)
        xs[nid], hs[nid] = (xs[a] + xs[b]) / 2, h
        nid += 1
    for i in range(6):
        ax.text(i, -0.35, chr(65 + i), ha="center", color=INK)
    ax.set_ylabel("distance (height)")
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_ylim(-0.6, 4.4)
    save(f, "dendrogram")


def _contours(ax, sx, sy, rot, n=4, color=ACC):
    t = np.linspace(0, 2 * np.pi, 120)
    c, s_ = np.cos(rot), np.sin(rot)
    for k in range(1, n + 1):
        x, y = k * sx * np.cos(t) / n, k * sy * np.sin(t) / n
        ax.plot(c * x - s_ * y, s_ * x + c * y, color=color, lw=1.1, alpha=0.4 + 0.6 * k / n)
    ax.set_aspect("equal")
    ax.axis("off")


@fig
def feature_scaling():
    """p23: features on different scales (elongated contours) vs scaled features (round contours)."""
    f, (a, b) = plt.subplots(1, 2, figsize=(4.6, 1.9))
    _contours(a, 2.2, 0.6, 0)
    a.set_title("before scaling", fontsize=9, color=INK)
    _contours(b, 1.0, 1.0, 0)
    b.set_title("after scaling", fontsize=9, color=INK)
    for ax in (a, b):
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-1.2, 1.2)
    f.text(0.5, 0.45, "→", fontsize=18, ha="center", color=INK)
    save(f, "feature-scaling")


@fig
def covariance_contours():
    """p24: contours of a 2-D Gaussian for Cov = 0, Cov > 0 and Cov < 0."""
    f, axs = plt.subplots(1, 3, figsize=(5.2, 1.9))
    for ax, (sx, sy, rot, lab) in zip(axs, ((1, 1, 0, "Cov = 0"), (1.4, 0.55, 0.78, "Cov > 0"),
                                            (1.4, 0.55, -0.78, "Cov < 0")), strict=True):
        _contours(ax, sx, sy, rot)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_title(lab, fontsize=9, color=INK)
    save(f, "covariance-contours")


@fig
def gaussian():
    """p24: the univariate Gaussian (bell curve)."""
    f, ax = plt.subplots(figsize=(3.4, 1.9))
    x = np.linspace(-4, 4, 300)
    ax.plot(x, np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi), color=ACC, lw=2)
    ax.fill_between(x, np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi), color=ACC, alpha=0.1)
    ax.axvline(0, color=MUT, lw=0.8, ls=":")
    ax.text(0.1, 0.02, r"$\mu$", color=INK)
    ax.annotate("", (1, 0.242), (0, 0.242), arrowprops=dict(arrowstyle="<->", color=WARM))
    ax.text(0.5, 0.26, r"$\sigma$", color="#b45309", ha="center")
    bare(ax)
    ax.set_ylim(0, 0.45)
    save(f, "gaussian")


def _network(ax, layers, labels=None, colors=(ACC2, "#ede9fe", "#fde68a")):
    xs = np.linspace(0, 1, len(layers))
    pos = []
    for i, n in enumerate(layers):
        ys = np.linspace(0.5 - 0.12 * (n - 1), 0.5 + 0.12 * (n - 1), n)
        pos.append([(xs[i], y) for y in ys])
    for a, b in zip(pos, pos[1:], strict=False):
        for p in a:
            for q in b:
                ax.plot([p[0], q[0]], [p[1], q[1]], color=MUT, lw=0.6, alpha=0.7)
    for i, layer in enumerate(pos):
        col = colors[0] if i == 0 else (colors[2] if i == len(pos) - 1 else colors[1])
        for p in layer:
            ax.add_patch(plt.Circle(p, 0.035, fc=col, ec=ACC, lw=1.1, zorder=3))
    if labels:
        for x, lab in zip(xs, labels, strict=True):
            ax.text(x, 0.5 - 0.12 * (max(layers) - 1) - 0.1, lab, ha="center", fontsize=8.5, color=MUT)
    ax.set_aspect("equal")
    ax.axis("off")


@fig
def mlp():
    """p25: a fully connected MLP with 3 inputs, 4 hidden units and 3 outputs."""
    f, ax = plt.subplots(figsize=(3.6, 2.4))
    _network(ax, [3, 4, 3], ["input (3)", "hidden (4)", "output (3)"])
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.05, 1.0)
    save(f, "mlp")


@fig
def momentum():
    """p26: a ball rolling on the loss surface can stop at a saddle point or local minimum."""
    f, ax = plt.subplots(figsize=(4.4, 2.2))
    cx = [0, 1.5, 3.5, 5.0, 6.3, 7.2, 8.6, 10]
    cy = [3.0, 2.2, 0.6, 1.8, 1.3, 1.3, -0.4, 1.0]
    x = np.linspace(0, 10, 400)
    i = np.clip(np.searchsorted(cx, x) - 1, 0, len(cx) - 2)
    t = (x - np.take(cx, i)) / (np.take(cx, i + 1) - np.take(cx, i))
    w = (1 - np.cos(np.pi * t)) / 2  # flat at every control point
    y = np.take(cy, i) * (1 - w) + np.take(cy, i + 1) * w
    ax.plot(x, y, color=ACC, lw=2)
    for xb, lab, dy in ((0.9, "ball", 0.75), (3.5, "local minimum\n∇C(θ) = 0", -0.85),
                        (6.75, "saddle point\n∇C(θ) = 0", 0.95), (8.6, "global minimum", -0.7)):
        yb = float(np.interp(xb, x, y))
        if lab != "global minimum":
            ax.add_patch(plt.Circle((xb, yb + 0.25), 0.22, fc=WARM, ec=INK, lw=0.8, zorder=3))
        ax.text(xb, yb + dy, lab, ha="center", fontsize=8, color=INK)
    ax.text(10, 3.2, "momentum carries\nthe ball onwards →", ha="right", fontsize=8, color="#b45309")
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "momentum")


def _grid(ax, x, y, n, cell=0.3, fc="white", ec=ACC, hl=None, vals=None, lw=0.8):
    from matplotlib.patches import Rectangle
    for i in range(n):
        for j in range(n):
            col = fc
            if hl and hl[0] <= i < hl[0] + hl[2] and hl[1] <= j < hl[1] + hl[2]:
                col = "#fde68a"
            ax.add_patch(Rectangle((x + j * cell, y + (n - 1 - i) * cell), cell, cell, fc=col, ec=ec, lw=lw))
            if vals is not None:
                ax.text(x + (j + 0.5) * cell, y + (n - 1 - i + 0.5) * cell, str(vals[i][j]), ha="center",
                        va="center", fontsize=7.5, color=INK)


@fig
def matrix_layer():
    """p26: a layer as a matrix operation, sigma(Wx + b) with x = (1, -1)."""
    f, ax = plt.subplots(figsize=(4.4, 2.0))
    ins = [(0, 1.4), (0, 0.2)]
    outs = [(2.2, 1.4), (2.2, 0.2)]
    w = [[1, -2], [-1, 1]]
    for i, (xi, yi) in enumerate(ins):
        for j, (xo, yo) in enumerate(outs):
            ax.annotate("", (xo - 0.22, yo), (xi + 0.22, yi), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.9))
            ax.text(xi + 0.6 + 0.55 * (j - i) * 0.4, (yi * 0.7 + yo * 0.3) + (0.12 if j == i else -0.05),
                    str(w[j][i]), fontsize=8.5, color=ACC)
    for (x, y), v in zip(ins, ("1", "−1"), strict=True):
        ax.add_patch(plt.Rectangle((x - 0.2, y - 0.17), 0.4, 0.34, fc="#ede9fe", ec=ACC))
        ax.text(x, y, v, ha="center", va="center", fontsize=9)
    for (x, y), b in zip(outs, ("1", "0"), strict=True):
        ax.add_patch(plt.Circle((x, y), 0.22, fc="#fde68a", ec=INK))
        ax.text(x, y, "σ", ha="center", va="center", fontsize=10)
        ax.text(x + 0.05, y - 0.5, f"bias {b}", ha="center", fontsize=8, color=MUT)
    ax.text(3.0, 0.8, "W = [[1, −2], [−1, 1]]\nx = (1, −1),  b = (1, 0)\n→ σ(Wx + b)",
            fontsize=8.5, color=INK, va="center")
    ax.set_xlim(-0.4, 5.2)
    ax.set_ylim(-0.5, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "matrix-layer")


@fig
def convolution():
    """p28: a 3x3 mask slides over a 6x6 image (stride 1, no padding) giving a 4x4 feature map."""
    f, ax = plt.subplots(figsize=(5.0, 2.2))
    _grid(ax, 0, 0, 6, hl=(0, 0, 3))
    ax.text(0.9, -0.3, "6 × 6 image", ha="center", fontsize=8.5, color=INK)
    ax.text(2.2, 0.9, "∗", fontsize=18, ha="center", va="center")
    _grid(ax, 2.55, 0.45, 3, fc="#fde68a")
    ax.text(3.0, 0.15, "3 × 3 mask\n(learned)", ha="center", fontsize=8, color=INK, va="top")
    ax.text(3.75, 0.9, "=", fontsize=16, ha="center", va="center")
    _grid(ax, 4.1, 0.3, 4, fc="#ede9fe", hl=(0, 0, 1))
    ax.text(4.7, -0.3, "4 × 4 feature map", ha="center", fontsize=8.5, color=INK)
    ax.set_xlim(-0.1, 5.4)
    ax.set_ylim(-0.6, 1.9)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "convolution")


@fig
def softmax():
    """p26: softmax layer: z_i -> e^{z_i} -> y_i = e^{z_i} / sum_j e^{z_j}."""
    f, ax = plt.subplots(figsize=(4.6, 1.9))
    for k, y in enumerate((1.5, 0.85, 0.2)):
        i = k + 1
        ax.text(0, y, f"$z_{i}$", ha="center", va="center", fontsize=10)
        ax.annotate("", (0.75, y), (0.2, y), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.9))
        ax.text(1.0, y, f"$e^{{z_{i}}}$", ha="center", va="center", fontsize=10,
                bbox=dict(boxstyle="round,pad=0.25", fc="#ede9fe", ec=ACC))
        ax.annotate("", (2.6, y), (1.3, y), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.9))
        ax.text(3.35, y, f"$y_{i} = e^{{z_{i}}} / \\sum_j e^{{z_j}}$", ha="center", va="center", fontsize=9.5)
    ax.add_patch(plt.Rectangle((0.55, -0.15), 1.6, 2.0, fc="none", ec=WARM, lw=1, ls="--"))
    ax.text(1.35, 1.95, "softmax layer", ha="center", fontsize=8.5, color=WARM)
    ax.set_xlim(-0.3, 4.4)
    ax.set_ylim(-0.25, 2.15)
    ax.axis("off")
    save(f, "softmax")


@fig
def multichannel_conv():
    """p29: a 3x3x3 filter on a 5x5x3 input: per-channel convolutions are summed, plus a bias."""
    f, ax = plt.subplots(figsize=(5.4, 2.6))
    chans = ["#fecaca", "#bbf7d0", "#bfdbfe"]
    for k, col in enumerate(chans):
        x0 = k * 1.25
        _grid(ax, x0, 1.2, 5, cell=0.17, fc=col, hl=None)
        _grid(ax, x0 + 0.22, 0.4, 3, cell=0.17, fc="#fde68a")
        ax.annotate("", (x0 + 0.47, 0.95), (x0 + 0.47, 1.17), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.8))
        ax.text(x0 + 0.42, 2.15, f"channel {k + 1} (5×5)", ha="center", fontsize=7.5, color=INK)
        ax.annotate("", (4.0, 0.65), (x0 + 0.75, 0.65),
                    arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.7, connectionstyle="arc3,rad=-0.25"))
    ax.text(0.47, 0.2, "3×3 results", ha="center", fontsize=7.5, color=MUT)
    ax.add_patch(plt.Circle((4.15, 0.65), 0.13, fc="white", ec=INK))
    ax.text(4.15, 0.65, "+", ha="center", va="center", fontsize=10)
    ax.text(4.15, 1.05, "bias", ha="center", fontsize=8, color=MUT)
    ax.annotate("", (4.15, 0.8), (4.15, 0.98), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.8))
    ax.annotate("", (4.5, 0.65), (4.3, 0.65), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1))
    _grid(ax, 4.55, 0.4, 3, cell=0.17, fc="#ede9fe")
    ax.text(4.8, 0.2, "output channel", ha="center", fontsize=7.5, color=INK)
    ax.set_xlim(-0.1, 5.2)
    ax.set_ylim(0.1, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "multichannel-conv")


@fig
def neuron():
    """p30: a neuron: inputs via synapses (w_i x_i), cell body sums them, activation f gives the output axon."""
    f, ax = plt.subplots(figsize=(5.0, 2.1))
    ins = [(0.0, 1.6, "$x_0$", "$w_0 x_0$"), (0.0, 0.85, "$x_1$", "$w_1 x_1$"), (0.0, 0.1, "$x_2$", "$w_2 x_2$")]
    for x, y, lab, wl in ins:
        ax.text(x, y, lab, ha="center", va="center", fontsize=10)
        ax.annotate("", (1.83, 0.85), (x + 0.2, y), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.9))
        ax.text(0.85, y * 0.62 + 0.85 * 0.38 + 0.12, wl, fontsize=8.5, color=ACC, ha="center")
    ax.plot([0.45], [1.45], "o", color=INK, ms=4)
    ax.text(0.45, 1.7, "synapse", fontsize=7.5, color=MUT, ha="center")
    ax.text(-0.15, -0.3, "axon from a neuron", fontsize=7.5, color=MUT)
    ax.text(1.45, 0.3, "dendrite", fontsize=7.5, color=MUT)
    ax.add_patch(plt.Circle((2.35, 0.85), 0.5, fc="#ede9fe", ec=ACC, lw=1.2))
    ax.text(2.35, 1.03, "cell body", fontsize=7.5, ha="center", color=MUT)
    ax.text(2.35, 0.78, "Σ wᵢxᵢ + b", fontsize=8.5, ha="center")
    ax.annotate("", (3.95, 0.85), (2.88, 0.85), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1))
    ax.text(3.42, 1.0, "f(Σ wᵢxᵢ + b)", fontsize=8.5, ha="center")
    ax.text(3.42, 0.6, "activation function", fontsize=7.5, ha="center", color=MUT)
    ax.text(4.02, 0.85, "output axon", fontsize=8.5, va="center", color=INK)
    ax.set_xlim(-0.2, 5.0)
    ax.set_ylim(-0.45, 1.95)
    ax.axis("off")
    save(f, "neuron")


@fig
def activations():
    """p30: sketches of the common activation functions."""
    x = np.linspace(-3, 3, 200)
    curves = [
        ("Sigmoid", 1 / (1 + np.exp(-x)), (-0.1, 1.1)),
        ("tanh", np.tanh(x), (-1.15, 1.15)),
        ("ReLU", np.maximum(0, x), (-0.6, 3)),
        ("Leaky ReLU", np.maximum(0.1 * x, x), (-0.6, 3)),
        ("ELU", np.where(x >= 0, x, np.exp(x) - 1), (-1.2, 3)),
    ]
    f, axs = plt.subplots(1, 5, figsize=(7.2, 1.55))
    for ax, (name, y, lim) in zip(axs, curves, strict=True):
        ax.axhline(0, color=MUT, lw=0.6)
        ax.axvline(0, color=MUT, lw=0.6)
        ax.plot(x, y, color=ACC, lw=1.8)
        ax.set_ylim(*lim)
        ax.set_title(name, fontsize=8.5, color=INK)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
    f.tight_layout()
    save(f, "activations")


@fig
def elbow():
    """p34: the elbow method: WSS against the number of clusters k."""
    f, ax = plt.subplots(figsize=(3.4, 2.1))
    k = np.arange(1, 10)
    wss = 100 / k ** 1.6 + 6
    ax.plot(k, wss, "-o", color=ACC, ms=4, lw=1.6)
    ax.annotate("elbow", (3, wss[2]), (4.6, wss[2] + 25), fontsize=8.5, color=WARM,
                arrowprops=dict(arrowstyle="-|>", color=WARM, lw=1))
    ax.set_xlabel("k (number of clusters)", fontsize=8.5)
    ax.set_ylabel("WSS", fontsize=8.5)
    ax.set_xticks(k)
    ax.set_yticks([])
    ax.tick_params(labelsize=7.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    f.tight_layout()
    save(f, "elbow")


def _axes_only(ax, xl, yl):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(xl, fontsize=8.5)
    ax.set_ylabel(yl, fontsize=8.5)


@fig
def flex_interp():
    """p37: interpretability against flexibility for common methods (ISLR)."""
    f, ax = plt.subplots(figsize=(4.6, 2.7))
    pts = [(0.8, 9.0, "Subset selection\nLasso"), (2.6, 7.6, "Least squares"),
           (4.6, 5.6, "Generalized additive models\nTrees"), (8.2, 1.6, "Bagging, Boosting\nSVM, Deep learning")]
    for x, y, t in pts:
        ax.text(x, y, t, fontsize=8, ha="center", va="center", color=INK,
                bbox=dict(boxstyle="round,pad=0.3", fc="#ede9fe", ec=ACC, lw=0.8))
    ax.set_xlim(-0.5, 10)
    ax.set_ylim(0, 10.3)
    ax.text(-0.3, 9.9, "High", fontsize=7.5, color=MUT)
    ax.text(-0.3, 0.2, "Low", fontsize=7.5, color=MUT)
    ax.text(9.3, -0.8, "High", fontsize=7.5, color=MUT)
    _axes_only(ax, "Flexibility", "Interpretability")
    f.tight_layout()
    save(f, "flexibility-interpretability")


@fig
def mse_flexibility():
    """p37: training MSE falls monotonically; test MSE is U-shaped; Var(eps) is the floor."""
    f, ax = plt.subplots(figsize=(4.0, 2.5))
    x = np.linspace(0.05, 1, 200)
    train = 0.6 + 7.4 * np.exp(-3.2 * x)
    test = train + 0.4 + 7 * x ** 2
    ax.plot(x, test, color=ACC, lw=2, label="Test MSE")
    ax.plot(x, train, color=MUT, lw=2, label="Training MSE")
    ax.axhline(1.0, color=WARM, lw=1.2, ls="--", label="Var(ε)")
    ax.legend(fontsize=7.5, frameon=False, loc="upper right")
    ax.set_ylim(0, 9)
    _axes_only(ax, "Flexibility", "MSE")
    f.tight_layout()
    save(f, "mse-flexibility")


@fig
def funnel():
    """p41: residuals fan out (funnel shape); after transforming Y to log Y their spread is constant."""
    rng = np.random.default_rng(4)
    xf = rng.uniform(0.5, 10, 120)
    f, (a1, a2) = plt.subplots(1, 2, figsize=(5.6, 2.0))
    a1.scatter(xf, rng.normal(0, 0.28 * xf), s=6, color=ACC, alpha=0.8)
    a1.set_title("Funnel shape (heteroscedasticity)", fontsize=8.5)
    a2.scatter(xf, rng.normal(0, 0.9, xf.size), s=6, color=ACC, alpha=0.8)
    a2.set_title("After Y → log Y or √Y: constant spread", fontsize=8.5)
    for a in (a1, a2):
        a.axhline(0, color=MUT, lw=0.6)
        a.set_ylim(-5.5, 5.5)
        _axes_only(a, "Fitted values", "Residuals")
    f.tight_layout()
    save(f, "funnel")


@fig
def roc():
    """p44: ROC curve: TPR against FPR; a good classifier hugs the top-left corner; chance gives AUC = 0.5."""
    f, ax = plt.subplots(figsize=(2.8, 2.6))
    x = np.linspace(0, 1, 200)
    ax.fill_between(x, x ** 0.25, color=ACC2, alpha=0.35, lw=0)
    ax.plot(x, x ** 0.25, color=ACC, lw=2, label="ROC curve (area = AUC)")
    ax.plot([0, 1], [0, 1], color=MUT, lw=1, ls="--", label="no better than chance (AUC = 0.5)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("FPR (1 − specificity)", fontsize=8)
    ax.set_ylabel("TPR (sensitivity, recall)", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=6.5, frameon=False, loc="lower right")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    f.tight_layout()
    save(f, "roc")


@fig
def lasso_ridge():
    """p47: the lasso (diamond) and ridge (circle) constraint regions with the RSS contours around beta-hat."""
    from matplotlib.patches import Ellipse, Polygon
    f, axs = plt.subplots(1, 2, figsize=(5.4, 2.5))
    for ax, name in zip(axs, ("Lasso", "Ridge"), strict=True):
        bh = (0.75, 2.0) if name == "Lasso" else (1.6, 1.25)
        ax.axhline(0, color=MUT, lw=0.7)
        ax.axvline(0, color=MUT, lw=0.7)
        t = np.linspace(0, 2 * np.pi, 2000)
        if name == "Lasso":
            ax.add_patch(Polygon([(1, 0), (0, 1), (-1, 0), (0, -1)], fc=ACC2, ec=ACC, alpha=0.8))
            norm1 = np.abs(np.cos(t)) + np.abs(np.sin(t))
            bx, by = np.cos(t) / norm1, np.sin(t) / norm1
        else:
            ax.add_patch(plt.Circle((0, 0), 1, fc=ACC2, ec=ACC, alpha=0.8))
            bx, by = np.cos(t), np.sin(t)
        c, s_ = np.cos(np.radians(35)), np.sin(np.radians(35))
        u = (bx - bh[0]) * c - (by - bh[1]) * s_
        v = (bx - bh[0]) * s_ + (by - bh[1]) * c
        rad = np.sqrt((u / 1.1) ** 2 + (v / 0.55) ** 2)
        k = int(rad.argmin())
        touch, rmin = (bx[k], by[k]), rad[k]
        for r in (rmin / 3, 2 * rmin / 3, rmin):
            ax.add_patch(Ellipse(bh, 2.2 * r, 1.1 * r, angle=-35, fc="none", ec=WARM, lw=1))
        ax.plot(*bh, "o", color=INK, ms=3.5)
        ax.text(bh[0] + 0.1, bh[1] + 0.1, r"$\hat\beta$", fontsize=9)
        ax.plot(*touch, "o", color=ACC, ms=4.5, mec="white")
        ax.text(2.45, -0.25, r"$\beta_1$", fontsize=9)
        ax.text(0.08, 2.35, r"$\beta_2$", fontsize=9)
        ax.set_title(name, fontsize=9)
        ax.set_xlim(-1.4, 2.8)
        ax.set_ylim(-1.3, 3.0)
        ax.set_aspect("equal")
        ax.axis("off")
    f.tight_layout()
    save(f, "lasso-ridge")


@fig
def bootstrap():
    """p46: bootstrap: resample the observations with replacement B times; each sample gives an estimate."""
    from matplotlib.patches import Rectangle
    f, ax = plt.subplots(figsize=(5.0, 2.8))

    def table(x, y, rows, fc):
        for i, r in enumerate(rows):
            ax.add_patch(Rectangle((x, y - i * 0.28), 0.45, 0.28, fc=fc, ec=ACC, lw=0.8))
            ax.text(x + 0.225, y - i * 0.28 + 0.14, str(r), ha="center", va="center", fontsize=8)
    table(0, 1.4, [1, 2, 3], "#ede9fe")
    ax.text(0.22, 1.8, "Data Z", ha="center", fontsize=8.5)
    samples = [([3, 1, 3], 2.6, "*1"), ([2, 3, 1], 1.45, "*2"), ([2, 2, 1], -0.3, "*B")]
    for rows, y, tag in samples:
        ax.annotate("", (1.45, y - 0.25), (0.5, 1.0), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.8))
        table(1.5, y, rows, "#fde68a")
        ax.text(1.72, y + 0.33, f"$Z^{{{tag}}}$", ha="center", fontsize=8.5)
        ax.annotate("", (2.55, y - 0.28), (2.0, y - 0.28), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.8))
        ax.text(2.62, y - 0.28, f"$\\hat\\alpha^{{{tag}}}$", va="center", fontsize=9)
    ax.text(1.72, 0.62, "⋮", ha="center", fontsize=12)
    note = "$SE_B(\\hat\\alpha)$ = standard\ndeviation of the $\\hat\\alpha^{*r}$\n(sampling with replacement)"
    ax.text(3.3, 0.85, note, fontsize=8, va="center")
    ax.set_xlim(-0.1, 5.2)
    ax.set_ylim(-1.0, 3.05)
    ax.axis("off")
    save(f, "bootstrap")


@fig
def hyperplane():
    """p52: the hyperplane 1 + 2 X1 + 3 X2 = 0 splits the plane into the regions > 0 and < 0."""
    f, ax = plt.subplots(figsize=(3.0, 2.5))
    x = np.linspace(-1.5, 1.5, 50)
    y = -(1 + 2 * x) / 3
    ax.fill_between(x, y, 1.5, color=ACC2, alpha=0.35, lw=0)
    ax.fill_between(x, -1.5, y, color="#fde68a", alpha=0.45, lw=0)
    ax.plot(x, y, color=ACC, lw=2)
    ax.axhline(0, color=MUT, lw=0.6)
    ax.axvline(0, color=MUT, lw=0.6)
    ax.text(0.15, 0.9, "$1 + 2X_1 + 3X_2 > 0$", fontsize=8.5)
    ax.text(-1.4, -1.25, "$1 + 2X_1 + 3X_2 < 0$", fontsize=8.5)
    ax.text(1.32, -0.18, "$X_1$", fontsize=8.5)
    ax.text(0.05, 1.32, "$X_2$", fontsize=8.5)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis("off")
    save(f, "hyperplane")


@fig
def two_sided_p():
    """p52: a two-sided p-value is the area in both tails of the null distribution beyond |T|."""
    f, ax = plt.subplots(figsize=(3.6, 1.7))
    x = np.linspace(-4, 4, 400)
    y = np.exp(-x ** 2 / 2)
    ax.plot(x, y, color=ACC, lw=1.8)
    t = 2.0
    ax.fill_between(x, y, where=x >= t, color=WARM, alpha=0.7, lw=0)
    ax.fill_between(x, y, where=x <= -t, color=WARM, alpha=0.7, lw=0)
    ax.axhline(0, color=MUT, lw=0.7)
    ax.text(t, -0.14, "$|T|$", ha="center", fontsize=8.5)
    ax.text(-t, -0.14, "$-|T|$", ha="center", fontsize=8.5)
    ax.text(-2.9, 0.6, "null distribution", ha="center", fontsize=8, color=MUT)
    ax.text(3.0, 0.25, "p-value =\nboth tails", ha="center", fontsize=8, color=WARM)
    ax.set_ylim(-0.22, 1.1)
    ax.axis("off")
    save(f, "two-sided-p")


@fig
def perfect_fit():
    """p48: with as many parameters as observations, least squares fits the points exactly."""
    f, ax = plt.subplots(figsize=(2.2, 1.6))
    ax.plot([0.25, 0.75], [0.35, 0.7], "o", color=ACC, ms=5)
    ax.plot([0.0, 1.0], [0.175, 0.875], color=INK, lw=1.4)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _axes_only(ax, "X", "Y")
    f.tight_layout()
    save(f, "perfect-fit")


def _vec(ax, x, y, n=3, w=0.22, h=0.18, fc="#ede9fe"):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x - w / 2, y - n * h / 2), w, n * h, boxstyle="round,pad=0.02", fc=fc, ec=ACC, lw=0.9))
    for i in range(n):
        ax.add_patch(plt.Circle((x, y - n * h / 2 + (i + 0.5) * h), h * 0.3, fc="white", ec=ACC, lw=0.6))


def _arrow(ax, a, b, color=MUT, lw=0.8, rad=0.0):
    ax.annotate("", b, a, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=2, shrinkB=2,
                                           connectionstyle=f"arc3,rad={rad}"))


@fig
def sentiment_ffn():
    """p64: feed-forward sentiment classifier: word embeddings -> pooling -> hidden layer -> softmax outputs."""
    f, ax = plt.subplots(figsize=(6.0, 2.5))
    words = [("dessert", 1.9), ("was", 1.1), ("great", 0.3)]
    for w, y in words:
        ax.text(0.45, y, w, ha="right", va="center", fontsize=9)
        _arrow(ax, (0.5, y), (0.82, y))
        _vec(ax, 0.95, y)
        _arrow(ax, (1.08, y), (1.62, 1.1))
    ax.text(1.05, -0.35, "embeddings", ha="center", fontsize=8, color=MUT)
    ax.text(0.4, -0.35, "input words", ha="right", fontsize=8, color=MUT)
    ax.add_patch(plt.Polygon([(1.65, 1.1), (1.85, 1.3), (2.05, 1.1), (1.85, 0.9)], fc="#fde68a", ec=INK, lw=0.9))
    ax.text(1.85, 1.1, "+", ha="center", va="center", fontsize=10)
    ax.text(1.85, 0.62, "pooling\n(max / mean)", ha="center", va="top", fontsize=8, color=MUT)
    _arrow(ax, (2.06, 1.1), (2.38, 1.1))
    _vec(ax, 2.5, 1.1)
    hs = [(3.3, 1.9, "$h_1$"), (3.3, 1.1, "$h_2$"), (3.3, 0.3, "$h_d$")]
    os_ = [(4.3, 1.9, "$\\hat y_1$", "P(+)"), (4.3, 1.1, "$\\hat y_2$", "P(−)"),
           (4.3, 0.3, "$\\hat y_3$", "P(neutral)")]
    for hx, hy, hl in hs:
        _arrow(ax, (2.63, 1.1), (hx - 0.2, hy))
        ax.add_patch(plt.Circle((hx, hy), 0.2, fc="#ede9fe", ec=ACC))
        ax.text(hx, hy, hl, ha="center", va="center", fontsize=9)
        for ox, oy, _, _ in os_:
            _arrow(ax, (hx + 0.2, hy), (ox - 0.2, oy), lw=0.6)
    ax.text(3.3, 0.72, "⋮", ha="center", va="center", fontsize=10)
    for ox, oy, ol, lab in os_:
        ax.add_patch(plt.Circle((ox, oy), 0.2, fc="#fde68a", ec=INK))
        ax.text(ox, oy, ol, ha="center", va="center", fontsize=9)
        _arrow(ax, (ox + 0.2, oy), (4.75, oy))
        ax.text(4.8, oy, lab, va="center", fontsize=9)
    ax.text(3.3, -0.35, "hidden layer", ha="center", fontsize=8, color=MUT)
    ax.text(4.3, -0.35, "softmax", ha="center", fontsize=8, color=MUT)
    ax.set_xlim(-0.4, 5.6)
    ax.set_ylim(-0.5, 2.25)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "sentiment-ffn")


@fig
def markov_chain():
    """p65: a weather Markov chain over HOT, COLD and WARM with its transition probabilities."""
    f, ax = plt.subplots(figsize=(4.4, 2.6))
    pos = {"HOT": (0.0, 0.0), "COLD": (1.6, 1.3), "WARM": (3.2, 0.0)}
    for k, (x, y) in pos.items():
        ax.add_patch(plt.Circle((x, y), 0.34, fc="#ede9fe", ec=ACC, lw=1.2, zorder=3))
        ax.text(x, y, k, ha="center", va="center", fontsize=9, zorder=4)
    edges = [("HOT", "COLD", "0.1", (0.55, 0.95)), ("COLD", "HOT", "0.1", (1.0, 0.45)),
             ("HOT", "WARM", "0.3", (1.6, 0.32)), ("WARM", "HOT", "0.3", (1.6, -0.42)),
             ("COLD", "WARM", "0.1", (2.2, 0.45)), ("WARM", "COLD", "0.1", (2.65, 0.95))]
    for a, b, lab, (lx, ly) in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        d = np.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        ax.annotate("", (x2 - 0.36 * ux, y2 - 0.36 * uy), (x1 + 0.36 * ux, y1 + 0.36 * uy),
                    arrowprops=dict(arrowstyle="-|>", color=MUT, lw=1, connectionstyle="arc3,rad=-0.25"))
        ax.text(lx, ly, lab, ha="center", va="center", fontsize=8.5, color=ACC)
    for k, lab in (("HOT", "0.6"), ("COLD", "0.8"), ("WARM", "0.6")):
        x, y = pos[k]
        ang = {"HOT": 200, "COLD": 90, "WARM": -20}[k]
        a1, a2 = np.radians(ang - 28), np.radians(ang + 28)
        start, end = (x + 0.34 * np.cos(a1), y + 0.34 * np.sin(a1)), (x + 0.34 * np.cos(a2), y + 0.34 * np.sin(a2))
        ax.annotate("", end, start, arrowprops=dict(arrowstyle="-|>", color=MUT, lw=1, connectionstyle="arc3,rad=1.9"))
        ax.text(x + 0.85 * np.cos(np.radians(ang)), y + 0.85 * np.sin(np.radians(ang)), lab,
                ha="center", va="center", fontsize=8.5, color=ACC)
    ax.set_xlim(-1.0, 4.2)
    ax.set_ylim(-0.75, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "markov-chain")


def _box(ax, x, y, text, w=0.5, h=0.32, fc="#ede9fe", ec=ACC, fs=9):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.03", fc=fc, ec=ec, lw=1))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs)


@fig
def rnn_cell():
    """p67: a simple RNN (left) and one time step drawn as a feed-forward network (right)."""
    f, ax = plt.subplots(figsize=(5.6, 2.2))
    _box(ax, 0, 0, "$x_t$")
    _box(ax, 0, 1.0, "$h_t$", fc="#fde68a", ec=INK)
    _box(ax, 0, 2.0, "$y_t$")
    _arrow(ax, (0, 0.17), (0, 0.83), color=INK, lw=1)
    _arrow(ax, (0, 1.17), (0, 1.83), color=INK, lw=1)
    ax.plot([0.27, 0.62, 0.62], [0.92, 0.92, 1.25], color=ACC, lw=1.1)
    ax.annotate("", (0.15, 1.17), (0.62, 1.25), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.1,
                                                                connectionstyle="arc3,rad=0.3"))
    ax.text(0.72, 1.0, "U\n(recurrent)", fontsize=7.5, color=ACC, va="center")
    # unrolled step
    x0 = 2.6
    _box(ax, x0, 0, "$h_{t-1}$", w=0.6)
    _box(ax, x0 + 1.5, 0, "$x_t$")
    _box(ax, x0 + 1.5, 1.0, "$h_t$", fc="#fde68a", ec=INK)
    _box(ax, x0 + 1.5, 2.0, "$y_t$")
    _arrow(ax, (x0 + 0.3, 0.12), (x0 + 1.25, 0.9), color=INK, lw=1)
    _arrow(ax, (x0 + 1.5, 0.17), (x0 + 1.5, 0.83), color=INK, lw=1)
    _arrow(ax, (x0 + 1.5, 1.17), (x0 + 1.5, 1.83), color=INK, lw=1)
    ax.text(x0 + 0.65, 0.6, "U", fontsize=9, color=ACC)
    ax.text(x0 + 1.6, 0.45, "W", fontsize=9, color=ACC)
    ax.text(x0 + 1.6, 1.45, "V", fontsize=9, color=ACC)
    ax.text(x0 + 2.1, 1.0, "$h_t = g(Uh_{t-1} + Wx_t)$\n$y_t = f(Vh_t)$", fontsize=8.5, va="center")
    ax.set_xlim(-0.5, 6.3)
    ax.set_ylim(-0.3, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "rnn-cell")


@fig
def teacher_forcing():
    """p67: training an RNN language model with teacher forcing: the correct word is fed at every step."""
    f, ax = plt.subplots(figsize=(4.6, 2.6))
    xs = [0, 1.2, 2.4]
    ins = ["<s>", "So", "long"]
    tgt = ["So", "long", "and"]
    ax.add_patch(plt.Rectangle((-0.45, 0.75), 3.3, 0.55, fc="none", ec=MUT, lw=0.8, ls="--"))
    ax.text(2.95, 1.02, "RNN", fontsize=8, color=MUT, va="center")
    for i, x in enumerate(xs):
        _box(ax, x, 0, ins[i], w=0.6)
        _vec(ax, x, 0.5, n=2, h=0.14)
        _box(ax, x, 1.02, f"$h_{i + 1}$", w=0.45, fc="#fde68a", ec=INK)
        _arrow(ax, (x, 0.17), (x, 0.36))
        _arrow(ax, (x, 0.64), (x, 0.86))
        _arrow(ax, (x, 1.18), (x, 1.52))
        _box(ax, x, 1.7, "softmax", w=0.75, fs=8)
        _arrow(ax, (x, 1.86), (x, 2.12))
        ax.text(x, 2.25, f"$-\\log\\, y_{{\\mathrm{{{tgt[i]}}}}}$", ha="center", fontsize=8.5)
        if i:
            _arrow(ax, (xs[i - 1] + 0.23, 1.02), (x - 0.23, 1.02), color=INK, lw=1)
    ax.text(-0.75, 0.0, "input", fontsize=7.5, color=MUT, ha="right", va="center")
    ax.text(-0.75, 2.25, "loss", fontsize=7.5, color=MUT, ha="right", va="center")
    ax.set_xlim(-1.4, 3.4)
    ax.set_ylim(-0.3, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "teacher-forcing")


@fig
def autoregressive():
    """p67: autoregressive generation: each sampled word is fed back as the next input."""
    f, ax = plt.subplots(figsize=(4.6, 2.2))
    xs = [0, 1.2, 2.4]
    ins = ["<s>", "So", "long"]
    outs = ["So", "long", "ago"]
    for i, x in enumerate(xs):
        _box(ax, x, 0, ins[i], w=0.6)
        _box(ax, x, 0.8, "RNN", w=0.6, fc="#fde68a", ec=INK, fs=8)
        _box(ax, x, 1.6, outs[i], w=0.6, fc="#dcfce7", ec="#16a34a")
        _arrow(ax, (x, 0.17), (x, 0.63))
        _arrow(ax, (x, 0.97), (x, 1.43))
        if i:
            _arrow(ax, (xs[i - 1] + 0.3, 0.8), (x - 0.3, 0.8), color=INK, lw=1)
        if i < 2:
            ax.annotate("", (xs[i + 1] - 0.2, 0.17), (x + 0.3, 1.5),
                        arrowprops=dict(arrowstyle="-|>", color=ACC, lw=0.9, ls="--", connectionstyle="arc3,rad=-0.2"))
    ax.text(3.0, 1.6, "sampled word", fontsize=7.5, color=MUT, va="center")
    ax.set_xlim(-0.5, 3.8)
    ax.set_ylim(-0.3, 1.9)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "autoregressive")


@fig
def causal_attention():
    """p68: a causal self-attention layer: each output y_i attends to the inputs x_1..x_i."""
    f, ax = plt.subplots(figsize=(4.2, 2.3))
    xs = [0, 1, 2, 3]
    ax.add_patch(plt.Rectangle((-0.5, 0.75), 4.0, 0.6, fc="#f5f3ff", ec=MUT, lw=0.8, ls="--"))
    ax.text(-0.6, 1.05, "self-attention\nlayer", ha="right", va="center", fontsize=7.5, color=MUT)
    for i, x in enumerate(xs):
        _box(ax, x, 1.05, "", w=0.45, h=0.26, fc="#fde68a", ec=INK)
        ax.text(x, 0.0, f"$x_{i + 1}$", ha="center", va="center", fontsize=10)
        ax.text(x, 2.05, f"$y_{i + 1}$", ha="center", va="center", fontsize=10)
        _arrow(ax, (x, 1.2), (x, 1.9), color=INK, lw=1)
        for j in range(i + 1):
            _arrow(ax, (xs[j], 0.15), (x - 0.05 * (i - j), 0.9), color=ACC if j == i else MUT, lw=0.8)
    ax.set_xlim(-1.6, 3.7)
    ax.set_ylim(-0.25, 2.25)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "causal-attention")


@fig
def semantic_space():
    """p60: words with similar meanings are nearby in the embedding space."""
    from matplotlib.patches import Ellipse
    f, ax = plt.subplots(figsize=(3.8, 2.0))
    groups = [((0.9, 1.3), ["not good", "bad", "worst"], "#fee2e2", "#dc2626"),
              ((2.8, 0.6), ["good", "wonderful", "great"], "#dcfce7", "#16a34a")]
    for (cx, cy), words, fc, ec in groups:
        ax.add_patch(Ellipse((cx, cy), 1.6, 0.95, fc=fc, ec=ec, lw=1))
        for k, w in enumerate(words):
            ax.text(cx + (k - 1) * 0.42, cy + (0.2 if k % 2 else -0.15), w, ha="center", fontsize=8.5)
    ax.annotate("", (4.0, 0), (0, 0), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.8))
    ax.annotate("", (0, 2.0), (0, 0), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.8))
    ax.set_xlim(-0.1, 4.1)
    ax.set_ylim(-0.1, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, "semantic-space")


@fig
def sentence_embeddings():
    """p75: sentence embeddings projected to 2-D form 3 clusters: greetings, dogs and soccer."""
    from matplotlib.patches import FancyBboxPatch
    f, ax = plt.subplots(figsize=(5.0, 2.9))
    pts = [(0.75, 2.55, "Hey, what's up?", "left"), (1.5, 2.15, "Hi, how's it going?", "left"),
           (0.4, 1.95, "Hello, how are you?", "left"),
           (1.0, 1.0, "I adore my dog", "left"), (0.5, 0.62, "I love my dog", "left"),
           (1.15, 0.3, "I like my dog", "left"),
           (2.7, 1.4, "I enjoyed watching the World Cup", "left"), (2.55, 0.85, "I love watching soccer", "left"),
           (2.65, 0.35, "I like watching soccer matches", "left")]
    for x, y, t, ha in pts:
        ax.plot(x, y, "o", color=ACC, ms=5)
        ax.text(x + (0.08 if ha == "left" else -0.08), y, t, ha=ha, va="center", fontsize=8)
    ax.add_patch(FancyBboxPatch((0.05, 0.05), 4.75, 2.75, boxstyle="round,pad=0.05", fc="none", ec=MUT, lw=0.9))
    ax.set_xlim(0, 5.75)
    ax.set_ylim(0, 2.9)
    ax.axis("off")
    save(f, "sentence-embeddings")


@fig
def cosine_angles():
    """p77: rays at a right angle have cosine 0 (similarity 0); rays at a small angle, cosine 0.98."""
    f, axs = plt.subplots(1, 2, figsize=(4.4, 1.9))
    panels = ((axs[0], 90, "cos α = 0  →  similarity = 0"), (axs[1], 11.5, "cos α = 0.98  →  similarity = 0.98"))
    for ax, ang, lab in panels:
        base = 25 if ang < 45 else 0
        for a in (base, base + ang):
            ax.annotate("", (np.cos(np.radians(a)), np.sin(np.radians(a))), (0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.3))
            ax.plot(np.cos(np.radians(a)), np.sin(np.radians(a)), "o", color=INK, ms=4)
        t = np.radians(np.linspace(base, base + ang, 30))
        ax.plot(0.3 * np.cos(t), 0.3 * np.sin(t), color=WARM, lw=1)
        ax.text(0.38 * np.cos(np.radians(base + ang / 2)) + 0.03, 0.38 * np.sin(np.radians(base + ang / 2)), "α",
                fontsize=9, color=WARM)
        ax.plot(0, 0, "o", color=MUT, ms=3)
        ax.set_title(lab, fontsize=8, y=-0.22)
        ax.set_xlim(-0.2, 1.2)
        ax.set_ylim(-0.15, 1.15)
        ax.set_aspect("equal")
        ax.axis("off")
    save(f, "cosine-angles")


@fig
def attention_bank():
    """p82: in each sentence attention links "bank" to the word that gives its context."""
    f, ax = plt.subplots(figsize=(3.6, 1.6))
    rows = [(1.0, ["The", "bank", "of", "the", "river"], 4, 1), (0.0, ["Money", "in", "the", "bank"], 0, 3)]
    for y, words, src, dst in rows:
        xs = np.cumsum([0] + [0.12 * len(w) + 0.25 for w in words[:-1]])
        cx = [x + 0.06 * len(w) for x, w in zip(xs, words, strict=True)]
        for x, w in zip(xs, words, strict=True):
            ax.text(x, y, w, fontsize=10, va="center")
        w = words[src]
        ax.add_patch(plt.Rectangle((xs[src] - 0.05, y - 0.17), 0.12 * len(w) + 0.1, 0.34, fc="none", ec=ACC, lw=1.1))
        ax.annotate("", (cx[dst], y + 0.2), (cx[src], y + 0.2),
                    arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.1,
                                    connectionstyle="bar,fraction=0.12" if src > dst else "bar,fraction=-0.12"))
    ax.text(-0.25, 0.5, "Attention", rotation=90, va="center", ha="center", fontsize=8, color=MUT)
    ax.set_xlim(-0.4, 2.7)
    ax.set_ylim(-0.3, 1.6)
    ax.axis("off")
    save(f, "attention-bank")


@fig
def apple_moves():
    """p93: attention moves "apple" towards "orange" (sentence 1) or towards "phone" (sentence 2)."""
    f, ax = plt.subplots(figsize=(3.4, 3.0))
    pts = {"orange": (11, 11), "phone": (1, 2), "apple": (6, 7)}
    for k, (x, y) in pts.items():
        ax.plot(x, y, "o", color=ACC if k != "apple" else INK, ms=6)
        dx, dy = (0.4, -0.6) if k == "apple" else (0.3, 0.3)
        ax.text(x + dx, y + dy, f"{k} ({x}, {y})", fontsize=8)
    for (x, y), lab in (((8, 8.5), "apple (8, 8.5)\nsentence 1"), ((4, 5), "apple (4, 5)\nsentence 2")):
        ax.annotate("", (x, y), (6, 7), arrowprops=dict(arrowstyle="-|>", color=WARM, lw=1.4))
        ax.plot(x, y, "o", color=WARM, ms=5)
        ax.text(x + 0.4, y + (0.2 if x > 6 else -1.3), lab, fontsize=7.5, color=WARM)
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 12.5)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    f.tight_layout()
    save(f, "apple-moves")


@fig
def good_worst_embedding():
    """p94: a good embedding separates orange and phone; the worst one puts them together."""
    f, axs = plt.subplots(1, 2, figsize=(4.4, 1.7))
    layouts = [("Good embedding", {"orange": (0.25, 0.85), "phone": (0.85, 0.15)}),
               ("Worst embedding", {"phone": (0.55, 0.75), "orange": (0.62, 0.68)})]
    for ax, (title, pts) in zip(axs, layouts, strict=True):
        ax.annotate("", (1.05, 0), (0, 0), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.8))
        ax.annotate("", (0, 1.05), (0, 0), arrowprops=dict(arrowstyle="-|>", color=MUT, lw=0.8))
        for k, (x, y) in pts.items():
            ax.plot(x, y, "o", color=ACC, ms=5)
            ax.text(x + 0.04, y + (0.06 if k == "phone" else -0.12), k, fontsize=8)
        ax.set_title(title, fontsize=8.5)
        ax.set_xlim(-0.05, 1.15)
        ax.set_ylim(-0.05, 1.1)
        ax.set_aspect("equal")
        ax.axis("off")
    save(f, "good-worst-embedding")


def _blk(ax, cx, cy, text, w=1.4, h=0.4, fc="#ede9fe", ec=ACC, fs=8.5, ls="-", lw=1.0):
    """A rounded block centred on (cx, cy); returns its (left, right, bottom, top) edges."""
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=lw, ls=ls))
    if text:
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=INK)
    return cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2


def _container(ax, x0, y0, x1, y1, label=None, fc="#f8fafc", ec=MUT, fs=8):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.02,rounding_size=0.1",
                                fc=fc, ec=ec, lw=0.9))
    if label:
        ax.text(x0 + 0.08, y1 + 0.06, label, fontsize=fs, color=MUT, va="bottom")


def _go(ax, a, b, color=INK, lw=1.0, style="-|>", cs=None):
    props = dict(arrowstyle=style, color=color, lw=lw, shrinkA=0, shrinkB=0)
    if cs:
        props["connectionstyle"] = cs
    ax.annotate("", b, a, arrowprops=props)


def _finish(ax, f, name, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    save(f, name)


def _ffn_attention_block(ax, cx, y0, w=1.5):
    """A transformer block: Attention below Feed-forward inside a container; returns (bottom, top)."""
    _container(ax, cx - w / 2 - 0.1, y0, cx + w / 2 + 0.1, y0 + 1.25, fc="white")
    _blk(ax, cx, y0 + 0.32, "Attention", w=w - 0.2, h=0.34)
    _blk(ax, cx, y0 + 0.93, "Feed-forward", w=w - 0.2, h=0.34, fc="#fde68a", ec=INK)
    _go(ax, (cx, y0 + 0.49), (cx, y0 + 0.76))
    return y0, y0 + 1.25


@fig
def transformer_architecture():
    """p110: input -> tokenisation -> embedding -> positional encoding -> transformer blocks -> softmax -> output."""
    f, ax = plt.subplots(figsize=(5.6, 3.9))
    xs = 0.9
    steps = [("Write a story", 0.4, "#ffffff"), ("Tokenisation", 1.25, "#ede9fe"),
             ("Embedding", 2.1, "#ede9fe"), ("Positional\nencoding", 2.95, "#ede9fe")]
    for i, (t, y, fc) in enumerate(steps):
        _blk(ax, xs, y, t, w=1.5, h=0.5, fc=fc, ls="--" if i == 0 else "-")
        if i:
            _go(ax, (xs, steps[i - 1][1] + 0.25), (xs, y - 0.25))
    ax.text(xs, -0.05, "Input", ha="center", fontsize=8.5, color=MUT)
    bx = 3.0
    tops = []
    for k in range(3):
        b, t = _ffn_attention_block(ax, bx, 0.15 + k * 1.45)
        tops.append((b, t))
        if k:
            _go(ax, (bx, tops[k - 1][1]), (bx, b))
    ax.text(bx, 4.55, "Series of transformer blocks", ha="center", fontsize=8.5, color=MUT)
    ax.plot([xs + 0.75, 1.95, 1.95], [2.95, 2.95, 0.47], color=INK, lw=1)
    _go(ax, (1.95, 0.47), (bx - 0.85, 0.47))
    _blk(ax, 5.0, 1.0, "Softmax", w=1.1, h=0.45, fc="#fde68a", ec=INK)
    _blk(ax, 5.0, 2.0, "Once", w=1.1, h=0.45, fc="white", ls="--")
    ax.text(5.0, 2.4, "Output", ha="center", fontsize=8.5, color=MUT)
    ax.plot([bx + 0.85, 4.15, 4.15], [tops[2][1] - 0.3, tops[2][1] - 0.3, 1.0], color=INK, lw=1)
    _go(ax, (4.15, 1.0), (4.45, 1.0))
    _go(ax, (5.0, 1.225), (5.0, 1.775))
    _finish(ax, f, "transformer-architecture", (-0.1, 5.7), (-0.25, 4.75))


@fig
def transformer_blocks():
    """p117: a transformer is a concatenation of many transformer blocks (attention + feed-forward)."""
    f, ax = plt.subplots(figsize=(5.6, 1.7))
    xs = [0.9, 2.9, 4.9]
    for i, x in enumerate(xs):
        _ffn_attention_block(ax, x, 0.0)
        ax.text(x, 1.32, "Transformer block", ha="center", fontsize=8, color=MUT)
        if i:
            _go(ax, (xs[i - 1] + 0.85, 0.62), (x - 0.85, 0.62))
    _go(ax, (-0.4, 0.62), (xs[0] - 0.85, 0.62))
    _go(ax, (xs[-1] + 0.85, 0.62), (6.2, 0.62))
    _finish(ax, f, "transformer-blocks", (-0.5, 6.3), (-0.1, 1.55))


@fig
def softmax_output():
    """p120: the transformer gives scores; softmax turns them into next-word probabilities."""
    f, ax = plt.subplots(figsize=(5.6, 2.6))
    for k in range(4):
        _blk(ax, 0.2 + k * 0.32, 1.2, "", w=0.3, h=0.3, fc="#ede9fe")
    ax.text(0.68, 0.8, "Write a story", ha="center", fontsize=8, color=MUT)
    _go(ax, (1.4, 1.2), (1.8, 1.2))
    _blk(ax, 2.45, 1.2, "Transformer", w=1.2, h=0.45, fc="#fde68a", ec=INK)
    _go(ax, (3.05, 1.2), (3.4, 1.2))
    _blk(ax, 3.95, 1.2, "Softmax", w=1.0, h=0.45, fc="#fde68a", ec=INK)
    _go(ax, (4.45, 1.2), (4.75, 1.2))
    rows = [("Aardvark", "0"), ("…", ""), ("Once", "0.5"), ("…", ""), ("Somewhere", "0.3"), ("…", ""),
            ("There", "0.2"), ("…", ""), ("Zygote", "0")]
    for i, (w, pr) in enumerate(rows):
        y = 2.3 - i * 0.27
        _blk(ax, 5.45, y, w, w=1.25, h=0.25, fc="#dcfce7" if w == "Once" else "white", ec=MUT, fs=7.5)
        ax.text(6.2, y, pr, va="center", fontsize=7.5, color=ACC)
    _finish(ax, f, "softmax-output", (-0.1, 6.6), (-0.1, 2.5))


def _cells(ax, x, y, n=4, cw=0.16, h=0.2, fc="#ede9fe"):
    for i in range(n):
        ax.add_patch(plt.Rectangle((x + i * cw, y - h / 2), cw, h, fc=fc, ec=ACC, lw=0.8))


@fig
def transformer_blackbox():
    """p123: the transformer as a black box, then opened into encoders and decoders."""
    f, ax = plt.subplots(figsize=(5.6, 2.3))
    _blk(ax, 0.75, 1.7, "Je suis étudiant", w=1.4, h=0.38, fc="white", ls="--")
    _go(ax, (1.45, 1.7), (1.85, 1.7))
    _blk(ax, 2.55, 1.7, "The Transformer", w=1.4, h=0.5, fc="#fde68a", ec=INK)
    _go(ax, (3.25, 1.7), (3.65, 1.7))
    _blk(ax, 4.35, 1.7, "I am a student", w=1.4, h=0.38, fc="white", ls="--")
    ax.text(0.75, 2.0, "Input", ha="center", fontsize=8, color=MUT)
    ax.text(4.35, 2.0, "Output", ha="center", fontsize=8, color=MUT)
    _container(ax, 1.65, 0.05, 3.45, 1.05, fc="#fffbeb", ec=WARM)
    _blk(ax, 2.1, 0.55, "Encoders", w=0.75, h=0.5)
    _blk(ax, 3.0, 0.55, "Decoders", w=0.75, h=0.5)
    _go(ax, (2.475, 0.55), (2.625, 0.55))
    _go(ax, (1.1, 0.55), (1.72, 0.55))
    ax.text(1.05, 0.55, "Je suis étudiant", ha="right", va="center", fontsize=8)
    _go(ax, (3.38, 0.55), (3.9, 0.55))
    ax.text(3.95, 0.55, "I am a student", va="center", fontsize=8)
    _go(ax, (2.55, 1.45), (2.55, 1.1), color=MUT, style="-|>")
    ax.text(2.62, 1.27, "opening the box", fontsize=7, color=MUT, va="center")
    _finish(ax, f, "transformer-blackbox", (-0.1, 5.2), (-0.05, 2.2))


@fig
def encoder_decoder_stack():
    """p123: a stack of 6 encoders and 6 decoders; the top encoder's output goes to every decoder."""
    f, ax = plt.subplots(figsize=(4.4, 3.4))
    for i in range(6):
        y = 0.4 + i * 0.42
        _blk(ax, 0.8, y, "Encoder", w=1.1, h=0.3)
        _blk(ax, 3.0, y, "Decoder", w=1.1, h=0.3, fc="#fde68a", ec=INK)
        if i:
            _go(ax, (0.8, y - 0.27), (0.8, y - 0.15), lw=0.8)
            _go(ax, (3.0, y - 0.27), (3.0, y - 0.15), lw=0.8)
        _go(ax, (1.35, 0.4 + 5 * 0.42), (2.45, y), color=ACC, lw=0.8)
    _container(ax, 0.1, 0.12, 3.7, 2.75, fc="none")
    _blk(ax, 0.8, -0.2, "Je suis étudiant", w=1.4, h=0.3, fc="white", ls="--")
    _go(ax, (0.8, -0.05), (0.8, 0.25))
    ax.text(0.8, -0.6, "Input", ha="center", fontsize=8, color=MUT)
    _blk(ax, 3.0, 3.1, "I am a student", w=1.4, h=0.3, fc="white", ls="--")
    _go(ax, (3.0, 0.4 + 5 * 0.42 + 0.15), (3.0, 2.95))
    ax.text(3.0, 3.35, "Output", ha="center", fontsize=8, color=MUT)
    _finish(ax, f, "encoder-decoder-stack", (-0.1, 3.9), (-0.75, 3.5))


@fig
def encoder_layers():
    """p124-125: an encoder (self-attention, feed-forward) and a decoder (adds encoder-decoder attention)."""
    f, ax = plt.subplots(figsize=(5.0, 2.3))
    _container(ax, 0.1, 0.1, 2.0, 1.4, label="Encoder")
    _blk(ax, 1.05, 0.45, "Self-Attention", w=1.6, h=0.35)
    _blk(ax, 1.05, 1.05, "Feed Forward", w=1.6, h=0.35, fc="#fde68a", ec=INK)
    _go(ax, (1.05, 0.625), (1.05, 0.875))
    _container(ax, 2.8, 0.1, 4.7, 2.0, label="Decoder")
    _blk(ax, 3.75, 0.45, "Self-Attention", w=1.6, h=0.35)
    _blk(ax, 3.75, 1.05, "Encoder-Decoder\nAttention", w=1.6, h=0.42)
    _blk(ax, 3.75, 1.65, "Feed Forward", w=1.6, h=0.35, fc="#fde68a", ec=INK)
    _go(ax, (3.75, 0.625), (3.75, 0.84))
    _go(ax, (3.75, 1.26), (3.75, 1.475))
    _go(ax, (1.85, 1.05), (2.95, 1.05), color=ACC, cs="arc3,rad=-0.2")
    for x in (1.05, 3.75):
        _go(ax, (x, -0.25), (x, 0.275), lw=0.8)
    _finish(ax, f, "encoder-layers", (-0.05, 4.85), (-0.3, 2.25))


@fig
def encoder_flow():
    """p125-126: each word vector flows through its own path: self-attention gives z_i, then the feed-forward."""
    f, ax = plt.subplots(figsize=(4.6, 3.0))
    words = [("$x_1$", "Je", 0.9), ("$x_2$", "suis", 2.2), ("$x_3$", "étudiant", 3.5)]
    _container(ax, 0.2, 0.65, 4.4, 2.75)
    ax.text(4.35, 2.62, "Encoder", ha="right", fontsize=8, color=MUT)
    _blk(ax, 2.3, 1.0, "Self-Attention", w=3.8, h=0.4)
    _blk(ax, 2.3, 2.2, "Feed Forward Neural Network", w=3.8, h=0.4, fc="#fde68a", ec=INK)
    for xl, w, x in words:
        _cells(ax, x - 0.32, 0.15)
        ax.text(x - 0.42, 0.15, xl, ha="right", va="center", fontsize=9)
        ax.text(x, -0.15, w, ha="center", fontsize=8)
        _go(ax, (x, 0.27), (x, 0.8), lw=0.8)
        _cells(ax, x - 0.32, 1.65, fc="#fef3c7")
        ax.text(x - 0.42, 1.65, xl.replace("x", "z"), ha="right", va="center", fontsize=9)
        _go(ax, (x, 1.2), (x, 1.55), lw=0.8)
        _go(ax, (x, 1.75), (x, 2.0), lw=0.8)
        _go(ax, (x, 2.4), (x, 3.0), lw=0.8)
    _finish(ax, f, "encoder-flow", (0.0, 4.6), (-0.3, 3.1))


def _mat(ax, x, y, rows, cols, cell=0.16, fc="#ede9fe", ec=ACC, label=None, lfs=8.5):
    """A rows x cols grid whose bottom-left corner is (x, y); returns its (width, height)."""
    for i in range(rows):
        for j in range(cols):
            ax.add_patch(plt.Rectangle((x + j * cell, y + i * cell), cell, cell, fc=fc, ec=ec, lw=0.7))
    if label:
        ax.text(x + cols * cell / 2, y + rows * cell + 0.06, label, ha="center", va="bottom", fontsize=lfs)
    return cols * cell, rows * cell


@fig
def qkv_matrices():
    """p136: Q, K and V are the embeddings matrix X times the trained weight matrices W^Q, W^K, W^V."""
    f, ax = plt.subplots(figsize=(3.0, 3.1))
    cols = [("#ede9fe", "Q"), ("#fde68a", "K"), ("#dcfce7", "V")]
    for k, (fc, nm) in enumerate(cols):
        y0 = (2 - k) * 1.15
        _mat(ax, 0, y0 + 0.25, 2, 4, label="$X$" if k == 0 else None)
        ax.text(0.8, y0 + 0.41, "×", ha="center", va="center", fontsize=11)
        _mat(ax, 0.95, y0, 4, 3, fc=fc, ec=INK if nm == "K" else ACC)
        ax.text(1.19, y0 - 0.14, f"$W^{nm}$", ha="center", va="center", fontsize=9)
        ax.text(1.65, y0 + 0.41, "=", ha="center", va="center", fontsize=11)
        _mat(ax, 1.85, y0 + 0.25, 2, 3, fc=fc)
        ax.text(2.4, y0 + 0.41, f"${nm}$", va="center", fontsize=10)
    _finish(ax, f, "qkv-matrices", (-0.1, 2.7), (-0.3, 3.2))


@fig
def attention_matrix_form():
    """p137: the self-attention calculation in matrix form: softmax(Q K^T / sqrt(d_k)) V = Z."""
    f, ax = plt.subplots(figsize=(4.6, 1.55))
    ax.text(0.0, 0.55, "softmax", va="center", fontsize=10)
    ax.text(0.95, 0.55, "(", va="center", fontsize=26, color=MUT)
    _mat(ax, 1.15, 0.72, 2, 3, label="$Q$")
    ax.text(1.75, 0.88, "×", ha="center", va="center", fontsize=10)
    _mat(ax, 1.95, 0.64, 3, 2, fc="#fde68a", ec=INK, label="$K^T$")
    ax.plot([1.1, 2.35], [0.55, 0.55], color=INK, lw=1)
    ax.text(1.72, 0.32, "√dₖ", ha="center", va="center", fontsize=10)
    ax.text(2.4, 0.55, ")", va="center", fontsize=26, color=MUT)
    _mat(ax, 2.7, 0.39, 2, 3, fc="#dcfce7", label="$V$")
    ax.text(3.35, 0.55, "=", ha="center", va="center", fontsize=12)
    _mat(ax, 3.6, 0.39, 2, 3, fc="#fecaca", ec="#dc2626", label="$Z$")
    _finish(ax, f, "attention-matrix-form", (-0.1, 4.3), (0.05, 1.35))


@fig
def multihead_concat():
    """p140-142: 8 heads give 8 Z matrices; they are concatenated and multiplied by W^O into one Z."""
    f, ax = plt.subplots(figsize=(5.6, 2.7))
    _mat(ax, 2.4, 2.25, 2, 4, label="Thinking Machines  $X$", lfs=8)
    xs = [0.2, 0.95, 1.7, 2.45, 3.2, 3.95, 4.7]
    labels = ["$Z_0$", "$Z_1$", "$Z_2$", "$Z_3$", "$Z_4$", "$Z_5$", "$Z_6$"]
    for x, lab in zip(xs[:3], labels[:3], strict=True):
        _go(ax, (2.72, 2.2), (x + 0.24, 1.98), color=MUT, lw=0.7)
        _mat(ax, x, 1.38, 2, 3, fc="#fecaca", ec="#dc2626", label=lab)
    ax.text(3.35, 1.55, "…", ha="center", va="center", fontsize=12)
    _go(ax, (2.72, 2.2), (4.95, 1.98), color=MUT, lw=0.7)
    _mat(ax, 4.7, 1.38, 2, 3, fc="#fecaca", ec="#dc2626", label="$Z_7$")
    ax.text(0.2, 2.35, "8 attention heads", fontsize=8, color=MUT)
    for k in range(8):
        _mat(ax, 0.2 + k * 0.42, 0.25, 2, 3, cell=0.14, fc="#fecaca", ec="#dc2626")
    ax.text(0.2, 0.75, "1) concatenate all the attention heads", fontsize=8, color=MUT)
    ax.text(3.75, 0.39, "×", ha="center", va="center", fontsize=11)
    _mat(ax, 3.95, 0.0, 4, 3, cell=0.14, fc="#fde68a", ec=INK, label="$W^O$")
    ax.text(4.55, 0.39, "=", ha="center", va="center", fontsize=11)
    _mat(ax, 4.75, 0.25, 2, 3, cell=0.14, fc="#ede9fe", label="$Z$")
    _finish(ax, f, "multihead-concat", (0.0, 5.4), (-0.1, 2.85))


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for fn in FIGS:
        fn()
    print(f"{len(FIGS)} figures written to {os.path.relpath(OUT)}")


if __name__ == "__main__":
    main()
