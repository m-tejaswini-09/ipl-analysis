import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

DB_USER = "root"
DB_PASSWORD = "@MTejaswini09"   # <-- your real password
DB_HOST = "localhost"
DB_NAME = "ipl_auction_analysis"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}")

# Pull deliveries joined with match season
query = """
SELECT d.*, m.season
FROM deliveries d
JOIN matches m ON d.match_id = m.id
"""
df = pd.read_sql(query, con=engine)
print(f"Pulled {len(df)} delivery rows with season info")

# ---- BATTING STATS per player per season ----
batting = df.groupby(["batter", "season"]).agg(
    runs=("batsman_runs", "sum"),
    balls_faced=("batsman_runs", "count")
).reset_index()
batting["strike_rate"] = round(batting["runs"] / batting["balls_faced"] * 100, 2)
batting.rename(columns={"batter": "player_name"}, inplace=True)

# ---- BOWLING STATS per player per season ----
bowling = df.groupby(["bowler", "season"]).agg(
    wickets=("is_wicket", "sum"),
    balls_bowled=("ball", "count"),
    runs_conceded=("total_runs", "sum")
).reset_index()
bowling["overs"] = round(bowling["balls_bowled"] / 6, 1)
bowling["economy"] = round(bowling["runs_conceded"] / (bowling["balls_bowled"] / 6), 2)
bowling.rename(columns={"bowler": "player_name"}, inplace=True)

# Save both to the database as new tables
batting.to_sql("batting_stats", con=engine, if_exists="replace", index=False)
bowling.to_sql("bowling_stats", con=engine, if_exists="replace", index=False)

print(f"Saved batting_stats: {len(batting)} rows")
print(f"Saved bowling_stats: {len(bowling)} rows")

print("\nSample batting stats:")
print(batting.head())
print("\nSample bowling stats:")
print(bowling.head())