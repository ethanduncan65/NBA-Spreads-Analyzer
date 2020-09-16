#!/usr/bin/env python
# coding: utf-8

# ![](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4eed7459-e8ff-4707-83fc-eb3dc361ca18/d5e2ndd-6a2f037e-6b16-4805-9cdc-0a4a7cb5e983.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzRlZWQ3NDU5LWU4ZmYtNDcwNy04M2ZjLWViM2RjMzYxY2ExOFwvZDVlMm5kZC02YTJmMDM3ZS02YjE2LTQ4MDUtOWNkYy0wYTRhN2NiNWU5ODMuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.jTxT7BPw_Ng4jCefLfpGdo_WXYNWtYGLvHUir9MeIqs)

# # NBA Spreads Analyzer

# In[1]:


# Dependencies for data manipulation, widgets, and plotting
import pandas as pd
import ipywidgets as widgets
import plotly.graph_objects as go
# Dependencies needed for the NBA API
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder


# In[2]:


# Create dropdown menu widget for user to select team 
widgetTeam = widgets.Dropdown(
    options=['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'],
    description='Select Team:',
    disabled=False,
)
# Display the widget
display(widgetTeam)


# In[3]:


# Query all teams
nba_teams = teams.get_teams()
# Select the team id needed for the next api call 
selectedTeamName = [team for team in nba_teams if team['abbreviation'] == widgetTeam.value][0]
selectedTeamID = selectedTeamName['id']
# Query for games where the selected team were playing (all seasons available)
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=selectedTeamID)
# The first DataFrame of those returned is what we want
games = gamefinder.get_data_frames()[0]
# Display the first 25 rows of the df
print("dataframe of games for all seasons:")
games.head(25)


# In[4]:


# Store the current season id to parse the full df
currentSeasonID = '22019'
currentSeasonMatchups = []
currentSeasonDifferentials = []

# Compile the lists for matchup titles and differentials associated with each game
for i in range(0, 100):
    # Once the loop hits pre-season games in the df, it will break 
    if((str(games.iloc[i]['SEASON_ID'])) != currentSeasonID):
        break
    # Pull the following fields to be used for the plot
    i_gameDate = games.iloc[i]['GAME_DATE']
    i_matchup = games.iloc[i]['MATCHUP']
    i_gameName = i_gameDate + " " + i_matchup
    i_differential = games.iloc[i]['PLUS_MINUS']
    # Add the name & differential for each game to the respective lists which will serve as data vectors for our plot below
    currentSeasonMatchups.append(i_gameName)
    currentSeasonDifferentials.append(i_differential)
    
# Create list of colors based on postive or negative differential 
barColors = []
# Loop through the list of game differentials and assign colors accordingly
for k in range(0, len(currentSeasonDifferentials)):
    k_differential = currentSeasonDifferentials[k]
    # If the differential is positive, we want the bar to be yellowgreen
    if(k_differential > 0): 
        barColors.append('yellowgreen')
    # If the differential is negative, we want the bar to be crimson 
    else:
        barColors.append('crimson')

# Get the team name for the plot title 
teamName = games.iloc[0]['TEAM_NAME']

print("Number of games in current season: ", len(currentSeasonDifferentials))

# Plot the differentials
fig = go.Figure(data=[go.Bar(
    x=currentSeasonDifferentials,
    y=currentSeasonMatchups,
    orientation='h',
    marker_color=barColors # marker color can be a single color value or an iterable
)])
fig.update_layout(title_text=teamName)


# In[10]:


# See if we can create button to download the df? --> this is possible 
# Use same article for the interactive dashboard stuff
games.to_csv('Celtics Game Log Test.csv')
# How can we export the plot? (can it retain interactivity? Can we open in new tab?)

