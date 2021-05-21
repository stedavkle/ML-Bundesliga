"""
web gui
"""

import eel

"""Initialize Browser Presettings"""
my_options = {
    'host': 'localhost',
    'port': '8080'
}

""" TEST DATA """
clubs = {   19: "Bayern München",
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

"""directory where web files located"""
eel.init('web')

""" FUNCTION COLLECTION """

# TODO: Crawler Call
@eel.expose
def start_crawler():
    print("start_crawler executed")
    # Crawler wird aufgerufen


@eel.expose
def get_clubs(league):
    return clubs


# TODO: Algo aufrufen und Parameter übergeben
@eel.expose
def start_algo(team1, team2):
    result = [team1, team2, '60%', '10%', '30%']
    print(result)
    return result

def main():
    eel.start('index.html', size=(600, 400))  # landing page of gui and window size
