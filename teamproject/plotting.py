# plotting certain statistics

# importing the required module
import matplotlib.pyplot as plt
import numpy

from teamproject import crawler

cr = crawler.Crawler()


#### FUNCTIONS FOR SEASONS ####

#### game result ####
def plot_game_result_distribution(league, seasons):
    """ input: league
        output: how may times the game ended in home_win, tie, guest_win"""

    # initialize variables
    home_wins = 0
    ties = 0
    guest_wins = 0

    # get data from crawler
    dataset_matches, dataset_results, dataset_goals = cr.get_data_for_algo(league, seasons, 0, 0, 0, 0)

    # cut only end results
    dataset_results = dataset_results[dataset_results['result_type_id'] == 1]

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

    # title
    plt.title('1 -- Verteilung der Spielausgänge in der ' + str(league[0]) + '. Bundesliga im Jahr ' + str(seasons[0]))

    # save figure
    # TODO: if you want to save the file, uncomment here
    # plt.savefig(
    #    'C:/Users/User/Universität/plot_game_result_distribution_' + str(league[0]) + '_' + str(seasons[0]) + '.png')

    # show
    plt.show()

    # comment
    print()
    print('plot_game_result_distribution(' + str(league) + ' , ' + str(seasons) + ')')
    print('Dieses Schaubild zeigt eine Verteilung, wie häufig die Heimmannschaft gewonnen hat,\n'
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
    dataset_matches, dataset_results, dataset_goals = cr.get_data_for_algo(league, seasons, 0, 0, 0, 0)

    # cut only end results
    dataset_results = dataset_results[dataset_results['result_type_id'] == 1]

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

    # title
    plt.title('2 -- Anzahl der Tore pro Spiel in der ' + str(league[0]) + '. Bundesliga im Jahr ' + str(seasons[0]))

    # save figure
    # TODO: if you want to save the file, uncomment here
    # plt.savefig('C:/Users/User/Universität/plot_mean_of_goals_' + str(league[0]) + '_' + str(seasons[0]) + '.png')

    # show
    plt.show()

    # comment
    print()
    print('plot_mean_of_goals(' + str(league) + ' , ' + str(seasons) + ')')
    print('Dieses Schaubild zeigt, wie viele Tore pro Spiel für das Heimteam,'
          ' das Auswärtsteam und insgesamt gefallen sind. ')
    print('Tore fürs Heimteam: ' + str(round(goals_home, 2)))
    print('Tore fürs Auswärtsteam: ' + str(round(goals_guest, 2)))
    print('Tore Insgesamt: ' + str(round(goals_total, 2)))
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
    dataset_matches, dataset_results, dataset_goals = cr.get_data_for_algo(league, seasons, 0, 0, 0, 0)

    # cut only end results
    dataset_results = dataset_results[dataset_results['result_type_id'] == 1]

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

    # title
    plt.title('3 -- Verteilung der Tore pro Spiel in der ' + str(league[0]) + '. Bundesliga im Jahr ' + str(seasons[0]))

    # save figure
    # TODO: if you want to save the file, uncomment here
    # plt.savefig('C:/Users/User/Universität/plot_goal_distribution_' + str(league[0]) + '_' + str(seasons[0]) + '.png')

    # show
    plt.show()

    # comment
    print()
    print('plot_goal_distribution(' + str(league) + ' , ' + str(seasons) + ')')
    print('Dieses Schaubild zeigt ein Histogramm darüber, wie viele Tore'
          'geschossen wurden pro Spiel.')
    print('_______')


#### FUNCTIONS FOR ONE TEAM ####

#### without plot game result distribution for one team only ####
def game_result_distribution_one_team(team_id, league, seasons):
    ''' input: team-id, league, season
        output: plot of the distribution for home_wins, guest_wins and ties'''
    # get data from crawler
    dataset_matches, dataset_results, dataset_goals = cr.get_data_for_algo(league, seasons, 0, 0, 0, 0)

    # cut only end results
    dataset_results = dataset_results[dataset_results['result_type_id'] == 1]

    id_to_team, team_to_id = cr.get_team_dicts(league, seasons)

    # initialize variables
    home_wins = 0
    ties = 0
    guest_wins = 0
    game_amount = 0
    team_name = id_to_team[team_id]

    # extracts all matches from team_id
    match_data_cut = dataset_matches.loc[
        (dataset_matches['team_home_id'] == team_id) | (dataset_matches['team_guest_id'] == team_id)]
    # extracts all home matches from team_id
    home_match_data_cut = dataset_matches.loc[(dataset_matches['team_home_id'] == team_id)]
    # extracts all guest matches from team_id
    guest_match_data_cut = dataset_matches.loc[(dataset_matches['team_guest_id'] == team_id)]

    # gets the corresponding results table for all matches
    result_data_cut = dataset_results[dataset_results['match_id'].isin(match_data_cut['match_id'])]
    # gets the corresponding results table for the home matches
    home_result_data_cut = dataset_results[dataset_results['match_id'].isin(home_match_data_cut['match_id'])]
    # gets the corresponding results table for the guest matches
    guest_result_data_cut = dataset_results[dataset_results['match_id'].isin(guest_match_data_cut['match_id'])]

    # iterate through home result object to find the games, where the team won
    for index in home_result_data_cut.index:
        # if points of the home team > points of the guest team
        if home_result_data_cut.loc[index, 'points_home'] > home_result_data_cut.loc[index, 'points_guest']:
            home_wins += 1

    # iterate through guest result object to find the games, where the team won
    for index in guest_result_data_cut.index:
        if guest_result_data_cut.loc[index, 'points_home'] < guest_result_data_cut.loc[index, 'points_guest']:
            guest_wins += 1

    # iterate through result object of all games to find the games, where the teams played a tie
    for index in result_data_cut.index:
        if result_data_cut.loc[index, 'points_home'] == result_data_cut.loc[index, 'points_guest']:
            ties += 1
        game_amount += 1

    # normalize
    home_wins_percent = round(home_wins / game_amount, 2)
    guest_wins_percent = round(guest_wins / game_amount, 2)
    ties_percent = round(ties / game_amount, 2)
    loses_percent = round(1 - (home_wins_percent + guest_wins_percent + ties_percent), 2)

    # comment
    print()
    print('plot_game_result_distribution_one_team(' + str(team_id) + ' , ' + str(league) + ' , ' + str(seasons) + ')')
    print()
    print('Dieses Schaubild zeigt, wie häufig ' + team_name + ' als Heimmannschaft und als Gastmannschaft gewonnen hat.'
                                                              '\nUnd wie häufig sie unentschieden gespielt hat.')
    print('Als Heimmannschaft gewonnen: ' + str(home_wins_percent))
    print('Als Gastmannschaft gewonnen: ' + str(guest_wins_percent))
    print('Unentschieden: ' + str(ties_percent))
    print('Verloren dementsprechend: ' + str(loses_percent))
    print('______')


#### plot game result distribution for one team only ####
def plot_game_result_distribution_one_team(team_id, league, seasons):
    ''' input: team-id, league, season
        output: plot of the distribution for home_wins, guest_wins and ties'''
    # get data from crawler
    dataset_matches, dataset_results, dataset_goals = cr.get_data_for_algo(league, seasons, 0, 0, 0, 0)

    # cut only end results
    dataset_results = dataset_results[dataset_results['result_type_id'] == 1]

    id_to_team, team_to_id = cr.get_team_dicts(league, seasons)

    # initialize variables
    home_wins = 0
    ties = 0
    guest_wins = 0
    game_amount = 0
    team_name = id_to_team[team_id]

    # extracts all matches from team_id
    match_data_cut = dataset_matches.loc[
        (dataset_matches['team_home_id'] == team_id) | (dataset_matches['team_guest_id'] == team_id)]
    # extracts all home matches from team_id
    home_match_data_cut = dataset_matches.loc[(dataset_matches['team_home_id'] == team_id)]
    # extracts all guest matches from team_id
    guest_match_data_cut = dataset_matches.loc[(dataset_matches['team_guest_id'] == team_id)]

    # gets the corresponding results table for all matches
    result_data_cut = dataset_results[dataset_results['match_id'].isin(match_data_cut['match_id'])]
    # gets the corresponding results table for the home matches
    home_result_data_cut = dataset_results[dataset_results['match_id'].isin(home_match_data_cut['match_id'])]
    # gets the corresponding results table for the guest matches
    guest_result_data_cut = dataset_results[dataset_results['match_id'].isin(guest_match_data_cut['match_id'])]

    # iterate through home result object to find the games, where the team won
    for index in home_result_data_cut.index:
        # if points of the home team > points of the guest team
        if home_result_data_cut.loc[index, 'points_home'] > home_result_data_cut.loc[index, 'points_guest']:
            home_wins += 1

    # iterate through guest result object to find the games, where the team won
    for index in guest_result_data_cut.index:
        if guest_result_data_cut.loc[index, 'points_home'] < guest_result_data_cut.loc[index, 'points_guest']:
            guest_wins += 1

    # iterate through result object of all games to find the games, where the teams played a tie
    for index in result_data_cut.index:
        if result_data_cut.loc[index, 'points_home'] == result_data_cut.loc[index, 'points_guest']:
            ties += 1
        game_amount += 1

    # normalize
    home_wins_percent = round(home_wins / game_amount, 2)
    guest_wins_percent = round(guest_wins / game_amount, 2)
    ties_percent = round(ties / game_amount, 2)
    loses_percent = round(1 - (home_wins_percent + guest_wins_percent + ties_percent), 2)

    amounts = [home_wins, ties, guest_wins]
    result_types = ['Heim-Sieg', 'Unentschieden', 'Gast-Sieg']

    # create bars
    plt.bar(result_types, amounts)

    # names
    plt.xticks(result_types, result_types)

    # title
    plt.title(
        'Verteilung der Spielausgänge der Mannschaft \n'
        + team_name + ' aus der ' + str(league[0]) + '. Bundesliga im Jahr ' + str(seasons[0]))

    # save figure
    # TODO: if you want to save the file, uncomment here
    # plt.savefig(
    #   'C:/Users/User/Universität/plot_game_result_distribution_one_team_' + team_name + '_' + str(league[0]) + '_' + str(seasons[0]) + '.png')

    # show
    plt.show()

    # comment
    print()
    print('plot_game_result_distribution_one_team(' + str(team_id) + ' , ' + str(league) + ' , ' + str(seasons) + ')')
    print()
    print('Dieses Schaubild zeigt, wie häufig ' + team_name + ' als Heimmannschaft und als Gastmannschaft gewonnen hat.'
                                                              '\nUnd wie häufig sie unentschieden gespielt hat.')
    print('Als Heimmannschaft gewonnen: ' + str(home_wins_percent))
    print('Als Gastmannschaft gewonnen: ' + str(guest_wins_percent))
    print('Unentschieden: ' + str(ties_percent))
    print('Verloren dementsprechend: ' + str(loses_percent))
    print('______')


#### plot mean of goals for one team only ####
def plot_mean_of_goals_one_team(team_id, league, seasons):
    ''' input: team-id, league, season
        output: plot of the mean of goals for home_matches, guest_matches and total'''

    # get data from crawler
    dataset_matches, dataset_results, dataset_goals = cr.get_data_for_algo(league, seasons, 0, 0, 0, 0)
    id_to_team, team_to_id = cr.get_team_dicts(league, seasons)

    # cut only end results
    dataset_results = dataset_results[dataset_results['result_type_id'] == 1]

    # initialize variables
    goals_as_home_team = 0
    goals_as_guest_team = 0
    goals_total = 0
    game_amount = 0
    team_name = id_to_team[team_id]

    # extracts all matches from team_id
    match_data_cut = dataset_matches.loc[
        (dataset_matches['team_home_id'] == team_id) | (dataset_matches['team_guest_id'] == team_id)]
    # extracts all home matches from team_id
    home_match_data_cut = dataset_matches.loc[(dataset_matches['team_home_id'] == team_id)]
    # extracts all guest matches from team_id
    guest_match_data_cut = dataset_matches.loc[(dataset_matches['team_guest_id'] == team_id)]
    # gets the corresponding results table for the home matches
    home_result_data_cut = dataset_results[dataset_results['match_id'].isin(home_match_data_cut['match_id'])]
    # gets the corresponding results table for the guest matches
    guest_result_data_cut = dataset_results[dataset_results['match_id'].isin(guest_match_data_cut['match_id'])]

    # extrahiert alle results deren match_id in match_data_cut['match_id'] auftaucht
    # --------> pd.isin()

    # sum of goals
    for index in home_result_data_cut.index:
        ''' this for loop iterates through the database of home_games and sums up the goals '''
        goals_as_home_team += home_result_data_cut.loc[index, 'points_home']
        goals_total += home_result_data_cut.loc[index, 'points_home']
        game_amount += 1

    for index in guest_result_data_cut.index:
        ''' this for loop iterates through the database of guest_games and sums up the goals '''
        goals_as_guest_team += guest_result_data_cut.loc[index, 'points_guest']
        goals_total += guest_result_data_cut.loc[index, 'points_guest']
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

    # title
    plt.title('Anzahl an Toren gemittelt pro Spiel von \n' + team_name + ' aus der '
              + str(league[0]) + '. Bundesliga im Jahr ' + str(seasons[0]))

    # save figure
    # TODO: if you want to save the file, uncomment here
    # plt.savefig(
    #     'C:/Users/User/Universität/plot_mean_of_goals_one_team_' + team_name + '_' + str(
    #         league[0]) + '_' + str(seasons[0]) + '.png')

    # show
    plt.show()

    # comment
    print()
    print('plot_mean_of_goals_one_team(' + str(team_id) + ' , ' + str(league) + ' , ' + str(seasons) + ')')
    print()
    print('Dieses Schaubild zeigt, wie viele Tore ' + team_name + ' gemittelt pro Spiel geschossen hat. \n'
                                                                  'Ist unterteilt in als Heimmannschaft, als Gastmannschaft und Insgesamt.')
    print('Als Heimmannschaft geschossen pro Spiel: ' + str(round(goals_home, 2)))
    print('Als Gastmannschaft geschossen pro Spiel: ' + str(round(goals_guest, 2)))
    print('Total geschossen pro Spiel: ' + str(round(goals_total, 2)))
    print('________')


#### plot goal distribution for one team only ####
def plot_goal_distribution_one_team(team_id, league, seasons):
    ''' input: team-id, league, season
        output: plot of the histogram for goals'''
    # creating an array which contains the number of games with goals_per_game = index
    goal_amounts = numpy.zeros(13)

    # get data from crawler
    dataset_matches, dataset_results, dataset_goals = cr.get_data_for_algo(league, seasons, 0, 0, 0, 0)
    id_to_team, team_to_id = cr.get_team_dicts(league, seasons)

    # cut only end results
    dataset_results = dataset_results[dataset_results['result_type_id'] == 1]

    # team name
    team_name = id_to_team[team_id]

    # extracts all home matches from team_id
    home_match_data_cut = dataset_matches.loc[(dataset_matches['team_home_id'] == team_id)]
    # extracts all guest matches from team_id
    guest_match_data_cut = dataset_matches.loc[(dataset_matches['team_guest_id'] == team_id)]
    # gets the corresponding results table for the home matches
    home_result_data_cut = dataset_results[dataset_results['match_id'].isin(home_match_data_cut['match_id'])]
    # gets the corresponding results table for the guest matches
    guest_result_data_cut = dataset_results[dataset_results['match_id'].isin(guest_match_data_cut['match_id'])]

    for index in home_result_data_cut.index:
        goals_per_game = home_result_data_cut.loc[index, 'points_home']
        goal_amounts[goals_per_game] += 1

    for index in guest_result_data_cut.index:
        goals_per_game = guest_result_data_cut.loc[index, 'points_guest']
        goal_amounts[goals_per_game] += 1

    # creating array to display amount of goals on x-axis
    result_types = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    # create bars
    plt.bar(result_types, goal_amounts)

    # names
    plt.xticks(result_types, result_types)

    # title
    plt.title('Verteilung der Tore pro Spiel von \n' + team_name + ' aus der '
              + str(league[0]) + '. Bundesliga im Jahr ' + str(seasons[0]))

    # save figure
    # TODO: if you want to save the file, uncomment here
    # plt.savefig('C:/Users/User/Universität/plot_goal_distribution_one_team_' + team_name + '_' + str(
    #      league[0]) + '_' + str(seasons[0]) + '.png')

    # show
    plt.show()

    # comment
    print()
    print('plot_goal_distribution_one_team(' + str(team_id) + ' , ' + str(league) + ' , ' + str(seasons) + ')')
    print()
    print(
        'Dieses Schaubild zeigt eine Verteilung an darüber, wie viele Tore ' + team_name + ' in einem Spiel gemacht hat.')
    # print('Als Heimmannschaft geschossen pro Spiel: ' + str(round(goals_home, 2)))
    # print('Als Gastmannschaft geschossen pro Spiel: ' + str(round(goals_guest, 2)))
    # print('Total geschossen pro Spiel: ' + str(round(goals_total, 2)))
    print('________')


#### FUNCTIONS FOR MORE TEAMS AND MORE SEASONS####
def statistic_for_more_teams_and_more_seasons(function, teams, league, seasons):
    """ input: function(game_result_distribution_one_team, plot_game_result_distribution_one_team,
                        plot_mean_of_goals_one_team, plot_goal_distribution_one_team)
               teams (either 'all' or array), league (array), seasons (array)
        output: prints of given teams with goal_distribution"""
    id_to_team, team_to_id = cr.get_team_dicts(league, seasons)

    if teams == 'all':
        teams = id_to_team

    for key in teams:
        for key2 in seasons:
            function(key, league, key2)


# call the statistics not specific for teams for more seasons
def statistic_for_more_seasons(function, league, seasons):
    """ input: function (plot_game_result_distribution, plot_mean_of_goals, plot_goal_distribution)
               league (array), seasons (array)
        output: prints of given teams with goal_distribution"""

    for key in seasons:
        function(league, key)


# TODO: function calls

plot_game_result_distribution([1], [2020])
plot_mean_of_goals([1], [2020])
plot_goal_distribution([1], [2020])

# statistic_for_more_seasons(plot_game_result_distribution, [1], [2020, 2019])

# statistic_for_more_teams(plot_game_result_distribution_one_team, [16, 40], [1], [2020])
# statistic_for_more_teams(plot_mean_of_goals_one_team, [16, 40], [1], [2020])
# statistic_for_more_teams(plot_goal_distribution_one_team, [16, 40], [1], [2020])

# plot_game_result_distribution_one_team(16, [1], [2020])
# plot_mean_of_goals_one_team(16, [1], [2020])
# plot_goal_distribution_one_team(16, [1], [2020])
# goal_distribution_all_teams([87, 16], [1], [2020])


#### plot goal distribution for all teams ####
def plot_goal_distribution_all_teams(teams, league, seasons):
    id_to_team, team_to_id = cr.get_team_dicts(league[0], seasons[0])
    new_teams = dict()

    if teams == 'all':
        teams = id_to_team

    for key in teams:
        plot_game_result_distribution_one_team(key, league, seasons)


def goal_distribution_all_teams(teams, league, seasons):
    """ input: teams (either 'all' or array), league (array), seasons (array)
        output: prints of given teams with goal_distribution"""
    id_to_team, team_to_id = cr.get_team_dicts(league[0], seasons[0])
    new_teams = dict()

    if teams == 'all':
        teams = id_to_team

    for key in teams:
        game_result_distribution_one_team(key, league, seasons)


'''def plot_goal_distribution_all_teams(league, seasons):
    id_to_team, team_to_id = cr.get_team_dicts(league[0], seasons[0])

    list_statistics = []
    list_team_key = []
    dictionary_teams_and_wins = id_to_team

    for key in id_to_team:
        home_wins_percent, guest_wins_percent, ties_percent, loses_percent =\
            game_result_distribution_one_team(key, league, seasons)
        dictionary_teams_and_wins[key].append(home_wins_percent)

        # list_statistics.append(home_wins_percent)
        # list_team_key.append(key)

    dictionary_teams_and_wins_reversed = dict((reversed(item) for item in dictionary_teams_and_wins.items()))

    maximum_home_win_chance = max(dictionary_teams_and_wins.items(), key=operator.itemgetter(1))[0]

    print()
    print('FAZIT:')
    print('Das ist die maximale Gewinnwahrscheinlichkeit: ' + maximum_home_win_chance)
    # print('Das ist die maximale Gewinnwahrscheinlichkeit: ' + str(max(list_statistics)))
    print('Es gehört zu dem Team: ' + str(dictionary_teams_and_wins_reversed[maximum_home_win_chance]))'''
