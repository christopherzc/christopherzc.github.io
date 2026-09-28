#!/usr/bin/env python3
"""Build compact trajectory JSON for the blog's trajectory viewer.

Reads a TALES run directory (one tales_* subdirectory per seed, each holding a
.jsonl trajectory) plus, optionally, the reference-matrix audit's
reference_edges.csv, and writes:

  <out>/manifest.json       seeds, outcomes, and counts
  <out>/seed-<seed>.json    per-step score / action / feedback / reasoning

Prompts are dropped (they are the bulk of the raw files). Reasoning summaries
are pre-split into segments so the viewer can render **bold** spans and
highlight future references (the audit's exact summary quotes) without
parsing markdown in the browser.

Usage:
  python3 scripts/build_trajectory_data.py RUN_DIR OUT_DIR [--edges reference_edges.csv]
"""
import argparse
import csv
import glob
import json
import os
import re
from collections import defaultdict


def segment(text, future):
    """Split `text` into [chunk, bold, [ref_indices]] runs.

    `future` is a list of (quote, ref_index); every occurrence of each quote
    is highlighted. ** markers are removed and toggle bold.
    """
    # Strip ** markers, remembering which output chars are bold.
    plain, bold = [], []
    on = False
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            on = not on
            i += 2
            continue
        plain.append(text[i])
        bold.append(on)
        i += 1
    plain = "".join(plain)

    # Map quotes onto the de-marked text (quotes may themselves contain **).
    ref = [set() for _ in plain]
    for quote, idx in future:
        q = quote.replace("**", "")
        start = 0
        while q and (pos := plain.find(q, start)) != -1:
            for k in range(pos, pos + len(q)):
                ref[k].add(idx)
            start = pos + len(q)

    out = []
    for ch, b, r in zip(plain, bold, ref):
        r = sorted(r)
        if out and out[-1][1] == int(b) and out[-1][2] == r:
            out[-1][0] += ch
        else:
            out.append([ch, int(b), r])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--edges", help="reference_edges.csv from the reference-matrix audit")
    ap.add_argument("--game", default="Zork I")
    ap.add_argument("--model", default="Astra")
    args = ap.parse_args()

    future = defaultdict(list)  # (seed, step) -> [edge]
    if args.edges:
        for e in csv.DictReader(open(args.edges, encoding="utf8")):
            if e["temporal_relation"] == "future":
                future[(e["seed"], int(e["reasoning_step"]))].append(e)

    os.makedirs(args.out_dir, exist_ok=True)
    seeds = []
    for path in sorted(glob.glob(os.path.join(args.run_dir, "tales_*", "*", "*.jsonl"))):
        seed = re.search(r"_s(\d+)_", os.path.basename(path)).group(1)
        rows = [json.loads(line) for line in open(path, encoding="utf8")]

        refs = []  # per-seed table: [reference, observation_step]
        steps = []
        n_future_summaries = 0
        for r in rows:
            step = r["Step"]
            think = None
            if r.get("Thinking"):
                edges = future.get((seed, step), [])
                quotes = []
                for e in edges:
                    refs.append([e["reference"], int(e["observation_step"])])
                    quotes.append((e["summary_quote"], len(refs) - 1))
                if edges:
                    n_future_summaries += 1
                think = segment(r["Thinking"], quotes)
            steps.append({
                "s": step,
                "sc": r["Score"],
                "a": r["Action"],
                "f": r["Feedback"].strip(),
                **({"t": think} if think else {}),
            })

        last = rows[-1]
        meta = {
            "seed": seed,
            "steps": len(rows),
            "highscore": max(r["Score"] for r in rows),
            "max_score": last["Max Score"],
            "summaries": sum(1 for s in steps if "t" in s),
            "future_summaries": n_future_summaries,
            "future_refs": len(refs),
        }
        data = {**meta, "start": rows[0]["Observation"].strip(), "refs": refs, "steps": steps}
        with open(os.path.join(args.out_dir, f"seed-{seed}.json"), "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        seeds.append(meta)

    manifest = {"game": args.game, "model": args.model, "seeds": seeds}
    with open(os.path.join(args.out_dir, "manifest.json"), "w", encoding="utf8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    for s in seeds:
        print(s)


if __name__ == "__main__":
    main()
