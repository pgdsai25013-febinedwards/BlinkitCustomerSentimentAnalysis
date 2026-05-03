import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from db_connection import supabase

os.makedirs("outputs/charts", exist_ok=True)  # ✅ moved to top

TOPIC_LABELS = {
    0: "Delivery Experience",
    1: "Positive App Experience",
    2: "Customer Support & Refunds",
    3: "Product Quality",
    4: "Hinglish / Mixed Reviews"
}

HINGLISH_STOPWORDS = {
    "nahi", "nhi", "nai", "hai", "tha", "thi", "kar", "kr",
    "karo", "karna", "ka", "ki", "ho", "hota", "hua", "raha",
    "rah", "h", "aap", "se", "ke", "ko", "bhi", "mera", "mere",
    "ek", "app", "blinkit"  # also remove app name from wordcloud
}


# -------------------------------
# FETCH DATA
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

    df = pd.DataFrame(all_data)
    print(f"  Loaded {len(df)} rows")
    return df


# -------------------------------
# SENTIMENT DISTRIBUTION
# -------------------------------
def sentiment_distribution(df):
    if "sentiment" not in df.columns:
        print("⚠️ Sentiment column not found")
        return

    order = ["Positive", "Neutral", "Negative"]
    colors = ["#2ecc71", "#95a5a6", "#e74c3c"]
    counts = df["sentiment"].value_counts().reindex(order, fill_value=0)

    plt.figure(figsize=(7, 5))
    ax = counts.plot(kind="bar", color=colors)
    for i, v in enumerate(counts):
        ax.text(i, v + 10, str(v), ha="center", fontsize=11)

    plt.title("Sentiment Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("outputs/charts/sentiment_distribution.png", dpi=150)
    plt.close()
    print("  ✅ sentiment_distribution.png")


# -------------------------------
# SENTIMENT BY SOURCE
# -------------------------------
def sentiment_by_source(df):
    if "sentiment" not in df.columns or "source" not in df.columns:
        print("⚠️ Required columns missing")
        return

    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x="source", hue="sentiment",
                       hue_order=["Positive", "Neutral", "Negative"],
                       palette={"Positive": "#2ecc71", "Neutral": "#95a5a6", "Negative": "#e74c3c"})

    for p in ax.patches:
        height = int(p.get_height())
        if height > 0:
            ax.annotate(str(height),
                        (p.get_x() + p.get_width() / 2, height + 5),
                        ha="center", va="bottom", fontsize=9)

    plt.title("Sentiment by Source", fontsize=14, fontweight="bold")
    plt.xlabel("Source")
    plt.ylabel("Count")
    plt.legend(title="Sentiment")
    plt.tight_layout()
    plt.savefig("outputs/charts/sentiment_by_source.png", dpi=150)
    plt.close()
    print("  ✅ sentiment_by_source.png")


# -------------------------------
# RATING DISTRIBUTION
# -------------------------------
def rating_distribution(df):
    if "rating" not in df.columns:
        print("⚠️ Rating column not found")
        return

    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="rating", hue="source",
                  palette={"app_store": "#3498db", "google_play": "#e67e22"})

    plt.title("Rating Distribution by Source", fontsize=14, fontweight="bold")
    plt.xlabel("Star Rating")
    plt.ylabel("Count")
    plt.legend(title="Source")
    plt.tight_layout()
    plt.savefig("outputs/charts/rating_distribution.png", dpi=150)
    plt.close()
    print("  ✅ rating_distribution.png")


# -------------------------------
# TOPIC DISTRIBUTION
# -------------------------------
def topic_distribution(df):
    if "topic" not in df.columns:
        print("⚠️ Topic column not found")
        return

    df["topic_label"] = df["topic"].map(TOPIC_LABELS)
    order = list(TOPIC_LABELS.values())
    counts = df["topic_label"].value_counts().reindex(order, fill_value=0)

    plt.figure(figsize=(9, 5))
    ax = counts.plot(kind="bar", color="#8e44ad")
    for i, v in enumerate(counts):
        ax.text(i, v + 5, str(v), ha="center", fontsize=10)

    plt.title("Topic Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Topic")
    plt.ylabel("Count")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig("outputs/charts/topic_distribution.png", dpi=150)
    plt.close()
    print("  ✅ topic_distribution.png")


# -------------------------------
# SENTIMENT VS RATING HEATMAP
# -------------------------------
def sentiment_rating_heatmap(df):
    if "sentiment" not in df.columns or "rating" not in df.columns:
        print("⚠️ Required columns missing")
        return

    pivot = df.groupby(["rating", "sentiment"]).size().unstack(fill_value=0)
    pivot = pivot.reindex(columns=["Positive", "Neutral", "Negative"], fill_value=0)

    plt.figure(figsize=(7, 5))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd")
    plt.title("Sentiment vs Star Rating", fontsize=14, fontweight="bold")
    plt.xlabel("Sentiment")
    plt.ylabel("Star Rating")
    plt.tight_layout()
    plt.savefig("outputs/charts/sentiment_vs_rating.png", dpi=150)
    plt.close()
    print("  ✅ sentiment_vs_rating.png")


# -------------------------------
# WORD CLOUD
# -------------------------------
def word_cloud(df):
    if "cleaned" not in df.columns:
        print("⚠️ Cleaned column not found")
        return

    text = " ".join(df["cleaned"].dropna())
    if not text.strip():
        print("⚠️ No text available for word cloud")
        return

    stopwords = set(STOPWORDS)
    stopwords.update(HINGLISH_STOPWORDS)  # ✅ only remove noise, not meaningful words

    wc = WordCloud(width=1200, height=600, background_color="white",
                   colormap="tab10", max_words=150,
                   stopwords=stopwords).generate(text)

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud — All Reviews", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("outputs/charts/wordcloud.png", dpi=150)
    plt.close()
    print("  ✅ wordcloud.png")


# -------------------------------
# WORD CLOUD PER TOPIC
# -------------------------------
def word_cloud_per_topic(df):
    if "topic" not in df.columns or "cleaned" not in df.columns:
        print("⚠️ Required columns missing")
        return

    stopwords = set(STOPWORDS)
    stopwords.update(HINGLISH_STOPWORDS)

    for topic_id, label in TOPIC_LABELS.items():
        subset = df[df["topic"] == topic_id]["cleaned"].dropna()
        if subset.empty:
            continue

        text = " ".join(subset)
        wc = WordCloud(width=800, height=400, background_color="white",
                       max_words=80, stopwords=stopwords).generate(text)

        plt.figure(figsize=(9, 4))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Topic {topic_id}: {label}", fontsize=13, fontweight="bold")
        plt.tight_layout()
        plt.savefig(f"outputs/charts/wordcloud_topic_{topic_id}.png", dpi=150)
        plt.close()
        print(f"  ✅ wordcloud_topic_{topic_id}.png")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    print("📊 Fetching data...")
    df = fetch_data()

    print("\n📈 Generating charts...")
    sentiment_distribution(df)
    sentiment_by_source(df)
    rating_distribution(df)
    topic_distribution(df)
    sentiment_rating_heatmap(df)
    word_cloud(df)
    word_cloud_per_topic(df)

    print("\n✅ All charts saved to outputs/charts/")