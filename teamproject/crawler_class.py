#%%

import pandas as pd
import json
import requests
import os.path
import urllib.request

class Crawler(object):
    # PATHs for uniform Data
    uniform_teams_database_path = r'./data/uniform_teams_bl{}_{}.csv'
    uniform_matches_database_path = r'./data/uniform_matches_bl{}_{}.csv'
    uniform_match_results_database_path = r'./data/uniform_match_results_bl{}_{}.csv'
    uniform_match_score_database_path = r'./data/uniform_match_score_bl{}_{}.csv'
    uniform_season_matches_db_path = r'./data/matches_bl{}_{}.csv'
    uniform_season_results_db_path = r'./data/matches_bl{}_{}_results.csv'
    uniform_season_goals_db_path = r'./data/matches_bl{}_{}_goals.csv'

    #COLUMNNAMES for uniform Data
    uniform_teams_columns = ['team_id', 'team_name', 'team_icon_url']
    uniform_match_content_columns = ['match_id', 'match_date_time_utc', 'matchday', 'team_home_id', 'team_guest_id']
    uniform_result_content_columns = ['result_id', 'points_home', 'points_guest', 'result_type_id', 'match_id']
    uniform_score_content_columns = ['goal_id','scores_home','scores_guest','scorer_id',
                                     'scorer_name', 'is_overtime', 'match_id']

    #PATHs for miscellaneous Data
    icons_path = r'./icons/{}.png'
    table_db_path = r'./data/table_bl{}_{}.csv'

    # URLs for OpenLigaDB API
    api_teams_url = "https://www.openligadb.de/api/getavailableteams/bl{}/{}"
    api_matches_lg_ss_url = "https://www.openligadb.de/api/getmatchdata/bl{}/{}"
    api_matches_1v1_url = "https://www.openligadb.de/api/getmatchdata/{}/{}"
    api_nextmatch_lg_tm_url = "https://www.openligadb.de/api/getnextmatchbyleagueteam/{}/{}"
    api_table_lg_yr_url = "https://www.openligadb.de/api/getbltable/bl{}/{}"
    
    # COLUMNNAMES for OpenLigaDB API
    api_teams_content_columns = ['TeamId', 'TeamName', 'TeamIconUrl']
    api_match_content_columns = ['MatchID', 'MatchDateTimeUTC', 'Group.GroupOrderID', 'Team1.TeamId', 'Team2.TeamId']
    api_result_content_columns = ['ResultID', 'PointsTeam1', 'PointsTeam2', 'ResultOrderID', 'MatchID']
    api_score_content_columns = ['GoalID','ScoreTeam1','ScoreTeam2','GoalGetterID',
                                'GoalGetterName', 'IsOvertime', 'MatchID']

    # METADATA for OpenLigaDB API
    api_meta_data = "MatchID"

    #SEASONS and LEAGUES available, hardcoded:
    # TODO: add available leagues and seasons
    available_leagues = []
    available_seasons = []

    # CONSTRUCTOR

    def __init__(self):
        """Crawler class constructor"""
        return Crawler.available_leagues, Crawler.available_seasons

    #   PRIVATE API FUNCTIONS BELOW
    #   
    #   PRIVATE API FUNCTIONS BELOW
    #
    #   PRIVATE API FUNCTIONS BELOW

    def get_teams_from_API(self, bl_league, year):
        """"""
        response = requests.get(Crawler.api_teams_url.format(bl_league,year))
        # TODO: proper errorcode
        if response.status_code != 200:
            return -1
        teams = pd.read_json(response.content)[Crawler.api_teams_content]
        teams.columns = Crawler.uniform_teams_columns
        #teams.to_csv(teams_db_path.format(bl_league,year), index=False)
        return teams

    def get_all_matches_for_year_from_api(bl_league, year):
        """"""
        response = requests.get(Crawler.api_matches_lg_ss_url.format(bl_league,year))
        # TODO: proper errorcode
        if response.status_code != 200:
            return -1
        data_json = response.json()

        matches = pd.json_normalize(data_json)[Crawler.uniform_match_content_columns]
        matches.columns = Crawler.uniform_match_content_columns

        match_results = pd.json_normalize(data_json, record_path='MatchResults', meta=Crawler.api_meta_data)[Crawler.api_result_content_columns]
        match_results.columns = Crawler.uniform_result_content_columns
        # TODO: concatenate score_home and score_guest to a tuple (score_home, score_guest) in one column 'temp_score'
        match_scores = pd.json_normalize(data_json, record_path='Goals', meta=Crawler.api_meta_data)[Crawler.api_score_content_columns]
        match_scores.columns = Crawler.uniform_score_content_columns
        # save datasets as csv
        # TODO: concatenate data sets?
        matches.to_csv(Crawler.uniform_season_matches_db_path.format(bl_league,year), index=False)
        match_results.to_csv(Crawler.uniform_season_results_db_path(bl_league,year), index=False)
        match_scores.to_csv(Crawler.uniform_season_goals_db_path.format(bl_league,year), index=False)
        return matches, match_results, match_scores

    def get_next_match_from_API(league_id, team_id):
        """"""
        # <BundesLiga, Saison, LeagueID> 1 2020 4442; 2 2020 4443; 3 2020 4444
        response = requests.get(Crawler.api_nextmatch_lg_tm_url.format(league_id, team_id))
        # TODO: proper errorcode
        if response.status_code != 200:
            return -1
        match = pd.json_normalize(response.json())
        # extract necessary data
        match = match[Crawler.api_match_content_columns]
        match.columns = Crawler.uniform_match_content_columns
        return match

    def get_team_icons_from_wiki(teams_data):
        """"""
    # TODO: check if Pics already saved
    for index, row in teams_data.iterrows():
        # TODO: handle icons that are .svg instead of .png (ID=9 and ID=95)
        try:
            urllib.request.urlretrieve(row["team_icon_url"], Crawler.icons_path.format(row["team_id"]))
        except Exception:
            continue

    #   PUBLIC FUNCTIONS BELOW
    #   
    #   PUBLIC FUNCTIONS BELOW
    #
    #   PUBLIC FUNCTIONS BELOW
    
    def get_team_dicts(bl_league, year):
        """"""
        if os.path.isfile(Crawler.uniform_teams_database_path):
            teams_db = pd.read_csv(Crawler.uniform_teams_database_path)
        else:
            teams_db = Crawler.get_teams_from_API(bl_league, year)
        # create dicts out of 2 columns, 'TeamId' and 'TeamName'
        id_to_team = pd.Series(teams_db.team_name.values,index=teams_db.team_id).to_dict()
        team_to_id = pd.Series(teams_db.team_id.values,index=teams_db.team_name).to_dict()
        return id_to_team, team_to_id

    
# %%
crawler = Crawler()
crawler2 = Crawler()

teams = crawler.get_teams_from_API(1,2020)
teams.head(5)

# %%
