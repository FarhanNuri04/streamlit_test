
import streamlit as st
import requests
import pandas as pd
import altair as alt
from textblob import TextBlob

# ========== Streamlit UI Setup ==========
st.set_page_config(page_title="Movie Explorer", layout="centered")

# ========== Background Styling ==========
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: white;
        padding: 2rem;
        border-radius: 15px;
    }

    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }

    h1, h2, h3, h4, h5, h6, .stMarkdown, label {
        color: #ffffff !important;
    }

    input, textarea, select {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    button[kind="primary"] {
        color: #fff !important;
        background-color: #1e88e5 !important;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ========== State management ==========
if "searched" not in st.session_state:
    st.session_state["searched"] = False
if "search_result" not in st.session_state:
    st.session_state["search_result"] = None

# ========== App Title ==========
st.title("  :rainbow[Movie Explorer App]")
st.markdown("Search movies by title or browse categories. Explore storyline, stats, trailer, and submit a review.")

# ========== User Name ==========
user_name = st.text_input("Enter your name:", "Guest")
st.markdown(f"  Hello, {user_name}! Let's explore some movies.")

# ========== TMDb API ==========
API_KEY = "4f658b3a4df357c0e36dea39fe745497"  # Replace with your own TMDb API key

# ========== Movie Search & Year ==========
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Enter a movie title:", "")
with col2:
    year_filter = st.text_input("Year (optional):", "")

# ========== Category Dropdown ==========
st.markdown("##   Browse by Category")
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

def get_movie_details(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    return requests.get(url).json()

def get_movie_credits(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
    return requests.get(url).json()

def get_movie_trailer(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
    videos = requests.get(url).json().get("results", [])
    for video in videos:
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

def get_movies_by_category(category_key, api_key):
    url = f"https://api.themoviedb.org/3/movie/{category_key}?api_key={api_key}&language=en-US&page=1"
    return requests.get(url).json().get("results", [])

# ========== Auto-correct Logic ==========
def autocorrect(text):
    corrected = str(TextBlob(text).correct())
    return corrected if corrected.lower() != text.lower() else text

# ========== Handle Category Browse ==========
if query.strip() == "":
    st.markdown(f"### 🎞 {category} Movies")
    movies = get_movies_by_category(category_map[category], API_KEY)
    cols = st.columns(3)
    for i, movie in enumerate(movies[:9]):
        with cols[i % 3]:
            st.markdown(f"{movie['title']}")
            if movie.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w200{movie['poster_path']}", use_container_width=True)
            st.caption(movie.get("overview", "No overview available."))
else:
    corrected_query = autocorrect(query)
    if st.button("Search Movie"):
        search_result = search_movie(corrected_query, API_KEY, year_filter)
        st.session_state["searched"] = True
        st.session_state["search_result"] = search_result

if st.session_state["searched"] and st.session_state["search_result"]:
    search_result = st.session_state["search_result"]

    if "results" not in search_result or len(search_result["results"]) == 0:
        st.error("  No movie found with that title.")
    else:
        movie = search_result["results"][0]
        movie_id = movie["id"]
        details = get_movie_details(movie_id, API_KEY)
        credits = get_movie_credits(movie_id, API_KEY)
        trailer_url = get_movie_trailer(movie_id, API_KEY)

        director = next((m["name"] for m in credits.get("crew", []) if m["job"] == "Director"), "Unknown")
        cast_list = credits.get("cast", [])
        top_cast = ", ".join([actor["name"] for actor in cast_list[:3]]) if cast_list else "N/A"

        st.subheader(f"🎞 {details['title']} ({details.get('release_date', '')[:4]})")
        if details.get("poster_path"):
            st.image(f"https://image.tmdb.org/t/p/w500{details['poster_path']}")
        st.markdown(f"Storyline: {details.get('overview', 'No overview available.')}")
        st.markdown(f"Director: {director}")
        st.markdown(f"Stars: {top_cast}")
        st.markdown(f"Runtime: {details.get('runtime', 'N/A')} mins")
        st.markdown(f"Vote Average: {details['vote_average']}")
        st.markdown(f"Total Votes: {details['vote_count']}")

        if trailer_url:
            st.subheader("  Watch Trailer")
            st.video(trailer_url)
        else:
            st.info("No trailer available.")

        vote_data = pd.DataFrame({
            "Metric": ["Average Rating", "Vote Count"],
            "Value": [details["vote_average"], details["vote_count"]]
        })
        st.subheader("  Rating and Vote Count")
        st.altair_chart(
            alt.Chart(vote_data).mark_bar().encode(
                x="Metric",
                y="Value",
                color=alt.Color("Metric", scale=alt.Scale(scheme='dark2')),
                tooltip=["Metric", "Value"]
            ).properties(width=600)
        )

        genres = [g["name"] for g in details["genres"]]
        genre_df = pd.DataFrame({"Genre": genres, "Count": [1]*len(genres)})
        st.subheader("  Genre Breakdown")
        st.altair_chart(
            alt.Chart(genre_df).mark_arc().encode(
                theta="Count",
                color=alt.Color("Genre", scale=alt.Scale(scheme='tableau10')),
                tooltip="Genre"
            )
        )

        st.markdown("---")
        st.subheader("  Your Review")
        with st.form("review_form"):
            user_review = st.text_area("Write your review here (optional):", "")

            star_rating = st.slider("Rate this movie (0 - 5 stars):", 0, 5, 5)

            submitted = st.form_submit_button("Submit Review")
            if submitted:
                st.success("  Thank you for your review!")
                st.markdown(f"  Reviewed by: *{user_name}*")
                st.markdown(f"  Your Rating: *{star_rating} / 5*")
                if user_review.strip():
                    st.markdown(f"  Your Review: *{user_review}*")
                else:
                    st.markdown("No written review provided.")



