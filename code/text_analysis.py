import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.auto import tqdm
nltk.download('vader_lexicon')
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import importlib
import sys
sys.path.append("/Users/dakshj/Desktop/IIT KGP/Semesters/Sem 5/Open IIT DATA/Netflix")

def score_descriptions(df: pd.DataFrame,
                       id_col: str = "show_id",
                       text_col: str = "description",
                       unknown_text: str = "Unknown description.",
                       show_progress: bool = True) -> pd.DataFrame:
    sia = SentimentIntensityAnalyzer()
    ids = df[id_col].tolist()
    texts = df[text_col].astype(str).tolist()

    iterator = zip(ids, texts)
    if show_progress:
        iterator = tqdm(iterator, total=len(ids))

    out = []
    for sid, desc in iterator:
        if desc == unknown_text:
            scores = {"neg": 0.0, "neu": 1.0, "pos": 0.0, "compound": 0.0}
        else:
            scores = sia.polarity_scores(desc)
        out.append((sid, scores["neg"], scores["neu"], scores["pos"], scores["compound"]))

    return pd.DataFrame(out, columns=[id_col, "neg", "neu", "pos", "compound"])

def add_vader_scores(
    df: pd.DataFrame,
    text_col: str = "description",
    unknown_text: str = "Unknown description.",
    show_progress: bool = True
) -> pd.DataFrame:
    """
    Returns a copy of `df` with VADER columns ['neg','neu','pos','compound'] appended.
    """
    sia =  SentimentIntensityAnalyzer()
    it = df[text_col].astype(str)

    if show_progress:
            it = tqdm(it, total=len(df))
    scores_list = []
    for desc in it:
        if desc == "nan" or desc == unknown_text:
            scores = {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
        else:
            scores = sia.polarity_scores(desc)
        scores_list.append(scores)

    vader_scores = pd.DataFrame(scores_list, index=df.index)
    return pd.concat([df.copy(), vader_scores], axis=1)