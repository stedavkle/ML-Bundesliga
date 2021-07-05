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
    UNIFORM_TEAMS_DB_PATH = r'./data/bl{}_{}_teams_unif.csv'
    UNIFORM_SEASON_MATCHES_DB_PATH = r'./data/bl{}_{}_matches_unif.csv'
    UNIFORM_SEASON_RESULTS_DB_PATH = r'./data/bl{}_{}_results_unif.csv'
    #uniform_season_scores_db_path = r'./data/bl{}_{}_scores_unif.csv'

    #COLUMNNAMES for uniform Data
    
    #uniform_score_content_columns = ['goal_id','scores_home','scores_guest','scorer_id',
    #                                 'scorer_name', 'is_overtime', 'match_id']

    # PATHs for miscellaneous Data
    ICONS_PATH = r'./web/img/{}.png'
    TABLE_DB_PATH = r'./data/table_bl{}_{}.csv'

    # URLs for OpenLigaDB API
    API_TEAMS_URL = "https://www.openligadb.de/api/getavailableteams/bl{}/{}"
    API_MATCHES_LEAGUE_SEASON_URL = "https://www.openligadb.de/api/getmatchdata/bl{}/{}"
    API_MATCHUP_URL = "https://www.openligadb.de/api/getmatchdata/{}/{}"
    API_NEXTMATCH_LEAGUE_TEAM_URL = "https://www.openligadb.de/api/getnextmatchbyleagueteam/{}/{}"
    API_TABLE_LEAGUE_YEAR_URL = "https://www.openligadb.de/api/getbltable/bl{}/{}"
    API_NEXT_MATCH_DAY_URL = "https://www.openligadb.de/api/getmatchdata/bl{}"
    API_GET_SINGLE_MATCH_URL ="https://www.openligadb.de/api/getmatchdata/{}"
    
    # COLUMNNAMES for OpenLigaDB API
    API_TEAMS_CONTENT_COLUMNS = ['TeamId', 'TeamName', 'TeamIconUrl']
    UNIFORM_TEAMS_COLUMNS =     ['team_id', 'team_name', 'team_icon_url']

    API_MATCH_CONTENT_COLUMNS =     ['MatchID', 'MatchDateTimeUTC', 'Group.GroupOrderID', 'Team1.TeamId', 'Team2.TeamId']
    UNIFORM_MATCH_CONTENT_COLUMNS = ['match_id', 'match_date_time_utc', 'matchday', 'team_home_id', 'team_guest_id']
    
    API_NEXTMATCHDAY_CONTENT_COLUMNS =     ['MatchID', 'MatchDateTimeUTC', 'MatchIsFinished', 'Team1.TeamId', 'Team1.TeamName', 'Team2.TeamId', 'Team2.TeamName', 'Location.LocationStadium']
    UNIFORM_NEXTMATCHDAY_CONTENT_COLUMNS = ['match_id', 'match_date_time_utc', 'is_finished', 'team_home_id', 'team_home_name', 'team_guest_id', 'team_guest_name', 'location_arena']
    
    API_NEXTMATCH_CONTENT_COLUMNS =     ['MatchID', 'MatchDateTimeUTC', 'MatchIsFinished', 'Team1', 'Team2', 'Location']
    UNIFORM_NEXTMATCH_CONTENT_COLUMNS = ['match_id', 'match_date_time_utc', 'is_finished', 'team_home_id', 'team_guest_id', 'location_arena']
    

    API_RESULT_CONTENT_COLUMNS =        ['ResultID', 'PointsTeam1', 'PointsTeam2', 'ResultOrderID', 'MatchID']
    UNIFORM_RESULT_CONTENT_COLUMNS =    ['result_id', 'points_home', 'points_guest', 'result_type_id', 'match_id']
    #api_score_content_columns = ['GoalID','ScoreTeam1','ScoreTeam2','GoalGetterID',
    #                            'GoalGetterName', 'IsOvertime', 'MatchID']

    # METADATA for OpenLigaDB API
    API_META_DATA = "MatchID"
    NO_MATCH = -1
    END_RESULT = 1
    FIRST_DAY = 1

    # CONSTRUCTOR

    def __init__(self):
        """Crawler class constructor"""
        self.dict = {}
        self.teams = pd.DataFrame()
        self.matches = pd.DataFrame()
        self.results = pd.DataFrame()
        #self.scores = pd.DataFrame()

        self.available_leagues = [1,2,3]
        self.bl_leagues_ids = {1 : 4442, 2 : 4443, 3 : 4444}
        if(datetime.datetime.now().month >= 8):
            self.current_season = datetime.datetime.now().year
        else:
            self.current_season = datetime.datetime.now().year-1
        self.first_league_available_seasons = list(range(2002, self.current_season+1))
        self.second_league_available_seasons = list(range(2006, self.current_season+1))
        self.third_league_available_seasons = list(range(2008, self.current_season+1))

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
        response = requests.get(self.API_TEAMS_URL.format(league,season))
        # TODO: proper errorcode
        if response.status_code != 200:
            raise Exception
        teams = pd.read_json(response.content)[self.API_TEAMS_CONTENT_COLUMNS]
        teams.columns = self.UNIFORM_TEAMS_COLUMNS
        teams.to_csv(self.UNIFORM_TEAMS_DB_PATH.format(league,season), index=False)
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
                response = requests.get(self.API_MATCHES_LEAGUE_SEASON_URL.format(league,season))
                # TODO: proper errorcode
                if response.status_code != 200:
                    raise Exception
                data_json = response.json()

                matches = pd.json_normalize(data_json)[self.API_MATCH_CONTENT_COLUMNS]
                matches.columns = self.UNIFORM_MATCH_CONTENT_COLUMNS

                match_results = pd.json_normalize(data_json, record_path='MatchResults', meta=self.API_META_DATA)[self.API_RESULT_CONTENT_COLUMNS]
                match_results.columns = self.UNIFORM_RESULT_CONTENT_COLUMNS
                # TODO: refactor magic numbers
                if (league in [1,2]) & (season in range(2015,2020)) | (league == 3) & (season in range(2016,2020)):
                    match_results['result_type_id'] = match_results['result_type_id'].apply(lambda x: x%2+1)
                # # TODO: concatenate score_home and score_guest to a tuple (score_home, score_guest) in one column 'temp_score'
                # # TODO: handle score_db not present
                # match_scores = pd.json_normalize(data_json, record_path='Goals', meta=self.API_META_DATA)[self.api_score_content_columns]
                # match_scores.columns = self.uniform_score_content_columns
                # save datasets as csv
                matches.to_csv(self.UNIFORM_SEASON_MATCHES_DB_PATH.format(league,season), index=False)
                match_results.to_csv(self.UNIFORM_SEASON_RESULTS_DB_PATH.format(league,season), index=False)
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
        response = requests.get(self.API_NEXTMATCH_LEAGUE_TEAM_URL.format(league_id, team_id))
        # TODO: proper errorcode
        if response.status_code != 200:
            raise Exception
        match = pd.json_normalize(response.json())
        # extract necessary data
        match = match[self.API_NEXTMATCH_CONTENT_COLUMNS]
        match.columns = [self.UNIFORM_NEXTMATCH_CONTENT_COLUMNS]
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
                urllib.request.urlretrieve(row["team_icon_url"], self.ICONS_PATH.format(row["team_id"]))
            except Exception:
                continue
        return 1
    def get_next_matchday_from_API(self, league):
        response = requests.get(self.API_NEXT_MATCH_DAY_URL.format(league))
        if response.status_code != 200:
            raise Exception
        matches = pd.json_normalize(response.json())
        
        # extract necessary data
        if not('Location.LocationStadium' in matches.columns):
            matches['Location.LocationStadium'] = 'Unbekannt'
        matches = matches[self.API_NEXTMATCHDAY_CONTENT_COLUMNS]
        matches.columns = [self.UNIFORM_NEXTMATCHDAY_CONTENT_COLUMNS]
        results = pd.json_normalize(response.json(), record_path='MatchResults', meta=self.API_META_DATA)
        if matches['is_finished'].any().item():
            results = results[self.API_RESULT_CONTENT_COLUMNS]
            results.columns = self.UNIFORM_RESULT_CONTENT_COLUMNS
        return matches, results

    def get_league_of_team(self, team_id):
        current_season = datetime.datetime.now().year-1
        for league in self.available_leagues:
            teams = self.get_teams([league], [current_season], 1)
            if not(teams[teams['team_id'].isin([team_id])].empty):
                return league
        return 0
    def split_utc(self, utc_string):
        utc_split = utc_string.split('T')
        date = utc_split[0]
        time = utc_split[1].split('Z')[0]
        return date, time
    #   
    #   PUBLIC FUNCTIONS BELOW
    #
    
    def get_next_matchday(self):
        all_matches_of_the_day = {1 : {}, 2 : {}, 3 : {}}
        # TODO: dont use teamdicts or skip downloading icons
        id_to_team, team_to_id = self.get_team_dicts(self.available_leagues, [2021])
        for league in self.available_leagues:
            matches, results = self.get_next_matchday_from_API(league)
            for index in matches.index:
                match = {'team_home_id': 0, 'team_home_name': 0, 'team_guest_id': 0, 'team_guest_name': 0,
                    'is_finished': 0, 'points_home': 0, 'points_guest': 0,
                    'date': 0, 'time': 0, 'location': 0}

                match['team_home_id'] = int(matches.loc[index, 'team_home_id'].item())
                match['team_home_name'] = matches.loc[index, 'team_home_name'].item()
                match['team_guest_id'] = int(matches.loc[index, 'team_guest_id'].item())
                match['team_guest_name'] = matches.loc[index, 'team_guest_name'].item()

                if matches.loc[index, 'is_finished'].item():
                    result = results[(results['match_id'] == matches.loc[index, 'match_id'].item())]
                    endresult = result[result['result_type_id'] == self.END_RESULT]
                    match['is_finished'] = 1
                    match['points_home'] = int(endresult.iloc[0]['points_home'].item())
                    match['points_guest'] = int(endresult.iloc[0]['points_guest'].item())

                utc_string = matches.loc[index, 'match_date_time_utc'].item()
                
                date, time = self.split_utc(utc_string)
                match['date'] = date
                match['time'] = time

                match['location'] = matches.loc[index, 'location_arena'].item()

                all_matches_of_the_day[league][int(matches.loc[index, 'match_id'].item())] = match
        return all_matches_of_the_day

    def get_teams(self, leagues, seasons, return_bool):
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
                teams_path = self.UNIFORM_TEAMS_DB_PATH.format(league,season)
                if (os.path.isfile(teams_path)):
                    new_teams = pd.read_csv(teams_path)
                else: 
                    new_teams = self.get_teams_from_API(league, season)
                    
                teams = pd.concat([teams, new_teams])
                teams = teams.drop_duplicates(['team_id'])
        if return_bool == 1:
            return teams
        self.teams = teams



    def load_season(self, league, season):
        matches_path = self.UNIFORM_SEASON_MATCHES_DB_PATH.format(league,season)
        results_path = self.UNIFORM_SEASON_RESULTS_DB_PATH.format(league,season)
        if (os.path.isfile(matches_path)) & (os.path.isfile(results_path)): # & (os.path.isfile(scores_path)
            matches = pd.read_csv(matches_path)
            results = pd.read_csv(results_path)
            return matches, results, True
        else:
            return -1, -1, False
    def cut_start_day(self, matches, results, day):
        if day != self.FIRST_DAY:
            matches = matches.loc[matches['matchday'] >= day]
            results = results[results['match_id'].isin(matches['match_id'])]
        return matches, results
    def cut_end_day(self, matches, results, day):
        matches = matches.loc[matches['matchday'] <= day]
        results = results[results['match_id'].isin(matches['match_id'])]
        return matches, results

    def create_dataset_recursive_helper(self, leagues, seasons, day_start, day_end):
        """
        Extracts the desired matches and results from specified leagues/seasons and saves them internaly.
        
        :param int[] leagues: one or more from (1,2,3)
        :param int[] seasons: array of seasons, format: [<YYYY>,..]
        :param int day_start: starting day of first season
        :param int day_end: end day of last season
        :returns: 1 if function is done

        -> see get_available_data_for_leagues()
        """
        # print(seasons)
        if len(leagues) == 0:
            return pd.DataFrame(), pd.DataFrame()
        if len(seasons) == 0:
            leagues.pop(0)
            seasons = list(self.seasons_backup)
            return self.create_dataset_recursive_helper(leagues, seasons, day_start, day_end)
        league = leagues[0]
        season = seasons.pop(0)
        # print(league, season)
        matches, results, LOADED = self.load_season(league, season)
        if not(LOADED):
            matches, results = self.get_matches_from_leagues_and_seasons_from_API([league], [season])
        # print('MATCHES SHAPE')
        # print(matches.shape)
        matches, results = self.cut_start_day(matches, results, day_start)

        if len(seasons) == 1:
            None
            matches, results = self.cut_end_day(matches, results, day_end)

        next_matches, next_results = self.create_dataset_recursive_helper(leagues, seasons, self.FIRST_DAY, day_end)
        # print('MATCHES SIZE')
        # print(matches.shape)
        matches = pd.concat([matches, next_matches])
        # print('MATCHES SIZE AFTER CONCAT')
        # print(matches.shape)
        results = pd.concat([results, next_results])
        # print('recursion done')
        self.matches = matches
        self.results = results
        return matches, results







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
                matches_path = self.UNIFORM_SEASON_MATCHES_DB_PATH.format(league,season)
                results_path = self.UNIFORM_SEASON_RESULTS_DB_PATH.format(league,season)
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
        self.get_teams(leagues, seasons, 0)
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
    
    def get_next_opponent(self, team_id):
        """
        Returns the teams playing in upcoming match of given team_id.

        :param int team_id: id of a team
        :returns: 0 if no upcoming match otherwise dict containing ids of teams.
        """
        league = self.get_league_of_team(team_id)
        league_id = self.bl_leagues_ids[league]
        match = self.get_next_match_from_API(league_id, team_id)
        dict = {'team_home_id' : match.iloc[0]['team_home_id'],
                'team_guest_id' : match.iloc[0]['team_guest_id']}
        if (match['match_id'] == self.NO_MATCH).bool():
            return 0
        return dict

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
        :returns: pd.DF[]: DataPacket for Algo

        If team_home_id==0==team_guest_id, all matches are taken.
        If team_home_id!=0 & team_guest_id==0, only matches were home_team participates are taken.
        
        -> see get_available_data_for_leagues()
        """
        # self.create_dataset_from_leagues_and_seasons(leagues, seasons, day_start, day_end)
        self.seasons_backup = list(seasons)
        self.create_dataset_recursive_helper(list(leagues), list(seasons), day_start, day_end)
        if team_home_id != 0:
            self.extract_matchup_history(team_home_id, team_guest_id)        
        return [self.matches, self.results]#, self.scores
# %%
if __name__ == '__main__':
    import time
    crawler = Crawler()

    # matches, results, scores = crawler.get_data_for_algo(leagues, seasons,
    #                                                         day_start, day_end,
    #                                                         team_home_id, team_guest_id)
    leagues = [1,2,3]
    seasons = [2021]
    
    id_to_team, team_to_id = crawler.get_team_dicts(leagues, seasons)

    #matches, results = crawler.create_dataset_recursive_helper(leagues, seasons, 1, 34)
    #crawler.create_dataset_from_leagues_and_seasons(leagues, seasons, 1, 34)
    dict = crawler.get_next_matchday()
    print(type(dict))
    print(dict[2][59465])
    #match = crawler.get_next_opponent(16)
    #print(match)

    #data = crawler.get_next_opponent(16)
    #print(data)
    #print(crawler.get_team_dicts([3],[2020]))
    #print(matches.head())
    #print(crawler.get_next_match_day(1))
    #teams = crawler.get_teams(leagues, seasons, 0)
    # print(teams)

    # response = requests.get('https://www.openligadb.de/api/getmatchdata/bl3')
    # matchday = pd.json_normalize(response.json())#[['MatchID', 'MatchDateTimeUTC', 'Group.GroupOrderID', 'Team1.TeamId', 'Team2.TeamId']]
    # print(matchday.head(5))

    
# %%
