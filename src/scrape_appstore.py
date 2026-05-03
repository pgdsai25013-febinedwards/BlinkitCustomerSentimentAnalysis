import requests
import pandas as pd
from db_connection import supabase
import time


def fetch_reviews(app_id="960335206", country="in", how_many=500, retries=3):
    all_reviews = []
    max_pages = min((how_many // 50) + 1, 10)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}...")
            all_reviews = []

            for page in range(1, max_pages + 1):
                url = (
                    f"https://itunes.apple.com/{country}/rss/customerreviews/"
                    f"page={page}/id={app_id}/sortby=mostrecent/json"
                )

                resp = requests.get(url, headers=headers, timeout=15)
                resp.raise_for_status()
                data = resp.json()

                entries = data.get("feed", {}).get("entry", [])

                if page == 1 and entries:
                    entries = entries[1:]  # first entry on page 1 is app metadata, skip it

                if not entries:
                    print(f"  No more reviews at page {page}, stopping.")
                    break

                for entry in entries:
                    all_reviews.append({
                        "review":  entry.get("content", {}).get("label", ""),
                        "rating":  int(entry.get("im:rating", {}).get("label", 0)),
                        "date":    entry.get("updated", {}).get("label", "")[:10],
                    })

                print(f"  Page {page}: {len(entries)} reviews (total: {len(all_reviews)})")
                time.sleep(0.5)

                if len(all_reviews) >= how_many:
                    break

            if all_reviews:
                df = pd.DataFrame(all_reviews[:how_many])
                df["source"] = "app_store"
                return df

            print("⚠️ No reviews fetched, retrying...")
            time.sleep(3)

        except Exception as e:
            print(f"❌ Error on attempt {attempt + 1}: {e}")
            time.sleep(3)

    print("❌ All attempts failed")
    return pd.DataFrame()


def prepare_data(df):
    if df.empty:
        return []

    df["date"] = pd.to_datetime(df["date"], errors="coerce").astype(str)
    df = df[["review", "rating", "date", "source"]]  # only columns that exist in Supabase
    df = df.dropna(subset=["review", "rating"])
    df["rating"] = df["rating"].astype(int)

    return df.to_dict(orient="records")


def insert_batches(data, batch_size=100):
    if not data:
        print("⚠️ No data to insert")
        return

    total_batches = (len(data) + batch_size - 1) // batch_size

    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        try:
            supabase.table("reviews").insert(batch).execute()
            print(f"✅ Inserted batch {i // batch_size + 1}/{total_batches} ({len(batch)} records)")
        except Exception as e:
            print(f"❌ Failed to insert batch {i // batch_size + 1}: {e}")


if __name__ == "__main__":
    print("🍏 Fetching Blinkit reviews from App Store...")

    df = fetch_reviews(app_id="960335206", country="in", how_many=500)

    if df.empty:
        print("❌ No reviews fetched. Exiting.")
        exit(1)

    print(f"\n📊 Fetched {len(df)} reviews")
    print(df[["rating", "date", "review"]].head(3))

    data = prepare_data(df)
    print(f"\n📤 Inserting {len(data)} records into Supabase...")

    insert_batches(data)
    print("✅ Done!")