import streamlit as st
import pandas as pd

# Load data
movies = pd.read_csv('movies_data.csv')
recommendations_df = pd.read_csv('recommendations.csv')

# Function to get recommendations
def recommend(movie):
    # Find the row in recommendations_df
    recommended_row = recommendations_df[recommendations_df['movie'] == movie]
    if not recommended_row.empty:
        return recommended_row.iloc[0, 1:].tolist()
    return []

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Enter the Movie Name:',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)
