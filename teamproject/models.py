"""
This module contains code for a prediction models.
"""
# %%
from abc import ABCMeta, abstractmethod

from numpy.core.numeric import outer
import crawler
from collections import Counter
import pandas as pd
import numpy as np
from scipy.stats import poisson, skellam
import statsmodels.api as sm
import statsmodels.formula.api as smf


# TODO: Hier fängt abstract an
class Models:
    __metaclass__ = ABCMeta

    MATCHES_INDEX = 0
    RESULTS_INDEX = 1
    MAX_GOALS = 10
    MATCH_CONTENT = ['match_id', 'team_home_id', 'team_guest_id']
    RESULT_CONTENT = ['match_id', 'points_home', 'points_guest']
    TEAM_ID_COLUMNS = ['team_home_id', 'team_guest_id']
    HOME_TEAM_WITH_GOALS = ['team_home_id', 'team_guest_id', 'points_home']
    GUEST_TEAM_WITH_GOALS = ['team_guest_id', 'team_home_id', 'points_guest']

    # TODO: Was dat?
    END_RESULT = 1

    # non-abstract methods
    def get_models(self):
        # TODO: if model added, edit models object
        models = {
            1: {'model_id': 1,
                'model': 'trivialer Algorithmus',
                'description': 'Einfacher Algorithmus, der Ergebnisse aller bisherigen Partieen zweier Teams vergleicht.',
                'run': MostWins()
                },
            2: {'model_id': 2,
                'model': 'Poisson Model',
                'description': 'Berechnet mithilfe der Poissonverteilung den Ausgang eines Matches zwischen 2 Teams',
                'run': PoissonModel()
                }
        };
        return models

    def prepare_data(self, data):
        """
        Extracts endresults of all matches and the team_ids playing.
        :param pd.DF data: DataPacket in Uniformat 
        :returns: pd.DF data: DB containing team_ids and scores in a match
        """
        matches = data[self.MATCHES_INDEX]
        results = data[self.RESULTS_INDEX]
        ids_in_match = matches[self.MATCH_CONTENT]
        end_results = results[results['result_type_id'] == self.END_RESULT]
        data = ids_in_match.merge(end_results, on='match_id')
        data[self.TEAM_ID_COLUMNS] = data[self.TEAM_ID_COLUMNS].astype(str)
        return data

    # abstract methods
    @abstractmethod
    def get_model_requirements(self):
        pass

    @abstractmethod
    def set_data(self):
        pass

    @abstractmethod
    def start_training(self):
        pass

    @abstractmethod
    def predict(self):
        pass


# TODO: hier hört abstract auf


class MostWins(Models):
    parameter = {'leagues': 1,
                 'seasons': 1,
                 'matchdays': 0,
                 'points': 0}

    def __init__(self):
        """
        Classconstructor, initializes 1 internal empty variable
        """
        self.data = ''

    def get_model_requirements(self):
        """
        Returns a dict with bools indicating what can be tuned for this Algorithm.
        :returns: dict parameter_dict
        """
        return self.parameter

    def set_data(self, data):
        """
        Takes match and result data in Uniformat and prepares it for the Algo.
        Saves the Data in self.data.

        :param pd.DF: DB containing matches and the results in Uniformat
        """
        self.data = self.prepare_data(data)

    def start_training(self):
        """No training necessary for this algorithm.
        SKIP"""
        return None

    def predict(self, team1, team2):
        """
        Extracts the matchup data from given teams,
        calculates the probability of 3 outcomes, returns dict in Uniformat.

        :param string team1_id: id of first team
        :param string team2_id: id of second team
        :returns: dict outcome: in Uniformat
        """
        team1 = str(team1)
        team2 = str(team2)

        outcome = {team1: 0, 'draw': 0, team2: 0}
        # extract the matchup history from the given teams
        data_2_teams = self.data[(self.data['team_home_id'] == team1) & (self.data['team_guest_id'] == team2)
                                 | (self.data['team_home_id'] == team2) & (self.data['team_guest_id'] == team1)]
        # subtract the goals and create new column
        data_2_teams['result'] = data_2_teams['points_home'] - data_2_teams['points_guest']

        total_matches = data_2_teams.shape[0]
        # look wich team scored more and sum the wins/draws
        for index in data_2_teams.index:
            result = data_2_teams.loc[index, 'result']
            home_team = data_2_teams.loc[index, 'team_home_id']
            guest_team = data_2_teams.loc[index, 'team_guest_id']
            if result == 0:
                outcome['draw'] = outcome['draw'] + 1
            elif result > 0:
                outcome[home_team] = outcome[home_team] + 1
            elif result < 0:
                outcome[guest_team] = outcome[guest_team] + 1
        return {'outcome': {'home_win': round((outcome[team1] / total_matches * 100), 2),
                            'draw': round((outcome['draw'] / total_matches * 100), 2),
                            'guest_win': round((outcome[team2] / total_matches * 100), 2)
                            },
                'score': -1
                }


class PoissonModel(Models):
    parameter_dict = {'leagues': 1,
                      'seasons': 1,
                      'matchdays': 1,
                      'points': 0
                      }

    def __init__(self):
        """
        Classconstructor, initializes 3 internal empty dicts.
        """
        #self.data
        #self.model
        #self.simulation

    def get_model_requirements(self):
        """
        Returns a dict with bools indicating what can be tuned for this Algorithm.
        :returns: dict parameter_dict
        """
        return self.parameter_dict

    def set_data(self, data):
        """
        Takes match and result data in Uniformat and prepares it for the Algo.
        Saves the Data in self.data.

        :param pd.DF: DB containing matches and the results in Uniformat
        """
        data = self.prepare_data(data)
        # rename columns for algo
        goal_model_data = pd.concat([data[self.HOME_TEAM_WITH_GOALS].assign(home=1).rename(
            columns={'team_home_id': 'team', 'team_guest_id': 'opponent', 'points_home': 'goals'}),
            data[self.GUEST_TEAM_WITH_GOALS].assign(home=0).rename(
                columns={'team_guest_id': 'team', 'team_home_id': 'opponent', 'points_guest': 'goals'})])
        goal_model_data = goal_model_data[['team', 'opponent', 'goals', 'home']]
        # cast the team_ids to strings because of algo
        goal_model_data['team'] = goal_model_data['team'].astype(str)
        goal_model_data['opponent'] = goal_model_data['opponent'].astype(str)
        self.data = goal_model_data

    def start_training(self):
        """
        Creates a model and corrects the algorithms parameters using the given data.
        """
        self.model = smf.glm(formula="goals ~ home + team + opponent", data=self.data,
                             family=sm.families.Poisson()).fit()

    def simulate_match(self, home_team, guest_team):
        """
        Takes 2 team_ids and simulates a match using the in advance trained model.
        Saves the Simulation in self.simulation,
        a matrix containing the probabilitiess of all outcomes with max Goals set in self.MAX_GOALS.

        :param string home_team: id of home team
        :param string guest_team: id of guest team
        :return: float[][] prediction where columns=awayTeamGoals, row=homeTeamGoals with probability of each team scoring |index| scores
        """
        home_goals_avg = self.model.predict(pd.DataFrame(data={'team': str(home_team),
                                                               'opponent': str(guest_team), 'home': 1},
                                                         index=[1])).values[0]
        guest_goals_avg = self.model.predict(pd.DataFrame(data={'team': str(guest_team),
                                                                'opponent': str(home_team), 'home': 0},
                                                          index=[1])).values[0]
        team_pred = [[poisson.pmf(i, team_avg) for i in range(0, self.MAX_GOALS + 1)] for team_avg in
                     [home_goals_avg, guest_goals_avg]]
        self.simulation = np.outer(np.array(team_pred[0]), np.array(team_pred[1]))

    def predict_outcome(self):
        """
        Extracts the probability of all 3 outcomes using the matchsimulation done in advance.
        win<-draw->win
        :returns: dict: containing outcome:probability       
        """
        home_win = np.sum(np.tril(self.simulation, -1))
        draw = np.sum(np.diag(self.simulation))
        guest_win = np.sum(np.triu(self.simulation, 1))
        return {'home_win': round(home_win,2), 'draw': round(draw,2), 'guest_win': round(guest_win,2)}

    def predict_score(self):
        """
        Extracts the most likely outcome with goals using the simulation done in advance.
        :returns dict: homePoints:x, guestPoints:y, probab:z
        """
        index = np.argmax(self.simulation)
        # argmax gives back the 1 dim. index from maximum in matrix
        # index mod rows = x + (remainer)y
        home_points, guest_points = divmod(index, self.MAX_GOALS + 1)
        return {1 : {'home_points': home_points, 'guest_points': guest_points,
                'probability': round(self.simulation[home_points, guest_points],2)}}

    def predict(self, home_id, guest_id):
        """
        Returns dict of two dicts containing probabilitys of the outcome and endresult.

        :returns: dict: 2 dicts in Uniformat
        """

        self.simulate_match(home_id, guest_id)
        outcome = self.predict_outcome()
        result = self.predict_score()
        dict = {'outcome': outcome, 'score': result}
        return dict


# %%
# for testing inside the script
if __name__ == '__main__':
    # matches, match_results, match_goals = getMatchupHistoryFromAPI(16,87)
    # algo = SumMostGoalsIsWinner(match_results)
    # print(algo.predict_winner())

    # algo_trivial = Model_Handler(6, 16, 0, 0, 1)
    # print(algo_trivial)

    # MOSTWINS TESTING
    crwlr = crawler.Crawler()
    data = crwlr.get_data_for_algo([1,2,3], [2020, 2019], 1, 34, 0, 0)
    model = PoissonModel()
    model.set_data(data)

    model.start_training()
    # print(data.head(5))
    # data_2_teams = data.loc[(data['team_home_id'] == '16')]
    #                                 | (data['team_home_id'] == team2) & (data['team_guest_id'] == team1)]
    # print(data[(data['team_home_id'] == '16') & (data['team_guest_id'] == '112')].head(5))
    # print(data[['points_home', 'points_guest']].subtract(axis=1))
    print(model.predict(16, 1635))

    # POISSON TESTING
    # crwlr = crawler.Crawler()
    # data = crwlr.get_data_for_algo([1], [2020], 1, 34, 0, 0)
    # algo = PoissonModel()
    # algo.set_data(data)
    # algo.start_training()
    # max_goals = 4
    # algo.simulate_match(16, 1635)
    # print(algo.predict(16, 87))

# %%
