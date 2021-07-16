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



def test_mostwins():
    """ tests the mostwins algorithm """
    # creates an instance of mostwins
    mostwins = models.MostWins()

    # prepares the data for most wins
    prep_data = mostwins.prepare_data(test_dataset)
    assert isinstance(prep_data, dict)

    # calls set_data
    mostwins.set_data(test_dataset)

    # starts the training, here it skips it
    test_return = mostwins.start_training()
    assert isinstance(test_return, None)

    # tests the algorithm
    predict_return = mostwins.predict
    assert isinstance(predict_return, dict)
    # todo: test the contents of dictionaries

def test_poisson():
    """ tests the poisson algorithm """
    # creates an instance of poisson
    poisson = models.PoissonModel()

    # prepares the data
    prep_data = poisson.prepare_data(test_dataset)
    assert isinstance(prep_data, dict)

    # calls set_data
    poisson.set_data()
    # todo: check ob poisson.data richtiges format hat

    # starts the training
    poisson.start_training()

    # starts the training
    poisson.simulate_match('A', 'B')
    # todo: check contents of poisson.simulation

    # tests the prediction of outcome
    predict_return = poisson.predict_outcome()
    assert isinstance(predict_return, dict)
    # todo: check contents of predict_return
    # todo: is the home_win >= guest_win >= draw

    # tests the prediction of score
    predict_return = poisson.predict_score()
    assert isinstance(predict_return, dict)
    # todo: check contents of predict_return
    # todo: is home/guest points >= 0

    # todo: test predict

def test_dixoncoles():
    """ tests the dixoncoles algorithm """
    # creates an instance of dixoncoles
    dixoncoles = models.DixonColes()

    # prepares the data
    prep_data = dixoncoles.prepare_data(test_dataset)
    assert isinstance(prep_data, dict)

    # calls set_data
    dixoncoles.set_data()
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




def test_experience_always_wins():
    model = models.ExperienceAlwaysWins(test_dataset)
    winner = model.predict_winner

    # B is the most experienced team with two matches:
    assert winner('A', 'B') == winner('B', 'A') == 'B'
    assert winner('C', 'B') == winner('B', 'C') == 'B'

    # A and C are tied with one match, so the home team wins:
    assert winner('A', 'C') == 'A'
    assert winner('C', 'A') == 'C'

    # We don't know 'D' or 'E' yet, so they should be counted as having zero
    # matches:
    assert winner('A', 'D') == winner('D', 'A') == 'A'
    assert winner('A', 'E') == winner('E', 'A') == 'A'
    assert winner('D', 'E') == 'D'
    assert winner('E', 'D') == 'E'
