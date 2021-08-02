# %%
import sys
from abc import ABCMeta, abstractmethod, ABC
import pandas as pd
pd.options.mode.chained_assignment = None
import json
import requests
import os
import urllib.request
import numpy as np
import datetime


class Crawler:
    __metaclass__ = ABCMeta
    cwd = os.getcwd()

    UNIFORM_TEAMS_COLUMNS = ['team_id', 'team_name', 'team_icon_url']
    UNIFORM_MATCH_CONTENT_COLUMNS = ['match_id', 'match_date_time_utc', 'matchday', 'team_home_id', 'team_guest_id']
    UNIFORM_RESULT_CONTENT_COLUMNS = ['result_id', 'points_home', 'points_guest', 'result_type_id', 'match_id']

    ICONS_PATH = os.path.join(cwd, 'teamproject/web/img/{}.png')

    # non-abstract methods
    def get_crawler(self):
        crawlers = {
                        1: {
                            'crawler_id': 1,
                            'sport': 'Fußball Deutschland',
                            'description': 'Daten zu den drei höchsten Fußball-Ligen in Deutschland. Quelle: openligadb.de',
                            'run': BundesligaCrawler(),
                            'max_goals': 15
                        },
                        2: {
                            'crawler_id': 2,
                            'sport': 'NBA - National Basketball Association',
                            'description': 'Daten zur NBA der USA, Quelle: data.nba.net',
                            'run': NBACrawler(),
                            'max_goals': 170
                        }
                    }
        return crawlers

    # abstract methods
    @abstractmethod
    def get_available_data_for_leagues(self):
        pass

    @abstractmethod
    def get_next_matchday(self):
        pass

    @abstractmethod
    def get_data_for_algo(self):
        pass

    @abstractmethod
    def get_team_dicts(self):
        pass

    @abstractmethod
    def get_next_opponent(self):
        pass

    @abstractmethod
    def pretrained_data_source(self):
        pass

    def get_team_icons_from_wiki(self):
        """
        Gets the team icons of all teams saved in self.teams.
        Is automatically called when executing get_teams(leagues, seasons)
        :returns: 1 if function is done
        """
        # TODO: check if Pics already saved
        for index, row in self.teams.iterrows():
            teams_path = self.ICONS_PATH.format(row["team_id"])
            # TODO: handle icons that are .svg instead of .png (ID=9 and ID=95)
            if not(os.path.isfile(teams_path)):
                try:
                    urllib.request.urlretrieve(row["team_icon_url"], teams_path)
                except Exception:
                    continue
        return 1
    def cut_start_day(self, matches, results, day):
        if day != self.FIRST_DAY:
            matches = matches.loc[matches['matchday'] >= day]
            results = results[results['match_id'].isin(matches['match_id'])]
        return matches, results

    def cut_end_day(self, matches, results, day):
        matches = matches.loc[matches['matchday'] <= day]
        results = results[results['match_id'].isin(matches['match_id'])]
        return matches, results

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
            self.matches = self.matches.loc[
                (self.matches['team_home_id'] == team_home_id) | (self.matches['team_guest_id'] == team_home_id)]
        else:
            self.matches = self.matches.loc[
                (self.matches['team_home_id'] == team_home_id) & (self.matches['team_guest_id'] == team_guest_id)
                | (self.matches['team_home_id'] == team_guest_id) & (self.matches['team_guest_id'] == team_home_id)]
        self.results = self.results[self.results['match_id'].isin(self.matches['match_id'])]
        # self.scores = self.scores[self.scores['match_id'].isin(self.matches['match_id'])]
        return 1

class BundesligaCrawler(Crawler):
    # PATHs for uniform Data
    cwd = os.getcwd()
    UNIFORM_TEAMS_DB_PATH = os.path.join(cwd, 'teamproject/data/bl{}_{}_teams_unif.csv')
    UNIFORM_SEASON_MATCHES_DB_PATH = os.path.join(cwd, 'teamproject/data/bl{}_{}_matches_unif.csv')
    UNIFORM_SEASON_RESULTS_DB_PATH = os.path.join(cwd, 'teamproject/data/bl{}_{}_results_unif.csv')
    # uniform_season_scores_db_path = r'./data/bl{}_{}_scores_unif.csv'

    # COLUMNNAMES for uniform Data

    # uniform_score_content_columns = ['goal_id','scores_home','scores_guest','scorer_id',
    #                                 'scorer_name', 'is_overtime', 'match_id']

    # PATHs for miscellaneous Data
    TABLE_DB_PATH = os.path.join(cwd, 'teamproject/data/table_bl{}_{}.csv')

    # URLs for OpenLigaDB API
    API_TEAMS_URL = "https://www.openligadb.de/api/getavailableteams/bl{}/{}"
    API_MATCHES_LEAGUE_SEASON_URL = "https://www.openligadb.de/api/getmatchdata/bl{}/{}"
    API_MATCHUP_URL = "https://www.openligadb.de/api/getmatchdata/{}/{}"
    API_NEXTMATCH_LEAGUE_TEAM_URL = "https://www.openligadb.de/api/getnextmatchbyleagueteam/{}/{}"
    API_TABLE_LEAGUE_YEAR_URL = "https://www.openligadb.de/api/getbltable/bl{}/{}"
    API_NEXT_MATCH_DAY_URL = "https://www.openligadb.de/api/getmatchdata/bl{}"
    API_GET_SINGLE_MATCH_URL = "https://www.openligadb.de/api/getmatchdata/{}"

    # COLUMNNAMES for OpenLigaDB API
    API_TEAMS_CONTENT_COLUMNS = ['TeamId', 'TeamName', 'TeamIconUrl']
    UNIFORM_TEAMS_COLUMNS = ['team_id', 'team_name', 'team_icon_url']

    API_MATCH_CONTENT_COLUMNS = ['MatchID', 'MatchDateTimeUTC', 'Group.GroupOrderID', 'Team1.TeamId', 'Team2.TeamId']
    UNIFORM_MATCH_CONTENT_COLUMNS = ['match_id', 'match_date_time_utc', 'matchday', 'team_home_id', 'team_guest_id']

    API_NEXTMATCHDAY_CONTENT_COLUMNS = ['MatchID', 'MatchDateTimeUTC', 'MatchIsFinished', 'Team1.TeamId',
                                        'Team1.TeamName', 'Team2.TeamId', 'Team2.TeamName', 'Location.LocationStadium']
    UNIFORM_NEXTMATCHDAY_CONTENT_COLUMNS = ['match_id', 'match_date_time_utc', 'is_finished', 'team_home_id',
                                            'team_home_name', 'team_guest_id', 'team_guest_name', 'location_arena']

    API_NEXTMATCH_CONTENT_COLUMNS = ['MatchID', 'MatchDateTimeUTC', 'MatchIsFinished', 'Team1.TeamId', 'Team1.TeamName',
                                     'Team2.TeamId', 'Team2.TeamName']
    UNIFORM_NEXTMATCH_CONTENT_COLUMNS = ['match_id', 'match_date_time_utc', 'is_finished', 'team_home_id',
                                         'team_home_name', 'team_guest_id', 'team_guest_name']

    API_RESULT_CONTENT_COLUMNS = ['ResultID', 'PointsTeam1', 'PointsTeam2', 'ResultOrderID', 'MatchID']
    
    # api_score_content_columns = ['GoalID','ScoreTeam1','ScoreTeam2','GoalGetterID',
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
        # self.scores = pd.DataFrame()

        self.available_leagues = [1, 2, 3]
        self.bl_leagues_ids = {1: 4500, 2: 4506, 3: 4507}
        if (datetime.datetime.now().month >= 7):
            self.current_season = datetime.datetime.now().year
        else:
            self.current_season = datetime.datetime.now().year - 1
        self.first_league_available_seasons = list(range(2002, self.current_season + 1))
        self.second_league_available_seasons = list(range(2006, self.current_season + 1))
        self.third_league_available_seasons = list(range(2008, self.current_season + 1))

    def pretrained_data_source(self, set, decay=False, ):
        if decay:
            return 'teamproject/data/dc_pretrained_data/bl1u2_{}_pretrained_data_decay.csv'.format(set)
        else:
            return 'teamproject/data/dc_pretrained_data/bl1u2_{}_pretrained_data_NO_decay.csv'.format(set)

    def get_available_data_for_leagues(self):
        """
        Returns dict with names and available seasons/avail. matchdays for the leagues 1-3.
        Dict is hard-coded.
        
        :returns: dict 
        """
        self.dict = {1: {'name': '1. Bundesliga', 'seasons': self.first_league_available_seasons,
                         'size': len(self.first_league_available_seasons), 'matchdays': 34},
                     2: {'name': '2. Bundesliga', 'seasons': self.second_league_available_seasons,
                         'size': len(self.second_league_available_seasons), 'matchdays': 34},
                     3: {'name': '3. Liga', 'seasons': self.third_league_available_seasons,
                         'size': len(self.third_league_available_seasons), 'matchdays': 38}
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
        response = requests.get(self.API_TEAMS_URL.format(league, season))
        # TODO: proper errorcode
        if response.status_code != 200:
            raise Exception
        teams = pd.read_json(response.content)[self.API_TEAMS_CONTENT_COLUMNS]
        teams.columns = self.UNIFORM_TEAMS_COLUMNS
        teams.to_csv(self.UNIFORM_TEAMS_DB_PATH.format(league, season), index=False)
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
        # filter if nextmatch is not available
        if (match['MatchID'] == self.NO_MATCH).bool():
            match['Team1.TeamId'] = 0
            match['Team2.TeamId'] = 0
            match['Team1.TeamName'] = "unbekannt"
            match['Team2.TeamName'] = "unbekannt"
            match['match_date_time_utc'] = 'unbekannt'

        # extract necessary data
        match = match[self.API_NEXTMATCH_CONTENT_COLUMNS]
        match.columns = [self.UNIFORM_NEXTMATCH_CONTENT_COLUMNS]
        return match

    

    def get_next_matchday_from_API(self, league):
        response = requests.get(self.API_NEXT_MATCH_DAY_URL.format(league))
        if response.status_code != 200:
            raise Exception
        matches = pd.json_normalize(response.json())

        # extract necessary data
        if not ('Location.LocationStadium' in matches.columns):
            matches['Location.LocationStadium'] = 'Unbekannt'
        matches['Location.LocationStadium'] = matches['Location.LocationStadium'].fillna('Unbekannt')
        matches = matches[self.API_NEXTMATCHDAY_CONTENT_COLUMNS]
        matches.columns = [self.UNIFORM_NEXTMATCHDAY_CONTENT_COLUMNS]
        matches['location_arena'] = matches['location_arena'].fillna('Unbekannt')
        results = pd.json_normalize(response.json(), record_path='MatchResults', meta=self.API_META_DATA)
        if matches['is_finished'].any().item():
            results = results[self.API_RESULT_CONTENT_COLUMNS]
            results.columns = self.UNIFORM_RESULT_CONTENT_COLUMNS
        return matches, results

    def get_league_of_team(self, team_id):
        current_season = datetime.datetime.now().year - 1
        for league in self.available_leagues:
            teams = self.get_teams([league], [current_season], 1)
            if not (teams[teams['team_id'].isin([team_id])].empty):
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
        all_matches_of_the_day = {1: {}, 2: {}, 3: {}}
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
                teams_path = self.UNIFORM_TEAMS_DB_PATH.format(league, season)
                if (os.path.isfile(teams_path)):
                    new_teams = pd.read_csv(teams_path)
                else:
                    new_teams = self.get_teams_from_API(league, season)

                teams = pd.concat([teams, new_teams])
                teams = teams.drop_duplicates(['team_id']).drop_duplicates(['team_name'])
        if return_bool == 1:
            return teams
            # TODO: Index should be reset but it causes a weird issue,
            # where level_0 already exists
        self.teams = teams

    def load_season(self, league, season):
        matches_path = self.UNIFORM_SEASON_MATCHES_DB_PATH.format(league, season)
        results_path = self.UNIFORM_SEASON_RESULTS_DB_PATH.format(league, season)
        if (os.path.isfile(matches_path)) & (os.path.isfile(results_path)):  # & (os.path.isfile(scores_path)
            matches = pd.read_csv(matches_path)
            results = pd.read_csv(results_path)
            return matches, results, True
        else:
            return -1, -1, False

    def create_dataset_recursive(self, leagues, seasons, day_start, day_end):
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
            return self.create_dataset_recursive(leagues, seasons, day_start, day_end)
        league = leagues[0]
        season = seasons.pop(0)
        # print(league, season)
        matches, results, LOADED = self.load_season(league, season)
        if not (LOADED):
            matches, results = self.get_matches_from_leagues_and_seasons_from_API([league], [season])
        # print('MATCHES SHAPE')
        # print(matches.shape)
        # TODO: only cut first season
        matches, results = self.cut_start_day(matches, results, day_start)
        if len(seasons) == 0:
            matches, results = self.cut_end_day(matches, results, day_end)

        next_matches, next_results = self.create_dataset_recursive(leagues, seasons, day_start, day_end)
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
        id_to_team = pd.Series(self.teams.team_name.values, index=self.teams.team_id).to_dict()
        team_to_id = pd.Series(self.teams.team_id.values, index=self.teams.team_name).to_dict()
        return id_to_team, team_to_id

    def get_next_opponent(self, team_id):
        """
        Returns the teams playing in upcoming match of given team_id.

        :param int team_id: id of a team
        :returns: 0 if no upcoming match otherwise dict containing ids of teams.
        """
        league = self.get_league_of_team(team_id)

        league_id = self.bl_leagues_ids[league]
        match = self.get_next_match_from_API(league_id, team_id)
        # dict = {'team_home_id' : int(match.iloc[0]['team_home_id']),
        #         'team_guest_id' : int(match.iloc[0]['team_guest_id'])}
        if (match['match_id'] == self.NO_MATCH).bool():
            return 0
        dict = {'team_home_id': 0, 'team_home_name': 'Unbekannt', 'team_guest_id': 0, 'team_guest_name': 'Unbekannt',
                'is_finished': 0, 'points_home': 0, 'points_guest': 0,
                'date': 'Unbekannt', 'time': 'Unbekannt', 'location': 'Unbekannt'}

        dict['team_home_id'] = int(match.loc[0, 'team_home_id'].item())
        dict['team_home_name'] = match.loc[0, 'team_home_name'].item()
        dict['team_guest_id'] = int(match.loc[0, 'team_guest_id'].item())
        dict['team_guest_name'] = match.loc[0, 'team_guest_name'].item()

        utc_string = match.loc[0, 'match_date_time_utc'].item()

        date, time = self.split_utc(utc_string)
        dict['date'] = date
        dict['time'] = time

        # dict['location'] = match.loc[0, 'location_arena'].item()

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

        self.create_dataset_recursive(list(leagues), sorted(seasons), day_start, day_end)
        if team_home_id != 0:
            self.extract_matchup_history(team_home_id, team_guest_id)
        return [self.matches, self.results]  # , self.scores


class NBACrawler(Crawler):
    cwd = os.getcwd()

    CALENDAR = 'http://data.nba.net/10s/prod/v1/calendar.json'
    TEAMS_URL = 'http://data.nba.net/10s/prod/v2/{}/teams.json'
    MATCHES_URL = 'http://data.nba.net/10s/prod/v1/{}/schedule.json'
    MATCHES_TEAM_URL = 'http://data.nba.net/10s/prod/v1/{}/teams/{}/schedule.json'
    ICON_URL = 'http://loodibee.com/wp-content/uploads/nba-{}-{}-logo.png'

    UNIFORM_TEAMS_DB_PATH = os.path.join(cwd, 'teamproject/data/nba_{}_teams_unif.csv')
    UNIFORM_SEASON_MATCHES_DB_PATH = os.path.join(cwd, 'teamproject/data/nba_{}_matches_unif.csv')
    UNIFORM_SEASON_RESULTS_DB_PATH = os.path.join(cwd, 'teamproject/data/nba_{}_results_unif.csv')

    NBA_MATCHES_API_COLUMNS =           ['gameId',  'startTimeUTC',         'hTeam.teamId', 'hTeam.score', 'vTeam.teamId',  'vTeam.score']
    UNIFORM_MATCHES_RESULTS_COLUMNS =   ['match_id','match_date_time_utc',  'team_home_id', 'points_home', 'team_guest_id', 'points_guest']
    
    FIRST_DAY = 1
    END_RESULT = 1

    def pretrained_data_source(self, decay=False):
        if decay:
            return 'teamproject/data/nba_dixon_coles_pre_trained_dataset_decay.csv'
        else:
            return 'teamproject/data/nba_dixon_coles_pre_trained_dataset_no_decay.csv'
    
    def get_available_data_for_leagues(self):
        response = requests.get(self.CALENDAR)
        # print(response.status_code)
        calendar = pd.read_json(response.content)
        #print(calendar.columns)
        calendar_json = json.loads(response.content)
        # print(list(calendar_json.keys())[1:4])
        # print('BLABLA')
        # print(calendar_json['startDate'])
        self.start_date = 2016
        self.end_date = datetime.datetime.strptime(calendar_json['endDate'], '%Y%m%d')
        self.available_seasons = list(range(self.start_date, self.end_date.year))
        dict = {1: {'name': 'NBA', 'seasons': self.available_seasons,
                         'size': (self.end_date.year-self.start_date), 'matchdays': 365}}
        return dict
    def get_teams_from_API(self, season):

        response = requests.get(self.TEAMS_URL.format(season))
        #teams_json = json.loads(response.content)
        teams = pd.json_normalize(response.json(), record_path=['league', 'standard'])[['teamId', 'fullName', 'urlName', 'city', 'nickname', 'confName']]
        teams = teams[(teams['confName'] == 'East') | (teams['confName'] == 'West')]
        print('TEAMS')
        print(teams.columns)
        teams.columns = ['team_id', 'team_name', 'team_url_name', 'city', 'team_short_name', 'conference_name']
        for index, row in teams.iterrows():
            city = row['city']
            name = row['team_short_name']
            teams.loc[index, 'team_icon_url'] = self.ICON_URL.format(city, name).lower()
        teams = teams[['team_id', 'team_name', 'team_url_name', 'team_icon_url']]
        teams.team_id = pd.to_numeric(teams.team_id)
        teams.to_csv(self.UNIFORM_TEAMS_DB_PATH.format(season), index=False)
        return teams
    def get_teams(self, seasons, return_bool):
        teams = pd.DataFrame()
        #seasons = [2020] # BECAUSE OFBUG WHERE STRANGE TEAMS APPEAR
        for season in seasons:
            teams_path = self.UNIFORM_TEAMS_DB_PATH.format(season)
            if (os.path.isfile(teams_path)):
                new_teams = pd.read_csv(teams_path)
            else:
                new_teams = self.get_teams_from_API(season)
            teams = pd.concat([teams, new_teams])
            teams = teams.drop_duplicates(['team_id']).drop_duplicates(['team_name'])
        if return_bool:
            return teams
        self.teams = teams

    def get_team_dicts(self, leagues, seasons):
        self.get_teams(seasons, 0)
        id_to_team = pd.Series(self.teams.team_name.values, index=self.teams.team_id).to_dict()
        team_to_id = pd.Series(self.teams.team_id.values, index=self.teams.team_name).to_dict()
        return id_to_team, team_to_id

    def get_matches_from_leagues_and_seasons_from_API(self, leagues, seasons):
        for season in seasons:
            response = requests.get(self.MATCHES_URL.format(season))
            df = pd.json_normalize(response.json()['league']['standard'])[self.NBA_MATCHES_API_COLUMNS]
            df.columns = self.UNIFORM_MATCHES_RESULTS_COLUMNS
            df['matchday'] = df['match_date_time_utc'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple().tm_yday)
            df['result_type_id'] = 1
            df['result_id'] = 1
            matches = df[self.UNIFORM_MATCH_CONTENT_COLUMNS]
            results = df[self.UNIFORM_RESULT_CONTENT_COLUMNS]
            # matches['match_id'] = pd.to_numeric(matches['match_id'])
            # matches['team_home_id'] = pd.to_numeric(matches['team_home_id'])
            # matches['team_guest_id'] = pd.to_numeric(matches['team_guest_id'])
            # results['points_home'] = pd.to_numeric(results['points_home'], downcast='integer').fillna(0)
            # results['points_guest'] = pd.to_numeric(results['points_guest'], downcast='integer').fillna(0)
            # results['match_id'] = pd.to_numeric(results['match_id'])
            matches['match_id'] = matches['match_id'].astype('int64')
            matches['team_home_id'] = matches['team_home_id'].astype('int64')
            matches['team_guest_id'] = matches['team_guest_id'].astype('int64')
            results['points_home'] = results['points_home'].replace('', 0).fillna(0).astype('int64')
            results['points_guest'] = results['points_guest'].replace('', 0).fillna(0).astype('int64')
            results['match_id'] = results['match_id'].astype('int64')

            matches.to_csv(self.UNIFORM_SEASON_MATCHES_DB_PATH.format(season), index=False)
            results.to_csv(self.UNIFORM_SEASON_RESULTS_DB_PATH.format(season), index=False)
        return matches, results
    def load_season(self, league, season):
        matches_path = self.UNIFORM_SEASON_MATCHES_DB_PATH.format(season)
        results_path = self.UNIFORM_SEASON_RESULTS_DB_PATH.format(season)
        if (os.path.isfile(matches_path)) & (os.path.isfile(results_path)):  # & (os.path.isfile(scores_path)
            matches = pd.read_csv(matches_path)
            results = pd.read_csv(results_path)
            return matches, results, True
        else:
            return -1, -1, False
        
    def create_dataset_recursive(self, seasons, day_start, day_end):
        """
        Extracts the desired matches and results from specified leagues/seasons and saves them internaly.
        
        :param int[] leagues: one or more from (1,2,3)
        :param int[] seasons: array of seasons, format: [<YYYY>,..]
        :param int day_start: starting day of first season
        :param int day_end: end day of last season
        :returns: 1 if function is done

        -> see get_available_data_for_leagues()
        """
        if len(seasons) == 0:
            return pd.DataFrame(), pd.DataFrame()
        season = seasons.pop(0)
        # print(league, season)
        matches, results, LOADED = self.load_season(1, season)
        if not (LOADED):
            matches, results = self.get_matches_from_leagues_and_seasons_from_API(1, [season])
        # print('MATCHES SHAPE')
        # print(matches.shape)
        matches, results = self.cut_start_day(matches, results, day_start)

        if len(seasons) == 0:
            matches, results = self.cut_end_day(matches, results, day_end)

        next_matches, next_results = self.create_dataset_recursive(seasons, self.FIRST_DAY, day_end)
        # print('MATCHES SIZE')
        # print(matches.shape)
        matches = pd.concat([matches, next_matches])
        # print('MATCHES SIZE AFTER CONCAT')
        # print(matches.shape)
        results = pd.concat([results, next_results])
        # print('recursion done')
        matches['match_date_time_utc'] = matches['match_date_time_utc'].apply(lambda x: x[:19] + 'Z')
        self.matches = matches
        self.results = results
        return matches, results
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
        self.create_dataset_recursive(list(seasons), day_start, day_end)
        if team_home_id != 0:
            self.extract_matchup_history(team_home_id, team_guest_id)
        return [self.matches, self.results]


    def get_next_opponent(self, team_id):
        dict = {'team_home_id': 0, 'team_home_name': 'Unbekannt', 'team_guest_id': 0, 'team_guest_name': 'Unbekannt',
                'is_finished': 0, 'points_home': 0, 'points_guest': 0,
                'date': 'Unbekannt', 'time': 'Unbekannt', 'location': 'Unbekannt'}
        # TODO: Use self.MATCHES_TEAM_URL, get current Date and search for the upcoming game
        team_url_code = self.teams[self.teams['team_id'] == team_id].team_url_name.item()
        current_season = self.available_seasons[-1]

        response = requests.get(self.MATCHES_TEAM_URL.format(current_season, team_url_code))
        matches = pd.json_normalize(response.json()['league']['standard'])[self.NBA_MATCHES_API_COLUMNS]
        matches.columns = self.UNIFORM_MATCHES_RESULTS_COLUMNS

        current_day = datetime.datetime.now()
        #current_day = datetime.datetime.strptime('2021-05-21 01:00:00', "%Y-%m-%d %H:%M:%S")
        last_matchday = datetime.datetime.strptime(matches.tail(1)['match_date_time_utc'].item(), "%Y-%m-%dT%H:%M:%S.%fZ")
        SEASON_FINISHED = (last_matchday-current_day).days<0

        if SEASON_FINISHED:
            return 0
        
        next_match = matches[matches['match_date_time_utc'].apply(lambda x: (datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")-current_day).days >= 0)].head(1)

        print(next_match)

        dict = {'team_home_id': 0, 'team_home_name': 0, 'team_guest_id': 0, 'team_guest_name': 0,
                'is_finished': 0, 'points_home': 0, 'points_guest': 0,
                'date': 0, 'time': 0, 'location': 'Unbekannt'}

        # print(self.teams[['team_id', 'team_name']])
        # print('GUEST_TEAM_ID')
        # guest_team_id = next_match['team_guest_id'].item()
        # print(guest_team_id)
        # print(self.teams[self.teams['team_id'] == int(guest_team_id)]['team_name'].item())
        # print('HOME_TEAM_ID')
        # home_team_id = next_match['team_home_id'].item()
        # print(home_team_id)
        # print(self.teams[self.teams['team_id'] == int(home_team_id)]['team_name'].item())

        home_team_id = int(next_match['team_home_id'].item())
        guest_team_id = int(next_match['team_guest_id'].item())

        dict['team_home_id'] = home_team_id
        dict['team_home_name'] = self.teams[self.teams['team_id'] == int(home_team_id)]['team_name'].item()
        dict['team_guest_id'] = guest_team_id
        dict['team_guest_name'] = self.teams[self.teams['team_id'] == int(guest_team_id)]['team_name'].item()

        utc_string = next_match['match_date_time_utc'].item()

        date, time = self.split_utc(utc_string)
        dict['date'] = date
        dict['time'] = time
        return dict

    def split_utc(self, utc_string):
        utc_split = utc_string.split('T')
        date = utc_split[0]
        time = utc_split[1].split('Z')[0][0:8]
        return date, time
    
    def get_next_matchday(self):
        all_matches = {1:{}}
        AMOUNT_OF_GAMES = 10
        league = 1
        
        current_season = self.get_available_data_for_leagues()[1]['seasons'][-1]

        id_to_team, team_to_id = self.get_team_dicts(league, [current_season])
        matches, results = self.get_matches_from_leagues_and_seasons_from_API(league, [current_season])
        #print(matches)
        #print(results.tail(10))
        
        newest_matches = matches[matches['match_date_time_utc'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple().tm_year) == current_season]

        current_day = datetime.datetime.now()
        #current_day = datetime.datetime.strptime('2021-05-21 01:00:00', "%Y-%m-%d %H:%M:%S")
        last_matchday = datetime.datetime.strptime(matches.tail(1)['match_date_time_utc'].item(), "%Y-%m-%dT%H:%M:%S.%fZ")
        SEASON_FINISHED = (last_matchday-current_day).days<0
        #print(SEASON_FINISHED)
        #print((last_matchday-current_day).days)
        if SEASON_FINISHED:
            newest_matches = matches.tail(AMOUNT_OF_GAMES)
            #newest_matches['is_finished'] = True
        else:
            newest_matches = matches[matches['match_date_time_utc'].apply(lambda x: (datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")-current_day).days >= 0)].head(AMOUNT_OF_GAMES)
            #newest_matches['is_finished'] = False
        #print('RESULT_IDs')
        #print(results['match_id'])
        #print(newest_matches['match_id'])
        result_match_ids = results['match_id'].values
        for index in newest_matches.index:
                if newest_matches.loc[index, 'match_id'] in result_match_ids:
                   newest_matches.loc[index, 'is_finished'] = True
                else:
                    newest_matches.loc[index, 'is_finished'] = False
                   
                match = {'team_home_id': 0, 'team_home_name': 0, 'team_guest_id': 0, 'team_guest_name': 0,
                         'is_finished': 0, 'points_home': 0, 'points_guest': 0,
                         'date': 0, 'time': 0, 'location': 0}
                match['team_home_id'] = int(newest_matches.loc[index, 'team_home_id'])
                match['team_home_name'] = id_to_team[match['team_home_id']]
                match['team_guest_id'] = int(newest_matches.loc[index, 'team_guest_id'])
                match['team_guest_name'] = id_to_team[match['team_guest_id']]
                if newest_matches.loc[index, 'is_finished']:
                    result = results[(results['match_id'] == newest_matches.loc[index, 'match_id'])]
                    
                    endresult = result[result['result_type_id'] == self.END_RESULT]
                    match['is_finished'] = 1
                    match['points_home'] = int(endresult.iloc[0]['points_home'])
                    match['points_guest'] = int(endresult.iloc[0]['points_guest'])

                utc_string = newest_matches.loc[index, 'match_date_time_utc']
                date, time = self.split_utc(utc_string)
                match['date'] = date
                match['time'] = time

                # TODO: get location, maybe check what team is the home_team and get their stadion - > extra function (input:match, output:stadion)
                match['location'] = 'Unbekannt'# newest_matches.loc[index, 'location_arena'].item()

                all_matches[league][int(newest_matches.loc[index, 'match_id'])] = match

        return all_matches

# %%
if __name__ == '__main__':
    import time

    crawler = BundesligaCrawler()
    # teams = crawler.get_teams([1], [2020], 1)
    # print(teams.head())
    #matches, results = crawler.get_data_for_algo([1,2,3], [2011,2020],1,34,0,0)
    #print(crawler.get_next_matchday())
    # print(matches.head())
    # leagues = [1, 2, 3]
    # seasons = [2021]

    #crwlr = NBACrawler()

    #print(crwlr.get_next_matchday())
    #crwlr.get_available_data_for_leagues()
    #id_to_team, team_to_id = crwlr.get_team_dicts([1],[2020,2019,2018])

    matches, results = crawler.get_data_for_algo([1], [2020,2019],1,33,0,0)
    print(matches.shape)
    print(matches)
    # #results['points_home'] = results['points_home'].fillna(0)
    # for index, row in results.iterrows():
    #     if not(row['points_guest'] <= 200):
    #         print('ERROR')
    #         print(row['points_guest'])
# %%
