import pandas as pd
from datetime import datetime, timedelta
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="premierleague"
)
cursor = conn.cursor()

csv_file = '../data/data.csv'
data = pd.read_csv(csv_file)

today = datetime.now()
cutoff_date = today - timedelta(days=7)

for index, row in data.iloc[::-1].iterrows():
    fixture_date = datetime.strptime(row['Date'], '%d/%m/%Y')

    if fixture_date < cutoff_date:
        break

    home_team = row['HomeTeam']
    away_team = row['AwayTeam']
    ftr = row['FTR']

    query = """
    SELECT BETTED_EVENT, BETTED_AMOUNT, ODDS, POTENTIAL_PAYOUT, BOOKMAKER
    FROM UNSETTLED_BETS
    WHERE HOME_TEAM = %s AND AWAY_TEAM = %s
    """
    cursor.execute(query, (home_team, away_team))
    result = cursor.fetchone()

    if result:
        betted_event, betted_amount, odds, potential_payout, bookmaker = result

        win = betted_event == ftr
        profit_loss = potential_payout - betted_amount if win else -betted_amount

        insert_query = """
        INSERT INTO SETTLED_BETS (
            HOME_TEAM, AWAY_TEAM, DATETIME, BOOKMAKER, BETTED_EVENT, BETTED_AMOUNT, ODDS, WIN, PROFIT_LOSS
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            home_team, away_team, fixture_date, bookmaker, betted_event,
            betted_amount, odds, win, profit_loss
        ))

        delete_query = """
        DELETE FROM UNSETTLED_BETS
        WHERE HOME_TEAM = %s AND AWAY_TEAM = %s
        """
        cursor.execute(delete_query, (home_team, away_team))

        print(f"Bet settled for fixture: {home_team} vs {away_team}")
    else:
        print(f"No bet found for fixture: {home_team} vs {away_team}")

conn.commit()
cursor.close()
conn.close()