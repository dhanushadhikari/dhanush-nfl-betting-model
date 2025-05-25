import pandas as pd

def scrape_draftkings_lines():
    print("🧪 DEBUG MODE: returning dummy odds data")
    data = {
        "home_team": ["Team A", "Team B"],
        "away_team": ["Team C", "Team D"],
        "spread": [-3.5, 2.0],
        "total": [48.5, 44.0],
        "moneyline_home": [-150, 110],
    }
    return pd.DataFrame(data)