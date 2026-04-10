import pandas as pd

def load_data():
    matches = pd.read_csv('data/matches.csv')
    deliveries = pd.read_csv('data/deliveries.csv')

    team_name_fixes = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Kings XI Punjab': 'Punjab Kings',
        'Deccan Chargers': 'Sunrisers Hyderabad',
        'Rising Pune Supergiants': 'Rising Pune Supergiant',
        'Pune Warriors': 'Rising Pune Supergiant'
    }

    for col in ['team1', 'team2', 'winner', 'toss_winner']:
        matches[col] = matches[col].replace(team_name_fixes)

    for col in ['batting_team', 'bowling_team']:
        deliveries[col] = deliveries[col].replace(team_name_fixes)

    matches['result_margin'] = matches['result_margin'].fillna(0)
    deliveries['player_dismissed'] = deliveries['player_dismissed'].fillna('none')
    deliveries['dismissal_kind'] = deliveries['dismissal_kind'].fillna('none')
    deliveries['fielder'] = deliveries['fielder'].fillna('none')
    matches['season'] = pd.to_datetime(matches['date']).dt.year

    deliveries = deliveries.merge(
        matches[['id', 'season', 'venue']],
        left_on='match_id',
        right_on='id',
        how='left'
    )

    return matches, deliveries