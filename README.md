# chirashi

Unofficial Crunchyroll API for Python.

`chirashi` wraps the Crunchyroll API and parses its raw JSON into typed [Pydantic](https://docs.pydantic.dev/) models, giving you a small, structured API for reading data about series, seasons, episodes, and search results.

## Installation

```bash
uv add git+https://github.com/ryn-cx/chirashi
```

## Usage

Create a client, then call `get(...)` on an endpoint to download from Crunchyroll and
get back a parsed, typed model.

```python
from chirashi import Chirashi

client = Chirashi()

# A series, by series ID.
series = client.series.get("GY8VEQ95Y")

# The seasons of a series, by series ID.
seasons = client.seasons.get("GY8VEQ95Y")

# The episodes of a season, by season ID.
episodes = client.episodes.get("GR3VWXP96")

# Browse series, sorted and paginated.
browse = client.browse_series.get(n=36, sort_by="newly_added")

# Search across music, series, episodes, and top results.
results = client.search.get("naruto")
series_hits = client.search.extract_series(results)
episode_hits = client.search.extract_episodes(results)
music_hits = client.search.extract_music(results)
top_hits = client.search.extract_top_results(results)
```
