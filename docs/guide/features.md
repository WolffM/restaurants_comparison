# Restaurant Comparison Grid: features

Everything below lives in the one script, `main.py`, run top to bottom from
its `__main__` block. How to configure and run it is in
[contributing.md](contributing.md).

## Flexible restaurant input

**What it does.** Takes a plain-text line describing one restaurant and
splits it into a name and a location hint, handling three shapes: a
numbered list entry (`1. Cactus bellevue`), a hyphen-separated name and URL
or city (`Korea house restaurant - https://...`), or a comma-separated name
and city (`Baekjeong KBBQ, Seattle`). Anything else is treated as a name
followed by a single trailing city word (`parse_restaurant_input`).

**How to use it.** Edit the `input_lines` list at the bottom of `main.py`
with your own restaurant lines, in any of the three shapes above.

**What it does not do.** There is no command-line argument or input file;
the list to process is hardcoded in the script itself.

## Yelp lookup

**What it does.** Searches the Yelp Fusion API for a business matching the
parsed name and location hint, then fetches that business's details for up
to five photos, falling back to its one main image if Yelp's details
response has none (`fetch_yelp_data`).

**How to use it.** Requires a Yelp API key (see
[contributing.md](contributing.md#yelp-api-key)). If no location hint was
parsed from the input line, the search falls back to a fixed default
location baked into the script.

**What it does not do.** It takes the first search result only; there is
no way to disambiguate between two businesses with the same name.

## Distance calculation

**What it does.** Computes the great-circle distance, in miles, from one
fixed pair of coordinates hardcoded in the script to each restaurant's
coordinates, using the Haversine formula (`compute_distance`).

**How to use it.** Nothing to configure; it runs automatically for every
restaurant that Yelp successfully finds.

**What it does not do.** The reference point is not a setting — changing
it means editing the two hardcoded coordinates in
`parse_restaurant_input`.

## Composite image grid

**What it does.** Draws one PNG with a row per restaurant: a text panel on
the left (name, city, distance) and up to five photo cells to its right,
each resized to fit while keeping its aspect ratio; a restaurant with fewer
than five photos gets grey "No Image" placeholders for the rest
(`create_restaurant_grid`).

**How to use it.** Runs automatically at the end of the script and saves
`restaurants_comparison.png` in the working directory.

**What it does not do.** The grid is always five image columns wide,
regardless of how many photos a restaurant actually has.

## Trivia

A restaurant that Yelp cannot find at all still gets a row: the script
falls back to a placeholder image service for all five photo cells rather
than skipping the restaurant (`c01cb9e`).
