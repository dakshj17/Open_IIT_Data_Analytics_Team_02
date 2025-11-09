import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
from helper_functions import *
### Cleaning the https://www.kaggle.com/datasets/shivamb/netflix-shows/data csv file

path = r"C:\Users\adity\Downloads\OPEN IIT NETFLIX\main_Csv\netflix_titles.csv"
df = pd.read_csv(path)
# check for NAN values 
df = df[df['country'].str.lower() != 'others']
df['country'] = df['country'].fillna('Others')

df['show_id'] = df['show_id'].str.extract('(\d+)').astype(int)

# Split the 'country' column on commas and expand into multiple rows
df = df.assign(country=df['country'].str.split(',')).explode('country')
df['country'] = df['country'].str.strip() # Clean up any whitespace around country names
df = df[df['country'] != ""].reset_index(drop=True)
df = df.reset_index(drop=True)

df.loc[df['director'].isna(),'director']='Unknown'
df.loc[df['cast'].isna(),'cast']='Unknown'
df.loc[df['country'].isna(),'country']='Unknown'

# Fill NAN Values of the rating feature
df.loc[6626,'rating']='TV-MA'
df.loc[6919,'rating']='TV-MA'
df.loc[6938,'rating']='TV-MA'
df.loc[7147,'rating']='TV-PG'
df.loc[8240,'rating']='TV-PG'
df.loc[8861,'rating']='TV-Y7'
df.loc[9133,'rating']='TV-MA'

### filling the nan values of the date_added with median value of when the (yearfrom date added - release_year);

# Ensure date_added is datetime
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Calculate year difference where available
df['year_diff'] = df['date_added'].dt.year - df['release_year']

# Compute median difference (ignoring NaNs)
median_diff = int(df['year_diff'].median())


# Fill NaN date_added using release_year + median_diff
df.loc[df['date_added'].isna(), 'date_added'] = pd.to_datetime(
    (df['release_year'] + median_diff).astype(str) + '-01-01'
)

# Drop helper column
df.drop(columns=['year_diff'], inplace=True)
df['duration'] = df['duration'].fillna(df['duration'].mean)

### Count how many Cast, Director, Listed_in are there
df['count_cast']=df['cast'].str.split(',').str.len()
df['count_director']=df['director'].str.split(',').str.len()
df['count_listed_in'] = df['listed_in'].str.split(',').str.len()

### Categories on the basis of rating groups

rating_groups = {
    'Kids': ['TV-Y', 'TV-Y7', 'TV-G', 'G', 'TV-Y7-FV'],
    'Teens': ['TV-PG', 'PG', 'PG-13', 'TV-14'],
    'Adults': ['TV-MA', 'R', 'NC-17', 'NR', 'UR']
}
def cat(x):
  for k ,v in rating_groups.items():
    if x['rating'] in v:
      return k

df['category']=df.apply(lambda x : cat(x),axis=1)


### Separating the genres (listed_in)
from collections import Counter
# Split by commas and strip spaces
all_genres = df['listed_in'].str.split(',').explode().str.strip()
# Count occurrences
genre_counts = Counter(all_genres)
# Convert to dictionary (optional)
genre_dict = dict(genre_counts)

genre_map = {
    "Documentaries": "Documentary",
    "International TV Shows": "International",
    "TV Dramas": "Drama",
    "TV Mysteries": "Mystery",
    "Crime TV Shows": "Crime",
    "TV Action & Adventure": "Action",
    "Docuseries": "Documentary",
    "Reality TV": "Reality",
    "Romantic TV Shows": "Romance",
    "TV Comedies": "Comedy",
    "TV Horror": "Horror",
    "Children & Family Movies": "Family",
    "Dramas": "Drama",
    "Independent Movies": "Independent",
    "International Movies": "International",
    "British TV Shows": "International",
    "Comedies": "Comedy",
    "Spanish-Language TV Shows": "International",
    "Thrillers": "Thriller",
    "Romantic Movies": "Romance",
    "Music & Musicals": "Music",
    "Horror Movies": "Horror",
    "Sci-Fi & Fantasy": "Sci-Fi",
    "TV Thrillers": "Thriller",
    "Kids' TV": "Family",
    "Action & Adventure": "Action",
    "TV Sci-Fi & Fantasy": "Sci-Fi",
    "Classic Movies": "Classic",
    "Anime Features": "Anime",
    "Sports Movies": "Sports",
    "Anime Series": "Anime",
    "Korean TV Shows": "International",
    "Science & Nature TV": "Sci-Fi",
    "Teen TV Shows": "Teen",
    "Cult Movies": "Cult",
    "TV Shows": "TV",
    "Faith & Spirituality": "Faith",
    "LGBTQ Movies": "LGBTQ",
    "Stand-Up Comedy": "Comedy",
    "Movies": "Movies",
    "Stand-Up Comedy & Talk Shows": "Comedy",
    "Classic & Cult TV": "Classic"
}
df['listed_in'] = (
    df['listed_in']
    .str.split(',')
    .apply(lambda genres: ', '.join(sorted(set(
        genre_map.get(g.strip(), g.strip()) for g in genres
    ))))
)

df = df[df['listed_in'] != ""].reset_index(drop=True)


columns = ['cast', 'director', 'listed_in']
for col in columns:
    # Split the column on commas and expand into multiple rows
    df = df.assign(**{col: df[col].str.split(',')}).explode(col)

    # Clean up any whitespace
    df[col] = df[col].str.strip()
    df = df[df[col] != ""].reset_index(drop=True)

# Drop completely duplicate rows (across all columns)
df = df.drop_duplicates().reset_index(drop=True)

df = df.dropna().reset_index(drop = True)
## save the cleaned file
df.to_csv('testing_python.csv', index = False)


### Cleaning the https://www.kaggle.com/datasets/bhargavchirumamilla/netflix-movies-and-tv-shows-till-2025 csv file

path = r'C:\Users\adity\Downloads\OPEN IIT NETFLIX\TV_Movies_Show\netflix_movies_detailed_up_to_2025.csv'

df = pd.read_csv(path)
df = df.drop(columns=['duration'])
df = df.dropna(subset=['director'])

df = df.dropna(subset=['country'])
df = df.dropna(subset=['genres'])

# from helper function 
df_s = safe_split_and_explode_country(df)   # replace df_main with your df variable if different

# Usage (just call this)
df_s = safe_split_and_explode_cast(df_s, 'cast')   # replace df_main with your df variable if different
df_s = df_s.dropna()
df_s.to_csv('trial_2025_movies.csv', index = False)