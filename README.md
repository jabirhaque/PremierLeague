# Sports Betting ML Model

A machine learning system that predicts Premier League fixture outcomes (Home/Draw/Away) using a **Scikit-Learn Logistic Regression classifier**.  
The system automates bet placement by comparing model probabilities with bookmaker odds and applying the **Kelly criterion** for stake sizing.


## Features
- Logistic Regression model trained on historical Premier League fixtures
- Automated weekly job pipeline:
  1. **Fetch recent fixture results** from football-data.co.uk
  2. **Settle past bets** by updating the pot balance with wins/losses
  3. **Retrain model** on the newly completed fixtures
  4. **Fetch upcoming fixtures and odds** for the next matchweek
  5. **Place bets automatically** based on model predictions and Kelly criterion

## Technology Stack
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Scikit Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![MySQL](https://shields.io/badge/MySQL-lightgrey?logo=mysql&style=plastic&logoColor=white&labelColor=blue)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)