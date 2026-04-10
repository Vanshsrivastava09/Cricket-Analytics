import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import pickle
import numpy as np

# ============================================================
# WHAT IS STREAMLIT?
# Streamlit turns Python code into a web app automatically.
# Every time you write st.something(), it creates a UI element.
# st.title() = big heading
# st.write() = text
# px.bar() = bar chart from plotly
# No HTML or CSS needed — Python does everything
# ============================================================

# --- Page Configuration ---
# This sets the browser tab title and layout
st.set_page_config(
    page_title="IPL Cricket Analytics",
    page_icon="🏏",
    layout="wide"  # uses full screen width
)

# --- Load Data from Database ---
# We use @st.cache_data so data loads only ONCE
# Without this, it would reload every time you click anything — very slow
@st.cache_data
def load_data():
    conn = sqlite3.connect('data/cricket.db')
    matches = pd.read_sql_query("SELECT * FROM matches_clean", conn)
    deliveries = pd.read_sql_query("SELECT * FROM deliveries_clean", conn)
    conn.close()
    return matches, deliveries

matches, deliveries = load_data()

# ============================================================
# SIDEBAR — the left panel with filters
# This lets users filter data by season
# ============================================================
st.sidebar.title("🏏 IPL Analytics")
st.sidebar.markdown("---")

# Get list of all seasons, sorted
all_seasons = sorted(matches['season'].unique().tolist())

# Multiselect = dropdown where you can pick multiple options
selected_seasons = st.sidebar.multiselect(
    "Select Season(s)",
    options=all_seasons,
    default=all_seasons  # by default, all seasons selected
)

# Filter data based on selected seasons
if selected_seasons:
    filtered_matches = matches[matches['season'].isin(selected_seasons)]
    filtered_deliveries = deliveries[deliveries['season'].isin(selected_seasons)]
else:
    filtered_matches = matches
    filtered_deliveries = deliveries

# ============================================================
# MAIN PAGE
# ============================================================
st.title("🏏 IPL Cricket Analytics Dashboard")
st.markdown("Complete analysis of IPL matches from 2008 to 2024")
st.markdown("---")

# ============================================================
# ROW 1: KPI CARDS (Key Performance Indicators)
# These are the big number boxes at the top
# st.columns(4) creates 4 equal columns side by side
# ============================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Matches", len(filtered_matches))

with col2:
    total_runs = filtered_deliveries['batsman_runs'].sum()
    st.metric("Total Runs Scored", f"{total_runs:,}")  # comma formatting

with col3:
    total_wickets = filtered_deliveries[
        filtered_deliveries['dismissal_kind'] != 'none'
    ].shape[0]
    st.metric("Total Wickets", f"{total_wickets:,}")

with col4:
    total_sixes = filtered_deliveries[
        filtered_deliveries['batsman_runs'] == 6
    ].shape[0]
    st.metric("Total Sixes", f"{total_sixes:,}")

st.markdown("---")

# ============================================================
# ROW 2: TWO CHARTS SIDE BY SIDE
# ============================================================
col_left, col_right = st.columns(2)

# --- Chart 1: Most Wins by Team ---
with col_left:
    st.subheader("🏆 Most Wins by Team")

    wins = filtered_matches[filtered_matches['winner'] != ''] \
        .groupby('winner')['winner'] \
        .count() \
        .reset_index(name='wins') \
        .sort_values('wins', ascending=False) \
        .head(10)

    # px.bar() creates a bar chart
    # x = horizontal axis, y = vertical axis, color = color by team
    fig1 = px.bar(
        wins,
        x='wins',
        y='winner',
        orientation='h',  # horizontal bar chart
        color='wins',
        color_continuous_scale='Viridis',
        labels={'winner': 'Team', 'wins': 'Total Wins'}
    )
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

# --- Chart 2: Matches per Season ---
with col_right:
    st.subheader("📅 Matches per Season")

    season_counts = filtered_matches.groupby('season').size().reset_index(name='matches')

    fig2 = px.line(
        season_counts,
        x='season',
        y='matches',
        markers=True,  # dots on the line
        color_discrete_sequence=['#FF6B35']
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ============================================================
# ROW 3: BATTING ANALYSIS
# ============================================================
st.subheader("🏏 Top Run Scorers")

col_l, col_r = st.columns(2)

with col_l:
    top_n = st.slider("Show top N batsmen", min_value=5, max_value=20, value=10)

with col_r:
    pass  # empty column for spacing

top_batsmen = filtered_deliveries.groupby('batter')['batsman_runs'] \
    .sum() \
    .reset_index() \
    .rename(columns={'batsman_runs': 'total_runs'}) \
    .sort_values('total_runs', ascending=False) \
    .head(top_n)

fig3 = px.bar(
    top_batsmen,
    x='batter',
    y='total_runs',
    color='total_runs',
    color_continuous_scale='Blues',
    labels={'batter': 'Batsman', 'total_runs': 'Total Runs'}
)
fig3.update_layout(height=400)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ============================================================
# ROW 4: BOWLING ANALYSIS
# ============================================================
st.subheader("🎯 Top Wicket Takers")

top_bowlers = filtered_deliveries[
    filtered_deliveries['dismissal_kind'].isin([
        'caught', 'bowled', 'lbw', 'stumped',
        'caught and bowled', 'hit wicket'
    ])
].groupby('bowler')['dismissal_kind'] \
    .count() \
    .reset_index(name='wickets') \
    .sort_values('wickets', ascending=False) \
    .head(10)

fig4 = px.bar(
    top_bowlers,
    x='bowler',
    y='wickets',
    color='wickets',
    color_continuous_scale='Reds',
    labels={'bowler': 'Bowler', 'wickets': 'Total Wickets'}
)
fig4.update_layout(height=400)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============================================================
# ROW 5: TOSS ANALYSIS
# ============================================================
st.subheader("🪙 Toss Decision Analysis")

col1, col2 = st.columns(2)

with col1:
    toss_decision = filtered_matches['toss_decision'].value_counts().reset_index()
    toss_decision.columns = ['decision', 'count']

    fig5 = px.pie(
        toss_decision,
        values='count',
        names='decision',
        title='Bat vs Field after Toss'
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # Does winning toss = winning match?
    filtered_matches['toss_win_match_win'] = (
        filtered_matches['toss_winner'] == filtered_matches['winner']
    )
    toss_effect = filtered_matches['toss_win_match_win'].value_counts().reset_index()
    toss_effect.columns = ['won_match', 'count']
    toss_effect['won_match'] = toss_effect['won_match'].map({True: 'Won Match', False: 'Lost Match'})

    fig6 = px.pie(
        toss_effect,
        values='count',
        names='won_match',
        title='Toss Winners: Did They Win the Match?'
    )
    st.plotly_chart(fig6, use_container_width=True)

# ============================================================
# ROW 6: MATCH PREDICTOR (ML MODEL)
# ============================================================
import pickle
import numpy as np

st.markdown("---")
st.subheader("🤖 Match Winner Predictor")
st.markdown("Predict the likely winner based on teams, toss and venue")

# Load the saved model and encoders
@st.cache_resource  # cache so it loads only once
def load_model():
    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/le_team.pkl', 'rb') as f:
        le_team = pickle.load(f)
    with open('models/le_venue.pkl', 'rb') as f:
        le_venue = pickle.load(f)
    with open('models/le_toss.pkl', 'rb') as f:
        le_toss = pickle.load(f)
    return model, le_team, le_venue, le_toss

model, le_team, le_venue, le_toss = load_model()

# Get list of all teams and venues for dropdowns
all_teams_list = sorted(le_team.classes_.tolist())
all_venues_list = sorted(le_venue.classes_.tolist())

# Create input form with 3 columns
pred_col1, pred_col2, pred_col3 = st.columns(3)

with pred_col1:
    team1 = st.selectbox("🏏 Team 1", all_teams_list, index=all_teams_list.index('Mumbai Indians'))
    team2 = st.selectbox("🏏 Team 2", all_teams_list, index=all_teams_list.index('Chennai Super Kings'))

with pred_col2:
    toss_winner = st.selectbox("🪙 Toss Winner", [team1, team2])
    toss_decision = st.selectbox("📋 Toss Decision", ['bat', 'field'])

with pred_col3:
    venue = st.selectbox("🏟️ Venue", all_venues_list)

# Predict button
if st.button("🔮 Predict Winner", use_container_width=True):
    try:
        # Encode inputs — convert text to numbers for the model
        input_data = pd.DataFrame({
            'team1_enc': [le_team.transform([team1])[0]],
            'team2_enc': [le_team.transform([team2])[0]],
            'toss_winner_enc': [le_team.transform([toss_winner])[0]],
            'toss_decision_enc': [le_toss.transform([toss_decision])[0]],
            'venue_enc': [le_venue.transform([venue])[0]]
        })

        # Get prediction and probability
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)
        predicted_winner = le_team.inverse_transform(prediction)[0]

        # Get confidence score for the predicted team
        team_index = list(model.classes_).index(prediction[0])
        confidence = probability[0][team_index] * 100

        # Show result
        st.success(f"🏆 Predicted Winner: **{predicted_winner}**")

        # Confidence bar
        st.metric("Model Confidence", f"{confidence:.1f}%")

        # Show both teams probability
        prob_col1, prob_col2 = st.columns(2)
        with prob_col1:
            try:
                t1_idx = list(model.classes_).index(le_team.transform([team1])[0])
                t1_prob = probability[0][t1_idx] * 100
                st.metric(f"{team1}", f"{t1_prob:.1f}%")
            except:
                st.metric(f"{team1}", "N/A")

        with prob_col2:
            try:
                t2_idx = list(model.classes_).index(le_team.transform([team2])[0])
                t2_prob = probability[0][t2_idx] * 100
                st.metric(f"{team2}", f"{t2_prob:.1f}%")
            except:
                st.metric(f"{team2}", "N/A")

        st.caption("⚠️ Note: Cricket is unpredictable! This model uses historical toss and venue patterns only.")

    except Exception as e:
        st.error(f"Prediction error: {e}")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("Built with ❤️ using Python, Pandas, SQLite & Streamlit | IPL Data 2008-2024")