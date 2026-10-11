import pickle
import streamlit as st
import requests
import pandas as pd

# ---------------- FETCH POSTER USING MOVIE NAME ---------------- #
@st.cache_data
def fetch_poster(movie_name):
    api_key = "87683ffbb1401a2e671bf6cbb3e8a66e"

    try:
        # Step 1: Search movie by name
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
        response = requests.get(search_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # No results
        if not data['results']:
            return "https://via.placeholder.com/500x750?text=No+Poster"

        #  Get first result
        movie = data['results'][0]

        poster_path = movie.get('poster_path')

        # If poster exists
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except:
        return "https://via.placeholder.com/500x750?text=Error"


# ---------------- RECOMMEND FUNCTION ---------------- #
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]]['title']   # use name instead of id

        recommended_movie_names.append(movie_name)
        recommended_movie_posters.append(fetch_poster(movie_name))

    return recommended_movie_names, recommended_movie_posters


# ---------------- LOAD DATA ---------------- #
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


# ---------------- UI ---------------- #
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title('🎬 Hollywood Movie Recommender System')

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

# ---------------- BUTTON ---------------- #
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i], use_container_width=True)