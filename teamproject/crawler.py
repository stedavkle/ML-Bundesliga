#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import json
import requests
import os.path
import urllib.request

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.max_rows', 80)
pd.set_option('display.width', 200)

# PATHs for Data
teams_db_path = r'./data/teams_bl{}_{}.csv'
icons_path = "./icons/{}.png"
table_db_path = r'./data/table_bl{}_{}.csv'
season_matches_db_path = r'./data/matches_bl{}_{}.csv'
season_results_db_path = r'./data/matches_bl{}_{}_results.csv'
season_goals_db_path = r'./data/matches_bl{}_{}_goals.csv'
matchup_matches_db_path = r'./data/matches_{}_{}.csv'
matchup_results_db_path = r'./data/matches_{}_{}.csv'
matchup_goals_db_path = r'./data/matches_{}_{}.csv'

# URLs for API
api_teams_url = "https://www.openligadb.de/api/getavailableteams/bl{}/{}"
api_matches_lg_ss_url = "https://www.openligadb.de/api/getmatchdata/bl{}/{}"
api_matches_1v1_url = "https://www.openligadb.de/api/getmatchdata/{}/{}"
api_nextmatch_lg_tm_url = "https://www.openligadb.de/api/getnextmatchbyleagueteam/{}/{}"
api_table_lg_yr_url = "https://www.openligadb.de/api/getbltable/bl{}/{}"

# Parameters for necessary Data in dataset
table_content = ['TeamInfoId',
                 'Points', 'OpponentGoals',	'Goals',
                 'Matches', 'Won', 'Lost', 'Draw', 'GoalDiff']
match_content = ['MatchID','LeagueId','MatchDateTimeUTC','MatchIsFinished',
                 'Team1.TeamId','Team2.TeamId','Location.LocationID']
results_content = ['MatchID', 'Team1.TeamId','Team2.TeamId', 'PointsTeam1','PointsTeam2','ResultTypeID']
goals_content = ['MatchID','GoalID','ScoreTeam1','ScoreTeam2','GoalGetterID','IsOwnGoal']

meta_data = ['MatchID', ['Team1', 'TeamId'], ['Team2', 'TeamId']]

# In[26]:


def getTeamsFromAPI(bl_league, year):
    response = requests.get(api_teams_url.format(bl_league,year))
    # TODO: proper errorcode
    if response.status_code != 200:
        return -1
    teams = pd.read_json(response.content)
    teams.to_csv(teams_db_path.format(bl_league,year), index=False)
    return teams


# In[27]:


def getBlTableFromAPI(bl_league, year):
    response = requests.get(api_table_lg_yr_url.format(bl_league,year))
    # TODO: proper errorcode
    if response.status_code != 200:
        return -1
    table = pd.read_json(response.content)[table_content]
    table.to_csv(table_db_path.format(bl_league,year), index=False)
    return table


# In[28]:


def getAllMatchesOfYearFromAPI(bl_league, year):
    response = requests.get(api_matches_lg_ss_url.format(bl_league,year))
    # TODO: proper errorcode
    if response.status_code != 200:
        return -1
    data_json = response.json()
    # split and extract necessary data
    # TODO: fix error where 'Location' is always None
    #       and Location.LocationId not present (occuring on year 2018 league 3)
    matches = pd.json_normalize(data_json)[match_content]
    match_results = pd.json_normalize(data_json, record_path='MatchResults',
                                      meta=meta_data)[results_content]
    match_goals = pd.json_normalize(data_json, record_path='Goals',
                                    meta=meta_data)[goals_content]
    # save datasets as csv
    matches.to_csv(season_matches_db_path.format(bl_league,year), index=False)
    match_results.to_csv(season_results_db_path.format(bl_league,year), index=False)
    match_goals.to_csv(season_goals_db_path.format(bl_league,year), index=False)
    return matches, match_results, match_goals


# In[41]:


def getMatchupHistoryFromAPI(team1_id, team2_id):
    
    # format paths to store data
    matches_path = matchup_matches_db_path.format(team1_id, team2_id)
    results_path = matchup_results_db_path.format(team1_id, team2_id)
    goals_path = matchup_goals_db_path.format(team1_id, team2_id)
    api_url = api_matches_1v1_url.format(team1_id, team2_id)
    # check if data is stored, otherwise use API
    response = requests.get(api_url)
    # TODO: proper errorcode
    if response.status_code != 200:
        return -1
    data_json = response.json()
    # split and extract necessary data
    matches = pd.json_normalize(data_json)[match_content]
    match_results = pd.json_normalize(data_json,
                                      record_path='MatchResults',
                                      meta=meta_data, errors='ignore')[results_content]
    match_goals = pd.json_normalize(data_json,
                                    record_path='Goals',
                                    meta=meta_data)[goals_content]
    # save datasets as csv
    matches.to_csv(matches_path)
    match_results.to_csv(results_path)
    match_goals.to_csv(goals_path)
    return matches, match_results, match_goals


# In[42]:


def getNextMatchFromAPI(league_id, team_id):
    # 1.BL 2020 ID4442, 2.BL 2020 ID4443, 3.BL 2020 ID4444
    response = requests.get(api_nextmatch_lg_tm_url.format(league_id, team_id))
    # TODO: proper errorcode
    if response.status_code != 200:
        return -1
    match = pd.json_normalize(response.json())
    # extract necessary data
    match = data[match_content]
    return match


# In[43]:


def getTeamIconsFromWiki(teams_data):
    # TODO: check if Pics already saved
    for index, row in teams.iterrows():
        # TODO: handle icons that are .svg instead of .png (ID=9 and ID=95)
        try:
            urllib.request.urlretrieve(row["TeamIconUrl"], icons_path.format(row["TeamId"]))
        except Exception:
            continue


# In[44]:


# All functions that should be used from outside


# In[45]:


def getTeams(bl_leagues, year):
    db_path = teams_db_path.format(bl_league,year)
    if os.path.isfile(db_path):
        teams = pd.read_csv(db_path)
    else:
        teams = getTeamsFromAPI(bl_league, year)
    return teams


# In[46]:


def getTeamDicts(bl_league, year):
    if os.path.isfile(teams_db_path):
        teams_db = pd.read_csv(teams_db_path)
    else:
        teams_db = getTeamsFromAPI(bl_league, year)
    # create dicts out of 2 columns, 'TeamId' and 'TeamName'
    id_to_team = pd.Series(teams_db.TeamName.values,index=teams_db.TeamId).to_dict()
    team_to_id = pd.Series(teams_db.TeamId.values,index=teams_db.TeamName).to_dict()
    return id_to_team, team_to_id


# In[47]:


def getBlTable(bl_league, year):
    db_path = table_db_path.format(bl_league,year)
    if os.path.isfile(db_path):
        table = pd.read_csv(db_path)
    else:
        table = getBlTableFromAPI(bl_league, year)
    return table


# In[48]:


def getDatasetOfMatchesFromLeaguesAndYears(bl_leagues, years):
    dataset_matches = pd.DataFrame()
    dataset_results = pd.DataFrame()
    dataset_goals = pd.DataFrame()
    # for all leagues in every year get matchdata
    for league in bl_leagues:
        for year in years:
            # format path strings
            matches_path = season_matches_db_path.format(league,year)
            results_path = season_results_db_path.format(league,year)
            goals_path = season_goals_db_path.format(league,year)
            # check if data is stored, if not get from API
            if (os.path.isfile(matches_path)) & (os.path.isfile(results_path)) & (os.path.isfile(goals_path)):
                matches = pd.read_csv(season_matches_db_path.format(league,year))
                results = pd.read_csv(season_results_db_path.format(league,year))
                goals = pd.read_csv(season_goals_db_path.format(league,year))
            else:
                matches, results, goals = getAllMatchesOfYearFromAPI(league, year)
            # concatenate data and drop old indices
            dataset_matches = pd.concat([dataset_matches, matches])
            dataset_results = pd.concat([dataset_results, results])
            dataset_goals = pd.concat([dataset_goals, goals])
            # drop old indices
            
    return dataset_matches, dataset_results, dataset_goals


# In[49]:


def getNextMatch(league_id, team_id):
    # TODO:
    return


# In[50]:


def getMatchupHistory1vX(team_id, teams_ids):
    # TODO:
    return


# In[51]:


def downloadTeamIcons():
    # TODO:
    return


# In[53]:

# for testing inside the script
if __name__ == '__main__':
    bl_league = 1
    year = 2020
    league_id = 4222

    print("TEAMS DATA STRUCTURE:")
    teams = getTeams(bl_league, year)
    print(teams.head(3), end='\n\n')

    print("ID <=> TeamName DICTS:")
    id_to_team, team_to_id = getTeamDicts(bl_league, year)
    print(str(team_to_id['VfB Stuttgart']) + ' : ' + id_to_team[16], end='\n\n')

    print("TABLE FROM LEAGUE")
    table = getBlTable(bl_league, year)
    print(table.head(3), end='\n\n')

    matches, results, goals = getDatasetOfMatchesFromLeaguesAndYears([1,2], [2020,2019,2018])
    print("MATCHES DATA STRUCTURE:")
    print(matches.head(3))
    print("RESULTS DATA STRUCTURE:")
    print(results.head(3))
    print("GOALS DATA STRUCTURE:")
    print(goals.head(3))


    matches, results, goals = getMatchupHistoryFromAPI(16,87)
    print(results.head(3))
    print(results[results['Team1.TeamId']==16]['PointsTeam1'])
    print("SUMME: ")
    print(results['PointsTeam1'].sum(axis=0))
