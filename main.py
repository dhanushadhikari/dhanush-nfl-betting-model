import streamlit as st
from draftkings_scraper import scrape_draftkings_nfl
from model.predictor import load_model_and_data, make_predictions

st.set_page_config(page_title="NFL Betting Model", layout="wide")
st.title("NFL Betting Model: DraftKings Odds vs Model Predictions")

# Load odds
df_odds = scrape_draftkings_nfl()

# Load model and features
model, features_df = load_model_and_data()

# Make predictions
predictions_df = make_predictions(model, features_df, df_odds)

# Display results
st.subheader("Model vs DraftKings Lines")
st.dataframe(predictions_df.round(2))
