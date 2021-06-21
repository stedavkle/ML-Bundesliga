"""
web gui
"""
import eel
import numpy as np
import json

import crawler
import models

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
    model_instance = ''
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

    model = models.Models()
    Core.model = model.get_models()
    return Core.model


@eel.expose
def get_required_model_data(model):
    print("get_required_model_data(): executed successfully")
    model = int(model)
    print(type(model))

    selected_model_data = Core.model[model]
    selected_model = selected_model_data['run']
    Core.model_instance = selected_model
    parameter = selected_model.get_model_requirements()

    print(parameter)
    print(type(Core.model_instance))

    return parameter


@eel.expose
def get_next_matchday_from_parameters(parameter):
    print("get_next_matchday_from_parameters(): executed successfully")
    print(parameter)

    Core.leagues = [int(i) for i in parameter['leagues']]
    Core.seasons = [int(i) for i in parameter['seasons']]
    Core.first_matchday = int(parameter['first_matchday'])
    Core.last_matchday = int(parameter['last_matchday'])
    Core.points = int(parameter['points'])

    print(Core.leagues)
    print(Core.seasons)

    #TODO: nächsten Spieltag vom Crawler beziehen
    crawler_instance = Core.crawler_instance
    dummy_crawler = crawler.Crawler()


    return None


@eel.expose
def start_training_and_get_teams():
    print("start_training_and_get_teams(): executed successfully")
    print()

    # TODO: Daten für Training vom Crawler beziehen
    crawler_instance = Core.crawler_instance

    # TODO: Daten für Training an model übergeben
    model_instance = Core.model_instance
    dummy_model = models.PoissonModel
    #model_instance.start_training()

    id_to_team, team_to_id = crawler_instance.get_team_dicts(Core.leagues, Core.seasons)
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

