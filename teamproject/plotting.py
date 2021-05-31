# plotting certain statistics

# importing the required module
import matplotlib.pyplot as plt
import crawler

#### game result ####
def plot_game_result_distribution(league, seasons):
    """ input: league
        output: how may times the game ended in home_win, tie, guest_win"""

    # initialize variables
    home_wins = 0
    ties = 0
    guest_wins = 0
    league_name =''

    # get data from crawler
    matches, match_results, match_goals = crawler.getAllMatchesOfYearFromAPI(league, seasons)

    # for loop to sum up amount of wins, ties, loses
    for index in match_results.index:
        if match_results.loc[index, 'PointsTeam1'] > match_results.loc[index, 'PointsTeam2']:
            home_wins += 1
        elif match_results.loc[index, 'PointsTeam1'] == match_results.loc[index, 'PointsTeam2']:
            ties += 1
        elif match_results.loc[index, 'PointsTeam1'] < match_results.loc[index, 'PointsTeam2']:
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
    plt.title('Verteilung der Spielausgänge in der ' + league_name + ' im Jahr ' + str(seasons))

    # show
    plt.show()


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
    matches, match_results, match_goals = crawler.getAllMatchesOfYearFromAPI(league, seasons)

    # sum of goals
    for index in match_results.index:
        ''' this for loop iterates through the database and sums up the goals '''
        goals_home += match_results.loc[index, 'PointsTeam1']
        goals_guest += match_results.loc[index, 'PointsTeam2']
        goals_total += match_results.loc[index, 'PointsTeam1'] + match_results.loc[index, 'PointsTeam2']
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
    plt.title('Anzahl der Tore pro Spiel in der ' + league_name + ' im Jahr ' + str(seasons))
    # title
    #plt.title('Tor-Verteilung für Heim und Auswärtsteam und Total')

    # show
    plt.show()


#### goal distribution ####
def plot_goal_distribution(league, seasons):
    # initialize
    goals_per_game = 0
    # creating an array which contains the number of games with goals_per_game = index
    goal_amounts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # get data from crawler
    matches, match_results, match_goals = crawler.getAllMatchesOfYearFromAPI(league, seasons)

    for index in match_results.index:
        goals_per_game = match_results.loc[index, 'PointsTeam1'] + match_results.loc[index, 'PointsTeam2']
        # database[goals_home] + database[goals_guest]
        goal_amounts[goals_per_game] += 1

    # creating array to display amount of goals on x-axis
    result_types = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    # create bars
    plt.bar(result_types, goal_amounts)

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
    plt.title('Verteilung der Tore pro Spiel in der ' + league_name + ' im Jahr ' + str(seasons))

    # title
    #plt.title('Verteilung der Tore pro Spiel')

    # show
    plt.show()


#### function calls ####
plot_game_result_distribution(1, 2020)
plot_mean_of_goals(1, 2020)
plot_goal_distribution(1, 2020)
