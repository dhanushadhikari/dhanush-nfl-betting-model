# main.py
import streamlit as st
from draftkings_scraper import scrape_draftkings_lines
from model.predictor import load_model_and_data, make_predictions
import pandas as pd

st.set_page_config(page_title="NFL Betting Model", layout="centered")
st.title("🏈 NFL Betting Model")
st.write("Fetch DraftKings odds, run the model, and find +EV opportunities.")

# Button to trigger scraping and predictions
if st.button("📈 Fetch and Predict"):

    with st.spinner("Scraping DraftKings odds..."):
        try:
            odds_df = scrape_draftkings_lines()
        except Exception as e:
            st.error("❌ Failed to scrape DraftKings odds.")
            st.exception(e)
            odds_df = pd.DataFrame()  # Fallback to empty

    if odds_df.empty or 'home_team' not in odds_df.columns:
        st.error("❌ No valid betting lines found. DraftKings may have blocked scraping or structure changed.")
        st.stop()
    else:
        st.success("✅ DraftKings odds scraped!")
        st.write(odds_df.head())

    # Load model and features
    with st.spinner("Loading model and feature data..."):
        try:
            model, features_df = load_model_and_data()
        except Exception as e:
            st.error("❌ Failed to load model or feature data.")
            st.exception(e)
            st.stop()

    if features_df.empty or 'home_team' not in features_df.columns:
        st.error("❌ Feature data appears to be missing or invalid.")
        st.stop()

    st.success("✅ Model and features loaded!")
    st.write(features_df.head())

    # Make predictions
    with st.spinner("Running predictions..."):
        try:
            predictions_df = make_predictions(model, features_df, odds_df)
            if predictions_df.empty:
                st.warning("⚠️ No matchups matched between features and odds. Check formatting.")
                st.stop()
            st.success("✅ Predictions complete!")
            st.dataframe(predictions_df)
        except Exception as e:
            st.error("❌ Prediction step failed.")
            st.exception(e)
