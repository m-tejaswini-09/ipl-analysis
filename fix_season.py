from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

DB_USER = "root"
DB_PASSWORD = "@MTejaswini09"   # <-- your real password
DB_HOST = "localhost"
DB_NAME = "ipl_auction_analysis"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}")

fixes = {
    "2007/08": "2008",
    "2009/10": "2010",
    "2020/21": "2021",
}

with engine.begin() as conn:
    for old, new in fixes.items():
        result = conn.execute(
            text("UPDATE matches SET season = :new WHERE season = :old"),
            {"new": new, "old": old}
        )
        print(f"Updated {result.rowcount} rows: {old} -> {new}")