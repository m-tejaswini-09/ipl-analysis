import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

DB_USER = "root"
DB_PASSWORD = "@MTejaswini09"   # <-- your real password
DB_HOST = "localhost"
DB_NAME = "ipl_auction_analysis"

AUCTION_CSV = "C:/Users/mteje/Downloads/IPLPlayerAuctionData.csv"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}")

auctions = pd.read_csv(AUCTION_CSV, encoding="utf-8-sig")
auctions.rename(columns={
    "Player": "player_name",
    "Role": "role",
    "Amount": "amount",
    "Team": "team",
    "Year": "year",
    "Player Origin": "player_origin"
}, inplace=True)
auctions.to_sql("auctions", con=engine, if_exists="append", index=False)
print(f"Loaded {len(auctions)} rows into auctions")