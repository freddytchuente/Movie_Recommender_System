# Import necessary librairies

import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch the movie poster using an API

def fetch_poster(movie_id):
    # Construct the API URL with the movie ID
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)

     # Send a request to the API and parse the JSON response
    data = requests.get(url)
    data = data.json()

    # Get the poster path and construct the full URL
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies based on user selection
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]   # Find the index of the selected movie in the DataFrame
    distances = similarity[movie_index]                        # Get the similarity scores for the selected movie

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]  # Sort the movies by similarity and get the top 5 recommendations

    # Initialize lists to store recommended movie titles and posters
    recommended_movies_posters = []
    recommended_movies = []

    # Iterate through the recommended movies and fetch their posters
    for i in movies_list:
        movie_id =movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from API and add it to the list
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load movie data from a pickled file
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity data from a pickled file
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set the title of the Streamlit web app
st.title('Movies Recommender System')

# Create a dropdown select box for choosing a movie
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

# Create a button to trigger movie recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)                # Create five columns to display recommended movies and posters

    with col1:
        st.text(names[0])                                       # Display the recommended movies and their posters in columns
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

    
