"""
This module contains code for a prediction models.
"""
# %%
from abc import ABCMeta, abstractmethod
import crawler
from collections import Counter
import pandas as pd
import numpy as np
from scipy.stats import poisson,skellam
import statsmodels.api as sm
import statsmodels.formula.api as smf

# TODO: Hier fängt abstract an
class Models:
    __metaclass__ = ABCMeta

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
    def get_model_requirements(self):
        parameter = {'leagues': 1,
                     'seasons': 1,
                     'matchdays': 0,
                     'points': 0}

        return parameter

    def set_data(self, team1, team2):
        # TODO: umschreiben für Core
        self.team1 = team1
        self.team2 = team2
        #self.matches, self.match_results, self.match_goals = getMatchupHistoryFromAPI(team1, team2)
        self.end_results = self.match_results[self.match_results['ResultTypeID'] == 2]
        #print(self.end_results)

    def start_training(self):
        return None

    def predict(self, team1, team2):
        team1_wins = 0
        team2_wins = 0
        draws = 0

        for key in self.end_results.index:
            team = self.end_results.loc[key, "Team1.TeamId"]
            result = self.end_results.loc[key, "PointsTeam1"] - self.end_results.loc[key, "PointsTeam2"]

            if team == self.team1:
                if result > 0:
                    team1_wins += 1
                elif result < 0:
                    team2_wins += 1
                else:
                    draws += 1
            else:
                if result < 0:
                    team1_wins += 1
                elif result > 0:
                    team2_wins += 1
                else:
                    draws += 1

        total_matches = team1_wins + team2_wins + draws
        return [self.team1, self.team2, (team1_wins / total_matches)*100, (draws / total_matches)*100, (team2_wins / total_matches)*100]

class PoissonModel(Models):
    parameter_dict = {  'leagues': 1,
                        'seasons': 1,
                        'matchdays': 1,
                        'points': 0
                      }
    matches_index = 0
    results_index = 1
    max_goals = 10
    MATCH_CONTENT = ['match_id','team_home_id','team_guest_id']
    RESULT_CONTENT = ['match_id','points_home','points_guest']
    TEAM_ID_COLUMNS = ['team_home_id','team_guest_id']
    HOME_TEAM_WITH_GOALS = ['team_home_id','team_guest_id','points_home']
    GUEST_TEAM_WITH_GOALS = ['team_guest_id','team_home_id','points_guest']
    
    END_RESULT = 1

    def get_model_requirements(self):
        return self.parameter_dict

    def set_data(self, data):
        matches = data[self.matches_index]
        results = data[self.results_index]
        ids_in_match = matches[self.MATCH_CONTENT]
        end_results = results[results['result_type_id'] == self.END_RESULT]
        data = ids_in_match.merge(end_results,on='match_id')
        data[self.TEAM_ID_COLUMNS] = data[self.TEAM_ID_COLUMNS].astype(str)

        goal_model_data = pd.concat([data[self.HOME_TEAM_WITH_GOALS].assign(home=1).rename(
            columns={'team_home_id':'team', 'team_guest_id':'opponent','points_home':'goals'}),
           data[self.GUEST_TEAM_WITH_GOALS].assign(home=0).rename(
            columns={'team_guest_id':'team', 'team_home_id':'opponent','points_guest':'goals'})])
        goal_model_data = goal_model_data[['team', 'opponent', 'goals', 'home']]
        goal_model_data['team'] = goal_model_data['team'].astype(str)
        goal_model_data['opponent'] = goal_model_data['opponent'].astype(str)
        self.data = goal_model_data

    def start_training(self):
        self.model = smf.glm(formula="goals ~ home + team + opponent", data=self.data, 
                                        family=sm.families.Poisson()).fit()

    def simulate_match(self, homeTeam, guestTeam):
        """
        :param smf.glm model: trained model
        :param string homeTeam: id of home team
        :param string awayTeam: id of guest team
        :param int max_goals: maximum amount of total goals in predicting match
        :return: float[][] prediction where columns=awayTeam, row=homeTeam with probability of each team scoring |index| scores
        """
        home_goals_avg = self.model.predict(pd.DataFrame(data={'team': str(homeTeam), 
                                                                'opponent': str(guestTeam),'home':1},
                                                        index=[1])).values[0]
        guest_goals_avg = self.model.predict(pd.DataFrame(data={'team': str(guestTeam), 
                                                                'opponent': str(homeTeam),'home':0},
                                                        index=[1])).values[0]
        team_pred = [[poisson.pmf(i, team_avg) for i in range(0, self.max_goals+1)] for team_avg in [home_goals_avg, guest_goals_avg]]
        self.simulation = np.outer(np.array(team_pred[0]), np.array(team_pred[1]))
        return 1
    
    def predict_outcome(self):
        home_win = np.sum(np.tril(self.simulation, -1))
        draw = np.sum(np.diag(self.simulation))
        guest_win = np.sum(np.triu(self.simulation, 1))
        # TODO: return as dict
        return [home_win, draw, guest_win]
    def predict_score(self):
        index = np.argmax(self.simulation)
        home_points, guest_points = divmod(index, self.max_goals+1)
        # TODO: return as dict
        return [home_points, guest_points]
    def predict(self, home_id, guest_id):
        # TODO: call sim.match, pred.outcome, pred.score. concatenate and return results in dict 
        return {}


class ExperienceAlwaysWins():

    """
    An example model that predicts the winner predicts the winner
    solely based on number of games played.
    """

    def __init__(self, matches):
        # We just count the number of games played by all teams and ignore
        # the winner:
        self.num_games = (
            Counter(matches.home_team) +
            Counter(matches.guest_team))

    def predict_outcome(self, home_team, guest_team):
        """Cast prediction based on the "learned" parameters."""
        if self.num_games[home_team] >= self.num_games[guest_team]:
            return home_team
        else:
            return guest_team

# %%
# for testing inside the script
if __name__ == '__main__':

    None
    #matches, match_results, match_goals = getMatchupHistoryFromAPI(16,87)
    #algo = SumMostGoalsIsWinner(match_results)
    #print(algo.predict_winner())

    #algo_trivial = Model_Handler(6, 16, 0, 0, 1)
    #print(algo_trivial)

    # POISSON TESTING
    # crwlr = crawler.Crawler()
    # data = crwlr.get_data_for_algo([1],[2020], 1, 34, 0, 0)
    # algo = PoissonModel()
    # algo.set_data(data)
    # algo.start_training()
    # max_goals=4
    # algo.simulate_match(16,1635)
    # #print(algo.predict_outcome())
    # sim = algo.simulation
    # print(sim)
    # index = np.argmax(sim)
    # print(index)
    # home_goals, guest_goals = divmod(index, max_goals+1)
    # print(home_goals, guest_goals)
