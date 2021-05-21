"""
This module contains code for a prediction models.
"""

from collections import Counter
import pandas as pd

class sumMostGoalsIsWinner:
    def __init__(self, results):
        self.end_results = results[results['ResultTypeID'] == 2]
        self.team1_id = results.loc[0,'Team1.TeamId']
        self.team2_id = results.loc[0, 'Team2.TeamId']
        self.team1_is_team1_id_results = self.end_results[self.end_results['Team1.TeamId'] == self.team1_id]
        self.team1_is_team2_id_results = self.end_results[self.end_results['Team1.TeamId'] == self.team2_id]

        self.goals_team1_id = self.team1_is_team1_id_results['PointsTeam1'].sum(axis=0) + self.team1_is_team2_id_results['PointsTeam2'].sum(axis=0)
        self.goals_team2_id = self.team1_is_team1_id_results['PointsTeam2'].sum(axis=0) + self.team1_is_team2_id_results['PointsTeam1'].sum(axis=0)

    def predict_winner(self):
        if self.goals_team1_id > self.goals_team2_id:
            return self.team1_id
        if self.goals_team1_id < self.goals_team2_id:
            return self.team2_id
        return -1


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

    def predict_winner(self, home_team, guest_team):
        """Cast prediction based on the "learned" parameters."""
        if self.num_games[home_team] >= self.num_games[guest_team]:
            return home_team
        else:
            return guest_team

# for testing inside the script
if __name__ == '__main__':
    from crawler import getMatchupHistoryFromAPI

    matches, match_results, match_goals = getMatchupHistoryFromAPI(16,87)
    algo = sumMostGoalsIsWinner(match_results)
    print(algo.predict_winner())

