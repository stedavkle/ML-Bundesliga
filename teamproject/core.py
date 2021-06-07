"""
web gui
"""
import sys

import eel
import numpy as np
import json

# from crawler import getTeamDicts
# from models import Model_Handler

"""Initialize Browser Presettings"""
my_options = {
    'host': 'localhost',
    'port': '8080'
}

"""directory where web files located"""
eel.init('web')

""" FUNCTION COLLECTION """


# TODO: Crawler Call
@eel.expose
def get_crawler_data(sport):
    # TODO: init crawler function call
    print("get_crawler_data(): executed successfully")
    # seasons = {2019: "2019/20", 2020: "2020/21"}
    # leagues = {1: "1. Bundesliga", 2: "2. Bundesliga", 3: "3. Bundesliga"}

    #seasons_bl1 = json.dumps(np.arange(2002, 2020).tolist())
    #seasons_bl2 = json.dumps(np.arange(2006, 2020).tolist())
    #seasons_bl3 = json.dumps(np.arange(2008, 2020).tolist())

    seasons_bl1 = np.arange(2002, 2020).tolist()
    seasons_bl2 = np.arange(2006, 2020).tolist()
    seasons_bl3 = np.arange(2008, 2020).tolist()

    # TODO: Wo lege ich die Instanz meiner Crawler Klasse an?
    # leagues, size = crawler.init()

    leagues = {1: {'name': '1. Bundesliga', 'seasons': seasons_bl1, 'size': len(seasons_bl1), 'matchdays': 34},
               2: {'name': '2. Bundesliga', 'seasons': seasons_bl2, 'size': len(seasons_bl2), 'matchdays': 34},
               3: {'name': '3. Liga', 'seasons': seasons_bl3, 'size': len(seasons_bl3), 'matchdays': 38}
               }
    print(leagues)

    return leagues


@eel.expose
def start_crawler(sport, leagues, seasons):
    # TODO: start crawler, WAS BEKOMME ICH ZURÜCK?
    print("start_crawler(): executed successfully")
    print(leagues)
    print(seasons)

    # crawler.get_dataset_of_matches_from_leagues_and_years(leagues, seasons)

    return None


@eel.expose
def get_required_model_data(sport, model):
    print("get_required_model_data(): executed successfully")
    print(sport)
    print(model)
    # TODO: Rückgabe der Auswahl von trainings und analysedaten (acc. to model instance)

    # Algo Instanz gibt Dict zurück mit nötigen parametern
    parameter = {'leagues': 1,
                 'seasons': 1,
                 'matchdays': 1,
                 'points': 0}

    return parameter


@eel.expose
def start_training_and_get_teams(sport, model, parameter):
    print("start_training(): executed successfully")
    print(model)
    print(parameter)
    return None


@eel.expose
def get_teams_from_crawler(sport, model, parameter):
    print("get_teams(): executed successfully")
    print(model)
    print(parameter)
    # TODO: Parameter abspeichern, Crawler Call get teams
    teams = {19: "Bayern München",
             93: "VfB Stuttgart",
             17: "Borussia M'Gladbach",
             100: "RB Leipzig",
             9: "Borussia Dortmund",
             1: "VfL Wolfsburg",
             24: "Werder Bremen",
             7: "SC Freiburg",
             8: "FC Augsburg",
             42: "Arminia Bielefeld",
             2: "1. FC Heidenheim"}

    return teams

@eel.expose
def get_next_opponent(id):
    print("get_next_opponent(): executed successfully")
    print(id)
    # TODO: Crawler Call (sollte Team Id zurück geben)
    return 42

@eel.expose
def start_prediction(sport, model, team1_id, team2_id):
    print("start_prediction(): executed successfully")
    # TODO: get Icons and start Prediction
    print(team1_id)
    print(team2_id)

    dummy = {'home': team1_id,
             'guest': team2_id,
             'img_home': "link zu Bild Team1",
             'img_guest': "link zu Bild Team1",
             'home_win': 0.2,
             'draw': 0.1,
             'guest_win': 0.7}

    return dummy


def main():
    eel.start('index.html', size=(800, 600))  # landing page of gui and window size
