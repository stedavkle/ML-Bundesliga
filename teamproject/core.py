"""
web gui
"""
import eel
import numpy as np
import json

import crawler

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
    model = 0
    leagues = []
    seasons = []
    first_matchday = 0
    last_matchday = 0
    points = 0

    def __init__(self):
        eel.start('index.html', size=(800, 600))  # landing page of gui and window size
        print("Object of class 'Core' initialized.")




""" FUNCTION COLLECTION """


# TODO: Crawler Call Docstring
@eel.expose
def get_crawler_data(sport):
    sport = int(sport)
    Core.sport = sport

    if sport == 1:
        Core.crawler_instance = crawler.Crawler()

        available_data = Core.crawler_instance.get_available_data_for_leagues()
        print(available_data)

        return available_data
    else:
        print("get_crawler_data(): no sport selected")
        return None


@eel.expose
def start_crawler_get_models(leagues, seasons):
    print("start_crawler(): executed successfully")

    leagues = [int(i) for i in leagues]
    seasons = [int(i) for i in seasons]
    print(leagues)
    print(seasons)

    Core.crawler_instance.get_matches_from_leagues_and_seasons_from_API(leagues, seasons)

    # TODO: get Models
    models = {
        1: {'model_id': 1,
            'model': 'trivialer Algorithmus',
            'description': 'Einfacher Algorithmus, der Ergebnisse aller bisherigen Partieen zweier Teams vergleicht.',
            'training': 0
            },
        2: {'model_id': 2,
            'model': 'dummy Model',
            'description': 'ML Model DUMMY',
            'training': 1
            }
    };

    return models


@eel.expose
def get_required_model_data(model):
    print("get_required_model_data(): executed successfully")
    print(type(model))
    Core.model = model


    # TODO: Rückgabe der Auswahl von trainings und analysedaten (acc. to model instance)

    # Algo Instanz gibt Dict zurück mit nötigen parametern
    parameter = {'leagues': 1,
                 'seasons': 1,
                 'matchdays': 1,
                 'points': 0}

    return parameter


@eel.expose
def start_training_and_get_teams(parameter):
    print("start_training(): executed successfully")
    print(parameter)
    return None

# TODO: Zwischenschritt datenübergabe, get next matchday

@eel.expose
def get_teams_from_crawler(parameter):
    print("get_teams(): executed successfully")
    print(parameter)

    Core.leagues = [int(i) for i in parameter['leagues']]
    Core.seasons = [int(i) for i in parameter['seasons']]
    Core.first_matchday = int(parameter['first_matchday'])
    Core.last_matchday = int(parameter['last_matchday'])
    Core.points = int(parameter['points'])

    print(Core.leagues)
    print(Core.seasons)

    # TODO: Parameter abspeichern, Crawler Call get teams

    id_to_team, team_to_id = Core.crawler_instance.get_team_dicts(Core.leagues, Core.seasons)
    print(id_to_team)
    return id_to_team

@eel.expose
def get_next_opponent(id):
    print("get_next_opponent(): executed successfully")
    print(id)
    # TODO: Crawler Call (sollte Team Id zurück geben)
    return 42

@eel.expose
def start_prediction(team1_id, team2_id):
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

