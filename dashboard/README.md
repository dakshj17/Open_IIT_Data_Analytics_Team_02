# Netflix Strategic Dashboard (Streamlit)

A Netflix-styled Streamlit app to explore the catalog via **KPIs, trends, geography, genres, and creators**. Built for the Open IIT Data Analytics Hackathon deliverables.

---

## Features
- **Executive Overview:** KPI cards (total titles, Movie/TV mix, YoY growth, countries)
- **Content Explorer:** search, sort, export **unique titles**
- **Trend Intelligence:** titles added by year/month; Movies vs TV over time
- **Geographic Insights:** Top-N countries (unique titles)
- **Genre Intelligence:** treemap, co-occurrence heatmap, “opportunity” list
- **Creator & Talent Hub:** top directors; actor/director portfolio search
- **One-click export** of filtered titles (CSV)
- **Netflix theme** (dark UI, red accents)

---

## Project Structure
```
project/
  app.py
  requirements.txt
  data/         
    final_cleaned_main.csv
    netflix_movies_detailed_up_to_2025.csv    
    netflix_tv_shows_detailed_up_to_2025.csv          
  README.md
```

---

## Data Expectations
CSV with at least:
- `show_id`, `title`, `type` (Movie / TV Show)
- `date_added` (parsable), `release_year` (int), `rating`
- `country` (string; may contain multiple countries)
- `listed_in` (genres/categories; comma-separated string)
- `director`, `cast`, `description` (optional, used by search/creator pages)

The app derives:
- `year_added`, `month_added`
- `country_clean`, `category_clean`
- **titles_df** (one row per `show_id`) and a filtered **exploded** view for country/genre charts.

---

## Setup
1. Ensure **Python 3.9+**.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**requirements.txt**
```
streamlit
pandas
numpy
plotly
```

---

## Run
```bash
streamlit run app.py
```

By default, `app.py` loads:
```python
df_exp, titles_df = load_data("data/final_cleaned_main.csv")
```
Update the path if your file differs.

---

## How Filtering Works (important)
- **Country/Category** filters apply on the **exploded** dataframe.
- **Year/Type** filters apply on the **deduped titles** dataframe.
- Both are intersected via `show_id` → **no double counting**.

**Counting rule**
- Use `titles_f` for KPIs/totals (one row per title).
- Use `df_f_exp` for country/genre breakdowns and prefer `nunique("show_id")`.

---

## Customization
- Colors are defined at the top of `app.py`:
  ```python
  NETFLIX_RED = "#E50914"
  NETFLIX_BG  = "#141414"
  NETFLIX_CARD= "#181818"
  NETFLIX_TEXT= "#ffffff"
  ```
- UI styling lives in the injected `<style>` block.
- Replace absolute file paths with project-relative paths.

---

## Troubleshooting
- **TypeError: datetime64 does not support sum**  
  Specify columns to aggregate or use `numeric_only=True` in groupby.
- **Pie chart blank**  
  Ensure `value_counts()` result is renamed to `["type","count"]` before plotting.
- **Module not found**  
  Add the folder to `sys.path` or use relative imports.
- **Slow loads**  
  Pre-aggregate heavy groupbys and cache with `@st.cache_data`.

---


