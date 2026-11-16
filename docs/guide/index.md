---
title: Restaurant Comparison Grid
summary: >-
  A command-line Python script that looks up a list of restaurants on the
  Yelp Fusion API and renders them into one composite image — a row per
  restaurant, its name, city and distance from a fixed home-base location,
  alongside up to five of its photos. Written and finished in one 7-minute
  sitting.
features:
  - name: Flexible restaurant input
    summary: 'Parses a numbered list, hyphen-separated, or comma-separated line into a restaurant name and a location hint.'
    anchor: flexible-restaurant-input
  - name: Yelp lookup
    summary: "Looks each restaurant up on Yelp's API for its city, coordinates, and up to five photos."
    anchor: yelp-lookup
  - name: Distance calculation
    summary: 'Computes the great-circle distance from a fixed reference point to each restaurant.'
    anchor: distance-calculation
  - name: Composite image grid
    summary: 'Renders one PNG with a row per restaurant: a text panel, then up to five photo cells (placeholders if fewer).'
    anchor: composite-image-grid
trivia:
  - "All 3 commits in this repo's history land in about 7 minutes on one Saturday, 2025-02-08 (`c01cb9e`, `6b1b689`)."
  - 'The first commit already included a sample output image, `restaurants_comparison.png`, committed alongside the code that generates it (`c01cb9e`).'
  - "The README was created three minutes after the code (`e3c7e5a`), then almost entirely rewritten under five minutes later: the update added 98 lines and removed 13 from a 26-line draft (`6b1b689`)."
  - 'The distance shown for every restaurant is measured from one hardcoded pair of coordinates in the script itself, not from any input or setting (`c01cb9e`).'
---

# Restaurant Comparison Grid

This repo is one Python script, `main.py`. Given a short list of
restaurant names — in almost any format, numbered, comma-separated, or
with a trailing URL — it looks each one up on the
[Yelp Fusion API](https://www.yelp.com/developers), works out how far it is
from a fixed home-base location, and renders everything into one PNG: a
row per restaurant, a text panel with its name, city and distance, and up
to five of its photos (or grey placeholders if Yelp has fewer).

It is a single run-and-done script: no server, no scheduling, and no
stored history beyond the one image it writes.

- [Features](features.md): what the script parses, fetches and draws.
- [Contributing](contributing.md): running it locally, the Yelp key it needs.
- [History](history.md): one sitting, three commits, 7 minutes.
- [Trivia](trivia.md)

## Trivia

Every commit this repo has ever had landed in just over 7 minutes of each
other on the same Saturday ([history](history.md#one-sitting)).
