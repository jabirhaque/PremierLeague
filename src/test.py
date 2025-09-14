import pandas as pd
import joblib

def predict_probability(date, time, home_team, away_team, model, label_encoder):
    input_data = pd.DataFrame([{
        'DayOfWeek': pd.to_datetime(date + ' ' + time).dayofweek,
        'Hour': pd.to_datetime(date + ' ' + time).hour,
        'Minute': pd.to_datetime(date + ' ' + time).minute,
        'HomeTeam': home_team,
        'AwayTeam': away_team
    }])
    probabilities = model.predict_proba(input_data)
    return dict(zip(label_encoder.classes_, probabilities[0]))


def calculate_kelly_fraction(probability, odds):
    b = odds - 1
    q = 1 - probability
    return (b * probability - q) / b


def process_all_fixtures_and_calculate_overall_return(csv_file, model, label_encoder, base_bet=1.0):
    data = pd.read_csv(csv_file)

    total_amount_made = 0
    total_amount_staked = 0

    for _, fixture in data.iterrows():
        date = fixture['Date']
        time = fixture['Time']
        home_team = fixture['HomeTeam']
        away_team = fixture['AwayTeam']
        odds_home = fixture['B365H']
        odds_draw = fixture['B365D']
        odds_away = fixture['B365A']
        result = fixture['FTR']

        probabilities = predict_probability(date, time, home_team, away_team, model, label_encoder)
        prob_home = probabilities['H']
        prob_draw = probabilities['D']
        prob_away = probabilities['A']

        kelly_home = calculate_kelly_fraction(prob_home, odds_home)
        kelly_draw = calculate_kelly_fraction(prob_draw, odds_draw)
        kelly_away = calculate_kelly_fraction(prob_away, odds_away)

        bet_home = base_bet * kelly_home if kelly_home > 0 else 0
        bet_draw = base_bet * kelly_draw if kelly_draw > 0 else 0
        bet_away = base_bet * kelly_away if kelly_away > 0 else 0

        winnings = 0
        if result == 'H':
            winnings += bet_home * odds_home
        elif result == 'D':
            winnings += bet_draw * odds_draw
        elif result == 'A':
            winnings += bet_away * odds_away

        total_bet = bet_home + bet_draw + bet_away
        amount_made = winnings - total_bet

        total_amount_made += amount_made
        total_amount_staked += total_bet

    overall_percentage_return = (total_amount_made / total_amount_staked) * 100 if total_amount_staked > 0 else 0

    print(f"Total Amount Made: £{total_amount_made:.2f}")
    print(f"Total Amount Staked: £{total_amount_staked:.2f}")
    print(f"Overall Percentage Return: {overall_percentage_return:.2f}%")

    return {
        'Total Amount Made': total_amount_made,
        'Total Amount Staked': total_amount_staked,
        'Overall Percentage Return': overall_percentage_return
    }

model = joblib.load('../output/match_predictor.pkl')
label_encoder = joblib.load('../output/label_encoder.pkl')

result = process_all_fixtures_and_calculate_overall_return('../data/test.csv', model, label_encoder)

#python script.py && python train.py && python test.py