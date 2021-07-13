"""Example tests."""
import pytest
import pandas as pd
from numpy import int64
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import teamproject.crawler as crawler

# TODO: fehlermeldung beim import von models, weil darin der crawler
# TODO: aufgerufen wird und das wieder nicht funktioniert
# import teamproject.models as md

# TODO: AUSFÜHREN IM TERMINAL MIT:  python -m pytest ML-Bundesliga\test.py

cr = crawler.BundesligaCrawler()
# md = models.Models()

#def test_get_available_data_for_leagues():
#    test_dict = cr.get_available_data_for_leagues()
#    assert isinstance(test_dict, dict)
#    assert isinstance(test_dict[1]['seasons'], list)
#    for element in test_dict[1]['seasons']:
#        assert isinstance(element, int)
#        assert element >= 0

# TODO: No such file or directory: './data/bl1_2020_teams_unif.csv' lösen
# @pytest.mark.parametrize("league", [1, 2, 3])
# @pytest.mark.parametrize("season", [2010, 2015, 2020])
# def test_get_teams_from_API(league, season):
#   test_teams = cr.get_teams_from_API(league, season)
#   assert isinstance(test_teams, pd.DataFrame)
#   print(test_teams)

# TODO: No such file or directory: './data/bl1_2020_teams_unif.csv' lösen
# @pytest.mark.parametrize("league", [[1]])
# @pytest.mark.parametrize("season", [[2010], [2015], [2020]])
# def test_get_matches_from_leagues_and_seasons_from_API(league, season):
#    test_matches, test_results = cr.get_matches_from_leagues_and_seasons_from_API(league, season)
#    assert isinstance(test_matches, pd.DataFrame)
#    assert isinstance(test_results, pd.DataFrame)
# INHALTE ÜBERPRÜFEN

# test_get_matches_from_leagues_and_seasons_from_API([1], [2020])

# Todo: Expecting value: line 1 colmn 1
#@pytest.mark.parametrize("team_id", [16, 87, 40])
#@pytest.mark.parametrize("league_id", [4442])
#def test_get_next_match_from_API(league_id, team_id):
#    test_match = cr.get_next_match_from_API(league_id, team_id)
#    assert isinstance(test_match, pd.DataFrame)

#test_match = cr.get_next_match_from_API([4442], [16])
#print(test_match)

def test_get_team_icons_from_wiki():
    return_test = cr.get_team_icons_from_wiki()
    assert return_test == 1

# todo: json.decoder.JSONDecodeError: Expecting value: line 1 column 1
#@pytest.mark.parametrize("league", [[1]])
#def test_get_next_matchday_from_API(league):
    #test_matches, test_results = cr.get_next_matchday_from_API(league)
    #assert isinstance(test_matches, pd.DataFrame)

#@pytest.mark.parametrize("team_id", [16, 87, 40])
#def test_get_league_of_team(team_id):
#    test_return = cr.get_league_of_team(team_id)
#    assert isinstance(test_return, int)

#todo: split_utc, was für ein input ist utc_string

#todo: No such file or directory: './data/bl1_2021_teams_unif.csv'
#def test_get_next_matchday():
#    all_matches_of_the_day = cr.get_next_matchday()
#    assert isinstance(all_matches_of_the_day, pd.DataFrame)
#    print(all_matches_of_the_day)

#test_get_next_matchday()