/*
    Displays Page Content
 */
/**
 * creates layout of sport selection page
 * creates dropdown based on global sports content
 */
function sport_selection_render(){
    sport_selection_designer();
    set_innerHTML("right_btn", "<button class='btn btn-danger' onclick=create_session()>Bestätigen</button>");
    var html_str = "<h3>Willkommen!</h3>" +
    "<p>Wähle eine Sportart:</p>" +
    "<select class='form-control' id='sport_selection' onchange=display('right_btn')>" +
    "<option value=0 selected disabled hidden>nichts ausgewählt</option>";

    var sports = new Sports();

    for (var key in sports.sports){
        html_str += "<option value=" + key + ">" + sports.sports[key] + "</option>";
    }
    html_str += "</select>";

    set_innerHTML("1-col-1", html_str);
}

function crawler_data_render(leagues_seasons){
    crawler_data_designer();

    var leagues = {};
    var seasons = {};
    var biggest_league_size = 0;
    var biggest_league_id = 0;

    for (var key in leagues_seasons){

        leagues[key] = leagues_seasons[key].name;

        if (leagues_seasons[key].size > biggest_league_size){
            biggest_league_size = leagues_seasons[key].size;
            biggest_league_id = key;
        }
    }

    var biggest_league_seasons = leagues_seasons[biggest_league_id].seasons;
    for (var i = 0; i < biggest_league_seasons.length; i++){
        var year = biggest_league_seasons[i];
        var next_year = String(year + 1);
        var str = String(year) + "/" + next_year.slice(2);
        seasons[year] = str;
    }

    set_session_item('leagues', leagues);
    set_session_item('seasons', seasons);
    set_session_item('leagues_seasons_from_crawler', leagues_seasons);

    // TODO: Multi Select schöner machen
    // display hint
    var html_str_hint = "<p>Für Mehrfachauswahl \'Strg'\, bzw. 'Umschalt' gedrückt halten.</p>";
    set_innerHTML('1-col-1', html_str_hint);

    // define submit button
    set_innerHTML('right_btn', "<button class='btn btn-danger' onclick=store_crawler_parameter()>Daten beziehen</button>");

    // display league selection
    var html_str_left = "<p>Ligen:</p>" +
        "<select multiple class='form-control' id='leagues_selection' onchange=show_data_submit()>" +
        "<option value=0 selected disabled hidden>nichts ausgewählt</option>";

    for (var key in leagues){
        html_str_left += "<option value=" + key + ">" + leagues[key] + "</option>";
    }
    html_str_left += "</select>";
    set_innerHTML("2-col-1", html_str_left);

    // display season selection
    var html_str_right = "<p>Saisons:</p>" +
        "<select multiple class='form-control' id='seasons_selection' onchange=show_data_submit()>" +
        "<option value=0 selected disabled hidden>nichts ausgewählt</option>";

    for (var key in seasons){
        html_str_right += "<option value=" + key + ">" + seasons[key] + "</option>";
    }
    html_str_right += "</select>";
    set_innerHTML("2-col-2", html_str_right);
}


function model_selection_render(){
    model_selection_designer();
    //window.alert("model_selection_render(): entered");
    set_innerHTML("right_btn", "<button class='btn btn-danger' onclick=set_model()>Bestätigen</button>");

    set_innerHTML("1-col-1", "<p>Wähle einen Algorithmus oder ein ML-Modell aus:</p>");

    var html_str = "<select class='form-control' id='model_selection' onchange=show_model_description()>" +
    "<option value=0 selected disabled hidden>nichts ausgewählt</option>";

    var model = new Models();

    for (var key in model.models){
        html_str += "<option value=" + key + ">" + model.models[key]['model'] + "</option>";
    }
    html_str += "</select>";

    set_innerHTML("2-col-1", html_str);
}

function training_data_render(parameter){
    training_data_designer();
    var model_id = get_session_item('selected_model_id');
    var models = new Models();

    if (models.models[model_id].training){
        set_innerHTML('right_btn', "<button class='btn btn-danger' onclick=store_selected_parameter(4)>Training starten</button>");
    }
    else {
        set_innerHTML('right_btn', "<button class='btn btn-danger' onclick=store_selected_parameter(3)>Daten festlegen</button>");
    }

    var html_str_leagues = "<h4>Ligen:</h4>" + create_select_of_selected('leagues');
    var html_str_seasons = "<h4>Saisons:</h4>" + create_select_of_selected('seasons');
    var html_str_matchdays_first = "<p>ab Spieltag:</p>" + create_matchday_selection('first');
    var html_str_matchdays_last = "<p>bis einschließlich Spieltag:</p>" + create_matchday_selection('last');
    var html_str_points = "<input type='checkbox' id='points_checkbox'>" +
        "<label for='points_checkbox'>Tore berücksichtigen</label>";

    // TODO: sich klar werden, was genau eigentlich auswählbare Parameter sein sollen!!!
    set_innerHTML("2-col-1", html_str_leagues);
    set_innerHTML("2-col-2", html_str_seasons);
    set_innerHTML("3-col-1", html_str_matchdays_first);
    set_innerHTML("3-col-2", html_str_matchdays_last);
    set_innerHTML("3-col-3", html_str_points);

    // display parameter, if model needs it
    for (var key in parameter){
        if (parameter[key] == 1){

            switch (key) {
                case 'leagues':
                    display('2-col-1');
                    break;
                case 'seasons':
                    display('2-col-2');
                    break;
                case 'matchdays':
                    display('3-col-1');
                    display('3-col-2');
                    break;
                case 'points':
                    display('3-col-3');
                    break;
                default:
                    window.alert("training_data_render(): no parameter option fits");
            }
        }
    }
}

function team_select_render(team_list){
    team_select_designer();
    set_session_item('team_list', team_list);
    set_innerHTML("1-col-1", "<h3>Matchauswahl</h3>");

    var html_str = "<p>Heimteam:</p>" +
    "<select class='form-control' id='team1_selection' onchange=set_team(1)>" +
    "<option value=0 selected disabled hidden>kein Team ausgewählt</option>";

    for (var key in team_list){
        html_str += "<option value=" + key + ">" + team_list[key] + "</option>";
    }
    html_str += "</select>";
    set_innerHTML("2-col-1", html_str);
}

function result_stage_switcher_render(result){
    result_stage_switcher_designer();
    set_session_item('result', result);
    set_session_item('stage', 6);
    build_stage();
}

function result_screen_render(){
    var result = get_session_item('result');
    var team_list = get_session_item('team_list');

    var team1_name = team_list[result.home];
    var team2_name = team_list[result.guest];
    var img_team1 = result.img_home;
    var img_team2 = result.img_guest;
    var home_win = result.home_win;
    var draw = result.draw;
    var guest_win = result.guest_win;

    //TODO: Stages anpassen, damit man zu team_select_render springen kann
    set_innerHTML("left_btn", "<button class='btn btn-primary' onclick=''>anderes Match wählen</button>");
    set_innerHTML("right_btn", "<button class='btn btn-danger' onclick=reset_program()>zurück zur Startseite</button>");

    var col1_html = "<div><img src=" + img_team1 + " alt=" + team1_name + "><h3>" + team1_name + "</h3></div>" +
        "<div><p>Sieg " + team1_name + ":</p><h5>" + home_win + "</h5></div>";
    var col2_html = "<div><h2>:</h2></div>" +
        "<div><p>Unentschieden:</p><h5>" + draw + "</h5></div>";
    var col3_html = "<div><img src=" + img_team2 + " alt=" + team2_name + "><h3>" + team2_name + "</h3></div>" +
        "<div><p>Sieg " + team2_name + ":</p><h5>" + guest_win + "</h5></div>";

    set_innerHTML("1-col-1", "<h2 class='d-flex justify-content-center'>Ergebnis:</h2>");
    set_innerHTML("3-col-1", col1_html);
    set_innerHTML("3-col-2", col2_html);
    set_innerHTML("3-col-3", col3_html);
}

/**
 * DUMMYS
 * @param session
 */
function dummy_page_render(session){
    dummy_page_designer();
    window.alert("dummy_page_render()");
    //var stage = session.get_stage();

    //var sports = JSON.stringify(session.get_sports());
    //window.alert(sports)
    set_innerHTML("1-col-1", get_session_item('sport'));

    window.confirm("Set Random Variables to Stage");
    set_session_item('stage', 1);
    set_session_item('leagues', {1: "Bundesliga"});
    set_session_item('seasons', {2020: "2020/21"});
    set_session_item('team_list', {1: "Bayern", 2: "Gladbach"});
    set_session_item('selected_algo_id', 1);
    set_session_item('selected_leagues', [1]);
    set_session_item('selected_seasons', [2019, 2020]);
    set_session_item('team1_id', 1);
    set_session_item('team2_id', 2);
    set_session_item('team1_name', "Bayern");
    set_session_item('team2_name', "Gladbach");
    session.update_session_from_storage();
}

function display_storage_and_session(session){

    var sport = get_session_item('sport');
    var stage = get_session_item('stage');
    var leagues = get_session_item('leagues');
    var seasons = get_session_item('seasons');
    var team_list = get_session_item('team_list');
    var selected_algo_id = get_session_item('selected_algo_id');
    var selected_leagues = get_session_item('selected_leagues');
    var selected_seasons = get_session_item('selected_seasons');
    var team1_id = get_session_item('team1_id');
    var team2_id = get_session_item('team2_id');
    var team1_name = get_session_item('team1_name');
    var team2_name = get_session_item('team2_name');

    var html_arr = [sport, stage, leagues, seasons, team_list, selected_algo_id, selected_leagues, selected_seasons, team1_id, team2_id, team1_name, team2_name];

    var html_stor = "<h3>Storage Data</h3>" +
        "<ul>";

    for (var x in html_arr){
        html_stor += "<li>" + typeof html_arr[x] + "</li>";
    }
    html_stor += "</ul>";
    set_innerHTML('2-col-1', html_stor);

    html_arr = session.return_all_values();

    html_stor = "<h3>Session Data</h3>" +
        "<ul>";

    for (var x in html_arr){
        html_stor += "<li>" + typeof html_arr[x] + "</li>";
    }
    html_stor += "</ul>";
    set_innerHTML('2-col-2', html_stor);
}