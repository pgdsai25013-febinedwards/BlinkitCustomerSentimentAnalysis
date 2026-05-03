# 🟡 Blinkit Customer Sentiment Analysis & Topic Modeling

## 📌 Project Overview
This project performs **Sentiment Analysis and Topic Modeling** on customer reviews of Blinkit (formerly Grofers) using data collected from:

- Google Play Store  
- Apple App Store  

The objective is to extract actionable insights about customer satisfaction, pain points, and improvement areas.

---

## 🎯 Objectives

- Perform sentiment analysis on customer reviews  
- Identify key topics using topic modeling  
- Build an interactive dashboard for visualization  
- Provide business insights and recommendations  

---

## 📊 Dataset

- Total Reviews: ~2500  
- Sources:
  - Google Play Store (~2000)
  - Apple App Store (~500)

---

## ⚙️ Tech Stack

### 🔹 Data Collection
- google-play-scraper
- requests (App Store API)

### 🔹 Data Processing
- pandas
- numpy

### 🔹 NLP
- nltk (VADER Sentiment)
- scikit-learn (TF-IDF + Clustering)

### 🔹 Visualization
- matplotlib
- seaborn
- wordcloud

### 🔹 Database
- Supabase (PostgreSQL)

### 🔹 Dashboard
- Streamlit

---

## 🧠 Methodology

### 1. Data Collection
- Scraped reviews from Play Store and App Store
- Stored data in Supabase database

### 2. Data Cleaning
- Lowercasing, removing noise
- Handling Hinglish words
- Stopword removal (custom + dynamic)

### 3. Sentiment Analysis
- Used VADER (NLTK)
- Classified into:
  - Positive
  - Neutral
  - Negative

### 4. Topic Modeling
- TF-IDF Vectorization
- KMeans clustering
- Topics interpreted as:
  - Delivery Experience
  - Product Quality
  - Pricing & Charges
  - Customer Support
  - App Experience

### 5. Visualization
- Sentiment distribution
- Source-wise comparison
- Topic distribution
- Word cloud

### 6. Dashboard
- Built interactive Streamlit dashboard
- Displays KPIs, charts, insights

---

## 📈 Key Insights

- ~54% reviews are positive, but ~25% are negative  
- Google Play reviews are more polarized  
- Delivery is the most discussed topic  
- Major issues:
  - Pricing & hidden charges  
  - Product quality inconsistencies  
  - Refund delays & support issues  

---

## 🚀 Recommendations

- Improve refund processing speed  
- Enhance product quality checks  
- Improve customer support responsiveness  
- Increase transparency in pricing  

---

## 🌐 Live Dashboard

👉 [Streamlit Dashboard Link] *(Add after deployment)*

---

## 🗂️ Project Structure
CustomerReviewSentiment/
│
├── src/
│ ├── db_connection.py
│ ├── scrape_playstore.py
│ ├── scrape_appstore.py
│ ├── sentiment_analysis.py
│ ├── topic_modeling.py
│ ├── visualization.py
│
├── app.py
├── requirements.txt
├── README.md


---

## 🔧 Installation

```bash
git clone https://github.com/pgdsai25013-febinedwards/BlinkitCustomerSentimentAnalysis.git
cd BlinkitCustomerSentimentAnalysis
pip install -r requirements.txt

▶️ Run Dashboard Locally
streamlit run app.py

🔐 Environment Variables

Create a .env file (for local use):

SUPABASE_URL=your-url
SUPABASE_KEY=your-key

For deployment, use Streamlit Secrets instead.

📌 Future Improvements
Use Transformer models (BERT) for sentiment analysis
Add real-time data pipeline
Improve Hinglish NLP handling
Add advanced dashboard filters

👤 Author
Febin Edwards
PGDSAI – IIM Sirmaur


🔹 Step-by-step Breakdown
1. 📥 Data Ingestion
Google Play Store (scraper)
Apple App Store (API)

👉 Raw, unstructured customer reviews

2. 🗄️ Data Storage
Supabase (PostgreSQL)

👉 Centralized database → scalable + queryable

3. 🧹 Data Processing (ETL)
Cleaning text
Handling Hinglish
Removing stopwords (dynamic + custom)

👉 Converts raw text → usable format

4. 🧠 Modeling Layer
Sentiment Analysis
VADER (lexicon-based)
Topic Modeling
TF-IDF + KMeans

👉 Converts text → structured insights

5. 📊 Visualization Layer
Matplotlib / Seaborn charts
Word clouds
Topic distributions

6. 🌐 Serving Layer (VERY IMPORTANT)
Streamlit Dashboard
👉 Makes insights:
interactive
shareable
business-friendly

7. 💡 Insight Layer
Interpretation of results
Recommendations
👉 This is where business value comes

⭐ Notes
Data collection and dashboard are decoupled for efficient deployment
Lightweight NLP approach used for scalability

[Streamlit Dashboard Link]
https://blinkitcustomersentimentanalysis-iimdsai.streamlit.app/