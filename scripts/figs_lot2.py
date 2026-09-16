#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figures for the Black Gold Market academy, batch 2 (lessons 11 to 20).

Run:  python3 scripts/figs_lot2.py
Schematic only. No real prices, no entry, stop or target.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from figs_bgm import (figure, clean, title, candle, series, zone, hline, note,
                      arrow, save, PAPER, INK, GOLD, GOLD_L, RED, GREEN, MUTE,
                      LINE, UP_FACE, DOWN_FACE, BBOX, OUT)
import os


# 11 ------------------------------------------------------- fibonacci/pivots
def fibonacci_and_pivot_levels():
    fig, ax = figure(10, 5.4)
    title(ax, "Retracement levels are only as honest as the swing you drew them from")
    lo, hi = 3.0, 8.0
    data = [(3.2, 3.1, 3.4, 3.0), (3.1, 4.0, 4.2, 3.05), (4.0, 5.1, 5.3, 3.9),
            (5.1, 6.2, 6.5, 5.0), (6.2, 7.4, 7.6, 6.1), (7.4, 7.9, 8.0, 7.2),
            (7.9, 7.1, 8.0, 7.0), (7.1, 6.6, 7.3, 6.4), (6.6, 6.9, 7.1, 6.3),
            (6.9, 6.1, 7.0, 5.9), (6.1, 5.7, 6.3, 5.5), (5.7, 6.0, 6.2, 5.6)]
    series(ax, data)
    rng = hi - lo
    for r, lab in [(0.236, "0.236"), (0.382, "0.382"), (0.5, "0.5"), (0.618, "0.618"), (0.786, "0.786")]:
        y = hi - rng * r
        col = GOLD if r in (0.382, 0.618) else MUTE
        hline(ax, y, -0.6, 11.6, color=col, ls=(0, (5, 5)), lw=1.2, label=lab)
    note(ax, 0.6, 2.75, "swing low used", size=10.5, color=GREEN)
    note(ax, 5.6, 8.35, "swing high used", size=10.5, color=GREEN)
    arrow(ax, (0.8, 2.92), (1.05, 3.1), color=GREEN)
    arrow(ax, (5.6, 8.2), (5.4, 7.95), color=GREEN)
    note(ax, 9.2, 3.35, "Draw from a different pair of swings\nand every level below moves.",
         size=10.5, color=INK)
    clean(ax)
    save(fig, ax, "fibonacci-and-pivot-levels")


# 12 ------------------------------------------------------------ divergence
def patterns_and_divergence():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6.0), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2.0, 1.0], hspace=0.10))
    fig.patch.set_facecolor(PAPER)
    for a in (ax1, ax2):
        a.set_facecolor(PAPER); a.set_xticks([]); a.set_yticks([])
        for s in a.spines.values():
            s.set_visible(False)
    x = np.arange(60)
    price = np.concatenate([
        np.linspace(10, 16, 18), np.linspace(16, 13.5, 10),
        np.linspace(13.5, 17.6, 16), np.linspace(17.6, 16.4, 16)])
    price = price + np.sin(x / 2.2) * 0.22
    ax1.plot(x, price, color=INK, lw=1.8)
    ax1.plot([17, 43], [price[17] + 0.35, price[43] + 0.35], color=GREEN, lw=1.5, ls=(0, (4, 3)))
    ax1.annotate("higher high", xy=(43, price[43] + 0.5), xytext=(46, price[43] + 0.2),
                 color=GREEN, fontsize=10.5)
    ax1.text(1, price.max() - 0.4, "price", color=INK, fontsize=11)
    ax1.set_title("Regular bearish divergence, and why it is a reason to watch, not to enter",
                  color=INK, fontsize=15, fontweight="bold", loc="left", pad=16)

    osc = np.concatenate([
        np.linspace(45, 78, 18), np.linspace(78, 52, 10),
        np.linspace(52, 69, 16), np.linspace(69, 58, 16)])
    ax2.plot(x, osc, color=GOLD, lw=1.8)
    ax2.plot([17, 43], [osc[17] + 2, osc[43] + 2], color=RED, lw=1.5, ls=(0, (4, 3)))
    ax2.annotate("lower high", xy=(43, osc[43] + 3), xytext=(30, osc[43] + 12),
                 color=RED, fontsize=10.5,
                 arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.1))
    ax2.axhline(70, color=MUTE, lw=1.0, ls=(0, (4, 4)))
    ax2.text(1, 72, "oscillator", color=GOLD, fontsize=11)
    ax2.text(0, -0.24, "Black Gold Market  ·  schematic teaching diagram  ·  no prices, no signals",
             transform=ax2.transAxes, color=MUTE, fontsize=9.5, ha="left", va="top")
    path = os.path.join(OUT, "patterns-and-divergence-1.png")
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor=PAPER, pad_inches=0.3)
    plt.close(fig)
    print("->", os.path.basename(path))


# 13 ------------------------------------------------------------- breakouts
def breakouts_and_false_breaks():
    fig, ax = figure(10, 5.2)
    title(ax, "One wick through the level, one close beyond it. Not the same event.")
    level = 6.2
    left = [(5.2, 5.5, 5.7, 5.1), (5.5, 5.9, 6.0, 5.4), (5.9, 5.7, 6.1, 5.6),
            (5.7, 6.0, 6.15, 5.6), (6.0, 5.6, 6.55, 5.5)]
    series(ax, left)
    note(ax, 4.0, 5.15, "wick through, close back inside\nthis is the false break", size=10.5, color=RED)
    right = [(5.7, 5.9, 6.05, 5.6), (5.9, 6.1, 6.2, 5.8), (6.1, 6.6, 6.7, 6.05),
             (6.6, 6.45, 6.8, 6.3), (6.45, 6.9, 7.0, 6.4)]
    series(ax, right, x0=8)
    note(ax, 10.6, 7.25, "close beyond, then holds above\nthis is the break that stuck", size=10.5, color=GREEN)
    hline(ax, level, -0.6, 12.6, color=GOLD, lw=1.6, label="the level")
    zone(ax, level - 0.06, level + 0.06, -0.6, 12.6, color=GOLD, alpha=0.25)
    note(ax, 6.5, 4.9, "same level, two very different outcomes", size=11, color=MUTE)
    clean(ax)
    save(fig, ax, "breakouts-and-false-breaks")


# 14 ------------------------------------------------------ multi timeframe
def multiple_timeframes():
    fig, ax = figure(10, 5.0)
    title(ax, "Three charts, three jobs, and none of them does the other two")
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.6)
    rows = [("HIGHER CHART", "direction and the levels that matter", GOLD, 3.4),
            ("MIDDLE CHART", "the setup, is this a place worth acting on", GOLD_L, 2.2),
            ("LOWER CHART", "timing only, never the reason for the trade", MUTE, 1.0)]
    for label, job, color, y in rows:
        ax.add_patch(FancyBboxPatch((0.5, y - 0.42), 9.0, 0.9, boxstyle="round,pad=0.08",
                                    facecolor=color, alpha=0.16, edgecolor=color, lw=1.4))
        note(ax, 0.9, y + 0.14, label, size=12, weight="bold", color=INK, ha="left")
        note(ax, 0.9, y - 0.22, job, size=11, color=MUTE, ha="left")
    arrow(ax, (5.0, 2.95), (5.0, 2.68), color=MUTE)
    arrow(ax, (5.0, 1.75), (5.0, 1.48), color=MUTE)
    note(ax, 5.0, 0.28, "Levels travel downward. Decisions never travel back up.", size=11, color=INK)
    clean(ax, 0.01, 0.01)
    save(fig, ax, "multiple-timeframes")


# 15 ----------------------------------------------------------- heikin ashi
def heikin_ashi_waves_and_harmonics():
    fig, ax = figure(10, 5.2)
    title(ax, "The same swings, drawn twice: normal candles and Heikin Ashi")
    raw = [(5.0, 5.4, 5.6, 4.9), (5.4, 5.2, 5.7, 5.1), (5.2, 5.9, 6.0, 5.15),
           (5.9, 5.7, 6.1, 5.5), (5.7, 6.3, 6.4, 5.6), (6.3, 6.1, 6.5, 5.9),
           (6.1, 6.6, 6.8, 6.0)]
    series(ax, raw)
    note(ax, 3.0, 7.15, "normal candles, every wick is a real price", size=10.5, color=INK)
    ha = []
    prev_o, prev_c = raw[0][0], raw[0][1]
    for o, c, hi, lo in raw:
        ha_c = (o + c + hi + lo) / 4.0
        ha_o = (prev_o + prev_c) / 2.0
        ha.append((ha_o, ha_c, max(hi, ha_o, ha_c), min(lo, ha_o, ha_c)))
        prev_o, prev_c = ha_o, ha_c
    for i, (o, c, hi, lo) in enumerate(ha):
        candle(ax, 9 + i, o - 1.4, c - 1.4, hi - 1.4, lo - 1.4, w=0.30)
    note(ax, 12.0, 5.75, "Heikin Ashi, averaged: smoother, but these\nopens and closes are not tradeable prices",
         size=10.5, color=GOLD)
    clean(ax)
    save(fig, ax, "heikin-ashi-waves-and-harmonics")


# 16 ---------------------------------------------------------- real yields
def interest_rates_and_expectations():
    fig, ax = figure(10, 4.8)
    title(ax, "Real yield is the number gold is judged against")
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.4)
    blocks = [("NOMINAL YIELD", "what the bond pays on paper", 0.5, 3.6, GOLD),
              ("EXPECTED INFLATION", "what those payments lose to prices", 0.5, 2.4, MUTE),
              ("REAL YIELD", "what is actually left over", 0.5, 1.2, GOLD_L)]
    for label, sub, x, y, color in blocks:
        ax.add_patch(FancyBboxPatch((x, y - 0.40), 5.4, 0.88, boxstyle="round,pad=0.08",
                                    facecolor=color, alpha=0.18, edgecolor=color, lw=1.4))
        note(ax, x + 0.3, y + 0.14, label, size=12, weight="bold", color=INK, ha="left")
        note(ax, x + 0.3, y - 0.20, sub, size=10.5, color=MUTE, ha="left")
    note(ax, 6.3, 3.0, "minus", size=13, color=INK, ha="left")
    note(ax, 6.3, 1.8, "equals", size=13, color=INK, ha="left")
    ax.add_patch(FancyBboxPatch((7.4, 0.78), 2.1, 0.88, boxstyle="round,pad=0.08",
                                facecolor="#ffffff", edgecolor=GOLD, lw=1.6))
    note(ax, 8.45, 1.22, "gold pays 0%", size=11.5, weight="bold", color=GOLD)
    note(ax, 5.0, 0.35, "When the real yield rises, holding an asset that pays no interest costs you more.",
         size=11, color=INK)
    clean(ax, 0.01, 0.01)
    save(fig, ax, "interest-rates-and-expectations")


# 17 --------------------------------------------------------- base effect
def inflation_jobs_and_growth():
    fig, ax = figure(10, 5.0)
    title(ax, "Same prices this year, two very different annual numbers")
    months = np.arange(12)
    a = np.array([100, 101, 104, 105, 105.5, 106, 106.3, 106.6, 107, 107.3, 107.6, 108.0])
    b = np.array([100, 100.2, 100.4, 100.7, 101, 101.3, 101.7, 102.1, 102.6, 103.2, 103.9, 104.6])
    ax.plot(months, a, color=GOLD, lw=2.2, marker="o", ms=4, label="last year, an early jump")
    ax.plot(months, b, color=MUTE, lw=2.2, marker="o", ms=4, label="last year, a slow drift")
    ax.axvspan(1.6, 3.4, color=RED, alpha=0.07)
    ax.annotate("the month that sets the comparison", xy=(2.5, 104.3), xytext=(5.2, 100.4),
                color=RED, fontsize=10.5,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2),
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.5))
    ax.legend(frameon=False, fontsize=10.5, loc="upper left", labelcolor=INK)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.margins(y=0.16)
    ax.text(0.0, -0.13, "Hypothetical index levels. The annual figure compares today with one month twelve months ago.",
            transform=ax.transAxes, ha="left", va="top", color=MUTE, fontsize=10)
    save(fig, ax, "inflation-jobs-and-growth")


# 18 --------------------------------------------------------------- news
def trading_around_scheduled_news():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5.8), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2.0, 0.9], hspace=0.12))
    fig.patch.set_facecolor(PAPER)
    for a in (ax1, ax2):
        a.set_facecolor(PAPER); a.set_xticks([]); a.set_yticks([])
        for s in a.spines.values():
            s.set_visible(False)
    pre = [(5.0, 5.05, 5.1, 4.98), (5.05, 5.02, 5.08, 4.99), (5.02, 5.06, 5.1, 5.0),
           (5.06, 5.03, 5.09, 5.0)]
    for i, (o, c, hi, lo) in enumerate(pre):
        candle(ax1, i, o, c, hi, lo, w=0.26)
    candle(ax1, 4, 5.03, 5.62, 5.78, 4.72, w=0.26)
    post = [(5.62, 5.3, 5.7, 5.2), (5.3, 5.45, 5.55, 5.15), (5.45, 5.38, 5.5, 5.3)]
    for i, (o, c, hi, lo) in enumerate(post):
        candle(ax1, 5 + i, o, c, hi, lo, w=0.26)
    ax1.axvline(4, color=RED, lw=1.2, ls=(0, (5, 4)))
    ax1.text(4.15, 5.75, "the release", color=RED, fontsize=10.5)
    ax1.text(0.0, 5.75, "quiet, orderly", color=MUTE, fontsize=10.5)
    ax1.set_title("What the minutes around a scheduled release actually look like",
                  color=INK, fontsize=15, fontweight="bold", loc="left", pad=16)

    spread = [1, 1, 1, 1.4, 9, 6, 3, 1.6]
    ax2.bar(range(8), spread, color=[MUTE] * 3 + [GOLD_L, RED, RED, GOLD_L, MUTE], width=0.52)
    ax2.text(0.0, 7.4, "spread", color=INK, fontsize=10.5)
    ax2.text(4.35, 8.2, "spread widens, depth thins, a stop can fill far from its trigger",
             color=RED, fontsize=10.5)
    ax2.set_ylim(0, 11)
    ax2.text(0, -0.30, "Black Gold Market  ·  schematic teaching diagram  ·  no prices, no signals",
             transform=ax2.transAxes, color=MUTE, fontsize=9.5, ha="left", va="top")
    path = os.path.join(OUT, "trading-around-scheduled-news-1.png")
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor=PAPER, pad_inches=0.3)
    plt.close(fig)
    print("->", os.path.basename(path))


# 19 ------------------------------------------------------- gold vs dollar
def gold_the_dollar_and_real_yields():
    fig, ax = figure(10, 5.2)
    title(ax, "The textbook relationship, and the stretch where it stopped working")
    x = np.arange(80)
    real = np.concatenate([np.linspace(1.0, 2.4, 40), np.linspace(2.4, 3.1, 40)])
    gold = np.concatenate([np.linspace(3.2, 1.9, 40), np.linspace(1.9, 3.0, 40)])
    ax.plot(x, real, color=MUTE, lw=2.2, label="real yield")
    ax.plot(x, gold, color=GOLD, lw=2.4, label="gold")
    ax.axvspan(40, 79, color=RED, alpha=0.07)
    ax.text(8, 3.35, "textbook: real yield up, gold down", color=INK, fontsize=11)
    ax.text(44, 3.35, "the stretch where both rose together", color=RED, fontsize=11)
    ax.text(44, 1.35, "other buyers were in the market for reasons\nthat had nothing to do with yields",
            color=MUTE, fontsize=10.5)
    ax.legend(frameon=False, fontsize=10.5, loc="center left", labelcolor=INK)
    clean(ax)
    save(fig, ax, "gold-the-dollar-and-real-yields")


# 20 ------------------------------------------------------------ exposure
def correlation_and_combined_exposure():
    fig, ax = figure(10, 5.0)
    title(ax, "Three tickets, one bet")
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.6)
    tickets = [("Trade A", 1.2, 3.7), ("Trade B", 1.2, 2.6), ("Trade C", 1.2, 1.5)]
    for label, x, y in tickets:
        ax.add_patch(FancyBboxPatch((x - 0.9, y - 0.32), 2.6, 0.72, boxstyle="round,pad=0.08",
                                    facecolor="#ffffff", edgecolor=LINE, lw=1.4))
        note(ax, x + 0.4, y + 0.04, label + "  ·  risk 1%", size=11.5, color=INK)
        arrow(ax, (x + 1.75, y + 0.04), (5.6, 2.6), color=MUTE)
    ax.add_patch(FancyBboxPatch((5.8, 2.05), 3.7, 1.1, boxstyle="round,pad=0.10",
                                facecolor=GOLD, alpha=0.20, edgecolor=GOLD, lw=1.6))
    note(ax, 7.65, 2.85, "ONE SHARED DRIVER", size=12, weight="bold", color=INK)
    note(ax, 7.65, 2.42, "a bad day for that view costs 3%", size=11, color=RED)
    note(ax, 5.0, 0.62, "Count exposure to the driver, not the number of open tickets.",
         size=11.5, color=INK)
    note(ax, 5.0, 0.22, "Hypothetical example. Correlations also tend to tighten exactly when markets are stressed.",
         size=10, color=MUTE)
    clean(ax, 0.01, 0.01)
    save(fig, ax, "correlation-and-combined-exposure")


if __name__ == "__main__":
    fibonacci_and_pivot_levels()
    patterns_and_divergence()
    breakouts_and_false_breaks()
    multiple_timeframes()
    heikin_ashi_waves_and_harmonics()
    interest_rates_and_expectations()
    inflation_jobs_and_growth()
    trading_around_scheduled_news()
    gold_the_dollar_and_real_yields()
    correlation_and_combined_exposure()
