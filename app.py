import streamlit as st
import pandas as pd
import requests
import random
import urllib.parse
import time

# -------------------------------
# ⚙️ App Configuration
# -------------------------------
st.set_page_config(page_title="Movie Recommender System", layout="wide")

TMDB_API_KEY = "d068cae9e89fb80559c42bdf229b648d"
OMDB_API_KEY = "demo"  # you can get a free one from http://www.omdbapi.com/apikey.aspx

# -------------------------------
# 🧠 Load Data
# -------------------------------
@st.cache_data
def load_data():
    movies = pd.read_csv("movies_data.csv")
    recs = pd.read_csv("recommendations.csv")
    movies["title"] = movies["title"].astype(str)
    return movies, recs

movies, recommendations_df = load_data()


@st.cache_resource
def load_recommendations_dict(df):
    rec_dict = {}
    for _, row in df.iterrows():
        rec_dict[row["movie"]] = [x for x in row[1:].tolist() if isinstance(x, str)]
    return rec_dict


recommendation_dict = load_recommendations_dict(recommendations_df)

# -------------------------------
# 🎬 Movie Detail Fetchers
# -------------------------------
@st.cache_data(show_spinner=False)
def fetch_trailer(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
        data = requests.get(url, timeout=3).json()
        for v in data.get("results", []):
            if v.get("site") == "YouTube" and v.get("type") == "Trailer":
                return f"https://www.youtube.com/watch?v={v.get('key')}"
    except Exception:
        pass
    return None


@st.cache_data(show_spinner=False)
def fetch_movie_details(title):
    """Fetch details from TMDB, fallback to OMDb if TMDB fails."""
    placeholder_poster = "https://via.placeholder.com/300x450?text=No+Image"

    # Clean title for TMDB search
    clean_title = title.split("(")[0].replace("-", " ").replace(":", "").strip()
    encoded = urllib.parse.quote(clean_title)

    def try_request(url):
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                return r.json()
        except Exception:
            time.sleep(0.3)
        return None

    # Multiple TMDB queries (try exact, cleaned, with year)
    urls = [
        f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={encoded}",
        f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={urllib.parse.quote(title)}",
        f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={urllib.parse.quote(clean_title + ' 2006')}"
    ]

    data = None
    for u in urls:
        data = try_request(u)
        if data and data.get("results"):
            break

    # ✅ If TMDB found results
    if data and data.get("results"):
        movie = data["results"][0]
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else placeholder_poster
        overview = movie.get("overview", "No overview available.")
        release_date = movie.get("release_date", "N/A")
        rating = movie.get("vote_average", "N/A")
        movie_id = movie.get("id")
        trailer = fetch_trailer(movie_id) if movie_id else None
        return poster_url, overview, release_date, rating, trailer

    # ❌ TMDB failed — fallback to OMDb
    omdb_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={urllib.parse.quote(clean_title)}"
    data = try_request(omdb_url)

    if data and data.get("Response") == "True":
        poster_url = data.get("Poster", placeholder_poster)
        overview = data.get("Plot", "No overview available.")
        release_date = data.get("Year", "N/A")
        rating = data.get("imdbRating", "N/A")
        trailer = None
        return poster_url, overview, release_date, rating, trailer

    # Still no info — return placeholders
    return placeholder_poster, "No overview available.", "N/A", "N/A", None


# -------------------------------
# 🎯 Recommendation Logic
# -------------------------------
def recommend(movie, count):
    recs = recommendation_dict.get(movie, [])
    return recs[:count]


# -------------------------------
# 🧱 Streamlit UI
# -------------------------------
st.markdown(
    "<h1 style='text-align:center;color:#FFB000;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:gray;'>Powered by Streamlit • TMDB & OMDb APIs • Scikit-Learn NLP</p>",
    unsafe_allow_html=True,
)

# Sidebar slider
st.sidebar.header("🎛️ Options")
num_recs = st.sidebar.slider("Number of Recommendations", min_value=1, max_value=5, value=5)

# Search box
st.subheader("Search Movie")
selected_movie = st.selectbox(
    "🎥 Type or Select a Movie Name",
    options=sorted(movies["title"].tolist()),
    index=None,
    placeholder="Start typing a movie name..."
)

if not selected_movie:
    st.info("👆 Start typing a movie name to get recommendations.")

# -------------------------------
# 🔎 Recommend Button
# -------------------------------
if st.button("🔎 Recommend"):
    if not selected_movie:
        st.warning("Please select a movie first.")
    else:
        with st.spinner("Fetching recommendations..."):
            recs = recommend(selected_movie, num_recs)

        if not recs:
            st.error("No recommendations found for this movie.")
        else:
            st.subheader(f"Top {len(recs)} Movies Similar to '{selected_movie}'")
            cols_count = 1 if len(recs) <= 2 else (2 if len(recs) <= 4 else 3)
            cols = st.columns(cols_count)

            for i, rec in enumerate(recs):
                with cols[i % cols_count]:
                    poster, overview, release_date, rating, trailer = fetch_movie_details(rec)
                    st.markdown(f"### 🎞️ {rec}")
                    st.image(poster, width="stretch")
                    st.markdown(f"**Release Date:** {release_date}")
                    st.markdown(f"**Rating:** ⭐ {rating}")
                    st.markdown(f"**Overview:** {overview[:240]}{'...' if len(overview) > 240 else ''}")
                    if trailer:
                        st.markdown(f"[▶️ Watch Trailer]({trailer})", unsafe_allow_html=True)
                    st.markdown("---")

# -------------------------------
# 🎲 Random Movie Button
# -------------------------------
if st.button("🎲 Suggest a Random Movie"):
    random_movie = random.choice(movies["title"].tolist())
    st.success(f"Randomly selected: **{random_movie}**")

    with st.spinner("Fetching recommendations..."):
        recs = recommend(random_movie, num_recs)

    if recs:
        st.subheader(f"Top {len(recs)} Movies Similar to '{random_movie}'")
        cols_count = 1 if len(recs) <= 2 else (2 if len(recs) <= 4 else 3)
        cols = st.columns(cols_count)

        for i, rec in enumerate(recs):
            with cols[i % cols_count]:
                poster, overview, release_date, rating, trailer = fetch_movie_details(rec)
                st.markdown(f"### 🎞️ {rec}")
                st.image(poster, width="stretch")
                st.markdown(f"**Release Date:** {release_date}")
                st.markdown(f"**Rating:** ⭐ {rating}")
                st.markdown(f"**Overview:** {overview[:240]}{'...' if len(overview) > 240 else ''}")
                if trailer:
                    st.markdown(f"[▶️ Watch Trailer]({trailer})", unsafe_allow_html=True)
                st.markdown("---")
