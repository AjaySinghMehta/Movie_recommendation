# importing streamlit libray
import streamlit as st
import pickle
import requests
import numpy
import pandas as pd

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f7225b4aadeea74295cccdc2805b4dcd'.format(movie_id))
    data_movie = response.json()
    return "https://image.tmdb.org/t/p/w500" + data_movie['poster_path']

#using bag of words

# def recommend(movie):
#     movie_index = numpy.argmax(movies == movie)
#
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies_df.iloc[i[0]]['movie_id']
#         recommended_movies.append(movies[i[0]])
#
#         # now we will fetch the poster from the TMDB website
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies, recommended_movies_posters


# def recommend_Tfidf(movie):
#     movie_index = numpy.argmax(movies == movie)
#     distances = similarity2[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies_df.iloc[i[0]]['movie_id']
#         recommended_movies.append(movies[i[0]])
#
#         # now we will fetch the poster from the TMDB website
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies, recommended_movies_posters


def final_recommend(movie):
    combined_list = []

    # finding index of movie & it's similarity matrix
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    # finding index & most similar movies using TF-IDF
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances2 = similarity2[movie_index]
    movies_list2 = sorted(list(enumerate(distances2)), reverse=True, key=lambda x: x[1])[1:11]

    # combining lists and filtering unique result
    combined_list = movies_list + movies_list2
    unique_pairs = {}

    recommended_movies_posters = []
    for pair in combined_list:

        first_element = pair[0]
        if first_element not in unique_pairs:
            unique_pairs[first_element] = pair
    combined_list = list(unique_pairs.values())

    # sorting again to find top 10 similar movies
    combined_list = sorted(combined_list, key=lambda x: x[1], reverse=True)[1:11]

    output = []
    for i in combined_list:
        movie_id = movies_df.iloc[i[0]]['movie_id']
        output.append(movies_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return output,recommended_movies_posters

movies = pickle.load(open('movies.pkl','rb'))
movies = movies['title'].values
movies_df = pd.read_pickle("movies.pkl")

similarity = pickle.load(open('similarity.pkl','rb'))

similarity2 = pickle.load(open('similarity2.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select the movie ',
    movies)



if st.button('Recommend'):
    names, posters = final_recommend(selected_movie_name)

    num_movies = len(names)
    num_cols = 5
    num_rows = (num_movies + num_cols - 1) // num_cols

    for row in range(num_rows):
        cols = st.columns(num_cols)

        start_index = row * num_cols
        end_index = min((row + 1) * num_cols, num_movies)

        for i in range(start_index, end_index):
            with cols[i % num_cols]:
                st.text(names[i])
                st.image(posters[i])





