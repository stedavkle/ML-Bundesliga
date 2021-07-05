"""
web gui
"""
import eel
import crawler
import models

''' --- CLASS DECLARATION --- '''


class Core:
    """Build Instance of Core: initialize GUI framework"""

    """Initialize Browser Presettings"""
    my_options = {
        # TODO: may change settings, after chromium portable is implemented
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
        eel.start('index.html', port=0, size=(1440, 900))  # landing page of gui and window size
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

    # TODO: rewrite crawler to abstract class, so sport selection also can be set here (- in a later version -)
    if sport == 1:
        Core.crawler_instance = crawler.Crawler()

        available_data = Core.crawler_instance.get_available_data_for_leagues()

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
    print("\nstart_crawler(): executed successfully")

    leagues = [int(i) for i in leagues]
    seasons = [int(i) for i in seasons]

    Core.crawler_instance.get_matches_from_leagues_and_seasons_from_API(leagues, seasons)

    model = models.Models()
    Core.model = model.get_models()
    return Core.model


@eel.expose
def get_required_model_data(model):
    """
    get required data for model from crawler
    :param model: id of model
    :return: dictionary with parameter options
    """
    print("\nget_required_model_data(): executed successfully")
    model = int(model)

    selected_model_data = Core.model[model]
    selected_model = selected_model_data['run']
    Core.model_instance = selected_model
    parameter = selected_model.get_model_requirements()

    return parameter


@eel.expose
def get_next_matchday_from_parameters(parameter):
    """
    stores selected parameters
    calls crawler for dictionary of next matchday
    :param parameter: dictionary of selected parameters
    :return: dictionary of matchdays
    """
    print("\nget_next_matchday_from_parameters(): executed successfully")

    Core.leagues = [int(i) for i in parameter['leagues']]
    Core.seasons = [int(i) for i in parameter['seasons']]
    Core.first_matchday = int(parameter['first_matchday'])
    Core.last_matchday = int(parameter['last_matchday'])
    Core.points = int(parameter['points'])

    crawler_instance = Core.crawler_instance

    matchday = crawler_instance.get_next_matchday()

    print(matchday)

    return matchday


@eel.expose
def start_training_and_get_teams():
    """
    gets training data from crawler, calls model for training
    gets list of available teams from crawler
    :return: dictionary of teams
    """
    print("\nstart_training_and_get_teams(): executed successfully")

    crawler_instance = Core.crawler_instance
    training_data = crawler_instance.get_data_for_algo(Core.leagues, Core.seasons, Core.first_matchday,
                                                       Core.last_matchday, 0, 0)

    model_instance = Core.model_instance
    model_instance.set_data(training_data)
    model_instance.start_training()

    id_to_team, team_to_id = crawler_instance.get_team_dicts(Core.leagues, Core.seasons)
    crawler_instance.get_team_icons_from_wiki()
    return id_to_team


@eel.expose
def get_next_opponent(id):
    """
    calls crawler for next opponent, depending on given team id
    :param id: team id
    :return: dictionary of next match
    """
    print("\nget_next_opponent(): executed successfully")

    crawler_instance = Core.crawler_instance
    match = crawler_instance.get_next_opponent(int(id))
    opponent_name = match['team_home_name']
    opponent_id = match['team_home_id']

    if opponent_id == id:
        opponent_name = match['team_guest_name']
        opponent_id = match['team_guest_id']

    next_opponent = {
        'opponent_id': opponent_id,
        'opponent_name': opponent_name,
        'date': match['date'],
        'time': match['time'],
        'location': match['location']
    }

    return next_opponent


@eel.expose
def start_prediction(team1_id, team2_id):
    """
    calls model to start prediction on two given team ids
    :param team1_id: home team id
    :param team2_id: guest team id
    :return: dictionary with results
    """
    print("\nstart_prediction(): executed successfully")

    model_instance = Core.model_instance
    result = model_instance.predict(int(team1_id), int(team2_id))

    result_dict = {
        'home': team1_id,
        'guest': team2_id,
        'outcome': result['outcome'],
        'score': result['score']
    }

    return result_dict
