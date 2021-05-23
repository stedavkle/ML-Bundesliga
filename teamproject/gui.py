"""
web gui
"""
import sys

import eel
from crawler import getTeamDicts
from models import Model_Handler

"""Initialize Browser Presettings"""
my_options = {
    'host': 'localhost',
    'port': '8080'
}

''' globals '''
globals = sys.modules[__name__]
globals.id_team = 0
globals.team_id = 0
globals.seasons = 0
globals.league = 0

"""directory where web files located"""
eel.init('web')

""" FUNCTION COLLECTION """

# TODO: Crawler Call
@eel.expose
def start_crawler(league, seasons):
    id_teams, teams_id = getTeamDicts(league, seasons)
    globals.id_team = id_teams
    globals.league = league
    globals.seasons = seasons
    #print(globals.id_team)
    # Crawler wird aufgerufen


@eel.expose
def get_clubs():
    return globals.id_team


# TODO: Algo aufrufen und Parameter übergeben
@eel.expose
def start_algo(team1, team2, algo):
    print(team1)
    print(team2)
    print(algo)
    res_arr = Model_Handler(int(team1), int(team2), globals.seasons, globals.league, int(algo))

    print(res_arr)

    team1 = res_arr[0]
    team2 = res_arr[1]
    home = res_arr[2]
    draw = res_arr[3]
    guest = res_arr[4]
    print(home)
    print(draw)
    print(guest)

    return [team1, team2, "{:.1f}%".format(home), "{:.1f}%".format(draw), "{:.1f}%".format(guest)]

def main():
    eel.start('index.html', size=(800, 600))  # landing page of gui and window size
