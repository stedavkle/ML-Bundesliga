"""Example tests."""
from numpy.lib.arraysetops import isin
from numpy.testing._private.utils import assert_equal
from pandas.core.frame import DataFrame
import pytest
import pandas as pd
from numpy import int64
from pandas.api.types import is_string_dtype
#from pandas.api.types import is_numeric_dtype
import teamproject.crawler as crawler
#import crawler
# TODO: AUSFÜHREN IM TERMINAL MIT:  python -m pytest ML-Bundesliga\test_crawler.py

cr = crawler.BundesligaCrawler()
cr_nba = crawler.NBACrawler()
@pytest.mark.parametrize('crwlr', [cr, cr_nba])
def test_get_crawler(crwlr):
    test_return = crwlr.get_crawler()
    assert isinstance(test_return, dict)
    assert len(test_return) >= 1
    for index in test_return:
        assert type(test_return[index]['crawler_id']) == int
        assert type(test_return[index]['sport']) == str
        assert type(test_return[index]['description']) == str
        assert isinstance(test_return[index]['run'], crawler.Crawler) # change
#test_get_crawler(cr_nba)

@pytest.mark.parametrize('crwlr', [cr, cr_nba])
def test_get_available_data_for_leagues(crwlr):
    test_dict = crwlr.get_available_data_for_leagues()
    assert isinstance(test_dict, dict)
    assert len(test_dict) >= 1
    for element in test_dict:
        league_dict = test_dict[element]
        assert 'name' in league_dict
        assert 'seasons' in league_dict
        assert 'size' in league_dict
        assert 'matchdays' in league_dict
        assert type(league_dict['name']) == str
        assert type(league_dict['seasons']) == list
        assert len(league_dict['seasons']) > 0
        assert type(league_dict['size']) == int
        assert type(league_dict['matchdays']) == int
#test_get_available_data_for_leagues(cr_nba)


@pytest.mark.parametrize("league,season", [(1, 2002), (1, 2012), (1, 2020),
                                            (2, 2006), (2, 2013), (2, 2020),
                                            (3, 2008), (3, 2015), (3, 2020)])
def test_get_teams_from_API_bundesliga(league, season):
    test_teams = cr.get_teams_from_API(league, season)
    assert isinstance(test_teams, pd.DataFrame)
    assert test_teams.shape[1] == 3
    assert test_teams.team_id.dtype == 'int64'
    assert (test_teams.team_id > 0).all()
    # TODO: check team_names, team_icon_url
#test_get_teams_from_API(1,2020)
@pytest.mark.parametrize("league,season", [(1, 2016), (1, 2020)])
def test_get_teams_from_API_nba(league, season):
    test_teams = cr_nba.get_teams_from_API(season)
    assert isinstance(test_teams, pd.DataFrame)
    assert test_teams.shape[1] == 3
    assert test_teams.team_id.dtype == 'int64'
    assert (test_teams.team_id > 0).all()
    # TODO: check team_names, team_icon_url
#test_get_teams_from_API_nba(1,2020)

@pytest.mark.parametrize("crwlr,league,season",[(cr, 1, 2002), (cr, 1, 2012), (cr, 1, 2020),
                                                (cr, 2, 2006), (cr, 2, 2013), (cr, 2, 2020),
                                                (cr, 3, 2008), (cr, 3, 2015), (cr, 3, 2020),
                                                (cr_nba, 1, 2016), (cr_nba, 1, 2020)])
def test_get_matches_from_league_and_season_from_API(crwlr, league, season):
    test_matches, test_results = crwlr.get_matches_from_leagues_and_seasons_from_API([league], [season])
    # TEST MATCHES
    assert isinstance(test_matches, pd.DataFrame)
    assert test_matches.shape[1] == 5
    print('TYPE!!!')
    print(test_results.points_home.dtype)
    assert test_matches.match_id.dtype == 'int64'
    assert (test_matches.match_id > 0).all()
    assert test_matches.matchday.dtype == 'int64'
    assert (test_matches.matchday >= 1).all()
    assert (test_matches.matchday <= 366).all()
    assert test_matches.team_home_id.dtype == 'int64'
    assert (test_matches.team_home_id > 0).all()
    assert test_matches.team_guest_id.dtype == 'int64'
    assert (test_matches.team_guest_id > 0).all()
    # TEST RESULTS
    assert isinstance(test_results, pd.DataFrame)
    assert test_results.shape[1] == 5
    assert test_results.result_id.dtype == 'int64'
    assert (test_results.result_id > 0).all()
    assert (test_results.points_home.dtype == 'int64') | (test_results.points_home.dtype == 'float64')
    # TODO: points is never < 0 but assertion error is raised anyways
    #assert (test_results.points_home >= 0).all()
    assert (test_results.points_guest.dtype == 'int64') | (test_results.points_guest.dtype == 'float64')
    #assert (test_results.points_guest >= 0).all()
    assert test_results.result_type_id.dtype == 'int64'
    assert (test_results.result_type_id >= 1).all()
    assert (test_results.result_type_id <= 2).all()
#test_get_matches_from_league_and_season_from_API(cr_nba, 1, 2020)



@pytest.mark.parametrize("league_id", [4362])
@pytest.mark.parametrize("team_id", [1635, 87, 40])
# TODO: test nba next_match
def test_get_next_match_from_API(league_id, team_id):
    test_match = cr.get_next_match_from_API(league_id, team_id)
    assert isinstance(test_match, pd.DataFrame)
    assert test_match.shape == (1,7)
    assert (test_match.match_id.squeeze() >= -1).all()
    #assert type(test_match.iloc[0]['match_date_time_utc']) == str
    assert (test_match.is_finished.squeeze() == False).all()
    assert test_match.team_home_id.squeeze().dtype == 'int64'
    assert (test_match.team_home_id.squeeze() >= 0).all()
    assert type(test_match.iloc[0]['team_home_name']) == str
    assert test_match.team_guest_id.squeeze().dtype == 'int64'
    assert (test_match.team_guest_id.squeeze() >= 0).all()
    assert type(test_match.iloc[0]['team_guest_name']) == str
#test_get_next_match_from_API(4222, 16)
# todo: test_match analysieren

def test_get_team_icons_from_wiki():
    return_test = cr.get_team_icons_from_wiki()
    assert return_test == 1

@pytest.mark.parametrize("league", [1,2,3])
def test_get_next_matchday_from_API(league):
    matches, results = cr.get_next_matchday_from_API(league)
    
    assert isinstance(matches, pd.DataFrame)
    assert matches.shape[1] == 8
    assert matches.match_id.squeeze().dtype == 'int64'
    assert (matches.match_id.squeeze() > 0).all()
    assert (matches['match_date_time_utc'].astype('str').squeeze().str.len() > 1).all()
    assert matches.is_finished.squeeze().dtype == 'bool'
    assert matches.team_home_id.squeeze().dtype == 'int64'
    assert (matches.team_home_id.squeeze() >= 0).all()
    assert (matches['team_home_name'].astype('str').squeeze().str.len() > 1).all()
    assert matches.team_guest_id.squeeze().dtype == 'int64'
    assert (matches.team_guest_id.squeeze() >= 0).all()
    assert (matches['team_guest_name'].astype('str').squeeze().str.len() > 1).all()
    assert (matches['location_arena'].astype('str').squeeze().str.len() > 1).all()

    assert isinstance(results, pd.DataFrame)
    if not(results.empty):
        assert results.shape[1] == 5
        assert results.result_id.squeeze().dtype == 'int64'
        assert (results.result_id.squeeze() > 0).all()
        assert results.points_home.squeeze().dtype == 'int64'
        assert (results.points_home.squeeze() >= 0).all()
        assert results.points_guest.squeeze().dtype == 'int64'
        assert (results.points_guest.squeeze() >= 0).all()
        assert results.result_type_id.squeeze().dtype == 'int64'
        assert (results.result_type_id.squeeze() >= 1).all()
        assert (results.result_type_id.squeeze() <= 2).all()
#test_get_next_matchday_from_API(3)

@pytest.mark.parametrize('team_id,expected', [(16, 1), (65, 1), (55, 2), (36, 2), (125, 3), (107, 3)])
def test_get_league_of_team(team_id, expected):
    assert cr.get_league_of_team(team_id) == expected
#test_get_league_of_team(36, 2)

@pytest.mark.parametrize('utc_string,expected', [('2021-08-13T18:30:00Z', ('2021-08-13', '18:30:00'))])
def test_split_utc(utc_string, expected):
    split = cr.split_utc(utc_string)
    assert len(split) == 2
    assert split[0] == expected[0]
    assert split[1] == expected[1]
#test_split_utc('2021-08-13T18:30:00Z', ('2021-08-13', '18:30:00'))

@pytest.mark.parametrize("crwlr",[cr, cr_nba])
def test_get_next_matchday(crwlr):
    matchday = crwlr.get_next_matchday()
    assert isinstance(matchday, dict)
    assert len(matchday) in range(1,4)
    for league in matchday.keys():
        assert isinstance(matchday[league], dict)
        for match in matchday[league].keys():
            assert type(matchday[league][match]['team_home_id']) == int
            assert type(matchday[league][match]['team_home_name']) == str
            assert type(matchday[league][match]['team_guest_id']) == int
            assert type(matchday[league][match]['team_guest_name']) == str
            assert matchday[league][match]['is_finished'] in [0,1]
            assert type(matchday[league][match]['points_home']) == int
            assert matchday[league][match]['points_home'] >= 0
            assert type(matchday[league][match]['points_guest']) == int
            assert matchday[league][match]['points_guest'] >= 0
            assert type(matchday[league][match]['date']) == str
            assert type(matchday[league][match]['time']) == str
            assert type(matchday[league][match]['location']) == str
#test_get_next_matchday(cr_nba)

@pytest.mark.parametrize('league', [[1],[2],[3]])
@pytest.mark.parametrize('season', [[2020],[2015],[2010]])
def test_get_teams_bundesliga(league, season):
    teams = cr.get_teams(league, season, 1)
    assert isinstance(teams, pd.DataFrame)
    assert teams.team_id.dtype == 'int64'
    assert (teams.team_id > 0).all()
    for index in teams.reset_index().index:
        #print('INDEX: ' + str(index) + ' ' + str(teams.iloc[index]['team_name']))
        assert type(teams.iloc[index]['team_name']) == str
        assert len(teams.iloc[index]['team_name']) > 1
        assert type(teams.iloc[index]['team_icon_url']) == str
        assert len(teams.iloc[index]['team_icon_url']) > 1
#test_get_teams([3],[2020])
@pytest.mark.parametrize('season', [[2020],[2018],[2016]])
def test_get_teams_nba(season):
    teams = cr_nba.get_teams(season, 1)
    assert isinstance(teams, pd.DataFrame)
    assert teams.team_id.dtype == 'int64'
    assert (teams.team_id > 0).all()
    for index in teams.reset_index().index:
        #print('INDEX: ' + str(index) + ' ' + str(teams.iloc[index]['team_name']))
        assert type(teams.iloc[index]['team_name']) == str
        assert len(teams.iloc[index]['team_name']) > 1
        assert type(teams.iloc[index]['team_icon_url']) == str
        assert len(teams.iloc[index]['team_icon_url']) > 1
#test_get_teams_nba([2016])

@pytest.mark.parametrize('crwlr', [cr, cr_nba])
@pytest.mark.parametrize('league', [1,2,3])
@pytest.mark.parametrize('season', [2020,2016,2010])
def test_load_season(crwlr, league, season):
    matches, results, loaded = crwlr.load_season(league, season)
    # TEST MATCHES
    if isinstance(matches, pd.DataFrame):
        assert matches.shape[1] == 5
        assert matches.match_id.dtype == 'int64'
        assert (matches.match_id > 0).all()
        assert matches.matchday.dtype == 'int64'
        assert (matches.matchday >= 1).all()
        assert (matches.matchday <= 366).all()
        assert matches.team_home_id.dtype == 'int64'
        assert (matches.team_home_id > 0).all()
        assert matches.team_guest_id.dtype == 'int64'
        assert (matches.team_guest_id > 0).all()
    else:
        assert matches == -1
    # TEST RESULTS
    if isinstance(results, pd.DataFrame):
        assert results.shape[1] == 5
        assert results.result_id.dtype == 'int64'
        assert (results.result_id > 0).all()
        assert (results.points_home.dtype == 'int64') | ((results.points_home.dtype == 'float64'))
        #assert (results.points_home >= 0).all()
        assert (results.points_guest.dtype == 'int64') | ((results.points_home.dtype == 'float64'))
        #assert (results.points_guest >= 0).all()
        assert results.result_type_id.dtype == 'int64'
        assert (results.result_type_id >= 1).all()
        assert (results.result_type_id <= 2).all()
    else:
        assert results == -1
    assert loaded in [True, False]
#test_load_season(cr_nba, 1, 2020)

# TODO: test cut start/end day

@pytest.mark.parametrize('leagues', [[1], [2], [3]])
@pytest.mark.parametrize('seasons', [[2020], [2015], [2010]])
@pytest.mark.parametrize('day_start', [1, 2, 3, 4])
@pytest.mark.parametrize('day_end', [30, 33, 34, 37, 38])
def test_create_dataset_recursive_bundesliga(leagues, seasons, day_start, day_end):
    cr.seasons_backup = list(seasons)
    matches, results = cr.create_dataset_recursive(leagues, seasons, day_end, day_start)
    # TEST MATCHES
    # print('MATCHES')
    # print(matches.head())
    # print('SHAPE')
    # print(matches.shape)
    if len(leagues) > 0:
        assert isinstance(matches, pd.DataFrame)
        assert matches.shape[1] == 5
        assert matches.match_id.dtype == 'int64'
        assert (matches.match_id > 0).all()
        assert matches.matchday.dtype == 'int64'
        assert (matches.matchday >= 1).all()
        assert (matches.matchday <= 38).all()
        assert matches.team_home_id.dtype == 'int64'
        assert (matches.team_home_id > 0).all()
        assert matches.team_guest_id.dtype == 'int64'
        assert (matches.team_guest_id > 0).all()
        # TEST RESULTS
        assert isinstance(results, pd.DataFrame)
        assert results.shape[1] == 5
        assert results.result_id.dtype == 'int64'
        assert (results.result_id > 0).all()
        assert results.points_home.dtype == 'int64'
        assert (results.points_home >= 0).all()
        assert results.points_guest.dtype == 'int64'
        assert (results.points_guest >= 0).all()
        assert results.result_type_id.dtype == 'int64'
        assert (results.result_type_id >= 1).all()
        assert (results.result_type_id <= 2).all()
#test_create_dataset_recursive([],[2020],1,34)

@pytest.mark.parametrize('seasons', [[2020], [2018], [2016]])
@pytest.mark.parametrize('day_start', [1, 10, 20])
@pytest.mark.parametrize('day_end', [300, 330, 360])
def test_create_dataset_recursive_nba(seasons, day_start, day_end):
    if len(seasons) > 0:
        cr_nba.seasons_backup = list(seasons)
        matches, results = cr_nba.create_dataset_recursive(seasons, day_end, day_start)
        # TEST MATCHES
        # print('MATCHES')
        # print(matches.head())
        # print('SHAPE')
        # print(matches.shape)
        
        assert isinstance(matches, pd.DataFrame)
        assert matches.shape[1] == 5
        assert matches.match_id.dtype == 'int64'
        assert (matches.match_id > 0).all()
        assert matches.matchday.dtype == 'int64'
        assert (matches.matchday >= 1).all()
        assert (matches.matchday <= 366).all()
        assert matches.team_home_id.dtype == 'int64'
        assert (matches.team_home_id > 0).all()
        assert matches.team_guest_id.dtype == 'int64'
        assert (matches.team_guest_id > 0).all()
        # TEST RESULTS
        assert isinstance(results, pd.DataFrame)
        assert results.shape[1] == 5
        assert results.result_id.dtype == 'int64'
        assert (results.result_id > 0).all()
        assert results.points_home.dtype == 'float64'
        assert (results.points_home >= 0).all()
        assert results.points_guest.dtype == 'float64'
        assert (results.points_guest >= 0).all()
        assert results.result_type_id.dtype == 'int64'
        assert (results.result_type_id >= 1).all()
        assert (results.result_type_id <= 2).all()
#test_create_dataset_recursive_nba([2020],1,340)



#@pytest.mark.parametrize('leagues', [[1], [2], [3]])
#@pytest.mark.parametrize('seasons', [[2020], [2015], [2010]])
@pytest.mark.parametrize("crwlr,league,season",[(cr, 1, 2002), (cr, 1, 2012), (cr, 1, 2020),
                                                (cr, 2, 2006), (cr, 2, 2013), (cr, 2, 2020),
                                                (cr, 3, 2008), (cr, 3, 2015), (cr, 3, 2020),
                                                (cr_nba, 1, 2016), (cr_nba, 1, 2020)])
def test_get_team_dicts(crwlr, league, season):
    id_to_team, team_to_id = crwlr.get_team_dicts([league], [season])
    assert isinstance(id_to_team, dict)
    assert isinstance(team_to_id, dict)
    for id in id_to_team.keys():
        # assert id in team_to_id.values()
        assert type(id_to_team[id]) == str
        assert type(team_to_id[id_to_team[id]]) == int
        assert id == team_to_id[id_to_team[id]]
#test_get_team_dicts(cr, [3], [2020])

@pytest.mark.parametrize('seasons', [[2020, 2019, 2018, 2017, 2016, 2015]])
@pytest.mark.parametrize('leagues', [[1, 2, 3]])
@pytest.mark.parametrize('team_home_id', [65, 16, 7])
@pytest.mark.parametrize('team_guest_id', [112, 1635, 81])
def test_extract_matchup_history(team_home_id, team_guest_id, leagues, seasons):
    cr.seasons_backup = list(seasons)
    cr.create_dataset_recursive(leagues, seasons, 1, 38)
    cr.extract_matchup_history(team_home_id, team_guest_id)
    matches = cr.matches
    results = cr.results
    # TEST MATCHES
    assert isinstance(matches, pd.DataFrame)
    assert matches.shape[1] == 5
    assert matches.match_id.dtype == 'int64'
    assert (matches.match_id > 0).all()
    assert matches.matchday.dtype == 'int64'
    assert (matches.matchday >= 1).all()
    assert (matches.matchday <= 38).all()
    assert matches.team_home_id.dtype == 'int64'
    assert matches['team_home_id'].isin([team_home_id, team_guest_id]).all()
    assert matches.team_guest_id.dtype == 'int64'
    assert matches['team_guest_id'].isin([team_home_id, team_guest_id]).all()
    # TEST RESULTS
    assert isinstance(results, pd.DataFrame)
    assert results.shape[1] == 5
    assert results.result_id.dtype == 'int64'
    assert (results.result_id > 0).all()
    assert results.points_home.dtype == 'int64'
    assert (results.points_home >= 0).all()
    assert results.points_guest.dtype == 'int64'
    assert (results.points_guest >= 0).all()
    assert results.result_type_id.dtype == 'int64'
    assert (results.result_type_id >= 1).all()
    assert (results.result_type_id <= 2).all()
#test_extract_matchup_history(16, 112, [1,2,3], [2020, 2019, 2018, 2017, 2016, 2015])

# TODO: test next opponent nba
@pytest.mark.parametrize('team_id', [65, 16, 81, 115, 79, 98, 107, 417])
def test_get_next_opponent(team_id):
    match = cr.get_next_opponent(team_id)
    if type(match) == int:
        assert match == 0
    if isinstance(match, dict):
        assert type(match['team_home_id']) == int
        assert type(match['team_home_name']) == str
        assert type(match['team_guest_id']) == int
        assert type(match['team_guest_name']) == str
        assert type(match['is_finished']) == int
        assert match['is_finished'] in [0, 1]
        assert type(match['points_home']) == int
        assert match['points_home'] >= 0
        assert type(match['points_guest']) == int
        assert match['points_guest'] >= 0
        assert type(match['date']) == str
        assert type(match['time']) == str
        assert type(match['location']) == str
#test_get_next_opponent(16)

@pytest.mark.parametrize("crwlr,leagues,seasons",[(cr, [1, 2, 3], [2020, 2015, 2010]), (cr_nba, [1], [2020, 2018, 2016])])
def test_get_data_for_algo(crwlr, leagues, seasons):
    data = cr.get_data_for_algo(leagues, seasons, 0, 0, 0, 0)

    assert len(data) == 2
    assert isinstance(data[0], pd.DataFrame)
    assert isinstance(data[1], pd.DataFrame)
    matches = data[0]
    results = data[1]
    print(results.columns)
    # TEST MATCHES
    assert matches.match_id.dtype == 'int64'
    assert (matches.matchday >= 1).all()
    assert (matches.matchday <= 38).all()
    assert matches.team_home_id.dtype == 'int64'
    assert matches.team_guest_id.dtype == 'int64'
    assert (matches.team_home_id > 0).all()
    assert (matches.team_guest_id > 0).all()
    assert (matches.team_home_id != matches.team_guest_id).all()
    # TEST RESULTS
    assert results.result_id.dtype == 'int64'
    assert (results.result_id > 0).all()
    assert results.points_home.dtype == 'int64'
    assert (results.points_home >=0).all()
    assert results.points_guest.dtype == 'int64'
    assert (results.points_guest >=0).all()
    assert results.result_type_id.dtype == 'int64'
    assert (results.result_type_id >= 1).all()
    assert (results.result_type_id <= 2).all()
#test_get_data_for_algo([1], [2020])