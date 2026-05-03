import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# ---- TEST BLOCK ----
if __name__ == "__main__":
    print("URL:", url)
    print("KEY (first 10 chars):", key[:10])

    # Read test
    response = supabase.table("reviews").select("*").limit(5).execute()
    print("DB Response:", response)

    # Insert test
    test_data = {
        "review": "Test review from pipeline",
        "rating": 5,
        "source": "test"
    }

    insert_response = supabase.table("reviews").insert(test_data).execute()
    print("Insert Response:", insert_response)