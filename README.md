# christopherzc.github.io (Astro rebuild)

Personal site for Christopher Z. Cui. Two parallel "modes" sharing one content
source: an **Official** mode (clean academic site) and an **Adventure** mode
(text-adventure with parser). Parchment / IF-classic aesthetic.

## Develop

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # → dist/
npm run preview  # serve dist/ locally
```

## Structure

- `src/pages/index.astro` — landing title page (three doors)
- `src/pages/blog/` — blog index and per-post pages
- `src/pages/official/` — clean academic version
- `src/pages/adventure/` — text-adventure version (interactive parser on landing room)
- `src/content/` — shared content collections (publications, talks, teaching, blog)
- `src/layouts/` — `BaseLayout`, `OfficialLayout`, `AdventureLayout`, `BlogLayout`
- `src/styles/global.css` — parchment palette + typography
- `public/files/Resume.pdf` — current CV

## Adding a publication

Drop a markdown file in `src/content/publications/`:

```yaml
---
title: "..."
authors: "First, Second, ..."
venue: "..."
date: YYYY-MM-DD
paperurl: "https://..."
highlight: false   # set true to surface on the Official about page
order: 99          # for highlight ordering
excerpt: "..."
---
```

## Adding a blog post

Drop a markdown (`.md`) or MDX (`.mdx`) file in `src/content/blog/`. The
filename becomes the URL (`my-post.md` → `/blog/my-post/`). See
`example-post.md` for a template.

```yaml
---
title: "..."
date: YYYY-MM-DD
description: "..."   # shown on the blog index
deck: "..."          # optional lede under the title
tags: ["..."]        # optional
draft: false         # true hides it from the build
---
```

Post styling hooks (usable as raw HTML in `.md` or `.mdx`):

- `<p class="pull">…</p>` — pull quote
- `<figure><img …/><figcaption>…</figcaption></figure>` — captioned figure
- footnotes (`[^1]`) show as margin notes on wide screens, at the bottom otherwise

### Trajectory viewer

A post can show agent trajectories next to the text (post / split /
trajectories views). Build the data from a TALES run directory, once per game:

```bash
python3 scripts/build_trajectory_data.py RUN_DIR public/blog/<post>/trajectories \
  --id zork --game "Zork I" \
  --edges RUN_DIR/diagnostics/reference-matrix-audit/reference_edges.csv
# games whose env score is broken can read the status line instead:
#   --max-score 150
```

then add `trajectories: "/blog/<post>/trajectories/"` to the post's
frontmatter. Link to a step from the post with
`[step 1](#trajectory-<game>-<seed>-<step>)`.

In an `.mdx` post, `TrajectoryCard` renders a step as a transcript card at
build time (props are documented at the top of the component):

```mdx
import TrajectoryCard from "../../components/TrajectoryCard.astro";

<TrajectoryCard game="break-in" seed="202411061" step={170} earlier={94} then={278} />
```

Wrap two cards in `<div class="tcard-pair">` to set them side by side.

### Reference-matrix figures

```bash
python3 scripts/render_reference_matrix.py RUN_DIR/diagnostics/reference-matrix-audit/reference_edges.csv \
  public/blog/<post>/figure.png --title "..." --summaries N [--fonts DIR]
```

## Deploy

`.github/workflows/deploy.yml` builds on push to `master` and deploys via the
GitHub Pages "deploy from Actions" pipeline. In the repo settings, set
**Pages → Source** to **GitHub Actions**.
