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
    # TODO: create dict from leagues -> avail. seasons
    #       check if we are past june -> season is finished
    
    

    # CONSTRUCTOR

    def __init__(self):
        """Crawler class constructor"""
        self.dict = {}
        self.all_teams = pd.DataFrame()
        self.all_matches = pd.DataFrame()
        self.all_match_results = pd.DataFrame()
        self.all_match_scores = pd.DataFrame()
        self.cut_teams = pd.DataFrame()
        self.cut_matches = pd.DataFrame()
        self.cut_match_results = pd.DataFrame()
        self.cut_match_scores = pd.DataFrame()

        self.available_leagues = [1,2,3]
        self.first_league_available_seasons = np.arange(2002,datetime.datetime.now().year)
        self.second_league_available_seasons = np.arange(2006,datetime.datetime.now().year)
        self.third_league_available_seasons = np.arange(2008,datetime.datetime.now().year)

    def get_available_years_for_leagues(self):
        # TODO: return leagues, seasons and size of yeararray
        self.dict = {1: {'name': '1. Bundesliga', 'seasons': self.first_league_available_seasons, 'size': self.first_league_available_seasons.size, 'matchdays': 34},
                    2: {'name': '2. Bundesliga', 'seasons': self.second_league_available_seasons, 'size': self.second_league_available_seasons.size, 'matchdays': 34},
                    3: {'name': '3. Liga', 'seasons': self.third_league_available_seasons, 'size': self.third_league_available_seasons.size, 'matchdays': 38}
               }
        return dict

    #
    #   PRIVATE API FUNCTIONS BELOW
    #   
 
    def get_teams_from_API(self, bl_league, year):
        """Gets and saves the data of available teams from API. Input Format: <int>, <YYYY> example: (1,2020)"""
        response = requests.get(self.api_teams_url.format(bl_league,year))
        # TODO: proper errorcode
        if response.status_code != 200:
            return -1
        teams = pd.read_json(response.content)[self.api_teams_content_columns]
        teams.columns = self.uniform_teams_columns
        teams.to_csv(self.uniform_teams_database_path.format(bl_league,year), index=False)
        return teams

    def get_matches_from_year_from_API(self, bl_league, year):
        """Gets and saves Data of all matches played in one league in one season from API. Input Format: <int, YYYY> example: (1,2020)"""
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
        # TODO: download all pictures for teams listed in self.all_teams, remove parameter teams_data
        """gets team icon images for all teams in the Inputted uniform team data frame"""
        # TODO: check if Pics already saved
        for index, row in teams_data.iterrows():
            # TODO: handle icons that are .svg instead of .png (ID=9 and ID=95)
            try:
                urllib.request.urlretrieve(row["team_icon_url"], self.icons_path.format(row["team_id"]))
            except Exception:
                continue
    def init_cut_db(self):
        self.cut_matches = self.all_matches
        self.cut_match_results = self.all_match_results
        self.cut_match_scores = self.all_match_scores
        return 1


    #   
    #   PUBLIC FUNCTIONS BELOW
    #

    def get_teams(leagues, seasons):
        # TODO: concatenate TeamsDB from leagues/seasons and download all Pictures from the teams.
        #       CHECK REDUNDANCY
        # work with self.get_teams_from_api(), check if csv is saved, save all teams from one league/year seperately
        # save big DB to self.all_teams
        return None



    def create_dataset_from_leagues_and_years(self, bl_leagues, years):
        """Extracts the desired data from multiple leagues/years and saves it internaly. Inputformat: (int[],int[])"""
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
                    matches, results, goals = self.get_matches_from_year_from_API(league, year)
                # concatenate data and drop old indices
                dataset_matches = pd.concat([dataset_matches, matches])
                dataset_results = pd.concat([dataset_results, results])
                dataset_goals = pd.concat([dataset_goals, goals])
        # TODO: return only status code
        self.all_matches = dataset_matches
        self.all_match_results = dataset_results
        self.all_match_scores = dataset_goals
        return 1
    #
    #   Functions for cutting and extracting data from big DB
    #
    def get_team_dicts(self, bl_league, year):
        """returns 2 dictionarys, the first maps team_id to team_name, the second is vice versa"""
        # TODO: work with self.all_teams
        if os.path.isfile(self.uniform_teams_database_path):
            teams_db = pd.read_csv(self.uniform_teams_database_path)
        else:
            teams_db = self.get_teams_from_API(bl_league, year)
        # create dicts out of 2 columns, 'TeamId' and 'TeamName'
        id_to_team = pd.Series(teams_db.team_name.values,index=teams_db.team_id).to_dict()
        team_to_id = pd.Series(teams_db.team_id.values,index=teams_db.team_name).to_dict()
        return id_to_team, team_to_id

    def extract_matchup_history_1v1(self, team_home_id, team_guest_id):
        """extracts all matches containing the two inputted teams and returns them in a seperate dataframe
        does not alter original dataframe."""
        self.cut_matches = self.all_matches.loc[(self.all_matches['team_home_id'] == team_home_id) & (self.all_matches['team_guest_id'] == team_guest_id)
                                                | (self.all_matches['team_home_id'] == team_guest_id) & (self.all_matches['team_guest_id'] == team_home_id)]
        self.cut_match_results = self.all_match_results[self.all_match_results['match_id'].isin(self.cut_matches['match_id'])]
        self.cut_match_scores = self.all_match_scores[self.all_match_scores['match_id'].isin(self.cut_matches['match_id'])]
        
        return 1
    def extract_matchdays(self, days):
        # TODO: noch nicht sicher wie tage übergeben werden,
        # also extract results and scores for all matches
        dataset = pd.DataFrame()
        for day in days:
            matches_on_day = self.cut_matches.loc[self.cut_matches['matchday'] == day]
            dataset = pd.concat([dataset, matches_on_day])
        self.cut_matches
        return 1

    # Function for Data grabbing for Model
    def get_data_for_model(self, leagues, seasons, matchdays):
        # TODO:
        return 1
    # Function for Data grabbing for Algorithm
    def get_data_for_algo(self, leagues, seasons, matchdays, team_home_id, team_guest_id):
        self.init_cut_db()
        if((team_home_id != 0) & (team_guest_id != 0)):
            self.extract_matchup_history_1v1(team_home_id, team_guest_id)
        
        return self.cut_matches, self.cut_match_results, self.cut_match_scores
# %%
if __name__ == '__main__':
    data = pd.DataFrame()
    crawler = Crawler()
    crawler.create_dataset_from_leagues_and_years([1],[2020,2019,2018,2017])
    crawler.init_cut_db()
    print(crawler.all_matches.head(5))
    #print(crawler.all_match_results.head(5))
    #print(crawler.all_match_scores.head(5))
    matches, results, scores = crawler.get_data_for_algo(0,0,0,16,87)
    print(matches.head(5))
# %%
if __name__ == '__main__':
    api_match_content_columns = ['MatchID', 'MatchDateTimeUTC', 'Group.GroupOrderID', 'Team1.TeamId', 'Team2.TeamId']
    api_results_content_columns = ['ResultID', 'PointsTeam1', 'PointsTeam2', 'ResultOrderID', 'MatchID']
    api_score_content_columns = ['GoalID','ScoreTeam1','ScoreTeam2','GoalGetterID',
                                    'GoalGetterName', 'IsOvertime', 'MatchID']
    uniform_match_content_columns = ['match_id', 'match_date_time_utc', 'matchday', 'team_home_id', 'team_guest_id']
    uniform_result_content_columns = ['result_id', 'points_home', 'points_guest', 'result_type_id', 'match_id']

    years = np.arange(2009,2010)
    leagues = [1,2]

    response = requests.get("https://www.openligadb.de/api/getmatchdata/bl{}/{}".format(1,2019))
    matches = pd.json_normalize(response.json())
    matches = matches[api_match_content_columns]
    matches.columns = uniform_match_content_columns

    matches = matches[matches['match_id'] == 58577]

    match_results = pd.json_normalize(response.json(), record_path='MatchResults', meta='MatchID')
    match_results = match_results[api_results_content_columns]
    match_results.columns = uniform_result_content_columns
    results = match_results[match_results['match_id'].isin(matches['match_id'])]
    results


    #match_scores = pd.json_normalize(response.json(), record_path='Goals', meta='MatchID')
    #print(match_scores)


# %%
