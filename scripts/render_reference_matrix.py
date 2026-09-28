#!/usr/bin/env python3
"""Render a reasoning-attribution matrix in the site's parchment palette.

Input is the reference-matrix audit's reference_edges.csv. Each edge links one
reasoning summary (y = its step) to the step where the game first showed the
referenced element (x). Past/current references sit on or above the diagonal;
future references (named before the game showed them) fall below it.

Usage:
  python3 scripts/render_reference_matrix.py EDGES.csv OUT.png \
      --title "..." --summaries N [--fonts DIR]

`--summaries` is the number of visible reasoning summaries in the run, used
for the "no matched edge" count. `--fonts` may point at EB Garamond /
JetBrains Mono .ttf files to match the site's typography.
"""
import argparse
import csv
import glob
import os
from collections import Counter, defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

# Site palette (src/styles/global.css), with blue/red kept for past/future.
BG = "#f4ecd8"
PANEL = "#ede4cc"
INK = "#2a2522"
INK_SOFT = "#4a4039"
INK_DIM = "#7a6e5f"
RULE = "#c9b98a"
PAST = "#3d6fb0"
CURRENT = "#4f8f6e"
FUTURE = "#b8452a"
SPAN = "#9a7fb0"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edges")
    ap.add_argument("out")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="Each point links one reasoning summary to the step where "
                    "the game first showed what it mentions.")
    ap.add_argument("--summaries", type=int, required=True)
    ap.add_argument("--fonts")
    args = ap.parse_args()

    serif, mono = "DejaVu Serif", "DejaVu Sans Mono"
    if args.fonts:
        for f in glob.glob(os.path.join(args.fonts, "*.ttf")):
            font_manager.fontManager.addfont(f)
        names = {font_manager.FontProperties(fname=f).get_name() for f in glob.glob(os.path.join(args.fonts, "*.ttf"))}
        serif = "EB Garamond" if "EB Garamond" in names else serif
        mono = "JetBrains Mono" if "JetBrains Mono" in names else mono

    edges = list(csv.DictReader(open(args.edges, encoding="utf8")))
    for e in edges:
        e["x"], e["y"] = int(e["observation_step"]), int(e["reasoning_step"])

    counts = Counter(e["temporal_relation"] for e in edges)
    by_summary = defaultdict(list)
    for e in edges:
        by_summary[(e["seed"], e["y"])].append(e)
    kinds = [{e["temporal_relation"] for e in v} for v in by_summary.values()]
    both = sum(1 for k in kinds if "future" in k and k & {"past", "current"})
    past_only = sum(1 for k in kinds if "future" not in k)
    future_only = sum(1 for k in kinds if k == {"future"})
    unmatched = args.summaries - len(by_summary)

    plt.rcParams.update({"font.family": serif, "text.color": INK})
    fig = plt.figure(figsize=(13.3, 10), dpi=160, facecolor=BG)
    ax = fig.add_axes([0.075, 0.1, 0.62, 0.74])
    ax.set_facecolor(BG)

    top = max(max(e["x"] for e in edges), max(e["y"] for e in edges))
    limit = -(-top // 100) * 100 + 5  # round up to the next hundred
    diag = [0, limit]
    ax.fill_between(diag, 0, diag, color=FUTURE, alpha=0.07, lw=0, zorder=0)
    ax.fill_between(diag, diag, limit, color=PAST, alpha=0.06, lw=0, zorder=0)
    ax.plot(diag, diag, color=INK_SOFT, lw=1.2, alpha=0.7, zorder=2)

    # A summary whose references land on both sides gets a faint span line.
    for v in by_summary.values():
        rels = {e["temporal_relation"] for e in v}
        if "future" in rels and rels & {"past", "current"}:
            xs = [e["x"] for e in v]
            ax.plot([min(xs), max(xs)], [v[0]["y"]] * 2, color=SPAN, lw=0.6, alpha=0.35, zorder=1)

    style = {"past": (PAST, "o"), "current": (CURRENT, "D"), "future": (FUTURE, "o")}
    for rel, (color, marker) in style.items():
        pts = Counter((e["x"], e["y"]) for e in edges if e["temporal_relation"] == rel)
        if not pts:
            continue
        xs, ys = zip(*pts)
        sizes = [16 + 10 * (n - 1) for n in pts.values()]
        ax.scatter(xs, ys, s=sizes, c=color, marker=marker, alpha=0.85,
                   edgecolors=BG, linewidths=0.5, zorder=3)

    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_xticks(range(0, int(limit) + 1, 100))
    ax.set_yticks(range(0, int(limit) + 1, 100))
    ax.set_aspect("equal")
    ax.set_xlabel("Observation step (first time the game showed it)", fontsize=13, color=INK_SOFT, labelpad=8)
    ax.set_ylabel("Reasoning-summary step", fontsize=13, color=INK_SOFT, labelpad=8)
    ax.tick_params(colors=INK_DIM, labelsize=10)
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_fontfamily(mono)
    ax.grid(color=RULE, lw=0.6, alpha=0.5)
    for sp in ax.spines.values():
        sp.set_color(RULE)

    lab = dict(rotation=45, rotation_mode="anchor", ha="center", va="center", fontfamily=mono, zorder=4)
    ax.text(limit * 0.27, limit * 0.63, "OBSERVED BEFORE REASONING", color=PAST, fontsize=12, weight="bold", **lab)
    ax.text(limit * 0.30, limit * 0.60, "past references (x < y)", color=PAST, fontsize=9.5, alpha=0.8, **lab)
    ax.text(limit * 0.70, limit * 0.33, "REASONING BEFORE OBSERVATION", color=FUTURE, fontsize=12, weight="bold", **lab)
    ax.text(limit * 0.73, limit * 0.30, "future references (x > y)", color=FUTURE, fontsize=9.5, alpha=0.8, **lab)

    fig.text(0.075, 0.935, args.title, fontsize=26, weight="semibold", color=INK)
    fig.text(0.075, 0.895, args.subtitle, fontsize=13, style="italic", color=INK_SOFT)

    # Counts panel.
    px = 0.75
    panel = fig.add_axes([px, 0.3, 0.22, 0.5])
    panel.set_facecolor(PANEL)
    panel.set_xticks([])
    panel.set_yticks([])
    for sp in panel.spines.values():
        sp.set_color(RULE)
    rows = [
        ("REFERENCES", None, None),
        (f"{counts['past']:,}", "past", PAST),
        (f"{counts['current']:,}", "current observation", CURRENT),
        (f"{counts['future']:,}", "future", FUTURE),
        ("SUMMARIES", None, None),
        (f"{both}", "both sides", SPAN),
        (f"{past_only}", "past / current only", PAST),
        (f"{future_only}", "future only", FUTURE),
        (f"{unmatched}", "no matched reference", INK_DIM),
    ]
    for i, (big, small, color) in enumerate(rows):
        y = 0.9 - i * 0.1
        kw = dict(transform=panel.transAxes, va="center")
        if small is None:
            panel.text(0.1, y, big, fontsize=9.5, fontfamily=mono, color=INK_DIM, **kw)
            continue
        panel.text(0.1, y, big, fontsize=18 if i < 4 else 14, color=color, weight="semibold",
                   fontfamily=mono, **kw)
        panel.text(0.42, y, small, fontsize=11, color=INK_SOFT, **kw)

    fig.savefig(args.out, facecolor=BG)
    print(args.out, dict(counts), "both", both, "past-only", past_only, "future-only", future_only,
          "unmatched", unmatched)


if __name__ == "__main__":
    main()
