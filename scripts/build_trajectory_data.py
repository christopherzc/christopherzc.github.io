#!/usr/bin/env python3
"""Build compact trajectory JSON for the blog's trajectory viewer.

Reads a TALES run directory (one tales_* subdirectory per seed, each holding a
.jsonl trajectory) plus, optionally, the reference-matrix audit's
reference_edges.csv, and writes:

  <out>/index.json               games in this viewer folder
  <out>/<id>/manifest.json       seeds, outcomes, and counts
  <out>/<id>/seed-<seed>.json    per-step score / action / feedback / reasoning

Prompts are dropped (they are the bulk of the raw files). Reasoning summaries
are pre-split into segments so the viewer can render **bold** spans and
highlight future references (the audit's exact summary quotes) without
parsing markdown in the browser.

Usage:
  python3 scripts/build_trajectory_data.py RUN_DIR OUT_DIR --id ID --game NAME \\
      [--edges reference_edges.csv] [--max-score N]
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


STATUS = re.compile(r"Score:\s*(-?\d+)\s*Moves:\s*\d+")


def clean(text):
    """Tidy interpreter output: status-line padding, stray prompts, blank runs."""
    text = re.sub(r" {10,}", "\n", text)
    lines = []
    for line in text.split("\n"):
        line = line.rstrip()
        if line.strip() == ">" or STATUS.search(line):
            continue
        lines.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("out_dir", help="viewer root; this game is written to OUT_DIR/ID/")
    ap.add_argument("--id", required=True, help="short game id used in links, e.g. zork")
    ap.add_argument("--game", required=True, help="display name, e.g. 'Zork I'")
    ap.add_argument("--model", default="Astra")
    ap.add_argument("--edges", help="reference_edges.csv from the reference-matrix audit")
    ap.add_argument("--max-score", type=int,
                    help="game max score when the env does not track it; the score is then "
                         "read from the game's own 'Score: N Moves: M' status line")
    args = ap.parse_args()

    future = defaultdict(list)  # (seed, step) -> [edge]
    if args.edges:
        for e in csv.DictReader(open(args.edges, encoding="utf8")):
            if e["temporal_relation"] == "future":
                future[(e["seed"], int(e["reasoning_step"]))].append(e)

    game_dir = os.path.join(args.out_dir, args.id)
    os.makedirs(game_dir, exist_ok=True)
    seeds = []
    for path in sorted(glob.glob(os.path.join(args.run_dir, "tales_*", "*", "*.jsonl"))):
        seed = re.search(r"_s(\d+)_", os.path.basename(path)).group(1)
        rows = [json.loads(line) for line in open(path, encoding="utf8")]

        refs = []  # per-seed table: [reference, observation_step]
        steps = []
        n_future_summaries = 0
        status_score = 0
        for r in rows:
            step = r["Step"]
            if args.max_score:
                hits = STATUS.findall(r["Feedback"])
                if hits:
                    status_score = int(hits[-1])
                score = status_score
            else:
                score = r["Score"]
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
                "sc": score,
                "a": r["Action"],
                "f": clean(r["Feedback"]),
                **({"t": think} if think else {}),
            })

        meta = {
            "seed": seed,
            "steps": len(rows),
            "highscore": max(s["sc"] for s in steps),
            "max_score": args.max_score or rows[-1]["Max Score"],
            "summaries": sum(1 for s in steps if "t" in s),
            "future_summaries": n_future_summaries,
            "future_refs": len(refs),
        }
        data = {**meta, "start": clean(rows[0]["Observation"]), "refs": refs, "steps": steps}
        with open(os.path.join(game_dir, f"seed-{seed}.json"), "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        seeds.append(meta)

    manifest = {"id": args.id, "game": args.game, "model": args.model, "seeds": seeds}
    with open(os.path.join(game_dir, "manifest.json"), "w", encoding="utf8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    # Root index listing every game built into this viewer folder.
    index_path = os.path.join(args.out_dir, "index.json")
    index = json.load(open(index_path)) if os.path.exists(index_path) else {"games": []}
    entry = {"id": args.id, "game": args.game, "model": args.model}
    index["games"] = [g for g in index["games"] if g["id"] != args.id] + [entry]
    with open(index_path, "w", encoding="utf8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    for s in seeds:
        print(args.id, s)


if __name__ == "__main__":
    main()
