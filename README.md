# Interprice Search Engine (NLP)

Lightweight search engine prototype that uses NLP techniques to index and rank product/medical data. This repository contains data cleaning, indexing, and ranking scripts plus a small Flask app to serve search results.

## Features
- Data cleaning/preprocessing for structured inputs
- Building vector/index files for fast lookup
- Ranking based on similarity/scoring
- Simple web UI (Flask) for searching and showing results

## Repository layout
- `app.py` — Flask application entry point (serves web UI)
- `Data_Cleaning_Structured_v1_0.py` — data cleaning and preprocessing
- `Indexing_v1_0.py` — builds indices (numpy files) from cleaned data
- `Ranking_v1_final.py` — ranking logic to score and order results
- `Search_v1_0.py` — search interface and helpers used by the app
- `med_index_1000.npy`, `products_index.npy` — example index/vector files
- `static/` — static assets (CSS)
- `templates/` — HTML templates (`home.html`, `result.html`)

## Quick start

1. Create a Python environment (recommended):

   `python3 -m venv .venv`

   `source .venv/bin/activate`

   `pip install -r requirements.txt`  # if provided, otherwise install Flask and numpy

2. Run the app locally:

   `python app.py`

   then open `http://127.0.0.1:5000` in your browser

Note: If `requirements.txt` is not present, install minimal dependencies manually:

   `pip install flask numpy`

## Usage
- Use the web UI to enter queries and view ranked results.
- To rebuild indices, run `Indexing_v1_0.py` after preparing data with `Data_Cleaning_Structured_v1_0.py`.

## Development notes
- Scripts are written as standalone tools; adapt paths and filenames as needed.
- Index files are stored as numpy `.npy` arrays — ensure compatibility when regenerating.

## License
This project is provided as-is for experimentation. Add a license if you plan to publish or redistribute.

---
If you want, I can add a `requirements.txt`, run the app to verify it starts, or expand the README with examples. Which should I do next?
