import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ---- CONFIG: update this ----
DB_USER = "root"
DB_PASSWORD = "@MTejaswini09"   # <-- your real MySQL password
DB_HOST = "localhost"
DB_NAME = "ipl_auction_analysis"

MATCHES_CSV = "C:/Users/mteje/Downloads/matches.csv"
DELIVERIES_CSV = "C:/Users/mteje/Downloads/deliveries.csv"
# --------------------------------

engine = create_engine(f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}")

matches = pd.read_csv(MATCHES_CSV)
matches.to_sql("matches", con=engine, if_exists="append", index=False)
print(f"Loaded {len(matches)} rows into matches")

deliveries = pd.read_csv(DELIVERIES_CSV)
deliveries.rename(columns={"over": "over_num"}, inplace=True)
deliveries.to_sql("deliveries", con=engine, if_exists="append", index=False, chunksize=5000)
print(f"Loaded {len(deliveries)} rows into deliveries")
