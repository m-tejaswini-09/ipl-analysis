import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from rapidfuzz import process, fuzz

DB_USER = "root"
DB_PASSWORD = "@MTejaswini09"   # <-- your real password
DB_HOST = "localhost"
DB_NAME = "ipl_auction_analysis"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}")

print("Connecting and pulling names...")
auctions = pd.read_sql("SELECT DISTINCT player_name FROM auctions", con=engine)
scorecard_names = pd.read_sql(
    "SELECT DISTINCT player_name FROM batting_stats UNION SELECT DISTINCT player_name FROM bowling_stats",
    con=engine
)
scorecard_list = scorecard_names["player_name"].str.strip().tolist()
print(f"Auction names: {len(auctions)}, Scorecard names: {len(scorecard_list)}")

def to_initials_format(full_name):
    parts = full_name.strip().split()
    if len(parts) < 2:
        return full_name
    initials = "".join(p[0] for p in parts[:-1])
    surname = parts[-1]
    return f"{initials} {surname}"

mapping = {}
unresolved = []

print("Matching names...")
for i, name in enumerate(auctions["player_name"].str.strip()):
    converted = to_initials_format(name)
    if converted in scorecard_list:
        mapping[name] = converted
        continue
    result = process.extractOne(converted, scorecard_list, scorer=fuzz.ratio, score_cutoff=80)
    if result:
        mapping[name] = result[0]
    else:
        unresolved.append(name)
    if (i + 1) % 100 == 0:
        print(f"  ...processed {i+1}/{len(auctions)}")

print(f"\nResolved via initials/fuzzy match: {len(mapping)}")
print(f"Still unresolved: {len(unresolved)}")
print("\nSample unresolved names:")
for n in unresolved[:20]:
    print(" -", n)

mapping_df = pd.DataFrame(list(mapping.items()), columns=["auction_name", "scorecard_name"])
mapping_df.to_sql("name_mapping", con=engine, if_exists="replace", index=False)
print(f"\nSaved {len(mapping_df)} name mappings to 'name_mapping' table")
      