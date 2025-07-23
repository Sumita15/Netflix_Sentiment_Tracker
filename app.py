import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import random
import itertools
import nltk

nltk.download('punkt')  # Required for TextBlob to work


# Set page title and layout
st.set_page_config(page_title="Netflix Review Sentiment", layout="wide")
st.title("Netflix Review Sentiment Analyzer")
st.markdown("Analyze IMDb reviews for Netflix shows and movies. Upload a dataset or type your own review.")

# Fake Netflix show/movie titles
fake_titles = [
    "Stranger Things", "The Crown", "Money Heist", "Breaking Bad", "Wednesday",
    "The Witcher", "Dark", "Narcos", "Black Mirror", "You", "Ozark",
    "Bridgerton", "The Sandman", "Sweet Tooth", "The Night Agent", "Beef"
]

# Upload dataset
st.subheader("Upload IMDb Review Dataset")
uploaded_file = st.file_uploader("Upload CSV with: 'title', 'year', 'review', 'sentiment' columns", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using default IMDb dataset.")
    import zipfile

    with zipfile.ZipFile("IMDB Dataset.csv.zip", 'r') as zip_ref:
        with zip_ref.open("IMDB Dataset.csv") as file:
           df = pd.read_csv(file)

# Capitalize sentiments & filter only Positive/Negative
df["sentiment"] = df["sentiment"].str.capitalize()
df = df[df["sentiment"].isin(["Positive", "Negative"])]

# Add balanced fake titles
repeated_titles = list(itertools.islice(itertools.cycle(fake_titles), len(df)))
random.shuffle(repeated_titles)
df["title"] = repeated_titles

# Optional: add fake years
years = list(range(2015, 2024))
df["year"] = [random.choice(years) for _ in range(len(df))]

# Try Your Own Review
st.subheader("Try Sentiment Analysis Yourself")
col1, col2 = st.columns([1, 3])
with col1:
    manual_title = st.selectbox("Select a Show", fake_titles)
with col2:
    user_review = st.text_area("Write your review here")

if st.button("Analyze Sentiment"):
    if user_review.strip():
        blob = TextBlob(user_review)
        polarity = blob.sentiment.polarity
        sentiment = (
            "Positive" if polarity > 0 else
            "Negative" if polarity < 0 else
            "Neutral"
        )
        st.success(f"{manual_title} → Sentiment: {sentiment} (Polarity: {polarity:.2f})")
    else:
        st.warning("Please enter a review to analyze.")

# Dataset Preview
if "review" not in df.columns or "sentiment" not in df.columns:
    st.error("Dataset must contain 'review' and 'sentiment' columns.")
else:
    st.success("Dataset loaded successfully.")
    st.write("Preview of data:")
    st.dataframe(df.head(10))

    # Overall Sentiment
    st.subheader("Overall Sentiment Distribution")
    sentiment_counts = df["sentiment"].value_counts()
    st.bar_chart(sentiment_counts)

    # Pie Chart per Show
    st.subheader("Sentiment Pie Chart for a Specific Show")
    selected_show = st.selectbox("Choose a Show", df["title"].unique())
    show_data = df[df["title"] == selected_show]
    show_sentiments = show_data["sentiment"].value_counts()

    if not show_data.empty:
        fig1, ax1 = plt.subplots()
        ax1.pie(show_sentiments, labels=show_sentiments.index, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)
    else:
        st.warning("No reviews available for the selected show.")

    # Compare Two Shows
    st.subheader("Compare Sentiments Between Two Shows")
    all_titles = df["title"].unique().tolist()
    show1 = st.selectbox("Select Show 1", all_titles, key="compare1")
    show2_options = [t for t in all_titles if t != show1]
    show2 = st.selectbox("Select Show 2", show2_options, key="compare2")

    show1_data = df[df["title"] == show1]
    show2_data = df[df["title"] == show2]

    if show1_data.empty or show2_data.empty:
        st.warning("One of the selected shows has no reviews to compare.")
    else:
        sentiment_order = ["Positive", "Negative"]

        show1_counts = show1_data["sentiment"].value_counts(normalize=True) * 100
        show2_counts = show2_data["sentiment"].value_counts(normalize=True) * 100

        show1_vals = [show1_counts.get(s, 0) for s in sentiment_order]
        show2_vals = [show2_counts.get(s, 0) for s in sentiment_order]

        x = range(len(sentiment_order))
        width = 0.35

        fig2, ax2 = plt.subplots()
        ax2.bar([i - width/2 for i in x], show1_vals, width, label=show1)
        ax2.bar([i + width/2 for i in x], show2_vals, width, label=show2)

        ax2.set_ylabel("Percentage")
        ax2.set_title("Sentiment Comparison Between Shows")
        ax2.set_xticks(x)
        ax2.set_xticklabels(sentiment_order)
        ax2.legend()
        ax2.set_ylim(0, 100)
        st.pyplot(fig2)
