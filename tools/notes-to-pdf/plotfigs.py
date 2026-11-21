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
        ax.text(d[0] * 1.08, d[1] * 1.08 + 0.2, lab, fontsize=8.5, color=INK if k else "#b45309",
                ha="center", bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
    ax.set_xlim(-5, 5)
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


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for fn in FIGS:
        fn()
    print(f"{len(FIGS)} figures written to {os.path.relpath(OUT)}")


if __name__ == "__main__":
    main()
