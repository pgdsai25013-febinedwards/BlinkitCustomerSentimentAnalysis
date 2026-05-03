import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from db_connection import supabase


# -------------------------------
# FETCH DATA
# -------------------------------
def fetch_data():
    all_data = []
    start = 0
    batch_size = 1000

    while True:
        response = supabase.table("reviews") \
            .select("id, cleaned") \
            .range(start, start + batch_size - 1) \
            .execute()

        data = response.data

        if not data:
            break

        all_data.extend(data)
        start += batch_size

    return pd.DataFrame(all_data)


# -------------------------------
# TRAIN LDA MODEL
# -------------------------------
def train_lda(df, n_topics=5):
    vectorizer = CountVectorizer(
        max_df=0.9,
        min_df=10,
        stop_words="english"
    )

    X = vectorizer.fit_transform(df["cleaned"])

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42
    )

    lda.fit(X)

    return lda, vectorizer, X


# -------------------------------
# PRINT TOPICS
# -------------------------------
def display_topics(lda, vectorizer, n_words=10):
    words = vectorizer.get_feature_names_out()

    print("\n🔍 Topics Discovered:\n")

    for i, topic in enumerate(lda.components_):
        top_words = [words[i] for i in topic.argsort()[-n_words:]]
        print(f"Topic {i}: {', '.join(top_words)}")


# -------------------------------
# ASSIGN TOPIC TO EACH REVIEW
# -------------------------------
def assign_topics(lda, X, df):
    topic_values = lda.transform(X)
    df["topic"] = topic_values.argmax(axis=1)
    return df


# -------------------------------
# UPDATE DATABASE
# -------------------------------
def update_topics(df):
    for _, row in df.iterrows():
        supabase.table("reviews") \
            .update({"topic": int(row["topic"])}) \
            .eq("id", row["id"]) \
            .execute()


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    print("📥 Fetching cleaned data...")

    df = fetch_data()

    print(f"Total rows: {len(df)}")

    print("🧠 Training LDA model...")

    lda, vectorizer, X = train_lda(df)

    display_topics(lda, vectorizer)

    print("🏷 Assigning topics...")

    df = assign_topics(lda, X, df)

    print("📤 Updating database...")

    update_topics(df)

    print("✅ Topic modeling complete!")