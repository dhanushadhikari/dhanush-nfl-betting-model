import streamlit as st
from draftkings_scraper import scrape_draftkings_lines
from model.predictor import load_model_and_data, make_predictions

@st.cache_data(ttl=600)  # cache for 10 minutes
def get_odds():
    return scrape_draftkings_lines()

@st.cache_resource
def get_model_and_features():
    return load_model_and_data()

def main():
    st.title("NFL Betting Value Finder")

    st.write("Click the button below to fetch the latest DraftKings odds and run predictions.")
    if st.button("Fetch and Predict"):
        with st.spinner("Fetching DraftKings odds..."):
            odds_df = get_odds()
        with st.spinner("Loading model..."):
            model, features_df = get_model_and_features()
        with st.spinner("Making predictions..."):
            results_df = make_predictions(model, features_df, odds_df)
        st.write("Predicted vs DraftKings Lines")
        st.dataframe(results_df)
    else:
        st.info("Press the button to start the analysis.")

if __name__ == "__main__":
    main()
