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

model = joblib.load('../output/match_predictor.pkl')
label_encoder = joblib.load('../output/label_encoder.pkl')
result = predict_probability('25/05/2025', '16:00', 'Man United', 'Aston Villa', model, label_encoder)
print(result)