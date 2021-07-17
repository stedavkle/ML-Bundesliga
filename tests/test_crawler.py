"""Example tests."""
from numpy.testing._private.utils import assert_equal
import pytest
import pandas as pd
from numpy import int64
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import teamproject.crawler as crawler
#import crawler
# TODO: AUSFÜHREN IM TERMINAL MIT:  python -m pytest ML-Bundesliga\test_crawler.py

cr = crawler.BundesligaCrawler()

def test_get_crawler():
    test_return = cr.get_crawler()
    assert isinstance(test_return, dict)
    assert len(test_return) >= 1
    assert type(test_return[1]['crawler_id']) == int
    assert type(test_return[1]['sport']) == str
    assert type(test_return[1]['description']) == str
    assert isinstance(test_return[1]['run'], crawler.Crawler) # change
#test_get_crawler()

def test_get_available_data_for_leagues():
    test_dict = cr.get_available_data_for_leagues()
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
#test_get_available_data_for_leagues()


@pytest.mark.parametrize("league,season", [(1, 2002), (1, 2012), (1, 2020),
                                            (2, 2006), (2, 2013), (2, 2020),
                                            (3, 2008), (3, 2015), (3, 2020)])
def test_get_teams_from_API(league, season):
    test_teams = cr.get_teams_from_API(league, season)
    assert isinstance(test_teams, pd.DataFrame)
    assert test_teams.shape[1] == 3
    assert test_teams.team_id.dtype == 'int64'
    assert (test_teams.team_id > 0).all()
    # TODO: check team_names, team_icon_url
#test_get_teams_from_API(1,2020)

@pytest.mark.parametrize("league", [1, 2, 3])
@pytest.mark.parametrize("season", [2008, 2015, 2020])

def test_get_matches_from_league_and_season_from_API(league, season):
    test_matches, test_results = cr.get_matches_from_league_and_season_from_API(league, season)
    # TEST MATCHES
    assert isinstance(test_matches, pd.DataFrame)
    assert test_matches.shape[1] == 5
    assert test_matches.match_id.dtype == 'int64'
    assert (test_matches.match_id > 0).all()
    assert test_matches.matchday.dtype == 'int64'
    assert (test_matches.matchday >= 1).all()
    assert (test_matches.matchday <= 38).all()
    assert test_matches.team_home_id.dtype == 'int64'
    assert (test_matches.team_home_id > 0).all()
    assert test_matches.team_guest_id.dtype == 'int64'
    assert (test_matches.team_guest_id > 0).all()
    # TEST RESULTS
    print(test_results.head())
    assert isinstance(test_results, pd.DataFrame)
    assert test_results.shape[1] == 5
    assert test_results.result_id.dtype == 'int64'
    assert (test_results.result_id > 0).all()
    assert test_results.points_home.dtype == 'int64'
    assert (test_results.points_home >= 0).all()
    assert test_results.points_guest.dtype == 'int64'
    assert (test_results.points_guest >= 0).all()
    assert test_results.result_type_id.dtype == 'int64'
    assert (test_results.result_type_id >= 1).all()
    assert (test_results.result_type_id <= 2).all()
#test_get_matches_from_league_and_season_from_API(1, 2020)



@pytest.mark.parametrize("league_id", [4362])
@pytest.mark.parametrize("team_id", [1635, 87, 40])
def test_get_next_match_from_API(league_id, team_id):
    test_match = cr.get_next_match_from_API(league_id, team_id)
    assert isinstance(test_match, pd.DataFrame)
    assert test_match.shape == (1,7)
    assert (test_match['match_id'] >= -1).bool()
    #assert type(test_match.iloc[0]['match_date_time_utc']) == str
    assert test_match['is_finished'].bool() == False
    assert test_match.iloc[0]['team_home_id'].dtype == 'int64'
    assert test_match.iloc[0]['team_home_id'] >= 0
    assert type(test_match.iloc[0]['team_home_name']) == str
    assert test_match.iloc[0]['team_guest_id'].dtype == 'int64'
    assert test_match.iloc[0]['team_guest_id'] >= 0
    assert type(test_match.iloc[0]['team_guest_name']) == str
#test_get_next_match_from_API(4222, 16)
# todo: test_match analysieren

def test_get_team_icons_from_wiki():
    return_test = cr.get_team_icons_from_wiki()
    assert return_test == 1

@pytest.mark.parametrize("league", [1,2,3])
def test_get_next_matchday_from_API(league):
    matches, results = cr.get_next_matchday_from_API(league)
    print(matches.head())
    print(results.head())

    assert isinstance(matches, pd.DataFrame)
    assert matches.shape[1] == 8
    assert isinstance(results, pd.DataFrame)
#test_get_next_matchday_from_API(1)