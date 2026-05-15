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

- `src/pages/index.astro` — landing title page (two doors)
- `src/pages/official/` — clean academic version
- `src/pages/adventure/` — text-adventure version (interactive parser on landing room)
- `src/content/` — shared content collections (publications, talks, teaching)
- `src/layouts/` — `BaseLayout`, `OfficialLayout`, `AdventureLayout`
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

## Deploy

`.github/workflows/deploy.yml` builds on push to `master` and deploys via the
GitHub Pages "deploy from Actions" pipeline. In the repo settings, set
**Pages → Source** to **GitHub Actions**.
