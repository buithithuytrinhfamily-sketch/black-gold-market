#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Put Black Gold Market labels onto a plain candlestick illustration.

The drawing itself comes from ChatGPT (no text in it). This script adds the
title, the teaching labels and the brand footer, so the wording is always
correct and never mis-spelled by an image model.

Usage in code:
    from label_fig import label
    label(src, dst, title="...", notes=[(x, y, "text", "gold")], sub="...")
Coordinates are FRACTIONS of width and height (0 to 1), so they survive resizing.
"""
import os
from PIL import Image, ImageDraw, ImageFont

INK = (32, 35, 30)
GOLD = (140, 95, 0)
RED = (163, 34, 26)
GREEN = (41, 95, 56)
MUTE = (123, 127, 118)
COLORS = {"ink": INK, "gold": GOLD, "red": RED, "green": GREEN, "mute": MUTE}

FONT_DIRS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def _font(size, bold=False):
    paths = FONT_DIRS if bold else FONT_DIRS[1:] + FONT_DIRS[:1]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def label(src, dst, title, notes=(), sub=None,
          brand="Black Gold Market  ·  schematic teaching diagram  ·  no prices, no signals"):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    # a little headroom for the title and footer so nothing sits on the drawing
    pad_top = int(H * 0.14)
    pad_bottom = int(H * 0.10)
    bg = im.getpixel((6, 6))
    canvas = Image.new("RGB", (W, H + pad_top + pad_bottom), bg)
    canvas.paste(im, (0, pad_top))
    d = ImageDraw.Draw(canvas)
    s = W / 1600.0  # scale everything off a 1600px reference width

    d.text((int(60 * s), int(38 * s)), title, font=_font(int(44 * s), bold=True), fill=INK)
    if sub:
        d.text((int(60 * s), int(96 * s)), sub, font=_font(int(28 * s)), fill=MUTE)
    d.text((int(60 * s), H + pad_top + int(28 * s)), brand, font=_font(int(24 * s)), fill=MUTE)

    for note in notes:
        fx, fy, text = note[0], note[1], note[2]
        color = COLORS.get(note[3] if len(note) > 3 else "ink", INK)
        size = int((note[4] if len(note) > 4 else 30) * s)
        anchor = note[5] if len(note) > 5 else "la"
        d.text((int(fx * W), pad_top + int(fy * H)), text,
               font=_font(size, bold=(color != MUTE)), fill=color, anchor=anchor)

    canvas.save(dst, quality=90)
    print("->", os.path.basename(dst), canvas.size)
    return dst
