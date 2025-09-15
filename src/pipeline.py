import os
import requests
import pandas as pd
import joblib

clubs = {
    'Manchester United': 'Man United',
    'Manchester City': 'Man City',
    'West Ham United': 'West Ham',
    'Newcastle United': 'Newcastle',
    'Brighton and Hove Albion': 'Brighton',
    'Leeds United': 'Leeds',
    'Wolverhampton Wanderers': 'Wolves',
    'Tottenham Hotspur': 'Tottenham',
    'Nottingham Forest': "Nott'm Forest"
}

model = joblib.load('../output/match_predictor.pkl')
label_encoder = joblib.load('../output/label_encoder.pkl')

url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds/"
params = {
    "apiKey": os.getenv("ODDS_API"), 
    "regions": "uk"
}

response = requests.get(url, params=params)

def calculate_kelly_fraction(probability, odds):
    b = odds - 1
    if b == 0: return -1
    q = 1 - probability
    return (b * probability - q) / b

from datetime import datetime, timedelta

if response.status_code == 200:
    data = response.json()

    total_staked = 0
    total_potential_payout = 0

    current_time = datetime.now()
    one_week_ahead = current_time + timedelta(weeks=1)

    for match in data:
        commence_time = datetime.fromisoformat(match['commence_time'].replace('Z', ''))

        if current_time < commence_time < one_week_ahead:
            home_team = clubs.get(match['home_team'], match['home_team'])
            away_team = clubs.get(match['away_team'], match['away_team'])
            print(f"Match: {home_team} vs {away_team} at {commence_time}")

            date, time = commence_time.strftime('%Y-%m-%d'), commence_time.strftime('%H:%M:%S')
            input_data = pd.DataFrame([{
                'DayOfWeek': pd.to_datetime(date + ' ' + time).dayofweek,
                'Hour': pd.to_datetime(date + ' ' + time).hour,
                'Minute': pd.to_datetime(date + ' ' + time).minute,
                'HomeTeam': home_team,
                'AwayTeam': away_team
            }])

            probabilities = model.predict_proba(input_data)
            prob_distribution = dict(zip(label_encoder.classes_, probabilities[0]))
            print("  Predicted Probabilities:")
            for outcome, prob in prob_distribution.items():
                print(f"    {outcome}: {prob:.2%}")

            best_kelly = -1
            best_event = None
            best_bookmaker = None
            best_odds = None

            for bookmaker in match['bookmakers']:
                bookmaker_name = bookmaker['title']

                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':
                        for outcome in market['outcomes']:
                            event = outcome['name']
                            odds = outcome['price']
                            probability = prob_distribution.get(event[0].upper(), 0)

                            kelly_fraction = calculate_kelly_fraction(probability, odds)
                            if kelly_fraction > best_kelly:
                                best_kelly = kelly_fraction
                                best_event = event
                                best_bookmaker = bookmaker_name
                                best_odds = odds

            if best_kelly > 0:
                bet_amount = 1 * best_kelly
                potential_payout = bet_amount * best_odds
                profit = potential_payout - bet_amount
                roi = (profit / bet_amount) * 100 if bet_amount > 0 else 0

                total_staked += bet_amount
                total_potential_payout += potential_payout

                print(f"  Best Bet: {best_event} with {best_bookmaker} at odds {best_odds}")
                print(f"  Kelly Fraction: {best_kelly:.4f}, Bet Amount: £{bet_amount:.2f}")
                print(f"  Potential Payout: £{potential_payout:.2f}")
                print(f"  Potential Profit: £{profit:.2f}, ROI: {roi:.2f}%")
                print()
            else:
                print("  No positive Kelly Criterion found for this match.")
                print()

    total_profit = total_potential_payout - total_staked
    overall_roi = (total_profit / total_staked) * 100 if total_staked > 0 else 0

    print(f"Total Money Staked: £{total_staked:.2f}")
    print(f"Total Potential Payout: £{total_potential_payout:.2f}")
    print(f"Total Potential Profit: £{total_profit:.2f}")
    print(f"Potential ROI: {overall_roi:.2f}%")
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    print(response.text)

#open -a "PyCharm"