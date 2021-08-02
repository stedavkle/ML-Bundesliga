import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

test_acc = {'Most_Wins': 0.425531914893617, 'Poisson_Model': 0.4738562091503268, 'Logistic_Regression': 0.4869281045751634}

x_height = 12
y_height = 5

test_acc_diff = {
    '2019-2015': {
        'Most_Wins': 0.425531914893617,
        'Poisson_Model': 0.4738562091503268,
        'Logistic_Regression': 0.4869281045751634
    },
    '2019-2018': {
        'Most_Wins': 0.4562043795620438,
        'Poisson_Model': 0.49673202614379086,
        'Logistic_Regression': 0.5163398692810458
    },
    '2018-2016': {
        'Most_Wins': 0.4,
        'Poisson_Model': 0.4542483660130719,
        'Logistic_Regression': 0.4738562091503268
    },
    '2017-2015': {
        'Most_Wins': 0.3779527559055118,
        'Poisson_Model': 0.434640522875817,
        'Logistic_Regression': 0.42810457516339867
    }
}

dict_draw = {
    'Most_Wins': {
        'draws_2020': 81,
        'pred_draws': 49,
        'precision': 0.6049382716049383
    },
    'Poisson_Model': {
        'draws_2020': 81,
        'pred_draws': 0,
        'precision': 0.0
    },
    'Logistic_Regression': {
        'draws_2020': 81,
        'pred_draws': 25,
        'precision': 0.30864197530864196
    }
}

plot_path = 'teamproject/data/evaluation/'

def plot_draw_prediction(draw_dict, filename):
    draws = {}
    draw_sum = 0
    for key in draw_dict.keys():
        draws[key] = draw_dict[key]['precision']
        draw_sum = draw_dict[key]['draws_2020']
    plot_algorithm_compare_on_one_dataset(draws, 'Vorhersagegenauigkeit Unentschieden für Saison 2020\nDatensatz Saison 2015-2019, Anzahl Unentschieden in 2020: {}'.format(draw_sum), filename)


def plot_algorithm_compare_on_one_dataset(acc_dict, title, filename):
    color = ['blue', 'red', 'orange', 'purple', 'green']
    x_label = list(acc_dict.keys())
    x_pos = [i for i in range(1, len(x_label)+1)]
    data = list(acc_dict.values())

    f = plt.figure()
    f.set_figwidth(x_height)
    f.set_figheight(y_height)

    plt.bar(x_pos, data, tick_label=x_label, width=0.8, color=color[0:len(x_pos)])

    for i in x_pos:
        plt.text(i, data[i-1], '{:.2f}'.format(data[i-1]), ha='center')

    plt.xlabel('Vorhersagemodelle')
    plt.ylabel('Genauigkeit')
    plt.title(title)

    filename = plot_path + filename + '.png'

    plt.savefig(filename)
    plt.show()




def plot_algorithm_compare_on_diff_datasets(acc_dict, title, filename):
    color = ['blue', 'red', 'orange', 'purple', 'green']
    x_label = list(acc_dict.keys()) # dataset keys
    models = list(acc_dict[x_label[0]].keys())
    x_pos = [i for i in range(1, len(x_label)+1)]

    f = plt.figure()
    f.set_figwidth(x_height)
    f.set_figheight(y_height+3)

    col_count = 0
    for model in models:
        acc_model = [] # y-axis
        for key in x_label:
            acc_model.append(acc_dict[key][model])

        plt.plot(x_label, acc_model, color=color[col_count], linestyle='dashed',
                 linewidth=3, marker='o', markersize=10)
        col_count += 1

    # random marker
    random = [0.33] * len(x_label)
    plt.plot(x_label, random, color='black', linestyle='dashed', linewidth=2, alpha=0.5)

    plt.xlabel('Datensätze Saisons')
    plt.ylabel('Genauigkeit')
    plt.title(title)

    plt.ylim(0.3, 0.6)

    models.append('Zufall')
    plt.legend(models)

    filename = plot_path + filename + '.png'

    plt.savefig(filename)
    plt.show()

def plot_matchday_compare(without_2020, with_2020, day):
    color = ['dodgerblue', 'orange', 'dodgerblue', 'orange','dodgerblue', 'orange','dodgerblue', 'orange','dodgerblue', 'orange']
    x_label = list(with_2020.keys())
    x_pos = [i for i in range(1, (len(x_label) * 2) + 1)]

    keys_without2020 = list(without_2020.keys())
    keys_with2020 = list(with_2020.keys())
    values_without2020 = list(without_2020.values())
    values_with2020 = list(with_2020.values())
    data = []
    label = []

    for i in range(len(x_label)):
        data.append(values_without2020[i])
        data.append(values_with2020[i])
        label.append(keys_without2020[i])
        label.append(keys_with2020[i])

    f = plt.figure()
    f.set_figwidth(x_height)
    f.set_figheight(y_height)
    plt.xticks(rotation=45)

    plt.bar(x_pos, data, align='edge', tick_label=label, width=0.6, color=color[0:len(x_pos)])

    for i in x_pos:
        plt.text(i, data[i - 1], '{:.2f}'.format(data[i - 1]), ha='left')

    plt.xlabel('Vorhersagemodelle')
    plt.ylabel('Genauigkeit')
    plt.title('Vorhersagegenauigkeit {}. Spieltag 2020'.format(day))

    filename = plot_path + 'prediction_of_matchday_{}.png'.format(day)

    blue_patch = mpatches.Patch(color='dodgerblue', label='Datensatz 2015-2019')
    red_patch = mpatches.Patch(color='orange', label='Datensatz 2015 - {}. Spieltag 2020'.format(day-1))
    plt.legend(handles=[blue_patch, red_patch])

    plt.savefig(filename)
    plt.show()


if __name__ == '__main__':
    None
    # TODO: to start plots from here, remove teamproject/ from directory path!
    #plot_algorithm_compare_on_one_dataset(test_acc, 'Vorhersagegenauigkeit für Saison 2020 auf Datensatz Saison 2015-2019')
    #plot_algorithm_compare_on_diff_datasets(test_acc_diff, 'Vorhersagegenauigkeit für Saison 2020 auf verschiedenen Datensätzen')
    #plot_draw_prediction(dict_draw, 'test')