# importing the required module
import matplotlib.pyplot as plt
import numpy

from teamproject import crawler
from teamproject import models


if __name__ == "__main__":
    cr = crawler.BundesligaCrawler()
    data = cr.get_data_for_algo([1], [2017, 2018, 2019, 2020], 0, 0, 0, 0)
    data_mostwins = cr.get_data_for_algo([1], [2017, 2018, 2019, 2020], 1, 34, 0, 0)

    # instanzen erstellen
    poisson = models.PoissonModel()
    regression = models.LogisticRegModel()
    mostwins = models.MostWins()

    # daten übergeben
    poisson.set_data(data)
    regression.set_data(data)
    mostwins.set_data(data_mostwins)

    # training starten
    poisson.start_training()
    regression.start_training()

    # predict starten
    poisson_outcome = poisson.predict(7, 175)
    regression_outcome = regression.predict('7', '175')
    mostwins_outcome = mostwins.predict(1635, 95)

    # alle teams
    id_to_team, team_to_id = cr.get_team_dicts([1], [2020])


def draw_analyses(league, season):
    matches, results = cr.get_matches_from_leagues_and_seasons_from_API(league, season)
    count_draws = 0
    count_total_games = 0
    for index in matches.index:
        if results.loc[index, 'points_home'] == results.loc[index, 'points_guest']:
            count_draws += 1

    count_total_games = matches.shape[0]
    print('Es gab im Jahr ' + str(season[0]) + ' in der ' + str(league[0]) + '. Bundesliga ingesamt ' + str(count_draws) + ' Unentschieden')
    print('und ' + str(count_total_games) + ' Spiele insgesamt. Das Verhältnis beträgt: ' + str(count_draws/count_total_games))

    ## prediction of mostwins

    # print(matches, results)

draw_analyses([1], [2017, 2018, 2019, 2020])

def poisson_2020_20():
    print('RB vs Augsburg: ')
    print(poisson.predict(1635, 95))
    print('BVB vs Hoffenheim: ')
    print(poisson.predict(7, 175))
    print('bayer vs Mainz: ')
    print(poisson.predict(6, 81))
    print('bremen vs freiburg: ')
    print(poisson.predict(134, 112))
    print('vfb vs hertha: ')
    print(poisson.predict(16, 54))
    print('berlin vs schalke: ')
    print(poisson.predict(80, 9))
    print('frankfurt vs köln: ')
    print(poisson.predict(91, 65))
    print('wolfsburg vs gladbach: ')
    print(poisson.predict(131, 87))
    print('bayern vs bielefeld: ')
    print(poisson.predict(40, 83))

def regression_2020_20():
    print('RB vs Augsburg: ')
    print(regression.predict(1635, 95))
    print('BVB vs Hoffenheim: ')
    print(regression.predict(7, 175))
    print('bayer vs Mainz: ')
    print(regression.predict(6, 81))
    print('bremen vs freiburg: ')
    print(regression.predict(134, 112))
    print('vfb vs hertha: ')
    print(regression.predict(16, 54))
    print('berlin vs schalke: ')
    print(regression.predict(80, 9))
    print('frankfurt vs köln: ')
    print(regression.predict(91, 65))
    print('wolfsburg vs gladbach: ')
    print(regression.predict(131, 87))
    print('bayern vs bielefeld: ')
    print(regression.predict(40, 83))

def mostwins_2020_20():
    print('RB vs Augsburg: ')
    print(mostwins.predict(1635, 95))
    print('BVB vs Hoffenheim: ')
    print(mostwins.predict(7, 175))
    print('bayer vs Mainz: ')
    print(mostwins.predict(6, 81))
    print('bremen vs freiburg: ')
    print(mostwins.predict(134, 112))
    print('vfb vs hertha: ')
    print(mostwins.predict(16, 54))
    print('berlin vs schalke: ')
    print(mostwins.predict(80, 9))
    print('frankfurt vs köln: ')
    print(mostwins.predict(91, 65))
    print('wolfsburg vs gladbach: ')
    print(mostwins.predict(131, 87))
    print('bayern vs bielefeld: ')
    print(mostwins.predict(40, 83))

    # print(poisson_outcome)
    # (regression_outcome)
    # print(mostwins_outcome)

#####


def poisson_2020_17():
    print('Gladbach vs Bremen')
    print(poisson.predict(87, 134))
    print('Leverkusen vs Dortmund')
    print(poisson.predict(6, 7))
    print('hertha vs Hoffenheim')
    print(poisson.predict(54, 175))
    print('Mainz vs Wolfsburg')
    print(poisson.predict(81, 131))
    print('Schalke vs Köln')
    print(poisson.predict(9, 65))
    print('Leipzig vs Berlin')
    print(poisson.predict(1635, 80))
    print('Freiburg vs Frankfurt')
    print(poisson.predict(112, 91))
    print('Augsburg vs München')
    print(poisson.predict(95, 40))
    print('Bielefeld vs Stuttgart')
    print(poisson.predict(83, 16))
    print()


def regression_2020_17():
    print('Gladbach vs Bremen')
    print(regression.predict(87, 134))
    print('Leverkusen vs Dortmund')
    print(regression.predict(6, 7))
    print('hertha vs Hoffenheim')
    print(regression.predict(54, 175))
    print('Mainz vs Wolfsburg')
    print(regression.predict(81, 131))
    print('Schalke vs Köln')
    print(regression.predict(9, 65))
    print('Leipzig vs Berlin')
    print(regression.predict(1635, 80))
    print('Freiburg vs Frankfurt')
    print(regression.predict(112, 91))
    print('Augsburg vs München')
    print(regression.predict(95, 40))
    print('Bielefeld vs Stuttgart')
    print(regression.predict(83, 16))
    print()


def mostwins_2020_17():
    print('Gladbach vs Bremen')
    print(mostwins.predict(87, 134))
    print('Leverkusen vs Dortmund')
    print(mostwins.predict(6, 7))
    print('hertha vs Hoffenheim')
    print(mostwins.predict(54, 175))
    print('Mainz vs Wolfsburg')
    print(mostwins.predict(81, 131))
    print('Schalke vs Köln')
    print(mostwins.predict(9, 65))
    print('Leipzig vs Berlin')
    print(mostwins.predict(1635, 80))
    print('Freiburg vs Frankfurt')
    print(mostwins.predict(112, 91))
    print('Augsburg vs München')
    print(mostwins.predict(95, 40))
    print('Bielefeld vs Stuttgart')
    print(mostwins.predict(83, 16))
    print()

# mostwins_2020_20()
# poisson_2020_20()
# regression_2020_20()

# mostwins_2020_17()
# poisson_2020_17()
# regression_2020_17()

# regression.predict(83, 16)