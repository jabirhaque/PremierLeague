import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

data = pd.read_csv('../data/filtered_2024:25.csv')

data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
data['DayOfWeek'] = data['DateTime'].dt.dayofweek
data['Hour'] = data['DateTime'].dt.hour
data['Minute'] = data['DateTime'].dt.minute

X = data[['DayOfWeek', 'Hour', 'Minute', 'HomeTeam', 'AwayTeam']]
y = data['FTR']

categorical_features = ['HomeTeam', 'AwayTeam']
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough'
)

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(multi_class='multinomial', max_iter=1000))
])

model.fit(X_train, y_train)

# Save the model
joblib.dump(model, '../output/match_predictor.pkl')
joblib.dump(label_encoder, '../output/label_encoder.pkl')