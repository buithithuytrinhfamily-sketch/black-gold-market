#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figures for Black Gold Market academy, batch 1 (lessons 1 to 10).

Run:  python3 scripts/figs_lot1.py
Every figure is schematic. No real prices, no entry, stop or target.
"""
import numpy as np
from figs_bgm import (figure, clean, title, candle, series, zone, hline, note,
                      arrow, save, PAPER, INK, GOLD, GOLD_L, RED, GREEN, MUTE,
                      LINE, UP_FACE, DOWN_FACE, BBOX)
from matplotlib.patches import Rectangle, FancyBboxPatch


# 1 ------------------------------------------------------------------ pair
def reading_a_currency_pair():
    fig, ax = figure(10, 4.6)
    title(ax, "What a currency pair quote is actually saying")
    ax.set_xlim(0, 10); ax.set_ylim(0, 5)

    ax.add_patch(FancyBboxPatch((0.5, 2.5), 3.0, 1.5, boxstyle="round,pad=0.12",
                                facecolor="#ffffff", edgecolor=GOLD, lw=1.6, zorder=3))
    note(ax, 2.0, 3.55, "EUR", size=22, weight="bold", color=INK)
    note(ax, 2.0, 2.95, "base currency", size=11, color=GOLD)

    note(ax, 4.0, 3.25, "/", size=24, color=MUTE, weight="bold")

    ax.add_patch(FancyBboxPatch((4.5, 2.5), 3.0, 1.5, boxstyle="round,pad=0.12",
                                facecolor="#ffffff", edgecolor=MUTE, lw=1.6, zorder=3))
    note(ax, 6.0, 3.55, "USD", size=22, weight="bold", color=INK)
    note(ax, 6.0, 2.95, "quote currency", size=11, color=MUTE)

    ax.add_patch(FancyBboxPatch((8.0, 2.5), 1.6, 1.5, boxstyle="round,pad=0.12",
                                facecolor="#f3ece0", edgecolor=LINE, lw=1.4, zorder=3))
    note(ax, 8.8, 3.25, "1.1050", size=17, weight="bold", color=INK)

    note(ax, 5.0, 1.75, "One unit of the base currency costs 1.1050 units of the quote currency",
         size=12.5, color=INK)
    arrow(ax, (2.0, 2.35), (2.0, 1.95), color=GOLD)
    arrow(ax, (6.0, 2.35), (6.0, 1.95), color=MUTE)

    note(ax, 2.6, 1.0, "price rises  =  base currency stronger", size=11.5, color=GREEN)
    note(ax, 7.4, 1.0, "price falls  =  base currency weaker", size=11.5, color=RED)
    note(ax, 5.0, 0.35, "XAU / USD works the same way: one ounce of gold is the base, the dollar is the quote",
         size=11, color=MUTE)
    clean(ax, 0.01, 0.01)
    save(fig, ax, "reading-a-currency-pair")


# 2 ------------------------------------------------------------------ lots
def pips_points_and_lots():
    fig, ax = figure(10, 5.0)
    title(ax, "Lot size is a quantity, not a risk budget")
    rows = [("Standard lot", "100,000 units", "1 pip = about 10 units of the quote currency", 1.00, GOLD),
            ("Mini lot", "10,000 units", "1 pip = about 1 unit of the quote currency", 0.55, GOLD_L),
            ("Micro lot", "1,000 units", "1 pip = about 0.1 unit of the quote currency", 0.30, MUTE)]
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.2)
    y = 3.3
    for name, units, pipline, width, color in rows:
        ax.add_patch(Rectangle((0.4, y - 0.30), 5.6 * width, 0.62, facecolor=color,
                               alpha=0.20, edgecolor=color, lw=1.3, zorder=2))
        note(ax, 0.62, y, name, size=12.5, weight="bold", color=INK, ha="left")
        note(ax, 6.2, y, units, size=11.5, color=INK, ha="left")
        note(ax, 6.2, y - 0.40, pipline, size=10.5, color=MUTE, ha="left")
        y -= 1.1
    note(ax, 0.4, 0.42, "Non JPY pair, pip = 0.0001. Gold is different: check ounces per contract on your own platform.",
         size=10.5, color=MUTE, ha="left")
    clean(ax, 0.01, 0.01)
    save(fig, ax, "pips-points-and-lots")


# 3 ------------------------------------------------------------- stop order
def how_orders_reach_the_market():
    fig, ax = figure(10, 5.2)
    title(ax, "A stop order has a trigger price and, separately, a fill price")
    data = [(5.0, 5.2, 5.4, 4.9), (5.2, 5.05, 5.3, 4.95), (5.05, 4.85, 5.1, 4.8),
            (4.85, 4.9, 5.0, 4.75), (4.9, 4.7, 4.95, 4.6)]
    series(ax, data)
    # gap down candle
    candle(ax, 5, 4.05, 3.9, 4.15, 3.75, face=DOWN_FACE)
    candle(ax, 6, 3.9, 4.0, 4.1, 3.85)
    candle(ax, 7, 4.0, 3.95, 4.1, 3.85)
    hline(ax, 4.55, -0.5, 7.6, color=GOLD, label="trigger price you set")
    hline(ax, 3.98, -0.5, 7.6, color=RED, ls=(0, (2, 3)), label="price where it actually filled")
    ax.add_patch(Rectangle((4.4, 3.98), 1.2, 0.57, facecolor=RED, alpha=0.12, edgecolor="none", zorder=1))
    note(ax, 5.0, 4.28, "gap", size=11, color=RED, weight="bold")
    note(ax, 1.6, 3.55, "The market reopened below the trigger, so the fill was worse than the level on the ticket.",
         size=11, color=INK, ha="left")
    clean(ax)
    save(fig, ax, "how-orders-reach-the-market")


# 4 ------------------------------------------------------- leverage vs cost
def leverage_and_margin():
    fig, ax = figure(10, 5.0)
    title(ax, "More leverage frees up margin. It does not shrink the loss.")
    labels = ["1:10", "1:20", "1:50", "1:100", "1:200"]
    margin = [2000, 1000, 400, 200, 100]
    cost = [200, 200, 200, 200, 200]
    x = np.arange(len(labels))
    ax.bar(x - 0.19, margin, width=0.36, color=GOLD, alpha=0.75, edgecolor=GOLD, label="Required margin (USD)")
    ax.bar(x + 0.19, cost, width=0.36, color=INK, alpha=0.85, edgecolor=INK, label="Loss on a 1% adverse move (USD)")
    for i, v in enumerate(margin):
        ax.text(i - 0.19, v + 45, str(v), ha="center", color=INK, fontsize=10.5)
    for i, v in enumerate(cost):
        ax.text(i + 0.19, v + 45, str(v), ha="center", color=INK, fontsize=10.5)
    ax.set_xticks(x); ax.set_xticklabels(labels, color=INK, fontsize=11.5)
    ax.tick_params(axis="x", length=0)
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(frameon=False, fontsize=10.5, loc="upper right", labelcolor=INK)
    ax.margins(y=0.18)
    ax.text(0.0, -0.15, "Hypothetical: a USD 20,000 position on USD 1,000 of equity. Costs excluded.",
            transform=ax.transAxes, ha="left", va="top", color=MUTE, fontsize=10)
    save(fig, ax, "leverage-and-margin")


# 5 ---------------------------------------------------------------- costs
def spread_commission_and_financing():
    fig, ax = figure(10, 5.0)
    title(ax, "What a two week hold pays, day by day")
    days = np.arange(1, 15)
    spread = np.array([12.0] + [0.0] * 13)
    commission = np.array([7.0] + [0.0] * 13)
    financing = np.array([0.0] + [2.5] * 13)
    financing[6] = 7.5  # triple charge day
    ax.bar(days, spread, color=GOLD, edgecolor=GOLD, label="Spread, paid once on entry")
    ax.bar(days, commission, bottom=spread, color=INK, edgecolor=INK, alpha=0.85,
           label="Commission, paid on entry and exit")
    ax.bar(days, financing, bottom=spread + commission, color=GOLD_L, edgecolor=GOLD_L,
           label="Overnight financing, charged every night")
    ax.annotate("triple charge night", xy=(7, 8.6), xytext=(8.6, 15),
                color=RED, fontsize=10.5,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
    ax.set_xticks(days)
    ax.set_xticklabels([str(d) for d in days], color=MUTE, fontsize=9.5)
    ax.tick_params(axis="x", length=0)
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(frameon=False, fontsize=10.5, loc="upper center", labelcolor=INK, ncol=1)
    ax.margins(y=0.30)
    ax.text(0.0, -0.15, "Hypothetical figures in USD. Your own numbers come from your contract specification.",
            transform=ax.transAxes, ha="left", va="top", color=MUTE, fontsize=10)
    save(fig, ax, "spread-commission-and-financing")


# 6 -------------------------------------------------------------- sessions
def sessions_and_liquidity():
    fig, ax = figure(10, 4.8)
    title(ax, "The trading day is a relay, and the busiest leg is the overlap")
    ax.set_xlim(0, 24); ax.set_ylim(0, 5)
    bars = [("Sydney", 21, 6, 3.9, MUTE), ("Tokyo", 0, 9, 3.1, MUTE),
            ("London", 7, 16, 2.3, GOLD), ("New York", 12, 21, 1.5, GOLD)]
    for name, start, end, y, color in bars:
        if end < start:
            ax.add_patch(Rectangle((start, y), 24 - start, 0.55, facecolor=color, alpha=0.30,
                                   edgecolor=color, lw=1.1))
            ax.add_patch(Rectangle((0, y), end, 0.55, facecolor=color, alpha=0.30,
                                   edgecolor=color, lw=1.1))
        else:
            ax.add_patch(Rectangle((start, y), end - start, 0.55, facecolor=color, alpha=0.30,
                                   edgecolor=color, lw=1.1))
        ax.text(0.15, y + 0.62, name, color=INK, fontsize=11.5, ha="left", va="bottom", fontweight="bold", zorder=7)
    ax.add_patch(Rectangle((12, 1.3), 4, 3.2, facecolor=GOLD, alpha=0.12, edgecolor=GOLD,
                           lw=1.2, ls=(0, (5, 4))))
    note(ax, 14, 4.65, "London and New York overlap", size=11.5, color=GOLD, weight="bold")
    for h in range(0, 25, 4):
        ax.text(h, 0.75, "%02d:00" % (h % 24), color=MUTE, fontsize=10, ha="center")
    note(ax, 12, 0.25, "Approximate UTC hours. They shift with daylight saving in each center.",
         size=10.5, color=MUTE)
    clean(ax, 0.01, 0.01)
    save(fig, ax, "sessions-and-liquidity")


# 7 --------------------------------------------------------------- candles
def candles_and_context():
    fig, ax = figure(10, 5.2)
    title(ax, "One candle, four prices, and what the wicks are telling you")
    ax.set_xlim(-0.8, 9.2); ax.set_ylim(0, 10)
    # anatomy candle
    candle(ax, 0.6, 3.2, 6.8, 8.4, 2.2, w=0.46)
    hline(ax, 8.4, 0.2, 2.6, color=MUTE, ls=(0, (3, 3)), lw=1.0, label="high")
    hline(ax, 6.8, 0.2, 2.6, color=MUTE, ls=(0, (3, 3)), lw=1.0, label="close")
    hline(ax, 3.2, 0.2, 2.6, color=MUTE, ls=(0, (3, 3)), lw=1.0, label="open")
    hline(ax, 2.2, 0.2, 2.6, color=MUTE, ls=(0, (3, 3)), lw=1.0, label="low")
    note(ax, 0.6, 9.3, "one candle", size=11, color=INK)

    shapes = [(4.4, "long lower wick", 6.0, 6.6, 7.0, 3.0),
              (6.4, "inside the\nprevious range", 6.2, 6.0, 6.6, 5.6),
              (8.4, "close near\nthe high", 5.4, 7.4, 7.6, 5.2)]
    for x, label, o, c, hi, lo in shapes:
        candle(ax, x, o, c, hi, lo, w=0.34)
        ax.text(x, 2.6, label, color=INK, fontsize=10.5, ha="center", va="top",
                linespacing=1.35)
    note(ax, 6.4, 9.3, "same market, three common shapes", size=11, color=MUTE)
    note(ax, 6.4, 0.75, "Each shape says who was in control. None of them predicts the next candle.",
         size=10.5, color=MUTE)
    clean(ax, 0.01, 0.02)
    save(fig, ax, "candles-and-context")


# 8 ---------------------------------------------------- support/resistance
def support_resistance_and_structure():
    fig, ax = figure(10, 5.4)
    title(ax, "A level is a zone, and structure is the sequence of swings")
    data = [(3.0, 3.6, 3.8, 2.9), (3.6, 4.4, 4.6, 3.5), (4.4, 5.2, 5.6, 4.3),
            (5.2, 4.6, 5.3, 4.4), (4.6, 5.0, 5.2, 4.4), (5.0, 5.9, 6.2, 4.9),
            (5.9, 6.4, 6.6, 5.7), (6.4, 5.8, 6.5, 5.5), (5.8, 6.1, 6.3, 5.5),
            (6.1, 5.4, 6.2, 5.1), (5.4, 5.0, 5.5, 4.7), (5.0, 5.4, 5.6, 4.8),
            (5.4, 5.1, 5.5, 4.9), (5.1, 4.6, 5.2, 4.4)]
    series(ax, data)
    zone(ax, 4.4, 4.9, -0.6, 13.6, color=GOLD)
    zone(ax, 6.2, 6.6, -0.6, 13.6, color=MUTE, alpha=0.12)
    note(ax, 12.2, 6.85, "resistance zone", size=10.5, color=MUTE)
    note(ax, 1.4, 4.65, "support zone, a band not a line", size=10.5, color=GOLD)
    note(ax, 2.2, 5.85, "higher high", size=10.5, color=GREEN)
    note(ax, 6.0, 6.9, "higher high", size=10.5, color=GREEN)
    note(ax, 3.6, 3.95, "higher low", size=10.5, color=GREEN)
    note(ax, 11.6, 3.7, "lower low, structure changed", size=10.5, color=RED)
    arrow(ax, (11.6, 3.88), (10.9, 4.38), color=RED)
    clean(ax)
    save(fig, ax, "support-resistance-and-structure")


# 9 -------------------------------------------------------- moving averages
def moving_averages_and_trend():
    rng = np.random.default_rng(7)
    trend = np.cumsum(rng.normal(0.28, 0.55, 46)) + 20
    chop = np.cumsum(rng.normal(0.0, 0.85, 40))
    chop = chop - chop.mean() + trend[-1]
    price = np.concatenate([trend, chop])

    def sma(a, n):
        out = np.full(len(a), np.nan)
        for i in range(n - 1, len(a)):
            out[i] = a[i - n + 1:i + 1].mean()
        return out

    fast, slow = sma(price, 10), sma(price, 30)
    fig, ax = figure(10, 5.0)
    title(ax, "The same two averages: helpful in a trend, unhelpful in a range")
    x = np.arange(len(price))
    ax.plot(x, price, color=INK, lw=1.3, alpha=0.65, label="price")
    ax.plot(x, fast, color=GOLD, lw=2.0, label="short average, 10 periods")
    ax.plot(x, slow, color=MUTE, lw=2.0, label="long average, 30 periods")
    ax.axvspan(0, 45, color=GREEN, alpha=0.07)
    ax.axvspan(46, len(price) - 1, color=RED, alpha=0.07)
    ax.text(22, np.nanmax(price) + 0.6, "trending stretch, the averages stay stacked",
            color=GREEN, fontsize=10.5, ha="center")
    ax.text(66, np.nanmax(price) + 0.6, "ranging stretch, the averages cross back and forth",
            color=RED, fontsize=10.5, ha="center")
    ax.legend(frameon=False, fontsize=10.5, loc="lower right", labelcolor=INK)
    clean(ax)
    save(fig, ax, "moving-averages-and-trend")


# 10 ------------------------------------------------------------------ rsi
def rsi_macd_and_volatility():
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6.0), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2.0, 1.0], hspace=0.12))
    fig.patch.set_facecolor(PAPER)
    for a in (ax1, ax2):
        a.set_facecolor(PAPER)
        a.set_xticks([]); a.set_yticks([])
        for s in a.spines.values():
            s.set_visible(False)
    rng = np.random.default_rng(3)
    price = np.cumsum(rng.normal(0.32, 0.5, 70)) + 30
    ax1.plot(price, color=INK, lw=1.7)
    ax1.set_title("An indicator summarizes the past. It adds no new information.",
                  color=INK, fontsize=15, fontweight="bold", loc="left", pad=16)
    ax1.text(2, price.max() - 1.2, "price keeps grinding higher", color=INK, fontsize=10.5)

    rsi = 52 + 26 * (price - price.mean()) / (price.std() * 1.15)
    rsi = np.clip(rsi, 34, 86)
    ax2.plot(rsi, color=GOLD, lw=1.9)
    ax2.axhspan(70, 92, color=RED, alpha=0.08)
    ax2.axhline(70, color=RED, lw=1.1, ls=(0, (5, 4)))
    ax2.axhline(30, color=GREEN, lw=1.1, ls=(0, (5, 4)))
    ax2.text(30, 88, "RSI above 70 for weeks while price kept rising", color=RED, fontsize=10.5, va="top")
    ax2.text(3, 32, "30 line", color=GREEN, fontsize=10.5, va="bottom")
    ax2.set_ylim(25, 98)
    ax2.text(0, -0.22, "Black Gold Market  ·  schematic teaching diagram  ·  no prices, no signals",
             transform=ax2.transAxes, color=MUTE, fontsize=9.5, ha="left", va="top")
    import os
    from figs_bgm import OUT
    path = os.path.join(OUT, "rsi-macd-and-volatility-1.png")
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor=PAPER, pad_inches=0.3)
    plt.close(fig)
    print("->", os.path.basename(path))


if __name__ == "__main__":
    reading_a_currency_pair()
    pips_points_and_lots()
    how_orders_reach_the_market()
    leverage_and_margin()
    spread_commission_and_financing()
    sessions_and_liquidity()
    candles_and_context()
    support_resistance_and_structure()
    moving_averages_and_trend()
    rsi_macd_and_volatility()
