
import streamlit as st
import pandas as pd

from draftkings_scraper import scrape_draftkings_lines
from feature_engineering import engineer_features
from predictor import predict_spread, predict_moneyline

st.set_page_config(page_title="NFL Betting Model", layout="wide")

st.title("🏈 NFL Betting Prediction Dashboard")
st.markdown("This app scrapes DraftKings lines, generates features, and predicts outcomes using machine learning models.")

# Sidebar controls
market = st.sidebar.radio("Select Market", ("Point Spread", "Moneyline"))
show_edges = st.sidebar.checkbox("Show Only Value Bets", value=True)

if st.button("Fetch and Predict"):
    with st.spinner("Scraping DraftKings and running predictions..."):
        try:
            # Step 1: Scrape lines
            df_lines = scrape_draftkings_lines()

            # Step 2: Generate features
            df_features = engineer_features(df_lines)

            # Step 3: Predict
            if market == "Point Spread":
                df_preds = predict_spread(df_features)
            else:
                df_preds = predict_moneyline(df_features)

            # Show results
            if show_edges:
                df_preds = df_preds[df_preds["value"] == True]

            st.success(f"Found {len(df_preds)} predictions.")
            st.dataframe(df_preds.reset_index(drop=True))

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Click the button above to fetch odds and generate predictions.")
