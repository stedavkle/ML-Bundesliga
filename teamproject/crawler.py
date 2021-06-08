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

    # CONSTRUCTOR

    def __init__(self):
        """Crawler class constructor"""
        self.dict = {}
        self.teams = pd.DataFrame()
        self.matches = pd.DataFrame()
        self.results = pd.DataFrame()
        self.results = pd.DataFrame()

        # TODO: create dict from leagues -> avail. seasons
        #       check if we are past june -> season is finished
        self.available_leagues = [1,2,3]
        if(datetime.datetime.now().month >= 7):
            year = datetime.datetime.now().year+1
        else:
            year = datetime.datetime.now().year
        self.first_league_available_seasons = np.arange(2002,year)
        self.second_league_available_seasons = np.arange(2006,year)
        self.third_league_available_seasons = np.arange(2008,year)

    def get_available_seasons_for_leagues(self):
        """return leagues, seasons and size of yeararray"""
        self.dict = {1: {'name': '1. Bundesliga', 'seasons': self.first_league_available_seasons, 'size': self.first_league_available_seasons.size, 'matchdays': 34},
                    2: {'name': '2. Bundesliga', 'seasons': self.second_league_available_seasons, 'size': self.second_league_available_seasons.size, 'matchdays': 34},
                    3: {'name': '3. Liga', 'seasons': self.third_league_available_seasons, 'size': self.third_league_available_seasons.size, 'matchdays': 38}
               }
        return self.dict

    #
    #   PRIVATE API FUNCTIONS BELOW
    #   
 
    def get_teams_from_API(self, leagues, seasons):
        """Gets and saves the data of available teams from API. Input Format: <int>, <YYYY> example: (1,2020)"""
        for league in leagues:
            for season in seasons:
                response = requests.get(self.api_teams_url.format(league,season))
                # TODO: proper errorcode
                if response.status_code != 200:
                    return -1
                teams = pd.read_json(response.content)[self.api_teams_content_columns]
                teams.columns = self.uniform_teams_columns
                teams.to_csv(self.uniform_teams_database_path.format(league,season), index=False)
        return 1

    def get_matches_from_leagues_and_seasons_from_API(self, leagues, seasons):
        """Gets and saves Data of all matches played in gicen leagues/seasons from API. Input Format: <[int], [YYYY]> example: ([1],[2020,2019])"""
        for league in leagues:
            for season in seasons:
                response = requests.get(self.api_matches_lg_ss_url.format(league,season))
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
                matches.to_csv(self.uniform_season_matches_db_path.format(league,season), index=False)
                match_results.to_csv(self.uniform_season_results_db_path.format(league,season), index=False)
                match_scores.to_csv(self.uniform_season_goals_db_path.format(league,season), index=False)
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
        # TODO: download all pictures for teams listed in self.teams, remove parameter teams_data
        """gets team icon images for all teams in the Inputted uniform team data frame"""
        # TODO: check if Pics already saved
        for index, row in teams_data.iterrows():
            # TODO: handle icons that are .svg instead of .png (ID=9 and ID=95)
            try:
                urllib.request.urlretrieve(row["team_icon_url"], self.icons_path.format(row["team_id"]))
            except Exception:
                continue

    #   
    #   PUBLIC FUNCTIONS BELOW
    #

    def get_teams(leagues, seasons):
        # TODO: concatenate TeamsDB from leagues/seasons and download all Pictures from the teams.
        #       CHECK REDUNDANCY
        # work with self.get_teams_from_api(), check if csv is saved, save all teams from one league/year seperately
        # save big DB to self.teams
        
        return None



    def create_dataset_from_leagues_and_seasons(self, leagues, seasons, day_start, day_end):
        # TODO: needs parameter start/end-day for first/last season, cut first and last season
        """Extracts the desired data from multiple leagues/seasons and saves it internaly. Inputformat: (int[],int[])"""
        dataset_matches = pd.DataFrame()
        dataset_results = pd.DataFrame()
        dataset_goals = pd.DataFrame()
        # for all leagues in every year get matchdata
        for league in leagues:
            for season in seasons:
                # format path strings
                matches_path = self.uniform_season_matches_db_path.format(league,season)
                results_path = self.uniform_season_results_db_path.format(league,season)
                goals_path = self.uniform_season_goals_db_path.format(league,season)
                # check if data is stored, if not get from API
                # TODO: Try: Except: instead of if() else()
                if (os.path.isfile(matches_path)) & (os.path.isfile(results_path)) & (os.path.isfile(goals_path)):
                    matches = pd.read_csv(self.uniform_season_matches_db_path.format(league,season))
                    results = pd.read_csv(self.uniform_season_results_db_path.format(league,season))
                    goals = pd.read_csv(self.uniform_season_goals_db_path.format(league,season))
                else:
                    matches, results, goals = self.get_matches_from_leagues_and_seasons_from_API([league], [season])
                # concatenate data and drop old indices
                dataset_matches = pd.concat([dataset_matches, matches])
                dataset_results = pd.concat([dataset_results, results])
                dataset_goals = pd.concat([dataset_goals, goals])
        self.matches = dataset_matches
        self.results = dataset_results
        self.scores = dataset_goals
        return 1
    #
    #   Functions for cutting and extracting data from big DB
    #
    def get_team_dicts(self, bl_league, season):
        """returns 2 dictionarys, the first maps team_id to team_name, the second is vice versa"""
        # TODO: work with self.teams
        if os.path.isfile(self.uniform_teams_database_path):
            teams_db = pd.read_csv(self.uniform_teams_database_path)
        else:
            teams_db = self.get_teams_from_API([bl_league], [season])
        # create dicts out of 2 columns, 'TeamId' and 'TeamName'
        id_to_team = pd.Series(teams_db.team_name.values,index=teams_db.team_id).to_dict()
        team_to_id = pd.Series(teams_db.team_id.values,index=teams_db.team_name).to_dict()
        return id_to_team, team_to_id

    def extract_matchup_history(self, team_home_id, team_guest_id):
        """extracts all matches containing one or two teams and returns them in a seperate dataframe
        does not alter original dataframe."""
        if team_guest_id == 0:
            self.matches = self.matches.loc[(self.matches['team_home_id'] == team_home_id) | (self.matches['team_guest_id'] == team_home_id)] 
        else:
            self.matches = self.matches.loc[(self.matches['team_home_id'] == team_home_id) & (self.matches['team_guest_id'] == team_guest_id)
                                                    | (self.matches['team_home_id'] == team_guest_id) & (self.matches['team_guest_id'] == team_home_id)]
        self.results = self.results[self.results['match_id'].isin(self.matches['match_id'])]
        self.scores = self.scores[self.scores['match_id'].isin(self.matches['match_id'])]  
        return 1

    # Function for Data grabbing for Model
    def get_data_for_model(self, leagues, seasons, matchdays):
        # TODO:
        return 1

    # Function for Data grabbing for Algorithm
    def get_data_for_algo(self, leagues, seasons, day_start, day_end, team_home_id, team_guest_id):
        """ gives back matches, results, scores DB from given leagues/seasons.
            Cuts the data according to the parameters.
            If team_home_id==0==team_guest_id, all matches are taken.
            If team_home_id!=0 & team_guest_id==0, only matches were home_team participates are taken."""
        # cutting the data on start/end-day does not work yet, in progress
        self.create_dataset_from_leagues_and_seasons(leagues, seasons, day_start, day_end)
        if team_home_id != 0:
            self.extract_matchup_history(team_home_id, team_guest_id)        
        return self.matches, self.results, self.scores
# %%
if __name__ == '__main__':
    crawler = Crawler()

    # matches, results, scores = crawler.get_data_for_algo(leagues, seasons,
    #                                                         day_start, day_end,
    #                                                         team_home_id, team_guest_id)

    matches, results, scores = crawler.get_data_for_algo([1],[2020,2019,2018],0,0,16,87)
    print(matches.head(10))

    teams = crawler.get_team_dicts(1,2020)
    print(teams)
# %%
if __name__ == '__main__':
    api_match_content_columns = ['MatchID', 'MatchDateTimeUTC', 'Group.GroupOrderID', 'Team1.TeamId', 'Team2.TeamId']
    api_results_content_columns = ['ResultID', 'PointsTeam1', 'PointsTeam2', 'ResultOrderID', 'MatchID']
    api_score_content_columns = ['GoalID','ScoreTeam1','ScoreTeam2','GoalGetterID',
                                    'GoalGetterName', 'IsOvertime', 'MatchID']
    uniform_match_content_columns = ['match_id', 'match_date_time_utc', 'matchday', 'team_home_id', 'team_guest_id']
    uniform_result_content_columns = ['result_id', 'points_home', 'points_guest', 'result_type_id', 'match_id']

    seasons = np.arange(2009,2010)
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
