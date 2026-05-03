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
