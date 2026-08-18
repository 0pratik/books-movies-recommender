import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
import time
import random
from PIL import Image
from io import BytesIO
import urllib.parse

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Functions for Book Recommender System
def recommend_book(user_input):
    if user_input not in pt.index:
        st.warning("No book found with the given title. 😔 Please try another title. 📚")
    else:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:7]

        for i in range(0, len(similar_items), 2):
            col1, col2 = st.columns(2)
            with col1:
                temp_df1 = books[books['Book-Title'] == pt.index[similar_items[i][0]]]
                st.subheader(temp_df1.drop_duplicates('Book-Title')['Book-Title'].values[0])
                st.write("Author:", temp_df1.drop_duplicates('Book-Title')['Book-Author'].values[0])
                st.image(temp_df1.drop_duplicates('Book-Title')['Image-URL-M'].values[0])
                # Add Amazon button
                book_title_encoded1 = urllib.parse.quote(temp_df1.drop_duplicates('Book-Title')['Book-Title'].values[0])
                amazon_url1 = f"https://www.amazon.com/s?k={book_title_encoded1}"
                st.write(f"[Buy on Amazon]({amazon_url1})", unsafe_allow_html=True)
            with col2:
                if i + 1 < len(similar_items):
                    temp_df2 = books[books['Book-Title'] == pt.index[similar_items[i + 1][0]]]
                    st.subheader(temp_df2.drop_duplicates('Book-Title')['Book-Title'].values[0])
                    st.write("Author:", temp_df2.drop_duplicates('Book-Title')['Book-Author'].values[0])
                    st.image(temp_df2.drop_duplicates('Book-Title')['Image-URL-M'].values[0])
                    # Add Amazon button
                    book_title_encoded2 = urllib.parse.quote(temp_df2.drop_duplicates('Book-Title')['Book-Title'].values[0])
                    amazon_url2 = f"https://www.amazon.com/s?k={book_title_encoded2}"
                    st.write(f"[Buy on Amazon]({amazon_url2})", unsafe_allow_html=True)

# Functions for Movie Recommender System
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8c4df95371c30631c6844fd1579f2c87&append_to_response=videos,images')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def fetch_trailer(movie_title):
    search_query = movie_title + " official trailer"
    search_query = search_query.replace(" ", "+")
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    return youtube_url

def assign_platform():
    platforms = ['Netflix', 'Prime Video', 'Disney+']
    return random.choice(platforms)

def recommend_movie(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append({
            'title': movies.iloc[i[0]].title,
            'platform': assign_platform(),
            'id': movie_id
        })
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Main Streamlit app
st.set_page_config(page_title="Discover Your Next Favorite", page_icon="📚🎬", layout="wide")

# Add some styling
st.markdown(
"""
<style>
body {
    background-color: #f0f2f6;
}

h1, .stRadio > div > label {
    color: #333;
}

.sidebar .sidebar-content {
    background-color: #ffffff;
    color: #333;
}

.stButton > button {
    background-color: #007bff;
    color: #ffffff;
}

.stButton > button:hover {
    background-color: #0056b3;
}

</style>
""",
unsafe_allow_html=True
)

# Sidebar navigation
option = st.sidebar.radio('', ('Literary Gems 📚💎', 'Book Voyage 🚢📖', 'Movie Marathon 🎬🍿', "Don't Know What to Watch 🤔", "Don't Know What to Read 📚", "Send Feedback"))

if option == 'Book Voyage 🚢📖':
    st.title("Set Sail on Your Book Voyage 🚢📖")
    user_input = st.text_input("Enter a book title")
    if st.button("Get Recommendations 📚"):
        recommend_book(user_input)

elif option == 'Movie Marathon 🎬🍿':
    st.title('🎬 Movie Marathon Madness 🍿')
    selected_movie_name = st.selectbox(
        '🎥 Tell Us Your Movie Taste 🍿',
        movies['title'].values,
        format_func=lambda x: '🎬 ' + x
    )

    if st.button('🚀 Recommend 🚀'):
        with st.spinner('🎬 Recommending...'):
            time.sleep(3)
            st.write("---")
            try:
                recommended_movies, posters = recommend_movie(selected_movie_name)

                for i in range(0, len(recommended_movies), 3):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if i < len(recommended_movies):
                            movie = recommended_movies[i]
                            poster = posters[i]
                            st.subheader(movie['title'])
                            st.image(poster, use_column_width=True)
                            st.write(f"Available on: [{movie['platform']}](https://www.netflix.com/)" if movie['platform'] == 'Netflix'
                                     else f"Available on: [{movie['platform']}](https://www.primevideo.com/)" if movie['platform'] == 'Prime Video'
                                     else f"Available on: [{movie['platform']}](https://www.disneyplus.com/)")
                            trailer_link = fetch_trailer(movie['title'])
                            st.write(f"[Watch Trailer]({trailer_link})", unsafe_allow_html=True)
                    with col2:
                        if i + 1 < len(recommended_movies):
                            movie = recommended_movies[i + 1]
                            poster = posters[i + 1]
                            st.subheader(movie['title'])
                            st.image(poster, use_column_width=True)
                            st.write(f"Available on: [{movie['platform']}](https://www.netflix.com/)" if movie['platform'] == 'Netflix'
                                     else f"Available on: [{movie['platform']}](https://www.primevideo.com/)" if movie['platform'] == 'Prime Video'
                                     else f"Available on: [{movie['platform']}](https://www.disneyplus.com/)")
                            trailer_link = fetch_trailer(movie['title'])
                            st.write(f"[Watch Trailer]({trailer_link})", unsafe_allow_html=True)
                    with col3:
                        if i + 2 < len(recommended_movies):
                            movie = recommended_movies[i + 2]
                            poster = posters[i + 2]
                            st.subheader(movie['title'])
                            st.image(poster, use_column_width=True)
                            st.write(f"Available on: [{movie['platform']}](https://www.netflix.com/)" if movie['platform'] == 'Netflix'
                                     else f"Available on: [{movie['platform']}](https://www.primevideo.com/)" if movie['platform'] == 'Prime Video'
                                     else f"Available on: [{movie['platform']}](https://www.disneyplus.com/)")
                            trailer_link = fetch_trailer(movie['title'])
                            st.write(f"[Watch Trailer]({trailer_link})", unsafe_allow_html=True)
            except IndexError:
                st.error("❌ Movie not found or could not be recommended. ❌")

elif option == 'Literary Gems 📚💎':
    st.title('Unearth Literary Gems 📚💎')
    for index, row in popular_df.head(50).iterrows():
        st.subheader(row['Book-Title'])
        st.write(f"Author: {row['Book-Author']}")
        st.write(f"Votes: {row['num_ratings']}")
        st.write(f"Rating: {row['avg_rating']}")
        st.image(row['Image-URL-M'], width=200)
        # Add Amazon button
        book_title_encoded = urllib.parse.quote(row['Book-Title'])
        amazon_url = f"https://www.amazon.com/s?k={book_title_encoded}"
        st.write(f"[Buy on Amazon]({amazon_url})", unsafe_allow_html=True)

elif option == "Don't Know What to Watch 🤔":
    st.title("🤔 Don't Know What to Watch?")
    if st.button("Generate Random Movies"):
        random_movies = movies.sample(n=15)
        for i in range(0, len(random_movies), 3):
            col1, col2, col3 = st.columns(3)
            with col1:
                if i < len(random_movies):
                    movie = random_movies.iloc[i]
                    st.subheader(movie['title'])
                    st.image(fetch_poster(movie['movie_id']), use_column_width=True)
                    platform = assign_platform()
                    st.write(f"Available on: [{platform}](https://www.netflix.com/)" if platform == 'Netflix'
                             else f"Available on: [{platform}](https://www.primevideo.com/)" if platform == 'Prime Video'
                             else f"Available on: [{platform}](https://www.disneyplus.com/)")
                    trailer_link = fetch_trailer(movie['title'])
                    st.write(f"[Watch Trailer]({trailer_link})", unsafe_allow_html=True)
            with col2:
                if i + 1 < len(random_movies):
                    movie = random_movies.iloc[i + 1]
                    st.subheader(movie['title'])
                    st.image(fetch_poster(movie['movie_id']), use_column_width=True)
                    platform = assign_platform()
                    st.write(f"Available on: [{platform}](https://www.netflix.com/)" if platform == 'Netflix'
                             else f"Available on: [{platform}](https://www.primevideo.com/)" if platform == 'Prime Video'
                             else f"Available on: [{platform}](https://www.disneyplus.com/)")
                    trailer_link = fetch_trailer(movie['title'])
                    st.write(f"[Watch Trailer]({trailer_link})", unsafe_allow_html=True)
            with col3:
                if i + 2 < len(random_movies):
                    movie = random_movies.iloc[i + 2]
                    st.subheader(movie['title'])
                    st.image(fetch_poster(movie['movie_id']), use_column_width=True)
                    platform = assign_platform()
                    st.write(f"Available on: [{platform}](https://www.netflix.com/)" if platform == 'Netflix'
                             else f"Available on: [{platform}](https://www.primevideo.com/)" if platform == 'Prime Video'
                             else f"Available on: [{platform}](https://www.disneyplus.com/)")
                    trailer_link = fetch_trailer(movie['title'])
                    st.write(f"[Watch Trailer]({trailer_link})", unsafe_allow_html=True)

elif option == "Don't Know What to Read 📚":
    st.title("📚 Don't Know What to Read?")
    if st.button("Generate Random Books"):
        random_books = books.sample(n=20)
        for i in range(0, len(random_books), 2):
            col1, col2 = st.columns(2)
            with col1:
                if i < len(random_books):
                    book = random_books.iloc[i]
                    st.subheader(book['Book-Title'])
                    st.write(f"Author: {book['Book-Author']}")
                    st.image(book['Image-URL-M'], use_column_width=True)
                    # Add Amazon button
                    book_title_encoded = urllib.parse.quote(book['Book-Title'])
                    amazon_url = f"https://www.amazon.com/s?k={book_title_encoded}"
                    st.write(f"[Buy on Amazon]({amazon_url})", unsafe_allow_html=True)
            with col2:
                if i + 1 < len(random_books):
                    book = random_books.iloc[i + 1]
                    st.subheader(book['Book-Title'])
                    st.write(f"Author: {book['Book-Author']}")
                    st.image(book['Image-URL-M'], use_column_width=True)
                    # Add Amazon button
                    book_title_encoded = urllib.parse.quote(book['Book-Title'])
                    amazon_url = f"https://www.amazon.com/s?k={book_title_encoded}"
                    st.write(f"[Buy on Amazon]({amazon_url})", unsafe_allow_html=True)

# Feedback mechanism
if option == "Send Feedback":
    st.title("Send Feedback")
    feedback_text = st.text_area("Please share your feedback here:", height=200)
    submit_feedback = st.button("Submit Feedback")

    # If submit button is clicked, process feedback
    if submit_feedback:
        # Here you can add code to process and store the feedback (e.g., send it to a database)
        # For now, just display a thank you message
        st.success("Thank you for your feedback! We appreciate your input.")
