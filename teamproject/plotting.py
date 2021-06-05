# plotting certain statistics

# importing the required module
import matplotlib.pyplot as plt
import numpy

import crawler


#### game result ####
def plot_game_result_distribution(league, seasons):
    """ input: league
        output: how may times the game ended in home_win, tie, guest_win"""

    # initialize variables
    home_wins = 0
    ties = 0
    guest_wins = 0
    league_name = ''

    # get data from crawler
    cr = crawler.Crawler()
    dataset_matches, dataset_results, dataset_goals = cr.get_dataset_of_matches_from_leagues_and_years(league, seasons)

    # for loop to sum up amount of wins, ties, loses
    for index in dataset_results.index:
        if dataset_results.loc[index, 'points_home'] > dataset_results.loc[index, 'points_guest']:
            home_wins += 1
        elif dataset_results.loc[index, 'points_home'] == dataset_results.loc[index, 'points_guest']:
            ties += 1
        elif dataset_results.loc[index, 'points_home'] < dataset_results.loc[index, 'points_guest']:
            guest_wins += 1

    amounts = [home_wins, ties, guest_wins]
    result_types = ['Heim-Sieg', 'Unentschieden', 'Gast-Sieg']

    # create bars
    plt.bar(result_types, amounts)

    # names
    plt.xticks(result_types, result_types)

    # name allocation of league
    if league == 1:
        league_name = "Bundesliga"
    elif league == 2:
        league_name = "2. Bundesliga"
    elif league == 3:
        league_name = "3. Bundesliga"

    # title
    plt.title('1 -- Verteilung der Spielausgänge in der ' + str(league) + ' im Jahr ' + str(seasons))

    # show
    plt.show()

    # comment
    print()
    print('plot_game_result_distribution(' + str(league) + ' , ' + str(seasons) + ')')
    print('Dieses Schaubild zeigt eine Verteilung, wie häufig die Heimmannschaft gewonnen hat,'
          'wie häufig es ein Unentschieden gab. Und wie häufig die Gastmannschaft gewonnen hat.')
    print('_______')

#### mean of goals ####
def plot_mean_of_goals(league, seasons):
    ''' input: league, season
        output: plot of the mean of goals for home, guest and total'''

    # initialize variables
    goals_home = 0
    goals_guest = 0
    goals_total = 0
    game_amount = 0

    # get data from crawler
    cr = crawler.Crawler()
    dataset_matches, dataset_results, dataset_goals = cr.get_dataset_of_matches_from_leagues_and_years(league, seasons)

    # sum of goals
    for index in dataset_results.index:
        ''' this for loop iterates through the database and sums up the goals '''
        goals_home += dataset_results.loc[index, 'points_home']
        goals_guest += dataset_results.loc[index, 'points_guest']
        goals_total += dataset_results.loc[index, 'points_home'] + dataset_results.loc[index, 'points_guest']
        game_amount += 1

    # normalizing the goals with the amount of games
    goals_home = goals_home / game_amount
    goals_guest = goals_guest / game_amount
    goals_total = goals_total / game_amount

    amounts = [goals_home, goals_guest, goals_total]
    result_types = ['Tore fürs Heimteam', 'Tore fürs Auswärtsteam', 'Tore pro Spiel']

    # create bars
    plt.bar(result_types, amounts)

    # names
    plt.xticks(result_types, result_types)

    # name allocation of league
    if league == 1:
        league_name = "Bundesliga"
    elif league == 2:
        league_name = "2. Bundesliga"
    elif league == 3:
        league_name = "3. Bundesliga"

    # title
    plt.title('2 -- Anzahl der Tore pro Spiel in der ' + str(league) + ' im Jahr ' + str(seasons))
    # title
    # plt.title('Tor-Verteilung für Heim und Auswärtsteam und Total')

    # show
    plt.show()

    # comment
    print()
    print('plot_game_result_distribution(' + str(league) + ' , ' + str(seasons) + ')')
    print('Dieses Schaubild zeigt, wie viele Tore pro Spiel für das Heimteam,'
          'das Auswärtsteam und insgesamt gefallen sind. ')
    print('_______')

#### goal distribution ####
def plot_goal_distribution(league, seasons):
    ''' input: league, season
        output: plot of the goal distribution per game'''
    # initialize
    goals_per_game = 0

    # creating an array which contains the number of games with goals_per_game = index
    goal_amounts = numpy.zeros(13)

    # get data from crawler
    cr = crawler.Crawler()
    dataset_matches, dataset_results, dataset_goals = cr.get_dataset_of_matches_from_leagues_and_years(league, seasons)

    for index in dataset_results.index:
        goals_per_game = dataset_results.loc[index, 'points_home'] + dataset_results.loc[index, 'points_guest']
        # database[goals_home] + database[goals_guest]
        goal_amounts[goals_per_game] += 1

    # creating array to display amount of goals on x-axis
    result_types = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    # create bars
    plt.bar(result_types, goal_amounts)

    # names
    plt.xticks(result_types, result_types)

    # name allocation of league
    # if league[1] == 1:
    #    league_name = "Bundesliga"
    # elif league[1] == 2:
    #    league_name = "2. Bundesliga"
    # elif league[1] == 3:
    #    league_name = "3. Bundesliga"

    # title
    plt.title('3 -- Verteilung der Tore pro Spiel in der ' + str(league) + ' im Jahr ' + str(seasons))
    # plt.title('Verteilung der Tore pro Spiel in der ' + league_name + ' im Jahr ' + str(seasons))

    # show
    plt.show()

    # comment
    print()
    print('plot_game_result_distribution(' + str(league) + ' , ' + str(seasons) + ')')
    print('Dieses Schaubild zeigt ein Histogramm darüber, wie viele Tore'
          'geschossen wurden pro Spiel.')
    print('_______')

#### game result distribution for one team only ####
def plot_game_result_distribution_one_team(team_id, league, seasons):
    # initialize variables
    home_wins = 0
    ties = 0
    guest_wins = 0
    league_name = ''

    # get data from crawler
    cr = crawler.Crawler()
    dataset_matches, dataset_results, dataset_goals = cr.get_dataset_of_matches_from_leagues_and_years(league, seasons)

    # extrahiert alle matches an denen das Team teilnimmt
    match_data_cut = dataset_matches.loc[(dataset_matches['team_home_id'] == team_id) | (dataset_matches['team_guest_id'] == team_id)]
    # extrahiert alle results deren match_id in match_data_cut['match_id'] auftaucht
    # --------> pd.isin()
    result_data_cut = dataset_results[dataset_results['match_id'].isin(match_data_cut['match_id'])]

    for index in dataset_results.index:
        # if points of the home team > points of the guest team
        if dataset_results.loc[index, 'points_home'] > dataset_results.loc[index, 'points_guest']:
            # if chosen team (parameter) is the same as the home id, it counts as a home_win
            if team_id == dataset_matches.loc[index, 'team_home_id']:
                home_wins += 1
        # if points of the home team = points of the guest team
        elif dataset_results.loc[index, 'points_home'] == dataset_results.loc[index, 'points_guest']:
            ties += 1
        # if points of the home team < points of the guest team
        elif dataset_results.loc[index, 'points_home'] < dataset_results.loc[index, 'points_guest']:
            # if chosen team (parameter) is the same as the guest id, it counts as a guest_win
            if team_id == dataset_matches.loc[index, 'team_guest_id']:
                guest_wins += 1

    amounts = [home_wins, ties, guest_wins]
    result_types = ['Heim-Sieg', 'Unentschieden', 'Gast-Sieg']

    # create bars
    plt.bar(result_types, amounts)

    # names
    plt.xticks(result_types, result_types)

    # name allocation of league
    if league == 1:
        league_name = "Bundesliga"
    elif league == 2:
        league_name = "2. Bundesliga"
    elif league == 3:
        league_name = "3. Bundesliga"

    # title
    plt.title(
        'Verteilung der Spielausgänge der Mannschaft' + team_id + 'in der ' + league_name + ' im Jahr ' + str(seasons))

    # show
    plt.show()

    # comment
    print('plot_game_result_distribution_one_team(' + team_id + ' , ' + str(league) + ' , ' + str(seasons) + ')')
    print('Dieses Schaubild zeigt, wie häufig eine Mannschaft als Heimmannschaft und als Gastmannschaft gewonnen hat.'
          'Und wie häufig sie Unentschieden gespielt hat.')


#### functions for one team only ####

#### mean of goals for one team only ####
def plot_mean_of_goals_one_team(team_id, league, seasons):
    ''' input: team-id, league, season
        output: plot of the mean of goals for home_matches, guest_matches and total'''

    # initialize variables
    goals_as_home_team = 0
    goals_as_guest_team = 0
    goals_total = 0
    game_amount = 0

    # get data from crawler
    cr = crawler.Crawler()
    dataset_matches, dataset_results, dataset_goals = cr.get_dataset_of_matches_from_leagues_and_years(league, seasons)

    # sum of goals
    for index in dataset_results.index:
        ''' this for loop iterates through the database and sums up the goals '''
        # if given team id matches home_id, add goals to goals_as_home_team
        if team_id == dataset_matches[index, 'team_home_id']:
            goals_as_home_team += dataset_results.loc[index, 'points_home']
        # if given team id matches guest_id, add goals to goals_as_guest_team
        elif team_id == dataset_matches[index, 'team_guest_id']:
            goals_as_guest_team += dataset_results.loc[index, 'points_guest']
        # if given team id matches home_id or guest_id, add goals to goals_total
        elif team_id == dataset_matches[index, 'team_home_id'] or dataset_matches[index, 'team_guest_id']:
            goals_total += dataset_results.loc[index, 'points_home'] + dataset_results.loc[index, 'points_guest']
            game_amount += 1

    # normalizing the goals with the amount of games
    goals_home = goals_as_home_team / game_amount
    goals_guest = goals_as_guest_team / game_amount
    goals_total = goals_total / game_amount

    amounts = [goals_home, goals_guest, goals_total]
    result_types = ['Tore als Heimteam', 'Tore als Auswärtsteam', 'Tore pro Spiel']

    # create bars
    plt.bar(result_types, amounts)

    # names
    plt.xticks(result_types, result_types)

    # name allocation of league
    if league == 1:
        league_name = "Bundesliga"
    elif league == 2:
        league_name = "2. Bundesliga"
    elif league == 3:
        league_name = "3. Bundesliga"

    # title
    # plt.title('Anzahl der Tore pro Spiel in der ' + league_name + ' im Jahr ' + str(seasons))

    # title
    plt.title('Tor-Verteilung für Heim und Auswärtsteam und Total')

    # show
    plt.show()

    # comment
    print('plot_mean_of_goals_one_team(' + team_id + ' , ' + str(league) + ' , ' + str(seasons) + ')')
    print('Dieses Schaubild zeigt, wie viele Tore eine Mannschaft gemittelt pro Spiel geschossen hat.'
          'Ist unterteilt in als Heimmannschaft, als Gastmannschaft und Insgesamt.')


#### goal distribution for one team only ####
def plot_goal_distribution_one_team(team_id, league, seasons):
    # creating an array which contains the number of games with goals_per_game = index
    goal_amounts = numpy.zeros(13)

    # get data from crawler
    cr = crawler.Crawler()
    dataset_matches, dataset_results, dataset_goals = cr.get_dataset_of_matches_from_leagues_and_years(league, seasons)

    for index in dataset_results.index:
        if team_id == dataset_matches[index, 'team_home_id'] or dataset_matches[index, 'team_guest_id']:
            goals_per_game = dataset_results.loc[index, 'points_home']
            goal_amounts[goals_per_game] += 1
        if team_id == dataset_matches[index, 'team_guest_id']:
            goals_per_game = dataset_results.loc[index, 'points_guest']
            goal_amounts[goals_per_game] += 1

    # creating array to display amount of goals on x-axis
    result_types = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    # create bars
    plt.bar(result_types, goal_amounts)

    # names
    plt.xticks(result_types, result_types)

    # name allocation of league
    # if league[1] == 1:
    #    league_name = "Bundesliga"
    # elif league[1] == 2:
    #    league_name = "2. Bundesliga"
    # elif league[1] == 3:
    #    league_name = "3. Bundesliga"

    # title
    plt.title('Verteilung der Tore pro Spiel von ' + team_id + ' in der ' + ' im Jahr ' + str(seasons))

    # show
    plt.show()

    # comment
    print('plot_goal_distribution_one_team(' + team_id + ' , ' + str(league) + ' , ' + str(seasons) + ')')
    print(
        'Dieses Schaubild zeigt eine Verteilung an darüber, wie viele Tore eine Mannschaft in einem Spiel gemacht hat.')


#### function calls ####
plot_game_result_distribution([1], [2020])
plot_mean_of_goals([1], [2020])
plot_goal_distribution([1], [2020])
# plot_game_result_distribution_one_team(87, [1], [2020])
# plot_mean_of_goals_one_team(87, [1], [2020])
# plot_goal_distribution_one_team(87, [1], [2020])
