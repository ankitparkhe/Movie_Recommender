# import streamlit as st
# import pickle
# import pandas as pd
#
#
# import requests
#
#
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a6d7a0ac444bc2ead6f365a3a117887e"
#     response = requests.get(url)
#
#     if response.status_code != 200:  # If API request fails
#         return "https://via.placeholder.com/500x750?text=No+Image"
#
#     data = response.json()
#     poster_path = data.get('poster_path', '')  # Correct way to get poster_path
#
#     if not poster_path:  # If no poster is available
#         return "https://via.placeholder.com/500x750?text=No+Image"
#
#     return f"https://image.tmdb.org/t/p/w500/{poster_path}"
#
#
# # Load data
# movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# # Recommendation function
# def recommend(movie_name):
#     recommended_movies = [movies]  # Replace with real movie IDs
#     recommend_movies_poster = []
#
#     for movie_id in recommended_movies:
#         poster = fetch_poster(movie_id)
#         recommend_movies_poster.append(poster)
#
#     return recommended_movies, recommend_movies_poster
#
#
#
#
#
# # Streamlit UI
# st.title('Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     'Select a movie:',
#     movies['title'].values)
#
# if st.button("Recommend"):
#      names, poster = recommend(selected_movie_name)
#
#
#      col1, col2, col3, col4, col5 = st.columns(5)
#
#      with col1:
#          st.text(names[0])
#          st.image(poster[0])
#      with col2:
#          st.text(names[1])
#          st.image(poster[1])
#      with col3:
#          st.text(names[2])
#          st.image(poster[2])
#      with col4:
#          st.text(names[3])
#          st.image(poster[3])
#      with col5:
#          st.text(names[4])
#          st.image(poster[4])

# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import gzip
#
# # API Key
# API_KEY = "a6d7a0ac444bc2ead6f365a3a117887e"
#
# # Function to fetch movie poster from TMDB
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
#     response = requests.get(url)
#
#     if response.status_code != 200:  # If API request fails
#         return "https://via.placeholder.com/500x750?text=No+Image"
#
#     data = response.json()
#     poster_path = data.get('poster_path', '')
#
#     if not poster_path:  # If no poster is available
#         return "https://via.placeholder.com/500x750?text=No+Image"
#
#     return f"https://image.tmdb.org/t/p/w500/{poster_path}"
#
# # ✅ Load data using gzip (Decompress during runtime)
# def load_pickle_gzip(file_path):
#     with gzip.open(file_path, "rb") as f:
#         return pickle.load(f)
#
# # Load compressed movie data
# movies_dict = load_pickle_gzip('movies_dict.pkl.gz')
# movies = pd.DataFrame(movies_dict)
# similarity = load_pickle_gzip('similarity.pkl.gz')  # Assuming similarity is also compressed
#
# # Recommendation function
# def recommend(movie_name):
#     if movie_name not in movies['title'].values:
#         return [], []  # Return empty lists if movie not found
#
#     movie_index = movies[movies['title'] == movie_name].index[0]  # Get index of selected movie
#     similar_movies = list(enumerate(similarity[movie_index]))  # Find similar movies
#
#     sorted_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:6]  # Top 5 movies
#
#     recommended_movie_names = []
#     recommended_movie_posters = []
#
#     for i in sorted_movies:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#         recommended_movie_posters.append(fetch_poster(movie_id))
#
#     return recommended_movie_names, recommended_movie_posters
#
# # Streamlit UI
# st.title('Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     'Select a movie:',
#     movies['title'].values)
#
# if st.button("Recommend"):
#     names, posters = recommend(selected_movie_name)
#
#     if not names:  # If empty, show warning
#         st.warning("No recommendations found.")
#     else:
#         cols = st.columns(len(names))  # Dynamically create columns
#
#         for i in range(len(names)):
#             with cols[i]:
#                 st.text(names[i])
#                 st.image(posters[i])

import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
import lzma  # For .xz files

# API Key
API_KEY = "a6d7a0ac444bc2ead6f365a3a117887e"

# Function to fetch movie poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:  # If API request fails
        return "https://via.placeholder.com/500x750?text=No+Image"

    data = response.json()
    poster_path = data.get('poster_path', '')

    if not poster_path:  # If no poster is available
        return "https://via.placeholder.com/500x750?text=No+Image"

    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

# ✅ Load data using gzip (Decompress during runtime for .gz files)
def load_pickle_gzip(file_path):
    with gzip.open(file_path, "rb") as f:  # Keep this for .gz files
        return pickle.load(f)

# ✅ Load data using lzma (Decompress during runtime for .xz files)
def load_pickle_xz(file_path):
    with lzma.open(file_path, "rb") as f:  # Use lzma for .xz files
        return pickle.load(f)

# Load compressed movie data
movies_dict = load_pickle_gzip('movies_dict.pkl.gz')  # .gz file
movies = pd.DataFrame(movies_dict)

# Load similarity data (now it's .xz file)
similarity = load_pickle_xz('similarity_compressed.pkl.xz')  # .xz file

# Recommendation function
def recommend(movie_name):
    if movie_name not in movies['title'].values:
        return [], []  # Return empty lists if movie not found

    movie_index = movies[movies['title'] == movie_name].index[0]  # Get index of selected movie
    similar_movies = list(enumerate(similarity[movie_index]))  # Find similar movies

    sorted_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:6]  # Top 5 movies

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in sorted_movies:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    if not names:  # If empty, show warning
        st.warning("No recommendations found.")
    else:
        cols = st.columns(len(names))  # Dynamically create columns

        for i in range(len(names)):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])













