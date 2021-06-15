"""
This module contains code for a prediction models.
"""

from abc import ABCMeta, abstractmethod
#from crawler import getMatchupHistoryFromAPI
from collections import Counter
import pandas as pd

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
                'training': 0,
                'run': MostWins()
                },
            2: {'model_id': 2,
                'model': 'dummy Model',
                'description': 'ML Model DUMMY',
                'training': 1,
                'run': MostWins()
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
    def predict_outcome(self):
        pass

# TODO: hier hört abstract auf


#def Model_Handler(team1, team2, seasons, leagues, algo_id):
#    if algo_id == 1:
#        model = MostWins(team1, team2)
#        return model.predict_winner()

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

    def predict_outcome(self):
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


class ExperienceAlwaysWins:

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


# for testing inside the script
if __name__ == '__main__':

    None
    #matches, match_results, match_goals = getMatchupHistoryFromAPI(16,87)
    #algo = SumMostGoalsIsWinner(match_results)
    #print(algo.predict_winner())

    #algo_trivial = Model_Handler(6, 16, 0, 0, 1)
    #print(algo_trivial)
