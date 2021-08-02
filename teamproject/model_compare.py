import models
import crawler
import matplotlib
import pandas as pd
import model_compare_plot as plot

model_dict = {
    1: {'run': models.MostWins(),
        'file': 'Most_Wins'},
    2: {'run': models.PoissonModel(),
        'file': 'Poisson_Model'},
    3: {'run': models.LogisticRegModel(),
        'file': 'Logistic_Regression'},
    4: {'run': models.DixonColes(),
        'file': 'Dixon_Coles_ohne_Zeit'},
    5: {'run': models.DixonColes(),
        'file': 'Dixon_Coles_mit_Zeit'}
}



def compare_algo_precision_for_2020(seasons, last_matchday=34, inlcude_matchdays=False):
    """
    :seasons array mit saisons
    :last_matchday int mit letztem spieltag, default=34
    :include_matchdays bool rechne spieltage der neuen saisons mit ein, default=False
    """
    precision_dict = {}

    craw = crawler.BundesligaCrawler()

    if inlcude_matchdays:
        seasons.append(2020)
        training_data = craw.get_data_for_algo([1, 2], seasons, 1, last_matchday, 0, 0)
    else:
        training_data = craw.get_data_for_algo([1, 2], seasons, 1, 34, 0, 0)

    test_data = craw.get_data_for_algo([1], [2020], 1, 34, 0, 0)

    for key in model_dict:
        model_instance = model_dict[key]['run']
        model_instance.set_data(training_data)

        if key == 4:
            continue #todo: wegmachen nicht vergessen!
            path = 'teamproject/data/evaluation/bl1u2_{}_{}_pretrained_data_NO_decay.csv'.format(seasons[0], seasons[-1])

            data = pd.read_csv(path, header=None, index_col=0, squeeze=True).to_dict()
            model_instance.set_pretrained_data(data)

        elif key == 5:
            continue #todo: wegmachen nicht vergessen!
            path = 'teamproject/data/evaluation/bl1u2_{}_{}_pretrained_data_decay.csv'.format(seasons[0], seasons[-1])

            data = pd.read_csv(path, header=None, index_col=0, squeeze=True).to_dict()
            model_instance.set_pretrained_data(data)

        else:
            model_instance.start_training()

        test_data_unif, prediced_data = model_instance.evaluate(test_data, model_dict[key]['file'])

        precision = compare(test_data_unif, prediced_data)

        precision_dict[model_dict[key]['file']] = precision

    return precision_dict


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


def draw_analysis(seasons):
    compare_algo_precision_for_2020(seasons)

    # csv abholen
    dataset = {}

    for key in model_dict:
        if key == 4 or key == 5:
            continue #todo:
        else:
            filename = model_dict[key]['file']
            path_test = 'teamproject/data/evaluation/{}_test_data.csv'.format(filename)
            path_eval = 'teamproject/data/evaluation/{}_eval_data.csv'.format(filename)

            test_data = pd.read_csv(path_test)
            pred_data = pd.read_csv(path_eval)

            draws_in_2020 = test_data[test_data['outcome'] == 0].shape[0]
            predicted_draws = pred_data[pred_data['outcome'] == 0].shape[0]
            precision = predicted_draws/draws_in_2020

            dataset[filename] = {
                'draws_2020': draws_in_2020,
                'pred_draws': predicted_draws,
                'precision': precision
            }

    return dataset


def matchday_analysis(season, day):
    '''result_dict = {match: {
                            home_id: 87,
                            guest_id: 16,
                            result: '3:2',
                            winner: 1,
                            w_most_wins: {outcome},
                            w_poisson
                           }}'''
    precision_without_2020 = compare_algo_precision_for_2020(season)
    without_2020_dict = create_matchday_dataset(day)

    precision_with_2020 = compare_algo_precision_for_2020(season, day-1, True)
    with_2020_dict = create_matchday_dataset(day)

    return without_2020_dict, with_2020_dict



def create_matchday_dataset(day):
    diction = {}
    for key in model_dict:
        if key == 4 or key == 5:
            continue #todo
        else:
            filename = model_dict[key]['file']
            path_test = 'teamproject/data/evaluation/{}_test_data.csv'.format(filename)
            path_eval = 'teamproject/data/evaluation/{}_eval_data.csv'.format(filename)

            test_data = pd.read_csv(path_test)
            pred_data = pd.read_csv(path_eval)

            matchday = test_data[test_data['matchday'] == day]
            if key == 1:
                matches = {}
                for index, row in matchday.iterrows():
                    matches[row['match_id'].item()] = {
                        'team_home_id': row['team_home_id'].item(),
                        'team_guest_id': row['team_guest_id'].item(),
                        'points_home': row['points_home'].item(),
                        'points_guest': row['points_guest'].item()
                    }
                diction['matches'] = matches

            prediction = {}
            for index, row in matchday.iterrows():
                id = row['match_id'].item()
                match = pred_data.index[pred_data['match_id'] == id].tolist()
                for i in match:
                    prediction[id] = {
                        'home_win': pred_data.loc[i, 'home_win'],
                        'draw': pred_data.loc[i, 'draw'],
                        'guest_win': pred_data.loc[i, 'guest_win']
                    }
            diction[model_dict[key]['file']] = prediction
    return diction


def compare_matchday(pred_matchday):
    results = pred_matchday['matches']
    precision_dict = {}

    for model in pred_matchday.keys():
        correct_predicted = 0
        match_count_of_model = 0
        if model == 'matches':
            continue

        for match_id in pred_matchday[model].keys():
            match_count_of_model += 1
            match = pred_matchday[model][match_id]
            outcome = max(match, key=match.get)

            points_home = results[match_id]['points_home']
            points_guest = results[match_id]['points_guest']

            if points_home > points_guest:
                if outcome == 'home_win':
                    correct_predicted += 1
            elif points_home < points_guest:
                if outcome == 'guest_win':
                    correct_predicted += 1
            else:
                if outcome == 'draw':
                    correct_predicted += 1

        model_precision = correct_predicted / match_count_of_model
        precision_dict[model] = model_precision

    return precision_dict


def matchday_dict_to_csv(dict, filename):
    matches = dict['matches']
    most_wins = dict['Most_Wins']
    poisson = dict['Poisson_Model']
    log_reg = dict['Logistic_Regression']
    #dixon_coles = dict['Dixon_Coles_ohne_Zeit']
    #dixon_coles_decay = dict['Dixon_Coles_mit_Zeit']

    craw = crawler.BundesligaCrawler()
    id_to_team, team_to_id = craw.get_team_dicts([1], [2020])
    # aSD steht für aktuelle Saison Daten (bis zum Spieltag)
    columns = ['match_id', 'home', 'guest', 'result', 'most_wins', 'poisson', 'logistic_regression', 'dc_no_decay', 'dc_decay']

    match_id = []
    home = []
    guest = []
    result = []
    most_wins_list = []
    poisson_list = []
    log_reg_list = []
    #dixon_coles_list = []
    #dixon_coles_decay_list = []
    for id in matches.keys():
        match_id.append(id)
        home.append(id_to_team[matches[id]['team_home_id']])
        guest.append(id_to_team[matches[id]['team_guest_id']])
        result.append("{} : {}".format(matches[id]['points_home'], matches[id]['points_guest']))

        if most_wins.get(id):
            most_wins_list.append("{} x {} x {}".format(most_wins[id]['home_win'], most_wins[id]['draw'], most_wins[id]['guest_win']))
        else:
            most_wins_list.append("")

        if poisson.get(id):
            poisson_list.append("{} x {} x {}".format(poisson[id]['home_win'], poisson[id]['draw'], poisson[id]['guest_win']))
        else:
            poisson_list.append("")

        if log_reg.get(id):
            log_reg_list.append("{} x {} x {}".format(log_reg[id]['home_win'], log_reg[id]['draw'], log_reg[id]['guest_win']))
        else:
            log_reg_list.append("")

        '''
        if dixon_coles.get(id):
            dixon_coles_list.append("{} x {} x {}".format(dixon_coles[id]['home_win'], dixon_coles[id]['draw'], dixon_coles[id]['guest_win']))
        else:
            dixon_coles_list.append("")

        if dixon_coles_decay.get(id):
            dixon_coles_decay_list.append("{} x {} x {}".format(dixon_coles_decay[id]['home_win'], dixon_coles_decay[id]['draw'], dixon_coles_decay[id]['guest_win']))
        else:
            dixon_coles_decay_list.append("")
        '''
    table = {
        'match_id': match_id,
        'home': home,
        'guest': guest,
        'result': result,
        'most_wins': most_wins_list,
        'poisson': poisson_list,
        'logistic_regression': log_reg_list,
        #'dc_no_decay': dixon_coles_list,
        #'dc_decay': dixon_coles_decay_list
    }
    df = pd.DataFrame(table, columns=columns)

    path = "teamproject/data/evaluation/{}.csv".format(filename)
    df.to_csv(path, encoding='utf-8-sig', index=False)




if __name__ == '__main__':

    # stat 1
    print('\nalgorithmenvergleich: alle algos precision von 2019-2015 für 1. BL 2020\n')
    prec_all_models_2019_2015 = compare_algo_precision_for_2020([2019, 2018, 2017, 2016, 2015])
    print(prec_all_models_2019_2015)
    plot.plot_algorithm_compare_on_one_dataset(prec_all_models_2019_2015,
                                               'Vorhersagegenauigkeit für Saison 2020 auf Datensatz Saison 2015-2019',
                                               'acc_alle_algos_fuer_2020_auf_2015_2019')
    
    # stat 2
    print('\n\nzeit faktor: alle algos precision von 2019-2015, 2019-2018, 2018-2016, 2017-2015 für 1. BL 2020\n')
    seasons = [[2017, 2016, 2015], [2018, 2017, 2016], [2019, 2018], [2019, 2018, 2017, 2016, 2015]]

    prec_all_models_diff_seasons = {}

    for s in seasons:
        prec = compare_algo_precision_for_2020(s)
        key = '{}-{}'.format(s[0], s[-1])
        prec_all_models_diff_seasons[key] = prec

    print(prec_all_models_diff_seasons)
    plot.plot_algorithm_compare_on_diff_datasets(prec_all_models_diff_seasons,
                                                 'Vorhersagegenauigkeit für Saison 2020 auf verschiedenen Datensätzen',
                                                 'acc_alle_algos_fuer_2020_diff_datensaetze')

    # stat 3
    print('\n\n unentschieden: alle algos precision von 2019-2015 die unentschieden für 1. BL 2020 vorhersagen')
    draws = draw_analysis([2019, 2018, 2017, 2016, 2015])
    print(draws)
    plot.plot_draw_prediction(draws, 'acc_unentschieden_2020')

    # stat 4
    print('\n\n einfluss von aktueller saison: alle algos precision von 2019-2015 für spieltag 8, 18 und 28 in 1. BL 2020')
    days = [8, 18, 28]
    for day in days:
        without_2020_dict, with_2020_dict = matchday_analysis([2019, 2018, 2017, 2016, 2015], day)
        matchday_dict_to_csv(without_2020_dict, 'bl1_2020_md{}_without2020_prediction'.format(day))
        matchday_dict_to_csv(with_2020_dict, 'bl1_2020_md{}_with2020_prediction'.format(day))
        precision_matchday_without_2020 = compare_matchday(without_2020_dict)
        precision_matchday_with_2020 = compare_matchday(with_2020_dict)
        print("Genauigkeit mit Datensatz 2019-2015 zu Spieltag {}: ".format(day) + str(precision_matchday_without_2020))
        print("Genauigkeit mit Datensatz 2020-2015 zu Spieltag {}: ".format(day) + str(precision_matchday_with_2020))



