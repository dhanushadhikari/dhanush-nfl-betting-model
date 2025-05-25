import requests
import pandas as pd

def scrape_draftkings_lines():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://sportsbook.draftkings.com/'
    }
    url = "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/88808?category=game-lines&format=json"
    response = requests.get(url, headers=headers)
    data = response.json()

    events = data['eventGroup']['events']
    teams = {team['id']: team['name'] for team in data['eventGroup']['teams']}
    games = []

    for event in events:
        home_team = teams[str(event['homeTeamId'])]
        away_team = teams[str(event['awayTeamId'])]
        event_id = event['eventId']

        home_spread, total, moneyline_home = None, None, None

        for offer_cat in data['eventGroup']['offerCategories']:
            if offer_cat['name'] != 'Game Lines':
                continue
            for subcat in offer_cat['offerSubcategoryDescriptors']:
                for offer in subcat['offerSubcategory']['offers']:
                    for market in offer:
                        if str(market.get('eventId')) != str(event_id):
                            continue

                        market_type = market.get('label')
                        outcomes = market.get('outcomes', [])

                        if market_type == 'Point Spread':
                            for o in outcomes:
                                if o['participant'] == home_team:
                                    home_spread = float(o['line']) / 1000
                        elif market_type == 'Total Points':
                            total = float(outcomes[0]['line']) / 1000
                        elif market_type == 'Moneyline':
                            for o in outcomes:
                                if o['participant'] == home_team:
                                    moneyline_home = o['oddsAmerican']

        games.append({
            'home_team': home_team,
            'away_team': away_team,
            'spread': home_spread,
            'total': total,
            'moneyline_home': moneyline_home
        })

    return pd.DataFrame(games)
