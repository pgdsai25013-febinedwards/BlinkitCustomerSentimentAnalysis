from db_connection import supabase
import pandas as pd


def fetch_all_data(table_name="reviews", batch_size=1000):
    """
    Fetch all rows from Supabase using pagination
    """
    all_data = []
    start = 0

    while True:
        response = supabase.table(table_name) \
            .select("*") \
            .range(start, start + batch_size - 1) \
            .execute()

        data = response.data

        if not data:
            break

        all_data.extend(data)
        start += batch_size

        print(f"Fetched {len(all_data)} rows so far...")

    return pd.DataFrame(all_data)


def run_checks(df):
    """
    Perform basic data validation checks
    """
    print("\n================ DATA SUMMARY ================\n")

    print("Total rows:", len(df))

    print("\nSource distribution:")
    print(df['source'].value_counts())

    print("\nRating summary:")
    print(df['rating'].describe())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nSample data:")
    print(df.head(5))


if __name__ == "__main__":
    print("🔍 Fetching data from Supabase...\n")

    df = fetch_all_data()

    run_checks(df)

    print("\n✅ Data check complete!")