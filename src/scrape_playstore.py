import pandas as pd
from google_play_scraper import reviews, Sort
from db_connection import supabase


def fetch_reviews(count=2000):
    """
    Fetch reviews from Google Play Store
    """
    result, _ = reviews(
        'com.grofers.customerapp',  # Blinkit app ID
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=count
    )

    df = pd.DataFrame(result)

    # Select and rename columns
    df = df[['content', 'score', 'at']]
    df.columns = ['review', 'rating', 'date']

    df['source'] = 'google_play'

    return df


def prepare_data(df):
    """
    Convert dataframe to Supabase-compatible format
    """
    df['date'] = df['date'].astype(str)  # avoid timestamp issues
    return df.to_dict(orient='records')


def insert_batches(data, batch_size=100):
    """
    Insert data into Supabase in batches
    """
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]

        response = supabase.table("reviews").insert(batch).execute()

        print(f"Inserted batch {i // batch_size + 1}")


if __name__ == "__main__":
    print("🚀 Fetching Blinkit reviews from Google Play...")

    df = fetch_reviews(count=2000)
    print(f"Fetched {len(df)} reviews")

    data = prepare_data(df)

    print("📤 Inserting into Supabase...")
    insert_batches(data)

    print("✅ Done!")