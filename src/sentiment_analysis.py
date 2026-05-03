import pandas as pd
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from db_connection import supabase


# -------------------------------
# TEXT CLEANING
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)     # remove links
    text = re.sub(r"[^a-z\s]", "", text)    # remove special chars
    text = re.sub(r"\s+", " ", text)        # remove extra spaces
    return text.strip()


# -------------------------------
# FETCH DATA FROM SUPABASE
# -------------------------------
def fetch_data():
    all_data = []
    start = 0
    batch_size = 1000

    while True:
        response = supabase.table("reviews") \
            .select("*") \
            .range(start, start + batch_size - 1) \
            .execute()

        data = response.data

        if not data:
            break

        all_data.extend(data)
        start += batch_size

    return pd.DataFrame(all_data)


# -------------------------------
# APPLY SENTIMENT
# -------------------------------
def apply_sentiment(df):
    sia = SentimentIntensityAnalyzer()

    df["cleaned"] = df["review"].apply(clean_text)

    df["sentiment_score"] = df["cleaned"].apply(
        lambda x: sia.polarity_scores(x)["compound"]
    )

    def label(score):
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        else:
            return "Neutral"

    df["sentiment"] = df["sentiment_score"].apply(label)

    return df


# -------------------------------
# UPDATE DATABASE
# -------------------------------
def update_sentiment(df):
    for _, row in df.iterrows():
        supabase.table("reviews") \
            .update({
                "cleaned": row["cleaned"],
                "sentiment": row["sentiment"]
            }) \
            .eq("id", row["id"]) \
            .execute()


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    print("📥 Fetching data...")

    df = fetch_data()

    print(f"Total rows: {len(df)}")

    print("🧹 Cleaning + Sentiment Analysis...")

    df = apply_sentiment(df)

    print("📤 Updating database...")

    update_sentiment(df)

    print("✅ Sentiment analysis complete!")