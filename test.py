"""Example tests."""
import pytest
import pandas as pd
import teamproject.crawler as crawler
# TODO: fehlermeldung beim import von models, weil darin der crawler
# TODO: aufgerufen wird und das wieder nicht funktioniert
# import teamproject.models as md

# TODO: AUSFÜHREN IM TERMINAL MIT:  python -m pytest ML-Bundesliga\test.py

cr = crawler.Crawler()
# md = models.Models()

def test_get_available_data_for_leagues():
    # tests get_available_data_for_leagues, is test
    @pytest.mark.parametrize("league", [1, 2, 3])
    @pytest.mark.parametrize("season", [2010, 2015, 2020])
    def test_get_teams_from_API(league, season):
        test_teams = cr.get_teams_from_API(league, season)
        assert isinstance(test_teams, pd.DataFrame)


# TODO: wir fangen bei get_available_data_for_leagues nicht ab, ob die eingabe überhaupt sinn ergibt

def test_get_matches_from_leagues_and_seasons_from_API():



 """data = md.prepare_data()
assert isinstance(data, pd.DataFrame)"""


""" def test_fetch_data():
    data = crawler.fetch_data()
    assert isinstance(data, pd.DataFrame)
    assert data.home_score.dtype == 'int64'
    assert data.guest_score.dtype == 'int64'
    assert (data.home_score >= 0).all()
    assert (data.guest_score >= 0).all()
    assert (data.home_team != data.guest_team).all() """
