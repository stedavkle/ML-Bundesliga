# %%

import pandas as pd
import json
import requests
import os.path
import urllib.request
import numpy as np
import datetime

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
    available_leagues = [1,2,3]
    available_seasons = np.arange(1950,datetime.datetime.now().year)

    # CONSTRUCTOR

    def __init__(self):
        """Crawler class constructor"""
        #return self.available_leagues, self.available_seasons



    #   PRIVATE API FUNCTIONS BELOW
    #   
    #   PRIVATE API FUNCTIONS BELOW
    #
    #   PRIVATE API FUNCTIONS BELOW

    def get_teams_from_API(self, bl_league, year):
        """gets the team data for one season and league. Input Format: <Bundesliga(as simple number), Year> example: (1,2020)"""
        response = requests.get(self.api_teams_url.format(bl_league,year))
        # TODO: proper errorcode
        if response.status_code != 200:
            return -1
        teams = pd.read_json(response.content)[self.api_teams_content_columns]
        teams.columns = self.uniform_teams_columns
        teams.to_csv(self.uniform_teams_database_path.format(bl_league,year), index=False)
        return teams

    def get_all_matches_from_year_from_api(self, bl_league, year):
        """gets all played matches for one season and league. Input Format: <Bundesliga(as simple number), Year> example: (1,2020)"""
        response = requests.get(self.api_matches_lg_ss_url.format(bl_league,year))
        # TODO: proper errorcode
        if response.status_code != 200:
            return -1
        data_json = response.json()

        matches = pd.json_normalize(data_json)[self.api_match_content_columns]
        matches.columns = self.uniform_match_content_columns

        match_results = pd.json_normalize(data_json, record_path='MatchResults', meta=self.api_meta_data)[self.api_result_content_columns]
        match_results.columns = self.uniform_result_content_columns
        # TODO: concatenate score_home and score_guest to a tuple (score_home, score_guest) in one column 'temp_score'
        match_scores = pd.json_normalize(data_json, record_path='Goals', meta=self.api_meta_data)[self.api_score_content_columns]
        match_scores.columns = self.uniform_score_content_columns
        # save datasets as csv
        # TODO: concatenate data sets?
        matches.to_csv(self.uniform_season_matches_db_path.format(bl_league,year), index=False)
        match_results.to_csv(self.uniform_season_results_db_path.format(bl_league,year), index=False)
        match_scores.to_csv(self.uniform_season_goals_db_path.format(bl_league,year), index=False)
        return matches, match_results, match_scores

    def get_next_match_from_API(self, league_id, team_id):
        """gets the next upcoming match for one team, Input: <league_id, team_id> example: (4442, 83)"""
        # <BundesLiga, Saison, LeagueID> 1 2020 4442; 2 2020 4443; 3 2020 4444
        response = requests.get(self.api_nextmatch_lg_tm_url.format(league_id, team_id))
        # TODO: proper errorcode
        if response.status_code != 200:
            return -1
        match = pd.json_normalize(response.json())
        # extract necessary data
        match = match[self.api_match_content_columns]
        match.columns = self.uniform_match_content_columns
        return match

    def get_team_icons_from_wiki(self, teams_data):
        """gets team icon images for all teams in the Inputted uniform team data frame"""
        # TODO: check if Pics already saved
        for index, row in teams_data.iterrows():
            # TODO: handle icons that are .svg instead of .png (ID=9 and ID=95)
            try:
                urllib.request.urlretrieve(row["team_icon_url"], self.icons_path.format(row["team_id"]))
            except Exception:
                continue

    #   PUBLIC FUNCTIONS BELOW
    #   
    #   PUBLIC FUNCTIONS BELOW
    #
    #   PUBLIC FUNCTIONS BELOW
    
    def get_team_dicts(self, bl_league, year):
        """returns 2 dicts, the first mapping id to teams, the second teams to id"""
        if os.path.isfile(self.uniform_teams_database_path):
            teams_db = pd.read_csv(self.uniform_teams_database_path)
        else:
            teams_db = self.get_teams_from_API(bl_league, year)
        # create dicts out of 2 columns, 'TeamId' and 'TeamName'
        id_to_team = pd.Series(teams_db.team_name.values,index=teams_db.team_id).to_dict()
        team_to_id = pd.Series(teams_db.team_id.values,index=teams_db.team_name).to_dict()
        return id_to_team, team_to_id

    def get_dataset_of_matches_from_leagues_and_years(self, bl_leagues, years):
        """returns all matches for the inputted arrays for leagues and years, league input format is Bundesliga-Number (e.g: 1, 2, 3)"""
        dataset_matches = pd.DataFrame()
        dataset_results = pd.DataFrame()
        dataset_goals = pd.DataFrame()
        # for all leagues in every year get matchdata
        for league in bl_leagues:
            for year in years:
                # format path strings
                matches_path = self.uniform_season_matches_db_path.format(league,year)
                results_path = self.uniform_season_results_db_path.format(league,year)
                goals_path = self.uniform_season_goals_db_path.format(league,year)
                # check if data is stored, if not get from API
                if (os.path.isfile(matches_path)) & (os.path.isfile(results_path)) & (os.path.isfile(goals_path)):
                    matches = pd.read_csv(self.uniform_season_matches_db_path.format(league,year))
                    results = pd.read_csv(self.uniform_season_results_db_path.format(league,year))
                    goals = pd.read_csv(self.uniform_season_goals_db_path.format(league,year))
                else:
                    matches, results, goals = self.get_all_matches_from_year_from_api(league, year)
                # concatenate data and drop old indices
                dataset_matches = pd.concat([dataset_matches, matches])
                dataset_results = pd.concat([dataset_results, results])
                dataset_goals = pd.concat([dataset_goals, goals])
        return dataset_matches, dataset_results, dataset_goals

    def extract_matchup_history_1v1(self, team_home_id, team_guest_id, data):
        """"extracts all matches containing the two inputted teams and returns them in a seperate dataframe
        does not alter original dataframe."""
        dataset = data.loc[(data['team_home_id'] == team_home_id) & (data['team_guest_id'] == team_guest_id)
                            | (data['team_home_id'] == team_guest_id) & (data['team_guest_id'] == team_home_id)]
        return dataset
# %%
if __name__ == '__main__':


    years = np.arange(2009,2010)
    leagues = [1,2]

    crawler = Crawler()

    #teams = crawler.get_teams_from_API(1,2020)
    matches, match_results, match_scores = crawler.get_dataset_of_matches_from_leagues_and_years([1], [2003])
    dataset = crawler.extract_matchup_history_1v1(16, 87, matches)
# %%
api_match_content_columns = ['MatchID', 'MatchDateTimeUTC', 'Group.GroupOrderID', 'Team1.TeamId', 'Team2.TeamId']
api_results_content_columns = ['ResultID', 'PointsTeam1', 'PointsTeam2', 'ResultOrderID', 'MatchID']
api_score_content_columns = ['GoalID','ScoreTeam1','ScoreTeam2','GoalGetterID',
                                'GoalGetterName', 'IsOvertime', 'MatchID']

years = np.arange(2009,2010)
leagues = [1,2]

response = requests.get("https://www.openligadb.de/api/getmatchdata/bl{}/{}".format(2,2008))
matches = pd.json_normalize(response.json())
#matches[api_match_content_columns]
match_results = pd.json_normalize(response.json(), record_path='MatchResults', meta='MatchID')
#match_results[api_results_content_columns]
match_scores = pd.json_normalize(response.json(), record_path='Goals', meta='MatchID')
#match_scores[api_score_content_columns]

# %%
