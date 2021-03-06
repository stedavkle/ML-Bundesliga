"""
This module contains code for prediction models.
"""
# %%
from abc import ABCMeta, abstractmethod, ABC

from numpy.core.numeric import outer
from teamproject import crawler
from collections import Counter
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from scipy.stats import poisson, skellam
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils.validation import check_is_fitted
from scipy.optimize import minimize


# begin of abstract class
class Models:
    __metaclass__ = ABCMeta

    MATCHES_INDEX = 0
    RESULTS_INDEX = 1
    MAX_GOALS = 10
    MATCH_CONTENT = ['match_id', 'team_home_id', 'team_guest_id', 'time_diff']
    RESULT_CONTENT = ['match_id', 'points_home', 'points_guest']
    TEAM_ID_COLUMNS = ['team_home_id', 'team_guest_id']
    HOME_TEAM_WITH_GOALS = ['team_home_id', 'team_guest_id', 'points_home']
    GUEST_TEAM_WITH_GOALS = ['team_guest_id', 'team_home_id', 'points_guest']
    END_RESULT = 1

    # non-abstract methods
    def get_models(self):
        '''
        returns a dictionary with available models
        '''
        # TODO: if model added, edit models object
        models = {
            1: {'model_id': 1,
                'model': 'Most Wins',
                'description': 'Einfacher Algorithmus, der Ergebnisse aller Partieen zweier Teams im ausgewählen Datensatz vergleicht.',
                'run': MostWins()
                },
            2: {'model_id': 2,
                'model': 'Poisson Model',
                'description': 'Berechnet mithilfe der Poissonverteilung den Ausgang eines Matches zwischen 2 Teams',
                'run': PoissonModel()
                },
            3: {'model_id': 3,
                'model': 'Logistic Regression Model',
                'description': 'Berechnet mithilfe logistischer Regression den Ausgang eines Matches zwischen 2 Teams',
                'run': LogisticRegModel()
                },
            4: {'model_id': 4,
                'model': 'Dixon-Coles Model',
                'description': 'Verbesserte Version des Poisson Model. Ergebnisse mit wenig Toren werden besser in die Berechnung miteinbezogen.'
                               '\nÄltere Ergebnisse können optional anders gewichtet werden als neuere (empfohlen).\n'
                               '\nHINWEIS! Das Training dieses Models dauert ungemein länger!',
                'run': DixonColes()
                }
        }
        return models

    def prepare_data(self, data):
        """
        Extracts endresults of all matches and the team_ids playing.
        :param pd.DF data: DataPacket in Uniformat 
        :returns: pd.DF data: DB containing team_ids and scores in a match
        """
        matches = data[self.MATCHES_INDEX]
        results = data[self.RESULTS_INDEX]
        matches['match_date_time_utc'] = pd.to_datetime(matches['match_date_time_utc'], format='%Y-%m-%dT%H:%M:%SZ')
        matches['time_diff'] = ""
        matches['time_diff'] = (max(matches['match_date_time_utc']) - matches['match_date_time_utc']).dt.days

        ids_in_match = matches[self.MATCH_CONTENT]
        end_results = results[results['result_type_id'] == self.END_RESULT]
        data = ids_in_match.merge(end_results, on='match_id')
        data[self.TEAM_ID_COLUMNS] = data[self.TEAM_ID_COLUMNS].astype(str)

        return data

    def evaluate(self, eval_data, filename):
        """
        compares prediction of each match listed in eval_data with real result and stores it in csv
        eval_data will be transformed to a dataset, containing important values for comparison
        :eval_data pd.Dataframe of matches and results
        :filename string with name of file
        :return pd.Dataframe of test dataset, pd.Dataframe of predicted results
        """
        test_matches = eval_data[0]
        test_results = eval_data[1]
        endresults = test_results[test_results['result_type_id'] == 1]

        test_data = pd.merge(test_matches, endresults, on='match_id')[
            ['match_id', 'matchday', 'team_home_id', 'team_guest_id', 'points_home', 'points_guest']]
        test_data['outcome'] = 0

        evaluation_data = pd.DataFrame(columns=['match_id', 'home_win', 'draw', 'guest_win', 'outcome'])

        for index, match in test_data.iterrows():
            team_home_id = match.team_home_id
            team_guest_id = match.team_guest_id
            if match['points_home'] > match['points_guest']:
                match['outcome'] = 1
            elif match['points_home'] < match['points_guest']:
                match['outcome'] = -1

            prediction = self.predict(team_home_id, team_guest_id)
            #
            outcome = prediction['outcome']
            if outcome == -1:
                continue
            evaluation_data = evaluation_data.append({'match_id': match['match_id'].item(),
                                                      'home_win': outcome['home_win'],
                                                      'draw': outcome['draw'],
                                                      'guest_win': outcome['guest_win'],
                                                      'outcome': (np.argmax(list(outcome.values())) - 1) * (-1)},
                                                     ignore_index=True)

        evaluation_data['match_id'] = evaluation_data['match_id'].astype('int64')
        evaluation_data['outcome'] = evaluation_data['outcome'].astype('int64')

        test_data_path = 'teamproject/data/evaluation/{}_test_data.csv'.format(filename)
        eval_data_path = 'teamproject/data/evaluation/{}_eval_data.csv'.format(filename)
        test_data.to_csv(test_data_path, index=False)
        evaluation_data.to_csv(eval_data_path, index=False)

        return test_data, evaluation_data


    def check_ids_in_data(self, team1_id, team2_id, data):
        """
        checks if training dataset contains team ids, otherwise prediction is not possible
        :team1_id int id of team 1
        :team2_id int id of team 2
        :data pd.Dataframe training dataset
        :return bool
        """
        team_columns = data[['team_home_id', 'team_guest_id']]
        team1_id = str(team1_id)
        team2_id = str(team2_id)

        team1_in_data = False
        team2_in_data = False

        if (team_columns["team_home_id"] == team1_id).any() or (team_columns["team_guest_id"] == team1_id).any():
            team1_in_data = True
        if (team_columns["team_home_id"] == team2_id).any() or (team_columns["team_guest_id"] == team2_id).any():
            team2_in_data = True
        return team1_in_data and team2_in_data

    def set_max_goals(self, max_goals):
        self.MAX_GOALS = max_goals

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

# end of abstract class

# -------------- implement new models here --------------

class MostWins(Models):
    parameter_dict = {'leagues': 1,
                      'seasons': 1,
                      'matchdays': 0,
                      'time': 0}

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
        return self.parameter_dict

    def set_data(self, data):
        """
        Takes match and result data in Uniformat and prepares it for the Algo.
        Saves the Data in self.data.

        :param pd.DF: DB containing matches and the results in Uniformat
        """

        self.data = self.prepare_data(data)

    def start_training(self, x=False):
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

        if not self.check_ids_in_data(team1, team2, self.data):
            outcome = -1
        else:
            outcome = {team1: 0, 'draw': 0, team2: 0}
            # extract the matchup history from the given teams
            data_2_teams = self.data[(self.data['team_home_id'] == team1) & (self.data['team_guest_id'] == team2)
                                     | (self.data['team_home_id'] == team2) & (self.data['team_guest_id'] == team1)]
            # subtract the goals and create new column
            data_2_teams['result'] = data_2_teams['points_home'] - data_2_teams['points_guest']

            total_matches = data_2_teams.shape[0]

            if total_matches == 0:
                outcome = -1
            else:
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

                outcome = {
                            'home_win': round((outcome[team1] / total_matches), 2),
                            'draw': round((outcome['draw'] / total_matches), 2),
                            'guest_win': round((outcome[team2] / total_matches), 2)
                        }

        return {
            'outcome': outcome,
            'score': -1
        }



class PoissonModel(Models):
    parameter_dict = {'leagues': 1,
                      'seasons': 1,
                      'matchdays': 1,
                      'time': 0
                      }

    def __init__(self):
        """
        Classconstructor, initializes 3 internal empty dicts.
        """
        self.data = ''
        self.simulation = ''
        self.model = ''

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

    def start_training(self, x=False):
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
        return {'home_win': round(home_win, 2), 'draw': round(draw, 2), 'guest_win': round(guest_win, 2)}

    def predict_score(self):
        """
        Extracts the most likely outcome with goals using the simulation done in advance.
        :returns dict: homePoints:x, guestPoints:y, probab:z
        """
        index = np.argmax(self.simulation)
        # argmax gives back the 1 dim. index from maximum in matrix
        # index mod rows = x + (remainer)y
        home_points, guest_points = divmod(index, self.MAX_GOALS + 1)
        return {1: {'home_points': int(home_points), 'guest_points': int(guest_points),
                    'probability': round(self.simulation[home_points, guest_points], 2)}}

    def predict(self, home_id, guest_id):
        """
        Returns dict of two dicts containing probabilitys of the outcome and endresult.

        :returns: dict: 2 dicts in Uniformat
        """

        if not (((self.data["team"] == str(home_id)).any() or (self.data["opponent"] == str(home_id)).any()) and
            ((self.data["team"] == str(guest_id)).any() or (self.data["opponent"] == str(guest_id)).any())):
            outcome = -1
            result = -1
        else:
            self.simulate_match(home_id, guest_id)
            outcome = self.predict_outcome()
            result = self.predict_score()
        return {'outcome': outcome, 'score': result}


class DixonColes(Models):
    XI = 0.0018

    parameter_dict = {'leagues': 1,
                      'seasons': 1,
                      'matchdays': 1,
                      'time': 1}

    def __init__(self):
        self.model = ''
        self.data = ''
        self.simulation = ''
        self.params = ''

    def get_model_requirements(self):
        """
        Returns a dict with bools indicating what can be tuned for this Algorithm.
        :returns: dict parameter_dict
        """
        return self.parameter_dict

    def set_data(self, data):
        self.data = self.prepare_data(data)

    def start_training(self, xi=False):
        """
        starts dixon-coles training with decay or without
        :xi bool if True is set, dixon coles traines with decay, otherwise not
        """
        if xi:
            self.params = self.solve_parameters_decay(self.data, self.XI)
        else:
            self.params = self.solve_parameters(self.data)

    def set_pretrained_data(self, data):
        """
        upload dataset with pretrained values
        :data dict pretrained values
        """
        self.params = data

    def predict(self, home_id, guest_id):
        """
        predicts possible outcome of a match by given team ids
        :home_id int
        :guest_id int
        :return dict with result of prediction
        """
        if not self.check_ids_in_data(home_id, guest_id, self.data):
            result = -1
        else:
            prediction = self.dixon_coles_simulate_match(self.params, str(home_id), str(guest_id), max_goals=self.MAX_GOALS)
            home_win = np.sum(np.tril(prediction, -1))
            draw = np.sum(np.diag(prediction))
            guest_win = np.sum(np.triu(prediction, 1))
            result = {'home_win': round(home_win, 2), 'draw': round(draw, 2), 'guest_win': round(guest_win, 2)}
        return {'outcome': result, 'score': -1}

    # specific funcions
    def rho_correction(self, x, y, lambda_x, mu_y, rho):
        if x == 0 and y == 0:
            return 1 - (lambda_x * mu_y * rho)
        elif x == 0 and y == 1:
            return 1 + (lambda_x * rho)
        elif x == 1 and y == 0:
            return 1 + (mu_y * rho)
        elif x == 1 and y == 1:
            return 1 - rho
        else:
            return 1.0

    def solve_parameters(self, dataset, debug=False, init_vals=None, options={'disp': True, 'maxiter': 100},
                         constraints=[{'type': 'eq', 'fun': lambda x: sum(x[:20]) - 20}], **kwargs):
        """
        calculates parameters for each team due training
        return - parameter dictionary
        """
        teams = np.sort(dataset['team_home_id'].unique())
        # check for no weirdness in dataset
        away_teams = np.sort(dataset['team_guest_id'].unique())
        if not np.array_equal(teams, away_teams):
            raise ValueError("Something's not right")
        n_teams = len(teams)
        if init_vals is None:
            # random initialisation of model parameters
            init_vals = np.concatenate((np.random.uniform(0, 1, (n_teams)),  # attack strength
                                        np.random.uniform(0, -1, (n_teams)),  # defence strength
                                        np.array([0, 1.0])  # rho (score correction), gamma (home advantage)
                                        ))

        def dc_log_like(x, y, alpha_x, beta_x, alpha_y, beta_y, rho, gamma):
            lambda_x, mu_y = np.exp(alpha_x + beta_y + gamma), np.exp(alpha_y + beta_x)
            return (np.log(self.rho_correction(x, y, lambda_x, mu_y, rho)) +
                    np.log(poisson.pmf(x, lambda_x)) + np.log(poisson.pmf(y, mu_y)))

        def estimate_paramters(params):
            score_coefs = dict(zip(teams, params[:n_teams]))
            defend_coefs = dict(zip(teams, params[n_teams:(2 * n_teams)]))
            rho, gamma = params[-2:]
            log_like = [dc_log_like(row.points_home, row.points_guest, score_coefs[row.team_home_id],
                                    defend_coefs[row.team_home_id],
                                    score_coefs[row.team_guest_id], defend_coefs[row.team_guest_id], rho, gamma) for row
                        in dataset.itertuples()]
            return -sum(log_like)

        opt_output = minimize(estimate_paramters, init_vals, options=options, constraints=constraints, **kwargs)
        if debug:
            # sort of hacky way to investigate the output of the optimisation process
            return opt_output
        else:
            return dict(zip(["attack_" + team for team in teams] +
                            ["defence_" + team for team in teams] +
                            ['rho', 'home_adv'],
                            opt_output.x))

    def solve_parameters_decay(self, dataset, xi=0.001, debug=False, init_vals=None,
                               options={'disp': True, 'maxiter': 100},
                               constraints=[{'type': 'eq', 'fun': lambda x: sum(x[:20]) - 20}], **kwargs):
        """
        calculates parameters for each team due training, including decay
        return - parameter dictionary
        """
        teams = np.sort(dataset['team_home_id'].unique())
        # check for no weirdness in dataset
        away_teams = np.sort(dataset['team_guest_id'].unique())
        if not np.array_equal(teams, away_teams):
            raise ValueError("something not right")
        n_teams = len(teams)
        if init_vals is None:
            # random initialisation of model parameters
            init_vals = np.concatenate((np.random.uniform(0, 1, (n_teams)),  # attack strength
                                        np.random.uniform(0, -1, (n_teams)),  # defence strength
                                        np.array([0, 1.0])  # rho (score correction), gamma (home advantage)
                                        ))

        def dc_log_like_decay(x, y, alpha_x, beta_x, alpha_y, beta_y, rho, gamma, t, xi=xi):
            lambda_x, mu_y = np.exp(alpha_x + beta_y + gamma), np.exp(alpha_y + beta_x)
            return np.exp(-xi * t) * (np.log(self.rho_correction(x, y, lambda_x, mu_y, rho)) +
                                      np.log(poisson.pmf(x, lambda_x)) + np.log(poisson.pmf(y, mu_y)))

        def estimate_paramters_decay(params):
            score_coefs = dict(zip(teams, params[:n_teams]))
            defend_coefs = dict(zip(teams, params[n_teams:(2 * n_teams)]))
            rho, gamma = params[-2:]
            log_like = [dc_log_like_decay(row.points_home, row.points_guest, score_coefs[row.team_home_id],
                                          defend_coefs[row.team_home_id],
                                          score_coefs[row.team_guest_id], defend_coefs[row.team_guest_id],
                                          rho, gamma, row.time_diff, xi=xi) for row in dataset.itertuples()]
            return -sum(log_like)

        opt_output = minimize(estimate_paramters_decay, init_vals, options=options, constraints=constraints)
        if debug:
            # sort of hacky way to investigate the output of the optimisation process
            return opt_output
        else:
            return dict(zip(["attack_" + team for team in teams] +
                            ["defence_" + team for team in teams] +
                            ['rho', 'home_adv'],
                            opt_output.x))

    def calc_means(self, param_dict, home_team, away_team):
        return [
            np.exp(param_dict['attack_' + home_team] + param_dict['defence_' + away_team] + param_dict['home_adv']),
            np.exp(param_dict['defence_' + home_team] + param_dict['attack_' + away_team])]

    def dixon_coles_simulate_match(self, params_dict, home_team, away_team, max_goals=10):
        team_avgs = self.calc_means(params_dict, home_team, away_team)
        team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)] for team_avg in team_avgs]
        output_matrix = np.outer(np.array(team_pred[0]), np.array(team_pred[1]))
        correction_matrix = np.array([[self.rho_correction(home_goals, away_goals, team_avgs[0],
                                                           team_avgs[1], params_dict['rho']) for away_goals in range(2)]
                                      for home_goals in range(2)])
        output_matrix[:2, :2] = output_matrix[:2, :2] * correction_matrix
        return output_matrix


class LogisticRegModel(Models):
    parameter_dict = {'leagues': 1,
                      'seasons': 1,
                      'matchdays': 1,
                      'time': 0
                      }

    def __init__(self):
        self.data = ''
        self.home_teams = ''
        self.away_teams = ''
        self.home_scores = ''
        self.away_scores = ''
        self.model_ = ''

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
        prepared_data = self.prepare_data(data)
        self.data = prepared_data
        self.home_teams = prepared_data['team_home_id'].tolist()
        self.away_teams = prepared_data['team_guest_id'].tolist()
        self.home_scores = prepared_data['points_home'].tolist()
        self.away_scores = prepared_data['points_guest'].tolist()

    def start_training(self, x=False):
        """
            Creates a model and corrects the algorithms parameters using the given data.
        """
        home_team_name = self.home_teams
        away_team_name = self.away_teams
        home_score = self.home_scores
        away_score = self.away_scores

        home_team_name, away_team_name, home_score, away_score = [
            np.array(x)
            for x in [home_team_name, away_team_name, home_score, away_score]
        ]

        team_names = np.array(list(home_team_name) + list(away_team_name)).reshape(-1, 1)

        self.team_encoding_ = OneHotEncoder(sparse=False).fit(team_names)

        home_dummies = self.team_encoding_.transform(home_team_name.reshape(-1, 1))
        away_dummies = self.team_encoding_.transform(away_team_name.reshape(-1, 1))

        X = np.concatenate([home_dummies, away_dummies], 1)
        y = np.sign(home_score - away_score)

        # start training
        model = LogisticRegression(
            penalty="l2", fit_intercept=False, multi_class="ovr", C=1
        )
        model.fit(X, y)
        self.model_ = model


    def check_teams(self, home_team_name, away_team_name):
        """Check if team are encoded."""
        if not home_team_name in self.team_encoding_.categories_[0]: return -1
        if not away_team_name in self.team_encoding_.categories_[0]: return -1

    def predict(self, home_team_name, away_team_name):
        """
        Predict the probabilities of draw and win for each team..

        Parameters
        ----------
        home_team_name: str
            Home team name.

        away_team_name: str
            Away team name.

        Returns
        -------
        A dataframe with the probabilities.

        """
        if not self.check_ids_in_data(home_team_name, away_team_name, self.data):
            outcome = -1
        else:
            home_team_name = str(home_team_name)
            away_team_name = str(away_team_name)
            check_is_fitted(self.model_)
            if self.check_teams(home_team_name, away_team_name) == -1:
                outcome = -1
            else:
                home_team_name = np.array(home_team_name)
                away_team_name = np.array(away_team_name)
                home_dummies = self.team_encoding_.transform(home_team_name.reshape(-1, 1))
                away_dummies = self.team_encoding_.transform(away_team_name.reshape(-1, 1))
                X = np.concatenate([home_dummies, away_dummies], 1)

                outcome = self.model_.predict_proba(X)[0]
                guest_win = outcome[0]
                draw = outcome[1]
                home_win = outcome[2]

                outcome = {'home_win': round(home_win, 2),
                                    'draw': round(draw, 2),
                                    'guest_win': round(guest_win, 2)
                           }

        return {'outcome': outcome,
                'score': -1
                }


# %%

# functions for evaluation
def compare(test_matches, evaluation_data):
    """
    compares each predicted result with real result and calculates prediction precision
    :test_matches pd.Dataframe test dataset
    :evaluation_data pd.Dataframe predicted data
    :return float prediction precision
    """
    total = evaluation_data.shape[0]
    correct = 0
    for match_id in evaluation_data['match_id']:
        predicted_outcome = evaluation_data[evaluation_data['match_id'] == match_id]['outcome'].item()
        real_outcome = test_matches[test_matches['match_id'] == match_id]['outcome'].item()

        if predicted_outcome == real_outcome:
            correct += 1
    hit_percentage = correct/total
    return hit_percentage

# for testing inside the script
if __name__ == '__main__':
    crawler = crawler.BundesligaCrawler()
    dataset = crawler.get_data_for_algo([1, 2], [2019, 2018, 2017, 2016], 1, 34, 0, 0)
    test_data = crawler.get_data_for_algo([1], [2020], 1, 34, 0, 0)

    model = LogisticRegModel()
    model.set_data(dataset)

    #csv_name = crawler.pretrained_data_source(True)
    #data = pd.read_csv(csv_name, header=None, index_col=0, squeeze=True).to_dict()
    #model.set_pretrained_data(data)

    model.start_training()

    test_data, evaluation_data = model.evaluate(test_data, 'log-reg_bl1u2_2019-2016')
    perc = compare(test_data, evaluation_data)
    print(perc)

    #outcome = model.predict(str(40), str(9))

    #print(outcome)

# %%
