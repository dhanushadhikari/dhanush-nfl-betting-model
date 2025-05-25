# main.py
import streamlit as st
from draftkings_scraper import scrape_draftkings_lines
from model.predictor import load_model_and_data, make_predictions

st.title("🏈 NFL Betting Model")
st.write("This app fetches DraftKings betting lines, predicts outcomes using a machine learning model, and highlights edges.")

# Step 1: Fetch lines
st.write("📡 Step 1: Scraping DraftKings lines...")
try:
    odds_df = scrape_draftkings_lines()
    st.write("✅ Odds scraped successfully!")
    st.write(odds_df.head())
except Exception as e:
    st.error(f"❌ Error scraping DraftKings lines: {e}")
    st.stop()

if odds_df.empty:
    st.error("❌ No odds found. The scraper may be broken or blocked.")
    st.stop()

# Step 2: Load model and features
st.write("🧠 Step 2: Loading model and features...")
try:
    model, features_df = load_model_and_data()
    st.write("✅ Model and feature data loaded!")
    st.write(features_df.head())
except Exception as e:
    st.error(f"❌ Error loading model or data: {e}")
    st.stop()

if features_df.empty:
    st.error("❌ Feature data is empty.")
    st.stop()

# Step 3: Predict and display
st.write("📊 Step 3: Making predictions...")
try:
    predictions_df = make_predictions(model, features_df, odds_df)
    st.success("✅ Predictions complete!")
    st.dataframe(predictions_df)
except Exception as e:
    st.error(f"❌ Prediction failed: {e}")
