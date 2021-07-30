# Use this file to test your prediction algorithms.

from teamproject import models
# models as models
import pandas as pd


# It is important to test your algorithms against handcrafted data to reliably
# cover edge cases! So feel free to make up several test datasets in the same
# format as would be returned by your crawler:
test_dataset = pd.DataFrame([
    ['A', 0, 1, 'B'],
    ['B', 1, 0, 'C'],
], columns=['home_team', 'home_score', 'guest_score', 'guest_team'])

# data = md_mostwins.prepare_data()
# print(data)
# The following is an example of how useful tests could look like:
matches = pd.DataFrame({'match_id': [1, 2, 3, 4],
                        'matchday': [1, 2, 3, 4],
                        'team_home_id': [10, 20, 30, 40],
                        'team_guest_id': [30, 10, 10, 30],
                        'match_date_time_utc': ['2020-06-02T18:00:00Z', '2020-06-02T18:00:00Z', '2020-06-02T18:00:00Z', '2020-06-02T18:00:00Z']})
results = pd.DataFrame({'result_id': [1, 2, 3, 4],
                        'points_home': [1, 2, 1, 5],
                        'points_guest': [2, 0, 1, 5],
                        'result_type_id': [1, 1, 1, 1],
                        'match_id': [1, 2, 3, 4]})

test_data = [matches, results]

'''
Team 10 vs Team 30 mit 1:2
Team 20 vs Team 10 mit 2:0
Team 30 vs Team 10 mit 1:1
Team 40 vs Team 30 mit 5:5      
'''


def test_mostwins():
    """ tests the mostwins algorithm """
    # creates an instance of mostwins
    mostwins = models.MostWins()

    # prepares the data for most wins
    prep_data = mostwins.prepare_data(test_data)
    assert isinstance(prep_data, pd.DataFrame)
    assert (prep_data.result_type_id == 1).all()

    # calls set_data
    mostwins.set_data(test_data)

    # starts the training, here it skips it
    test_return = mostwins.start_training()
    assert test_return is None

    # tests the algorithm with 10 - 30
    predict_return_10_30 = mostwins.predict(10, 30)
    assert isinstance(predict_return_10_30, dict)
    assert predict_return_10_30['outcome']['home_win'] == 0.0
    assert predict_return_10_30['outcome']['draw'] == 0.5
    assert predict_return_10_30['outcome']['guest_win'] == 0.5
    assert predict_return_10_30['score'] == -1

    # edge case, no previous matches with 0 - 10
    predict_return_0_10 = mostwins.predict(0, 10)
    assert isinstance(predict_return_0_10, dict)
    assert predict_return_0_10['outcome'] == -1
    assert predict_return_10_30['score'] == -1

    predict_return_20_10 = mostwins.predict(20, 10)
    assert isinstance(predict_return_20_10, dict)
    assert predict_return_20_10['outcome']['home_win'] == 1.0
    assert predict_return_20_10['outcome']['draw'] == 0.0
    assert predict_return_20_10['outcome']['guest_win'] == 0.0
    assert predict_return_20_10['score'] == -1

    predict_return_40_30 = mostwins.predict(40, 30)
    assert isinstance(predict_return_40_30, dict)
    assert predict_return_40_30['outcome']['home_win'] == 0.0
    assert predict_return_40_30['outcome']['draw'] == 1.0
    assert predict_return_40_30['outcome']['guest_win'] == 0.0
    assert predict_return_40_30['score'] == -1

    # {'outcome': {'home_win': 0.0, 'draw': 0.0, 'guest_win': 1.0}, 'score': -1}

test_mostwins()


def test_poisson():
    """ tests the poisson algorithm """
    # creates an instance of poisson
    poisson = models.PoissonModel()

    # prepares the data
    prep_data = poisson.prepare_data(test_data)
    assert isinstance(prep_data, pd.DataFrame)
    assert (prep_data.result_type_id == 1).all()

    # calls set_data
    poisson.set_data(test_data)

    # starts the training
    poisson.start_training()

    # simulates the match
    poisson.simulate_match('10', '20')
    assert len(poisson.simulation) == poisson.MAX_GOALS + 1
    assert len(poisson.simulation[0]) == poisson.MAX_GOALS + 1

    # tests the prediction of outcome
    predict_return_outcome = poisson.predict_outcome()
    assert isinstance(predict_return_outcome, dict)
    assert predict_return_outcome['home_win'] >= 0
    assert predict_return_outcome['draw'] >= 0
    assert predict_return_outcome['guest_win'] >= 0
    assert predict_return_outcome['home_win'] + predict_return_outcome['draw'] + predict_return_outcome['guest_win'] <= 1
    # todo: check contents of predict_return

    # tests the prediction of score
    predict_return_score = poisson.predict_score()
    assert isinstance(predict_return_score, dict)
    assert predict_return_score[1]['home_points'] >= 0
    assert predict_return_score[1]['guest_points'] >= 0
    assert predict_return_score[1]['probability'] >= 0
    assert predict_return_score[1]['probability'] <= 1

    # test predict
    predict_return = poisson.predict('10', '20')
    assert isinstance(predict_return, dict)
    assert predict_return['outcome'] == predict_return_outcome
    assert predict_return['score'] == predict_return_score

    # simulates the match
    poisson.simulate_match('10', '20')
    assert len(poisson.simulation) == poisson.MAX_GOALS + 1
    assert len(poisson.simulation[0]) == poisson.MAX_GOALS + 1

    # tests the prediction of outcome
    predict_return_outcome = poisson.predict_outcome()
    assert isinstance(predict_return_outcome, dict)
    assert predict_return_outcome['home_win'] >= 0
    assert predict_return_outcome['draw'] >= 0
    assert predict_return_outcome['guest_win'] >= 0
    assert predict_return_outcome['home_win'] + predict_return_outcome['draw'] + predict_return_outcome['guest_win'] <= 1
    # todo: check contents of predict_return

    # tests the prediction of score
    predict_return_score = poisson.predict_score()
    assert isinstance(predict_return_score, dict)
    assert predict_return_score[1]['home_points'] >= 0
    assert predict_return_score[1]['guest_points'] >= 0
    assert predict_return_score[1]['probability'] >= 0
    assert predict_return_score[1]['probability'] <= 1

    # test predict
    predict_return = poisson.predict('10', '20')
    assert isinstance(predict_return, dict)
    assert predict_return['outcome'] == predict_return_outcome
    assert predict_return['score'] == predict_return_score


'''
def test_dixoncoles():
    """ tests the dixoncoles algorithm """
    # creates an instance of dixoncoles
    dixoncoles = models.DixonColes()

    # prepares the data
    prep_data = dixoncoles.prepare_data(test_data)
    assert isinstance(prep_data, dict)

    # calls set_data
    dixoncoles.set_data(test_data)
    # todo: check ob poisson.data richtiges format hat

    # starts the training
    dixoncoles.start_training()

    # starts the training
    test_result = dixoncoles.predict('A', 'B')
    assert isinstance(test_result, dict)
    assert test_result['score'] == -1
    # todo: check contents of test_return['result']

    # test rho_correction (what parameters, then return abfangen)
    rho_0_0 = dixoncoles.rho_correction(0, 0, 2, 3, 4)
    rho_0_1 = dixoncoles.rho_correction(0, 1, 2, 3, 4)
    rho_1_0 = dixoncoles.rho_correction(1, 0, 2, 3, 4)
    rho_1_1 = dixoncoles.rho_correction(1, 1, 2, 3, 4)
    assert rho_0_0 == 1 - (2*3*4)
    assert rho_0_1 == 1 + (2*4)
    assert rho_1_0 == 1 + (3*4)
    assert rho_1_1 == 1 - 4
    assert isinstance(dixoncoles.rho_correction(2, 0, 2, 3, 4) == 1.0)

    # solve parameters
    # solve_parameters_decay
    # calc_means

    # tests the simulation of a match
    # todo: create the right kind of an input
    # output_matrix = dixoncoles.dixon_coles_simulate_match()
    # assert isinstance(output_matrix, dict)
    # todo: check contents of predict_return
'''


def test_LogisticRegModel():
    """tests the logistic regression model"""
    # creates an instance of logistic regression
    logRegModel = models.LogisticRegModel()

    # prepares the data
    prep_data = logRegModel.prepare_data(test_data)
    assert isinstance(prep_data, pd.DataFrame)
    assert (prep_data.result_type_id == 1).all()

    # calls set_data
    logRegModel.set_data(test_data)

    # starts the training
    logRegModel.start_training()

    # predicts
    test_result = logRegModel.predict('10', '30')
    home_win = test_result['outcome']['home_win']
    draw = test_result['outcome']['draw']
    guest_win = test_result['outcome']['guest_win']
    assert isinstance(test_result, dict)
    assert test_result['score'] == -1
    assert home_win >= 0
    assert draw >= 0
    assert guest_win >= 0
    assert home_win + draw + guest_win > 0.9
    assert home_win + draw + guest_win <= 1
    print(test_result)


test_LogisticRegModel()




