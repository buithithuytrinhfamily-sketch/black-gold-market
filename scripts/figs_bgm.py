#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draw schematic teaching figures for the Black Gold Market academy.

Light paper background, Black Gold Market ink and gold. Schematic only:
no real prices, no entry, stop or take profit that could read as a signal.
Figures are written to images/lessons/<slug>-<n>.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "lessons")
os.makedirs(OUT, exist_ok=True)

PAPER = "#faf7f0"
INK = "#20231e"
GOLD = "#986800"
GOLD_L = "#d0a74a"
RED = "#b3261e"
GREEN = "#2f6b3f"
MUTE = "#7b7f76"
LINE = "#ded8cc"
UP_FACE = "#ffffff"
DOWN_FACE = "#20231e"

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 11
BBOX = dict(facecolor=PAPER, edgecolor="none", pad=1.5)


def figure(w=10.0, h=5.4):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    return fig, ax


def clean(ax, xmargin=0.05, ymargin=0.14):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.margins(x=xmargin, y=ymargin)


def title(ax, text, sub=None):
    ax.set_title(text, color=INK, fontsize=15, fontweight="bold", loc="left", pad=16)
    if sub:
        ax.text(0, 1.015, sub, transform=ax.transAxes, color=MUTE, fontsize=11,
                va="bottom", ha="left")


def candle(ax, x, o, c, hi=None, lo=None, w=0.30, face=None, edge=INK, lw=1.2, z=4):
    hi = max(o, c) if hi is None else hi
    lo = min(o, c) if lo is None else lo
    up = c >= o
    ax.plot([x, x], [lo, hi], color=edge, lw=1.1, solid_capstyle="round", zorder=z)
    body_lo = min(o, c)
    height = abs(c - o) or 0.06
    ax.add_patch(Rectangle((x - w, body_lo), 2 * w, height,
                           facecolor=face or (UP_FACE if up else DOWN_FACE),
                           edgecolor=edge, lw=lw, zorder=z + 1))


def series(ax, candles, x0=0, **kw):
    for i, c in enumerate(candles):
        o, cl = c[0], c[1]
        hi = c[2] if len(c) > 2 else None
        lo = c[3] if len(c) > 3 else None
        candle(ax, x0 + i, o, cl, hi, lo, **kw)


def zone(ax, y0, y1, x0, x1, color=GOLD, alpha=0.14, label=None, label_x=None):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=color,
                           edgecolor="none", alpha=alpha, zorder=1))
    ax.plot([x0, x1], [y0, y0], color=color, lw=1.0, ls=(0, (5, 4)), zorder=2)
    ax.plot([x0, x1], [y1, y1], color=color, lw=1.0, ls=(0, (5, 4)), zorder=2)
    if label:
        ax.text(label_x if label_x is not None else x0 + 0.2, y1, " " + label,
                color=color, fontsize=10.5, fontweight="bold", va="bottom", bbox=BBOX, zorder=6)


def hline(ax, y, x0, x1, color=GOLD, ls=(0, (6, 4)), lw=1.4, label=None, side="right"):
    ax.plot([x0, x1], [y, y], color=color, lw=lw, ls=ls, zorder=5)
    if label:
        if side == "right":
            ax.text(x1, y, "  " + label, color=color, fontsize=10.5, va="center",
                    ha="left", bbox=BBOX, zorder=6)
        else:
            ax.text(x0, y, label + "  ", color=color, fontsize=10.5, va="center",
                    ha="right", bbox=BBOX, zorder=6)


def note(ax, x, y, text, color=INK, size=10.5, weight="normal", ha="center", va="center"):
    ax.text(x, y, text, color=color, fontsize=size, fontweight=weight,
            ha=ha, va=va, bbox=BBOX, zorder=7)


def arrow(ax, xy_from, xy_to, color=MUTE, lw=1.3, style="-|>"):
    ax.add_patch(FancyArrowPatch(xy_from, xy_to, arrowstyle=style, mutation_scale=13,
                                 color=color, lw=lw, zorder=6,
                                 shrinkA=2, shrinkB=2))


def footer(ax, text="Black Gold Market  ·  schematic teaching diagram  ·  no prices, no signals"):
    ax.text(0, -0.085, text, transform=ax.transAxes, color=MUTE, fontsize=9.5,
            ha="left", va="top")


def save(fig, ax, slug, n=1):
    footer(ax)
    path = os.path.join(OUT, "%s-%d.png" % (slug, n))
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor=PAPER, pad_inches=0.3)
    plt.close(fig)
    print("->", os.path.relpath(path, ROOT))
    return path
