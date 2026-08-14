import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

DB_USER = "root"
DB_PASSWORD = "@MTejaswini09"   # <-- your real password
DB_HOST = "localhost"
DB_NAME = "ipl_auction_analysis"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}")

query = """
SELECT
    a.player_name AS auction_name,
    nm.scorecard_name,
    a.role,
    a.amount,
    a.team,
    a.year,
    a.player_origin,
    b.runs, b.balls_faced, b.strike_rate,
    bw.wickets, bw.overs, bw.economy
FROM auctions a
JOIN name_mapping nm ON a.player_name = nm.auction_name
LEFT JOIN batting_stats b ON nm.scorecard_name = b.player_name AND a.year = b.season
LEFT JOIN bowling_stats bw ON nm.scorecard_name = bw.player_name AND a.year = bw.season
"""

df = pd.read_sql(query, con=engine)
print(f"Total rows before filtering: {len(df)}")

# Keep only rows where the player actually played that season (batted or bowled)
df = df[(df["runs"].notna()) | (df["wickets"].notna())]
print(f"Rows with actual season performance: {len(df)}")

# Fill missing stats with 0 (e.g., a pure bowler has no batting runs)
df["runs"] = df["runs"].fillna(0)
df["balls_faced"] = df["balls_faced"].fillna(0)
df["strike_rate"] = df["strike_rate"].fillna(0)
df["wickets"] = df["wickets"].fillna(0)
df["overs"] = df["overs"].fillna(0)
df["economy"] = df["economy"].fillna(0)

# ---- PERFORMANCE INDEX ----
# Simple composite: batting contribution + bowling contribution
# Batting: runs weighted by strike rate quality (SR/100 as multiplier, capped)
# Bowling: wickets weighted heavily, economy adjustment
df["batting_score"] = df["runs"] * (df["strike_rate"] / 100).clip(upper=2)
df["bowling_score"] = (df["wickets"] * 20) - (df["economy"] * df["overs"] * 0.5)
df["bowling_score"] = df["bowling_score"].clip(lower=0)
df["performance_index"] = df["batting_score"] + df["bowling_score"]

# ---- VALUE SCORE ----
# performance per crore spent (amount is in rupees, 1 crore = 10,000,000)
df["amount_crore"] = df["amount"] / 10_000_000
df["value_score"] = round(df["performance_index"] / df["amount_crore"].replace(0, 0.01), 2)

df.to_sql("player_value_analysis", con=engine, if_exists="replace", index=False)
print(f"Saved player_value_analysis: {len(df)} rows")

print("\nTop 10 best-value players:")
print(df.sort_values("value_score", ascending=False)[
    ["scorecard_name", "team", "year", "amount_crore", "performance_index", "value_score"]
].head(10).to_string(index=False))

print("\nTop 10 most overpaid (lowest value):")
print(df[df["performance_index"] > 0].sort_values("value_score")[
    ["scorecard_name", "team", "year", "amount_crore", "performance_index", "value_score"]
].head(10).to_string(index=False))