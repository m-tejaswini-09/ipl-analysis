# IPL Auction Value Analysis & Team Spending Intelligence

Analyzing whether IPL teams got good value for the players they bought — using multi-season auction and match data to see who was over- or under-priced relative to their actual on-field performance.

## Tech Stack
Python (pandas, SQLAlchemy) | MySQL | Power BI | Excel

## Overview
IPL teams spend crores of rupees on players every auction, but it's rarely clear afterward whether that spending paid off. This project builds a data pipeline that:
1. Loads multi-season match, ball-by-ball, and auction data into a MySQL database
2. Aggregates raw ball-by-ball data into per-player, per-season batting and bowling statistics
3. Matches player names across datasets (auction records and match scorecards use different naming conventions)
4. Computes a custom **Value Score** — performance relative to price paid — to rank players as under/overpaid
5. Visualizes results in an interactive Power BI dashboard

## Data Sources
- IPL match and ball-by-ball data (2008–2024), Kaggle
- IPL player auction data (2013–2024): player, role, price, team, year, Kaggle

## Approach

**Data pipeline (Python + MySQL):**
- Loaded ~261K ball-by-ball records and 970 auction records into a MySQL relational schema (`matches`, `deliveries`, `auctions`)
- Cleaned inconsistent season formats (e.g. `2007/08` → `2008`) for consistent joins
- Aggregated `deliveries` into `batting_stats` and `bowling_stats` tables (runs, strike rate, wickets, economy per player per season)

**Name matching:**
- Auction data uses full names ("Mitchell Starc"); match data uses scorecard-style initials ("MA Starc")
- Built a matching pipeline: initials-conversion first, then fuzzy string matching (RapidFuzz) as a fallback — resolved 442 of 543 auction players (~81%) to their scorecard identity

**Value Score:**
- Combined a batting score (runs weighted by strike rate) and bowling score (wickets weighted, adjusted for economy) into a single performance index
- Value Score = performance index ÷ price paid (in ₹ crore) — higher means better value for money

## Dashboard
Interactive Power BI dashboard with:
- Top value players by Value Score
- Team spending vs. performance (scatter plot)
- Detailed player comparison table (price, performance, value score)
- Slicers for season and team

## Known Limitations
- Retained players (e.g., icon players kept by their team without going through auction) don't appear in auction data, since they have no auction price — this dataset only reflects players who went through the open auction
- ~19% of auction records couldn't be matched to scorecard data (likely players who didn't play a match ball that season, or had name variants too different to auto-resolve)

## What I'd improve next
- Manual review/correction of the remaining unmatched player names
- Incorporate fielding stats into the performance index
- Add a "team ROI over time" trend view