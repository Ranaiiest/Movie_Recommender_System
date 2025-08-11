# 🎬 Movie Recommendation System

A content-based movie recommendation system built using NLP techniques and cosine similarity, deployed with Streamlit.

## ✨ Features
- Search for a movie and get top 5 similar movie recommendations.
- Uses **cosine similarity** on movie feature vectors for recommendations.
- Dataset preprocessing and feature engineering for better accuracy.
- Fast and interactive UI built with Streamlit.

## 🛠 Tech Stack
- **Python** (pandas, numpy, scikit-learn)
- **Streamlit** (for UI)
- **NLP** (TF-IDF Vectorization)
- **Cosine Similarity** (from scikit-learn)
- Dataset: TMDB or similar public movie dataset

## 🌐 Live Demo
[Click here to view the app](https://movie-recommender-system-aynx.onrender.com/)

## 🚀 How to Run Locally

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/movie-recommendation-system.git
    cd movie-recommendation-system
    ```

2. **Create a virtual environment & activate it**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit app**
    ```bash
    streamlit run app.py
    ```
## 📂 Project Structure
```plaintext
movie-recommendation-system/
│-- app.py                 # Main Streamlit app
│-- preprocessing.py       # Data preprocessing & similarity matrix generation
│-- movies.csv             # Dataset
│-- similarity.pkl         # Precomputed similarity matrix
│-- requirements.txt       # Python dependencies
│-- README.md              # Project documentation


