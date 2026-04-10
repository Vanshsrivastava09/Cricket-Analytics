import pandas as pd
import sqlite3
import pickle  # pickle saves our trained model to a file
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# ============================================================
# WHAT IS MACHINE LEARNING?
# We're going to teach a computer to predict match winners.
# 
# HOW? We show it 1000+ past matches and say:
# "Here's team1, team2, toss winner, venue... who won?"
# The model finds patterns and learns from them.
# Then when we give it a NEW match, it predicts the winner.
#
# RandomForestClassifier = one of the best beginner ML models
# Think of it as 100 decision trees voting on the answer
# ============================================================

print("Loading data...")
conn = sqlite3.connect('data/cricket.db')
matches = pd.read_sql_query("SELECT * FROM matches_clean", conn)
conn.close()

# -------------------------------------------------------
# STEP 1: Prepare Features
# Features = the inputs we give the model
# Label = what we want to predict (winner)
# -------------------------------------------------------

# Drop rows where there's no winner (abandoned matches)
matches = matches[matches['winner'].notna()]
matches = matches[matches['winner'] != '']

# Select only the columns that help predict the winner
# We use: team1, team2, toss_winner, toss_decision, venue
features = matches[['team1', 'team2', 'toss_winner', 'toss_decision', 'venue', 'winner']].copy()
features = features.dropna()  # remove any rows with empty values

print(f"Training data: {len(features)} matches")

# -------------------------------------------------------
# STEP 2: Label Encoding
# ML models only understand NUMBERS, not text
# LabelEncoder converts text -> numbers
# Example: "Mumbai Indians" -> 5, "CSK" -> 2
# -------------------------------------------------------
le_team = LabelEncoder()
le_venue = LabelEncoder()
le_toss = LabelEncoder()

# Fit on ALL team names so encoder knows every team
all_teams = pd.concat([
    features['team1'],
    features['team2'],
    features['toss_winner'],
    features['winner']
]).unique()

le_team.fit(all_teams)
le_venue.fit(features['venue'])
le_toss.fit(features['toss_decision'])

# Now transform text to numbers
features['team1_enc'] = le_team.transform(features['team1'])
features['team2_enc'] = le_team.transform(features['team2'])
features['toss_winner_enc'] = le_team.transform(features['toss_winner'])
features['toss_decision_enc'] = le_toss.transform(features['toss_decision'])
features['venue_enc'] = le_venue.transform(features['venue'])
features['winner_enc'] = le_team.transform(features['winner'])

print("Label encoding done!")

# -------------------------------------------------------
# STEP 3: Split into Training and Testing sets
# We train on 80% of data, test on 20%
# This is like studying 80% of a textbook, then taking
# a test on questions from the remaining 20%
# -------------------------------------------------------
X = features[['team1_enc', 'team2_enc', 'toss_winner_enc',
               'toss_decision_enc', 'venue_enc']]
y = features['winner_enc']

# test_size=0.2 means 20% goes to testing
# random_state=42 means results are reproducible
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# -------------------------------------------------------
# STEP 4: Train the Model
# This is where the actual learning happens
# n_estimators=100 means 100 decision trees
# -------------------------------------------------------
print("\nTraining model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)  # THIS is the learning step
print("Model trained!")

# -------------------------------------------------------
# STEP 5: Test the Model
# See how accurate it is on data it has never seen
# -------------------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy*100:.1f}%")
print("(This means the model predicts correctly this % of the time)")

# -------------------------------------------------------
# STEP 6: Save the model to a file
# pickle saves Python objects to disk
# So we can load it in our dashboard without retraining
# -------------------------------------------------------
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/le_team.pkl', 'wb') as f:
    pickle.dump(le_team, f)

with open('models/le_venue.pkl', 'wb') as f:
    pickle.dump(le_venue, f)

with open('models/le_toss.pkl', 'wb') as f:
    pickle.dump(le_toss, f)

print("\nModel saved to models/model.pkl ✅")

# -------------------------------------------------------
# STEP 7: Test it manually with one prediction
# -------------------------------------------------------
print("\n--- Test Prediction ---")
print("Mumbai Indians vs CSK, Toss: Mumbai Indians chose to bat")

test_input = pd.DataFrame({
    'team1_enc': [le_team.transform(['Mumbai Indians'])[0]],
    'team2_enc': [le_team.transform(['Chennai Super Kings'])[0]],
    'toss_winner_enc': [le_team.transform(['Mumbai Indians'])[0]],
    'toss_decision_enc': [le_toss.transform(['bat'])[0]],
    'venue_enc': [le_venue.transform(['Wankhede Stadium'])[0]]
})

prediction = model.predict(test_input)
predicted_winner = le_team.inverse_transform(prediction)[0]
print(f"Predicted Winner: {predicted_winner} 🏆")