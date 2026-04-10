import pandas as pd
import sqlite3  # sqlite3 comes built-in with Python, no installation needed

# ============================================================
# WHAT IS A DATABASE?
# Think of it like this:
# CSV file = a single Excel sheet
# Database = an entire Excel workbook with multiple sheets
# But much faster and you can query it with SQL
# ============================================================

# Step 1: Load our CSV files into pandas dataframes
print("Loading CSV files...")
matches = pd.read_csv('data/matches.csv')
deliveries = pd.read_csv('data/deliveries.csv')
print(f"Matches loaded: {len(matches)} rows")
print(f"Deliveries loaded: {len(deliveries)} rows")

# Step 2: Create a database file
# sqlite3.connect() creates a .db file in our project
# Think of this as creating a new Excel workbook
print("\nCreating database...")
conn = sqlite3.connect('data/cricket.db')

# Step 3: Save our dataframes INTO the database as tables
# to_sql() converts a pandas dataframe into a database table
# if_exists='replace' means: if table already exists, overwrite it
# index=False means: don't save the row numbers as a column
matches.to_sql('matches', conn, if_exists='replace', index=False)
deliveries.to_sql('deliveries', conn, if_exists='replace', index=False)
print("Tables created: matches, deliveries")

# Step 4: Now let's run our FIRST SQL QUERY!
# ============================================================
# WHAT IS SQL?
# SQL = Structured Query Language
# It's a way to ask questions to your database
# SELECT = what columns do you want
# FROM = which table
# LIMIT = how many rows to show
# ============================================================

print("\n--- Running first SQL query ---")
query = "SELECT * FROM matches LIMIT 5"
result = pd.read_sql_query(query, conn)
print(result)

# Step 5: A more interesting query
# Let's find out which team has won the most IPL titles
print("\n--- Most IPL Match Wins ---")
query2 = """
    SELECT winner, COUNT(*) as total_wins
    FROM matches
    WHERE winner != ''
    GROUP BY winner
    ORDER BY total_wins DESC
    LIMIT 10
"""
# COUNT(*) = count the rows
# GROUP BY = group all rows with same winner together
# ORDER BY DESC = sort from highest to lowest

result2 = pd.read_sql_query(query2, conn)
print(result2)

# Step 6: Another query - most runs by a batsman
print("\n--- Top 10 Run Scorers ---")
query3 = """
    SELECT batter, SUM(batsman_runs) as total_runs
    FROM deliveries
    GROUP BY batter
    ORDER BY total_runs DESC
    LIMIT 10
"""
result3 = pd.read_sql_query(query3, conn)
print(result3)

# Always close the connection when done
conn.close()
print("\nDatabase saved to data/cricket.db")
print("Done!")