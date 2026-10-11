import os
import base64
import pickle
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

# ---------------- CONFIGURATION ----------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- BACKGROUND IMAGE ----------------
background_file = BASE_DIR / "cinematch_background.png"

if background_file.exists():
    encoded_image = base64.b64encode(
        background_file.read_bytes()
    ).decode("utf-8")
    background = f'url("data:image/png;base64,{encoded_image}")'
else:
    background = "linear-gradient(135deg, #fffaf8, #fff0f3)"

# ---------------- CUSTOM UI ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {{
    font-family: 'Inter', sans-serif;
    color: #111a31;
    background: #fffaf9;
}}

[data-testid="stAppViewContainer"] {{
    background-image: {background};
    background-repeat: no-repeat;
    background-position: center top;
    background-size: 100% auto;
    background-color: #fffaf9;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.block-container {{
    max-width: 1250px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}}

#MainMenu, footer {{
    visibility: hidden;
}}

.brand {{
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #111a31;
    margin-bottom: 65px;
}}

.brand span, .accent {{
    color: #ed1745;
}}

.hero {{
    min-height: 275px;
}}

.hero-title {{
    font-size: clamp(38px, 5.1vw, 66px);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -2.5px;
    color: #111a31;
    margin-bottom: 14px;
}}

.hero-subtitle {{
    color: #68738b;
    font-size: 17px;
    line-height: 1.55;
}}

/* MOVIE SELECTOR LABEL */
div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] label,
.stSelectbox label,
.stSelectbox label p {{
    color: #111a31 !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
    line-height: 1.5 !important;
}}

/* DROPDOWN */
div[data-baseweb="select"] > div {{
    min-height: 54px;
    background: #252630 !important;
    border: 1px solid #ed1745 !important;
    border-radius: 12px;
}}

div[data-baseweb="select"] div {{
    color: #ffffff;
}}

div[data-baseweb="select"] input {{
    color: #ffffff !important;
    caret-color: #ffffff;
}}

div[data-baseweb="select"] svg {{
    fill: #ffffff;
}}

/* DROPDOWN OPTIONS */
li[role="option"] {{
    color: #111a31 !important;
    background: #ffffff;
}}

li[role="option"]:hover {{
    background: #fff0f3 !important;
}}

/* RECOMMENDATION BUTTON */
.stButton > button {{
    width: 100%;
    min-height: 52px;
    background: linear-gradient(110deg, #ff5268, #ed1745);
    color: #ffffff;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    font-size: 16px;
    box-shadow: 0 6px 18px rgba(237,23,69,.18);
    transition: .2s ease;
}}

.stButton > button:hover {{
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 9px 24px rgba(237,23,69,.25);
}}

/* RECOMMENDED MOVIES */
.section-title {{
    color: #111a31;
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -.7px;
    margin-bottom: 20px;
}}

.poster-card {{
    background: rgba(255,255,255,.97);
    border: 1px solid #f3e3e7;
    border-radius: 15px;
    padding: 7px;
    box-shadow: 0 8px 22px rgba(29,37,57,.10);
}}

div[data-testid="stImage"] {{
    border-radius: 12px;
    overflow: hidden;
}}

div[data-testid="stImage"] img {{
    border-radius: 12px;
    transition: transform .25s ease;
}}

div[data-testid="stImage"]:hover img {{
    transform: scale(1.025);
}}

.movie-caption {{
    color: #111a31;
    font-size: 13px;
    font-weight: 700;
    padding: 10px 2px 7px;
    text-align: center;
    min-height: 45px;
    overflow-wrap: anywhere;
}}

.movie-number {{
    display: inline-block;
    background: #ff3155;
    color: white;
    padding: 5px 7px;
    border-radius: 7px;
    margin-right: 4px;
    font-size: 11px;
}}

@media (max-width: 700px) {{
    .brand {{ margin-bottom: 30px; }}
    .hero {{ min-height: 220px; }}
    .hero-title {{ letter-spacing: -1px; }}

    div[data-testid="stWidgetLabel"] p,
    .stSelectbox label p {{
        font-size: 19px !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="brand">🎬 Cine<span>Match</span></div>

<div class="hero">
    <div class="hero-title">
        Find Your<br>
        <span class="accent">Next Favorite Movie</span>
    </div>
    <div class="hero-subtitle">
        Select a movie you like and get personalized<br>
        recommendations you might enjoy.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- API KEY CHECK ----------------
if not TMDB_API_KEY:
    st.error("Please configure TMDB_API_KEY in your .env file.")
    st.stop()

# ---------------- LOAD MOVIE DATA ----------------
@st.cache_resource
def load_movie_data():
    with open(BASE_DIR / "movies_dict.pkl", "rb") as file:
        movie_data = pickle.load(file)

    with open(BASE_DIR / "similarity.pkl", "rb") as file:
        similarity_matrix = pickle.load(file)

    movie_df = pd.DataFrame(movie_data)

    if "title" not in movie_df.columns:
        raise ValueError("Movie data must contain a title column.")

    if len(movie_df) != len(similarity_matrix):
        raise ValueError(
            "Movie data and similarity matrix sizes do not match."
        )

    return movie_df, similarity_matrix


try:
    movies, similarity = load_movie_data()
except FileNotFoundError as error:
    st.error(f"Missing file: {error.filename}")
    st.stop()
except Exception as error:
    st.error(f"Could not load movie data: {error}")
    st.stop()

# ---------------- FETCH MOVIE POSTER ----------------
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_poster(movie_name):
    try:
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "query": movie_name,
            },
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        if results and results[0].get("poster_path"):
            return (
                "https://image.tmdb.org/t/p/w500"
                + results[0]["poster_path"]
            )

    except (requests.RequestException, ValueError):
        pass

    return "https://placehold.co/500x750/f8eef0/17213a?text=Movie"

# ---------------- RECOMMENDATION ENGINE ----------------
def recommend(movie_title):
    matches = movies.index[movies["title"] == movie_title]

    if len(matches) == 0:
        return []

    movie_index = matches[0]

    ranked = sorted(
        enumerate(similarity[movie_index]),
        key=lambda item: item[1],
        reverse=True,
    )

    recommendations = []

    for index, score in ranked:
        if index == movie_index:
            continue

        title = movies.iloc[index]["title"]

        if pd.notna(title):
            recommendations.append(title)

        if len(recommendations) == 5:
            break

    return recommendations

# ---------------- MOVIE SELECTOR ----------------
movie_list = sorted(
    movies["title"].dropna().unique().tolist()
)

if not movie_list:
    st.error("No movie titles were found.")
    st.stop()

selected_movie = st.selectbox(
    "🎬 Choose a movie",
    movie_list,
    index=None,
    placeholder="Search for a movie...",
)

search_clicked = st.button(
    "✦  Show Recommendation",
    type="primary",
)

# ---------------- SAVE RESULTS ----------------
if "recommended_movies" not in st.session_state:
    st.session_state.recommended_movies = []
    st.session_state.selected_title = None

if search_clicked:
    if selected_movie is None:
        st.warning("Please select a movie first.")
    else:
        st.session_state.selected_title = selected_movie

        with st.spinner("Finding recommendations..."):
            st.session_state.recommended_movies = recommend(
                selected_movie
            )

# ---------------- DISPLAY POSTERS ----------------
recommended = st.session_state.recommended_movies
selected_title = st.session_state.selected_title

if recommended and selected_title:
    st.markdown(
        '<div class="section-title">🍿 Recommended '
        '<span class="accent">Movies</span></div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(len(recommended), gap="small")

    for number, (column, title) in enumerate(
        zip(columns, recommended), start=1
    ):
        with column:
            st.markdown(
                '<div class="poster-card">',
                unsafe_allow_html=True,
            )

            st.image(
                fetch_poster(title),
                use_container_width=True,
            )

            st.markdown(
                f'<div class="movie-caption">'
                f'<span class="movie-number">{number:02d}</span> '
                f'{title}</div>',
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

elif search_clicked:
    st.info("No recommendations found for this movie.")
