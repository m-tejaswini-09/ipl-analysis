import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

DB_USER = "root"
DB_PASSWORD = "@MTejaswini09"   # <-- your real password
DB_HOST = "localhost"
DB_NAME = "ipl_auction_analysis"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}")

auction_names = pd.read_sql("SELECT DISTINCT player_name FROM auctions", con=engine)
batting_names = pd.read_sql("SELECT DISTINCT player_name FROM batting_stats", con=engine)

auction_set = set(auction_names["player_name"].str.strip())
batting_set = set(batting_names["player_name"].str.strip())

matched = auction_set & batting_set
unmatched = auction_set - batting_set

print(f"Total unique auction players: {len(auction_set)}")
print(f"Matched directly: {len(matched)}")
print(f"Unmatched: {len(unmatched)}")
print("\nSample unmatched names:")
for name in list(unmatched)[:20]:
    print(" -", name)