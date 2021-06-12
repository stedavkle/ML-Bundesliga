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
    uniform_teams_db_path = r'./data/bl{}_{}_teams_unif.csv'
    uniform_season_matches_db_path = r'./data/bl{}_{}_matches_unif.csv'
    uniform_season_results_db_path = r'./data/bl{}_{}_results_unif.csv'
    #uniform_season_scores_db_path = r'./data/bl{}_{}_scores_unif.csv'

    #COLUMNNAMES for uniform Data
    uniform_teams_columns = ['team_id', 'team_name', 'team_icon_url']
    uniform_match_content_columns = ['match_id', 'match_date_time_utc', 'matchday', 'team_home_id', 'team_guest_id']
    uniform_result_content_columns = ['result_id', 'points_home', 'points_guest', 'result_type_id', 'match_id']
    #uniform_score_content_columns = ['goal_id','scores_home','scores_guest','scorer_id',
    #                                 'scorer_name', 'is_overtime', 'match_id']

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
    #api_score_content_columns = ['GoalID','ScoreTeam1','ScoreTeam2','GoalGetterID',
    #                            'GoalGetterName', 'IsOvertime', 'MatchID']

    # METADATA for OpenLigaDB API
    api_meta_data = "MatchID"

    # CONSTRUCTOR

    def __init__(self):
        """Crawler class constructor"""
        self.dict = {}
        self.teams = pd.DataFrame()
        self.matches = pd.DataFrame()
        self.results = pd.DataFrame()
        #self.scores = pd.DataFrame()

        self.available_leagues = [1,2,3]
        if(datetime.datetime.now().month >= 7):
            year = datetime.datetime.now().year+1
        else:
            year = datetime.datetime.now().year
        self.first_league_available_seasons = list(range(2002, year))
        self.second_league_available_seasons = list(range(2006,year))
        self.third_league_available_seasons = list(range(2008,year))

    def get_available_data_for_leagues(self):
        """
        Returns dict with names and available seasons/avail. matchdays for the leagues 1-3.
        Dict is hard-coded.
        
        :returns: dict 
        """
        self.dict = {1: {'name': '1. Bundesliga', 'seasons': self.first_league_available_seasons, 'size': len(self.first_league_available_seasons), 'matchdays': 34},
                    2: {'name': '2. Bundesliga', 'seasons': self.second_league_available_seasons, 'size': len(self.second_league_available_seasons), 'matchdays': 34},
                    3: {'name': '3. Liga', 'seasons': self.third_league_available_seasons, 'size': len(self.third_league_available_seasons), 'matchdays': 38}
               }
        return self.dict

    #
    #   PRIVATE API FUNCTIONS BELOW
    #   
 
    def get_teams_from_API(self, league, season):
        """
        Gets and saves the data of available teams from API
        :param int league: 1 | 2 | 3
        :param int season: year with format <YYYY>
        :returns: pd.DataFrame()
        """
        response = requests.get(self.api_teams_url.format(league,season))
        # TODO: proper errorcode
        if response.status_code != 200:
            raise Exception
        teams = pd.read_json(response.content)[self.api_teams_content_columns]
        teams.columns = self.uniform_teams_columns
        teams.to_csv(self.uniform_teams_db_path.format(league,season), index=False)
        return teams

    def get_matches_from_leagues_and_seasons_from_API(self, leagues, seasons):
        """
        Gets and saves data of all matches played in given leagues/seasons from API to .csv.
        :param int[] leagues: array of league numbers (1,2,3)
        :param int[] seasons: array of seasons, format: [<YYYY>,..] -> see get_available_data_for_leagues()
        :returns: 2 pd.DataFrame (matches, match_results)
        """
        for league in leagues:
            for season in seasons:
                response = requests.get(self.api_matches_lg_ss_url.format(league,season))
                # TODO: proper errorcode
                if response.status_code != 200:
                    raise Exception
                data_json = response.json()

                matches = pd.json_normalize(data_json)[self.api_match_content_columns]
                matches.columns = self.uniform_match_content_columns

                match_results = pd.json_normalize(data_json, record_path='MatchResults', meta=self.api_meta_data)[self.api_result_content_columns]
                match_results.columns = self.uniform_result_content_columns
                # # TODO: concatenate score_home and score_guest to a tuple (score_home, score_guest) in one column 'temp_score'
                # # TODO: handle score_db not present
                # match_scores = pd.json_normalize(data_json, record_path='Goals', meta=self.api_meta_data)[self.api_score_content_columns]
                # match_scores.columns = self.uniform_score_content_columns
                # save datasets as csv
                matches.to_csv(self.uniform_season_matches_db_path.format(league,season), index=False)
                match_results.to_csv(self.uniform_season_results_db_path.format(league,season), index=False)
                #match_scores.to_csv(self.uniform_season_scores_db_path.format(league,season), index=False)
        return matches, match_results#, match_scores

    def get_next_match_from_API(self, league_id, team_id):
        """
        Returns the upcoming match of a team in a specific league.
        :param int league_id: id of a league specified from OpenLigaDB
        :param int team_id: id of a team, see get_team_dicts()
        :returns: pd.DataFrame containing a single match
        
        example ids: <BundesLiga, Saison, LeagueID> 1 2020 4442; 2 2020 4443; 3 2020 4444
        """
        
        response = requests.get(self.api_nextmatch_lg_tm_url.format(league_id, team_id))
        # TODO: proper errorcode
        if response.status_code != 200:
            raise Exception
        match = pd.json_normalize(response.json())
        # extract necessary data
        match = match[self.api_match_content_columns]
        match.columns = self.uniform_match_content_columns
        return match

    def get_team_icons_from_wiki(self):
        """
        Gets the team icons of all teams saved in self.teams.
        Is automatically called when executing get_teams(leagues, seasons)
        :returns: 1 if function is done
        """
        # TODO: check if Pics already saved
        for index, row in self.teams.iterrows():
            # TODO: handle icons that are .svg instead of .png (ID=9 and ID=95)
            try:
                urllib.request.urlretrieve(row["team_icon_url"], self.icons_path.format(row["team_id"]))
            except Exception:
                continue
        return 1

    #   
    #   PUBLIC FUNCTIONS BELOW
    #

    def get_teams(self, leagues, seasons):
        """
        Gets all unique teams from the specified leagues/seasons from API or DB and saves them to self.teams.
        Then gets all team icons.
        :param int[] leagues: one or more from (1,2,3)
        :param int[] seasons: array of seasons, format: [<YYYY>,..] -> see get_available_data_for_leagues()
        :returns: 1 if function is done
        """
        teams = pd.DataFrame()
        for league in leagues:
            for season in seasons:
                teams_path = self.uniform_teams_db_path.format(league,season)
                if (os.path.isfile(teams_path)):
                    new_teams = pd.read_csv(teams_path)
                else: 
                    new_teams = self.get_teams_from_API(league, season)
                teams = pd.concat([teams, new_teams])
                teams = teams.drop_duplicates(['team_id'])
        self.teams = teams
        self.get_team_icons_from_wiki()
        return 1



    def create_dataset_from_leagues_and_seasons(self, leagues, seasons, day_start, day_end):
        """
        Extracts the desired matches and results from specified leagues/seasons and saves them internaly.
        
        :param int[] leagues: one or more from (1,2,3)
        :param int[] seasons: array of seasons, format: [<YYYY>,..]
        :param int day_start: starting day of first season
        :param int day_end: end day of last season
        :returns: 1 if function is done

        -> see get_available_data_for_leagues()
        """
        dataset_matches = pd.DataFrame()
        dataset_results = pd.DataFrame()
        dataset_scores = pd.DataFrame()
        is_first_season = True
        # for all leagues in every year get matchdata
        for season in seasons:
            for league in leagues:
                # format path strings
                matches_path = self.uniform_season_matches_db_path.format(league,season)
                results_path = self.uniform_season_results_db_path.format(league,season)
                #scores_path = self.uniform_season_scores_db_path.format(league,season)
                # check if data is stored, if not get from API
                # TODO: Try: Except: instead of if() else()
                if (os.path.isfile(matches_path)) & (os.path.isfile(results_path)): # & (os.path.isfile(scores_path)
                    matches = pd.read_csv(matches_path)
                    results = pd.read_csv(results_path)
                    #scores = pd.read_csv(scores_path)
                else:
                    matches, results = self.get_matches_from_leagues_and_seasons_from_API([league], [season])
                # check if we have to cut the first/last season to start/end day
                if is_first_season & (day_start > 1):
                    matches = matches.loc[matches['matchday'] >= day_start]
                    results = results[results['match_id'].isin(matches['match_id'])]
                    #scores = scores[scores['match_id'].isin(matches['match_id'])]
                if season == seasons[-1]: #& day_end < self.dict[league]['matchdays']:
                    matches = matches.loc[matches['matchday'] <= day_end]
                    results = results[results['match_id'].isin(matches['match_id'])]
                    #scores = scores[scores['match_id'].isin(matches['match_id'])]
                # concatenate data
                dataset_matches = pd.concat([dataset_matches, matches])
                dataset_results = pd.concat([dataset_results, results])
                #dataset_scores = pd.concat([dataset_scores, scores])
            is_first_season = False
        self.matches = dataset_matches
        self.results = dataset_results
        #self.scores = dataset_scores
        return 1
    #
    #   Functions for cutting and extracting data from big DB
    #
    def get_team_dicts(self, leagues, seasons):
        """
        Returns 2 dictionarys, the first maps team_id to team_name, the second is vice versa.

        :param int[] leagues: one or more from (1,2,3)
        :param int[] seasons: array of seasons, format: [<YYYY>,..]
        :returns: 2 dicts (id_to_team, team_to_id)
        
        -> see get_available_data_for_leagues()
        """
        self.get_teams(leagues, seasons)
        id_to_team = pd.Series(self.teams.team_name.values,index=self.teams.team_id).to_dict()
        team_to_id = pd.Series(self.teams.team_id.values,index=self.teams.team_name).to_dict()
        return id_to_team, team_to_id

    def extract_matchup_history(self, team_home_id, team_guest_id):
        """
        Extracts matches/results from internally saved data where the 2 teams specified play.
        If you want to filter only for one team, team_guest_id should be 0

        :param int team_home_id: id of first team
        :param int team_guest_id: id of second team
        :returns: 1 if function is done
        
        -> see get_team_dicts(leagues, seasons)
        """
        if team_guest_id == 0:
            self.matches = self.matches.loc[(self.matches['team_home_id'] == team_home_id) | (self.matches['team_guest_id'] == team_home_id)] 
        else:
            self.matches = self.matches.loc[(self.matches['team_home_id'] == team_home_id) & (self.matches['team_guest_id'] == team_guest_id)
                                                    | (self.matches['team_home_id'] == team_guest_id) & (self.matches['team_guest_id'] == team_home_id)]
        self.results = self.results[self.results['match_id'].isin(self.matches['match_id'])]
        #self.scores = self.scores[self.scores['match_id'].isin(self.matches['match_id'])]  
        return 1

    # Function for Data grabbing for Model
    def get_data_for_model(self, leagues, seasons, matchdays):
        # TODO:
        return 1

    # Function for Data grabbing for Algorithm
    def get_data_for_algo(self, leagues, seasons, day_start, day_end, team_home_id, team_guest_id):
        """
        Returns 2 pd.DataFrame matches, results for given parameters.

        :param int[] leagues: one or more from (1,2,3)
        :param int[] seasons: array of seasons, format: [<YYYY>,..]
        :param int day_start: starting day of first season
        :param int day_end: end day of last season
        :param int team_home_id: id of first team
        :param int team_guest_id: id of second team

        If team_home_id==0==team_guest_id, all matches are taken.
        If team_home_id!=0 & team_guest_id==0, only matches were home_team participates are taken.
        
        -> see get_available_data_for_leagues()
        """
        self.create_dataset_from_leagues_and_seasons(leagues, seasons, day_start, day_end)
        if team_home_id != 0:
            self.extract_matchup_history(team_home_id, team_guest_id)        
        return self.matches, self.results#, self.scores
# %%
if __name__ == '__main__':
    crawler = Crawler()

    # matches, results, scores = crawler.get_data_for_algo(leagues, seasons,
    #                                                         day_start, day_end,
    #                                                         team_home_id, team_guest_id)
    leagues = [1]
    seasons = np.arange(2009,2020)
    matches, results = crawler.get_data_for_algo([1,2,3],[2020,2019,2018],2,30,0,0)
    print(matches)

    # teams = crawler.get_teams(leagues, seasons).sort_values(['team_id'])
    # print(teams)

    #id_to_team, team_to_id = crawler.get_team_dicts(leagues, seasons)
    #print(team_to_id["1. FC Köln"])
