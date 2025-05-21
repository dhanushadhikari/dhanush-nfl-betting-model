import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

def load_model_and_data():
    model_path = os.path.join("model", "model.pkl")
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = RandomForestRegressor()
        model.fit([[0, 0]], [0])  # dummy fit for placeholder

    # For now, create a placeholder features_df
    features_df = pd.DataFrame({
        'home_team': ['Team A', 'Team B'],
        'away_team': ['Team C', 'Team D'],
        'feature_1': [1.2, 3.4],
        'feature_2': [5.6, 7.8],
    })
    return model, features_df

def make_predictions(model, features_df, odds_df):
    # Matchup key
    odds_df['matchup'] = odds_df['home_team'] + ' vs ' + odds_df['away_team']
    features_df['matchup'] = features_df['home_team'] + ' vs ' + features_df['away_team']

    df_merged = pd.merge(features_df, odds_df, on='matchup', how='inner')

    # Placeholder: use dummy numeric features for prediction
    df_merged['model_predicted_spread'] = model.predict(df_merged[["feature_1", "feature_2"]])
    df_merged['edge'] = df_merged['spread'] - df_merged['model_predicted_spread']

    return df_merged[['home_team', 'away_team', 'spread', 'model_predicted_spread', 'edge', 'total', 'moneyline_home']]
