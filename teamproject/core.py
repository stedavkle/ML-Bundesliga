"""
web gui
"""
import eel
import numpy as np
import json

import crawler


# TODO: macht der Spaß wirklich Sinn? Doch lieber Globals?

''' --- CLASS DECLARATION --- '''
class Core:
    """Initialize Browser Presettings"""
    my_options = {
        'host': 'localhost',
        'port': '8080'
    }
    """directory where web files located"""
    eel.init('web')

    """set instace variables"""
    sport = 0
    crawler_instance = ''

    def __init__(self):
        eel.start('index.html', size=(800, 600))  # landing page of gui and window size
        print("Object of class 'Core' initialized.")




""" FUNCTION COLLECTION """


# TODO: Crawler Call
@eel.expose
def get_crawler_data(sport):
    sport = int(sport)
    Core.sport = sport

    if sport == 1:
        Core.crawler_instance = crawler.Crawler()

        leagues = Core.crawler_instance.get_available_seasons_for_leagues()
        print(leagues)

        return leagues
    else:
        print("get_crawler_data(): no sport selected")
        return None


@eel.expose
def start_crawler(leagues, seasons):
    print("start_crawler(): executed successfully")

    leagues = [int(i) for i in leagues]
    seasons = [int(i) for i in seasons]
    print(leagues)
    print(seasons)

    Core.crawler_instance.get_matches_from_leagues_and_seasons_from_API(leagues, seasons)
    return None


@eel.expose
def get_required_model_data(model):
    print("get_required_model_data(): executed successfully")
    print(type(model))
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

