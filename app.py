import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

try:
    from src.db_connection import supabase
except ImportError:
    from db_connection import supabase

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Blinkit Dashboard", layout="wide")

st.markdown("""
<style>
.main {background-color: #f7f7f7;}
.kpi {
    background: white;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
.header { font-size: 28px; font-weight: bold; }
.insight-box {
    background: #fff;
    padding: 15px;
    border-left: 5px solid #f1c40f;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TOPIC LABELS
# -------------------------------
TOPIC_LABELS = {
    0: "Delivery Experience",
    1: "Positive App Experience",
    2: "Customer Support & Refunds",
    3: "Product Quality",
    4: "Hinglish / Mixed Reviews"
}

# -------------------------------
# FETCH DATA
# -------------------------------
@st.cache_data
def fetch_data():
    data = []
    start = 0

    while True:
        res = supabase.table("reviews") \
            .select("*") \
            .range(start, start + 999) \
            .execute()

        if not res.data:
            break

        data.extend(res.data)
        start += 1000

    df = pd.DataFrame(data)
    df["topic_label"] = df["topic"].map(TOPIC_LABELS)
    return df


df = fetch_data()

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<div class='header'>🟡 Blinkit Customer Analytics Dashboard</div>", unsafe_allow_html=True)
st.caption("Sentiment Analysis + Topic Modeling | Google Play & App Store")
st.divider()

# -------------------------------
# KPI SECTION
# -------------------------------
total = len(df)

if total > 0 and "sentiment" in df.columns:
    pos = (df["sentiment"] == "Positive").sum()
    neg = (df["sentiment"] == "Negative").sum()
    neu = (df["sentiment"] == "Neutral").sum()

    col1, col2, col3, col4 = st.columns(4)

    def card(col, title, value):
        with col:
            st.markdown(f"<div class='kpi'><h4>{title}</h4><h2>{value}</h2></div>",
                        unsafe_allow_html=True)

    card(col1, "Total Reviews", total)
    card(col2, "Positive %", f"{(pos/total)*100:.1f}%")
    card(col3, "Negative %", f"{(neg/total)*100:.1f}%")
    card(col4, "Neutral %",  f"{(neu/total)*100:.1f}%")

st.divider()

# -------------------------------
# FILTER
# -------------------------------
source_options = ["All"] + sorted(df["source"].unique().tolist())
source = st.selectbox("Filter by Source", source_options)

filtered_df = df if source == "All" else df[df["source"] == source]

# -------------------------------
# SENTIMENT DISTRIBUTION
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Sentiment Distribution")
    order = ["Positive", "Neutral", "Negative"]
    counts = filtered_df["sentiment"].value_counts().reindex(order, fill_value=0)
    st.bar_chart(counts)

with col2:
    st.subheader("📊 Sentiment by Source")
    pivot = pd.crosstab(filtered_df["source"], filtered_df["sentiment"])
    pivot = pivot.reindex(columns=["Positive", "Neutral", "Negative"], fill_value=0)
    st.bar_chart(pivot)

# -------------------------------
# RATING DISTRIBUTION
# -------------------------------
st.subheader("⭐ Rating Distribution by Source")
rating_pivot = pd.crosstab(filtered_df["rating"], filtered_df["source"])
st.bar_chart(rating_pivot)

# -------------------------------
# TOPIC DISTRIBUTION
# -------------------------------
st.subheader("🧠 Topic Distribution")
topic_counts = filtered_df["topic_label"].value_counts()
st.bar_chart(topic_counts)

# -------------------------------
# SENTIMENT VS RATING HEATMAP
# -------------------------------
st.subheader("🔥 Sentiment vs Star Rating")
pivot2 = filtered_df.groupby(["rating", "sentiment"]).size().unstack(fill_value=0)
pivot2 = pivot2.reindex(columns=["Positive", "Neutral", "Negative"], fill_value=0)

fig, ax = plt.subplots(figsize=(7, 4))
sns.heatmap(pivot2, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
ax.set_title("Sentiment vs Rating")
st.pyplot(fig)
plt.close()

# -------------------------------
# DYNAMIC INSIGHTS
# -------------------------------
st.subheader("📌 Key Insights")

pos_pct = (pos/total*100) if total > 0 else 0
neg_pct = (neg/total*100) if total > 0 else 0
top_topic = df["topic_label"].value_counts().idxmax() if "topic_label" in df.columns else "N/A"

st.markdown(f"""
<div class='insight-box'>
✔ Overall sentiment is <b>{pos_pct:.1f}% Positive</b> and <b>{neg_pct:.1f}% Negative</b> across {total} reviews
</div>
<div class='insight-box'>
✔ Most discussed topic: <b>{top_topic}</b>
</div>
<div class='insight-box'>
✔ Google Play reviews tend to be more polarized; App Store reviews are more balanced
</div>
<div class='insight-box'>
✔ Key pain points: pricing & extra charges, product quality, refund & support delays
</div>
""", unsafe_allow_html=True)

# -------------------------------
# RECOMMENDATIONS
# -------------------------------
st.subheader("🚀 Recommendations")

st.markdown("""
<div class='insight-box'>🔧 Improve refund processing speed to reduce negative sentiment</div>
<div class='insight-box'>📦 Strengthen product quality checks to reduce complaints</div>
<div class='insight-box'>💬 Enhance customer support responsiveness</div>
<div class='insight-box'>💰 Increase transparency in pricing and charges</div>
""", unsafe_allow_html=True)

# -------------------------------
# SAMPLE REVIEWS
# -------------------------------
st.subheader("📄 Sample Reviews")
st.dataframe(
    filtered_df[["review", "rating", "sentiment", "topic_label", "source"]].head(20),
    use_container_width=True
)