# Restaurant Comparison Grid: contributing

## Run it locally

```sh
pip install requests pillow python-dotenv
python main.py
```

There is no test suite and no CI in this repo.

## Yelp API key

The script requires a Yelp Fusion API key. Create a `.env` file in the
repo root (already in `.gitignore`, so it is never committed):

```
YELP_API_KEY=your_yelp_api_key_here
```

Without it, `main.py` raises immediately on startup rather than running
with missing data.

## Changing the restaurant list

The script has no input file or command-line flag: edit the `input_lines`
list in `main.py`'s `__main__` block directly, and re-run it.

## Trivia

The script tries Pillow's newer `Image.Resampling.LANCZOS` resize filter
first and only falls back to the older, since-removed `Image.ANTIALIAS`
constant if that attribute is missing (`c01cb9e`).
