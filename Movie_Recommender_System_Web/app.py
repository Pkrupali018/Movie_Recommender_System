import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=be54fe2e9e1822f427fb8c361515f6bd'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommend_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommend_movies_posters.append(fetch_poster(movie_id))
    # poster = pd.DataFrame(recommend_movies_posters)
    return recommend_movies,recommend_movies_posters

# movies_list = pickle.load(open('movies.pkl','rb'))
# movies_list = movies_list['title'].values

# Using pandas
movies_list = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load((open('similarity.pkl', 'rb')))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Which moviw you like?',
    # (movies_list)
    movies['title'].values
)

if st.button('Recommend'):
    st.write("Selected Movie Name: ",selected_movie_name)
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0])
    with col2:
        st.write(names[1])
        st.image(posters[1])
    with col3:
        st.write(names[2])
        st.image(posters[2])
    with col4:
        st.write(names[3])
        st.image(posters[3])
    with col5:
        st.write(names[4])
        st.image(posters[4])