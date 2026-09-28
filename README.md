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

Drop a markdown file in `src/content/blog/`. The filename becomes the URL
(`my-post.md` → `/blog/my-post/`). See `example-post.md` for a template.

```yaml
---
title: "..."
date: YYYY-MM-DD
description: "..."   # shown on the blog index
tags: ["..."]        # optional
draft: false         # true hides it from the build
---
```

## Deploy

`.github/workflows/deploy.yml` builds on push to `master` and deploys via the
GitHub Pages "deploy from Actions" pipeline. In the repo settings, set
**Pages → Source** to **GitHub Actions**.
