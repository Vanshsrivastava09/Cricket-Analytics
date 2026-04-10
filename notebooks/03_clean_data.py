import pandas as pd
import sqlite3

# ============================================================
# WHAT IS DATA CLEANING?
# Real data is messy. For example:
# - Some team names changed over the years
#   "Delhi Daredevils" became "Delhi Capitals"
#   "Kings XI Punjab" became "Punjab Kings"
# - Some values are missing (NaN = Not a Number = empty cell)
# We need to fix these before analysis
# ============================================================

# Load data from our database
conn = sqlite3.connect('data/cricket.db')
matches = pd.read_sql_query("SELECT * FROM matches", conn)
deliveries = pd.read_sql_query("SELECT * FROM deliveries", conn)

print("=== BEFORE CLEANING ===")
print(f"Matches shape: {matches.shape}")  # shape = (rows, columns)
print(f"Deliveries shape: {deliveries.shape}")

# -------------------------------------------------------
# PROBLEM 1: Missing Values
# NaN means the cell is empty. Let's see how many we have
# -------------------------------------------------------
print("\n--- Missing values in matches ---")
print(matches.isnull().sum())  # counts empty cells per column

# -------------------------------------------------------
# PROBLEM 2: Team Name Changes
# Same team, different names across seasons — confusing!
# We'll standardize them all to current names
# -------------------------------------------------------
print("\n--- Fixing team names ---")

# This is a dictionary: old name -> new name
team_name_fixes = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Rising Pune Supergiants': 'Rising Pune Supergiant',
    'Pune Warriors': 'Rising Pune Supergiant'
}

# Replace old names with new names in ALL relevant columns
# .replace() swaps every occurrence of the key with the value
for col in ['team1', 'team2', 'winner', 'toss_winner']:
    matches[col] = matches[col].replace(team_name_fixes)

for col in ['batting_team', 'bowling_team']:
    deliveries[col] = deliveries[col].replace(team_name_fixes)

print("Team names standardized!")

# -------------------------------------------------------
# PROBLEM 3: Fill Missing Values
# 'result_margin' is empty when match has no result
# We fill it with 0 so it doesn't cause errors later
# -------------------------------------------------------
matches['result_margin'] = matches['result_margin'].fillna(0)

# 'player_dismissed' is empty when no wicket fell — fill with 'none'
deliveries['player_dismissed'] = deliveries['player_dismissed'].fillna('none')
deliveries['dismissal_kind'] = deliveries['dismissal_kind'].fillna('none')
deliveries['fielder'] = deliveries['fielder'].fillna('none')

# -------------------------------------------------------
# PROBLEM 4: Add a 'season' column to deliveries
# Deliveries only has match_id, not the year
# We'll merge the year from matches table into deliveries
# This is like VLOOKUP in Excel
# -------------------------------------------------------
print("\n--- Adding season to deliveries ---")

# Extract just the year from the 'date' column
# matches['date'] looks like '2008-04-18', we want just '2008'
matches['season'] = pd.to_datetime(matches['date']).dt.year

# Now merge: add 'season' and 'venue' from matches into deliveries
# based on matching 'id' from matches with 'match_id' in deliveries
deliveries = deliveries.merge(
    matches[['id', 'season', 'venue']],
    left_on='match_id',
    right_on='id',
    how='left'
)

print(f"Deliveries now has season column: {deliveries['season'].unique()}")

# -------------------------------------------------------
# Save cleaned data back to database
# -------------------------------------------------------
print("\n--- Saving cleaned data ---")
matches.to_sql('matches_clean', conn, if_exists='replace', index=False)
deliveries.to_sql('deliveries_clean', conn, if_exists='replace', index=False)

conn.close()

print("\n=== AFTER CLEANING ===")
print(f"Matches shape: {matches.shape}")
print(f"Deliveries shape: {deliveries.shape}")
print("\nCleaned tables saved: matches_clean, deliveries_clean")
print("Data cleaning complete! ✅")