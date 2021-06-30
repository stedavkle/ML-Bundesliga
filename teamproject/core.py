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
    """Build Instance of Core: initialize GUI framework"""

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
        eel.start('index.html', size=(1024, 768))  # landing page of gui and window size
        print("Object of class 'Core' initialized.")


""" FUNCTION COLLECTION """


@eel.expose
def get_crawler_data(sport):
    """
    calls crawler for data
    :param sport: id of selected sport
    :return: dictionary of leagues and seasons
    """
    print("get_crawler_data(): executed successfully")
    sport = int(sport)
    Core.sport = sport

    # TODO: Crawler auf abstrakte Klasse umschreiben
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
    """
    league and season values casted to int and send to crawler
    calls models.py for available models
    :param leagues: list of league id
    :param seasons: list of seasons
    :return: dictionary of available models
    """
    print("start_crawler(): executed successfully")

    leagues = [int(i) for i in leagues]
    seasons = [int(i) for i in seasons]
    print(leagues)
    print(seasons)

    Core.crawler_instance.get_matches_from_leagues_and_seasons_from_API(leagues, seasons)

    model = models.Models()
    print(model)
    Core.model = model.get_models()
    return Core.model


@eel.expose
def get_required_model_data(model):
    """
    get required data for model from crawler
    :param model: id of model
    :return: dictionary with parameter options
    """
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
    """
    stores selected parameters
    calls crawler for dictionary of next matchday
    :param parameter: dictionary of selected parameters
    :return: dictionary of matchdays
    """
    print("get_next_matchday_from_parameters(): executed successfully")
    print(parameter)

    Core.leagues = [int(i) for i in parameter['leagues']]
    Core.seasons = [int(i) for i in parameter['seasons']]
    Core.first_matchday = int(parameter['first_matchday'])
    Core.last_matchday = int(parameter['last_matchday'])
    Core.points = int(parameter['points'])

    print(Core.leagues)
    print(Core.seasons)

    crawler_instance = Core.crawler_instance

    # TODO: einkommentieren, sobald irgendwas tut
    matchday = crawler_instance.get_next_matchday()

    match = {'team_home_name': 'Bayern München',
             'team_home_id': 40,
             'team_guest_name': 'Eintracht Frankfurt',
             'team_guest_id': 91,
             'points_home': 4,
             'points_guest': 2,
             'is_finished': 0,
             'date': '2021-05-22',
             'time': '15:30:00',
             'location': 'Allianz Arena'}

    matchday = {1: {978: match,
                    567: match},
                2: {234: match,
                    567: match},
                3: {568: match,
                    123: match}
                }
    #print(matchday[1][58877])
    return matchday #{key: matchday[key] for key in Core.leagues}


@eel.expose
def start_training_and_get_teams():
    """
    gets training data from crawler, calls model for training
    gets list of available teams from crawler
    :return: dictionary of teams
    """
    print("start_training_and_get_teams(): executed successfully")

    crawler_instance = Core.crawler_instance
    training_data = crawler_instance.get_data_for_algo(Core.leagues, Core.seasons, Core.first_matchday,
                                                       Core.last_matchday, 0, 0)

    model_instance = Core.model_instance
    model_instance.set_data(training_data)
    model_instance.start_training()

    id_to_team, team_to_id = crawler_instance.get_team_dicts(Core.leagues, Core.seasons)
    crawler_instance.get_team_icons_from_wiki()
    print(id_to_team)
    return id_to_team


@eel.expose
def get_next_opponent(id):
    """
    calls crawler for next opponent, depending on given team id
    :param id: team id
    :return: dictionary of next match
    """
    print("get_next_opponent(): executed successfully")
    print(id)
    # TODO: Crawler Call (sollte Team Id zurück geben, falls kein next Match, gebe 0 zurück)

    crawler_instance = Core.crawler_instance
    # TODO: einkommentieren, wenns geht
    #match = crawler_instance.get_next_opponent(int(id))

    #print(match)

    match = {'team_home_name': 'Bayern München',
             'team_home_id': 40,
             'team_guest_name': 'Eintracht Frankfurt',
             'team_guest_id': 91,
             'points_home': 4,
             'points_guest': 2,
             'is_finished': 0,
             'date': '2021-05-22',
             'time': '15:30:00',
             'location': 'Allianz Arena'}

    # TODO: team id gegenchecken und gegner umschreiben in opponent
    # --> neue Struktur:
    new = {'opponent_id': 6,
           'opponent_name': 'Bayer Leverkusen',
           'date': '2021-05-22',
           'time': '15:30:00',
           'location': 'Allianz Arena'}

    return 0


@eel.expose
def start_prediction(team1_id, team2_id):
    """
    calls model to start prediction on two given team ids
    :param team1_id: home team id
    :param team2_id: guest team id
    :return: dictionary with results
    """
    print("start_prediction(): executed successfully")
    print(team1_id)
    print(team2_id)

    model_instance = Core.model_instance
    result = model_instance.predict(int(team1_id), int(team2_id))

    print(result)

    # TODO: wenn score nicht da: score: -1
    test = {
        'outcome': {
            'home_win': 0.2,
            'draw': 0.1,
            'guest_win': 0.7
        },
        'score': {
            1: {
                'home_points': 4,
                'guest_points': 2,
                'probability': 0.2}
        },
        2: {
            'home_points': 0,
            'guest_points': 1,
            'probability': 0.9
        }
    }

    result_dict = {
        'home': team1_id,
        'guest': team2_id,
        'outcome': result['outcome'],
        'score': result['score']
    }


    return result_dict
