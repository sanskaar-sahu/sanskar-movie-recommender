import pickle
import streamlit as st
import requests
import pandas as pd

st.markdown("""
    <style>

    .stSelectbox > div {
        marign: 50px;
            font-size:14px;
    }
    
    </style>
""", unsafe_allow_html=True)


# UI header
st.header("🎬 Movie Recommendation using Machine Learning")

# Load data safely
movies = pd.read_pickle("movie_list.pkl")

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Movie dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendations',
    movie_list
)

# TMDB Poster Fetch Function (Fixed)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ec049e963e09da7c646e526db9814494&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return "https://via.placeholder.com/150"  # Fallback image
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/150"  # Fallback image

# ✅ Recommendation Function (Fixed)
def recommend(movie):
    try:
        index = movies[movies['title'].str.lower().str.strip() == movie.lower().strip()].index[0]
    except IndexError:
        st.error("❌ Movie not found in dataset. Please try another.")
        return [], []

    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_name = []
    recommended_movies_poster = []

    for i in movie_indices:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies_name.append(movies.iloc[i[0]]['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))
        #st.write("Type of similarity matrix:", type(similarity))


    return recommended_movies_poster, recommended_movies_name


# Recommend button
if st.button('Show Recommendations'):
    recommended_movies_poster, recommended_movies_name = recommend(selected_movie)

    if recommended_movies_name:  # show only if list is not empty
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.text(recommended_movies_name[0])
            st.image(recommended_movies_poster[0])
        with col2:
            st.text(recommended_movies_name[1])
            st.image(recommended_movies_poster[1])
        with col3:
            st.text(recommended_movies_name[2])
            st.image(recommended_movies_poster[2])
        with col4:
            st.text(recommended_movies_name[3])
            st.image(recommended_movies_poster[3])
        with col5:
            st.text(recommended_movies_name[4])
            st.image(recommended_movies_poster[4])

