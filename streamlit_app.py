import streamlit as st
import requests
import pandas as pd
import altair as alt

# ========== Streamlit UI Setup ==========
st.set_page_config(page_title="Movie Explorer", layout="centered")

# ========== Background Styling ==========
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #fc466b, #3f5efb, #00c9ff, #92fe9d);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite;
        color: white;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.7);
        border-radius: 15px;
        padding: 20px;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #ffffff !important;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
""", unsafe_allow_html=True)

# ========== App Title ==========
st.title(":rainbow[Movie Explorer App]")
st.markdown("Search movies by title or browse categories. Explore storyline, stats, trailer, and submit a review.")

# ========== TMDb API ==========
API_KEY = "4f658b3a4df357c0e36dea39fe745497"

# ========== User Name ==========
user_name = st.text_input("Enter your name:", "Guest")
st.markdown(f"Hello, {user_name}! Let's explore some movies.")

# ========== Search Input + Year ==========
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Enter a movie title:", "")
with col2:
    year_filter = st.text_input("Year (optional):", "")

# ========== Category Dropdown ==========
st.markdown("## Browse by Category")
category = st.selectbox("Or select a category:", ["Popular", "Now Playing", "Upcoming", "Top Rated"])
category_map = {
    "Popular": "popular",
    "Now Playing": "now_playing",
    "Upcoming": "upcoming",
    "Top Rated": "top_rated"
}

# ========== TMDb API Functions ==========
def search_movie(query, api_key, year=None):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    if year:
        url += f"&year={year}"
    return requests.get(url).json()

def get_movies_by_category(category_key, api_key):
    url = f"https://api.themoviedb.org/3/movie/{category_key}?api_key={api_key}&language=en-US&page=1"
    return requests.get(url).json().get("results", [])

# ========== Display Results ==========
if query.strip() == "":
    st.markdown(f"### 🎞 {category} Movies")
    movies = get_movies_by_category(category_map[category], API_KEY)
    cols = st.columns(3)
    for i, movie in enumerate(movies[:9]):
        with cols[i % 3]:
            st.markdown(f"**{movie['title']}**")
            if movie.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w200{movie['poster_path']}", use_container_width=True)
            st.caption(movie.get("overview", "No overview available."))
else:
    if st.button("Search Movie"):
        search_result = search_movie(query, API_KEY, year_filter)

        if not search_result.get("results"):
            st.error("No movie found.")
        else:
            st.success(f"Found {len(search_result['results'])} result(s).")
            for movie in search_result["results"][:3]:  # show top 3 results
                st.subheader(movie["title"])
                if movie.get("poster_path"):
                    st.image(f"https://image.tmdb.org/t/p/w300{movie['poster_path']}")
                st.markdown(f"Release Date: {movie.get('release_date', 'N/A')}")
                st.markdown(f"Overview: {movie.get('overview', 'No overview')}")
