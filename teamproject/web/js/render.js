/*
    Displays Page Content
 */
/**
 * creates layout of sport selection page
 * creates dropdown based on global sports content
 */
function sport_selection_render(){
    sport_selection_designer();
    set_innerHTML("right_btn", "<button class=\'btn btn-danger\' onclick=\"create_session()\">Bestätigen</button>");
    var html_str = "<h3>Willkommen!</h3>" +
    "<p>Wähle eine Sportart:</p>" +
    "<select class=\'form-control\' id=\'sport_selection\' onchange=\"display(\'right_btn\')\">" +
    "<option value=0 selected disabled hidden>nichts ausgewählt</option>";

    var sports = new Sports();

    for (var key in sports.sports){
        html_str += "<option value=" + key + ">" + sports.sports[key] + "</option>";
    }
    html_str += "</select>";

    // maintenance
    var html_btn = "<button onclick=\'maintenence_stage()\'>zur Stage</button>";
    html_str += html_btn;

    set_innerHTML("1-col-1", html_str);
}


/**
 * creates selection page for data, broadcasted by selected database
 * @param leagues_seasons - dictionary of leagues
 *
 */
function crawler_data_render(leagues_seasons){
    crawler_data_designer();
    set_back_button(-1);
    //set_innerHTML("back_btn", "<button class='btn btn-outline-danger btn-sm' onclick='welcome_page()'>zurück</button>");
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
    var html_str_hint = "<p>Für Mehrfachauswahl <kbd>Strg</kbd> bzw. <kbd>Umschalt</kbd> gedrückt halten.</p>";
    set_innerHTML('1-col-1', html_str_hint);

    // define submit button
    set_innerHTML('right_btn', "<button class=\'btn btn-danger\' onclick=\"store_crawler_parameter()\">Daten beziehen</button>");

    // display league selection
    var html_str_left = "<h5>Ligen:</h5>" +
        "<select multiple class=\'form-control\' id=\'leagues_selection\' onchange=\"show_data_submit()\">";

    for (var key in leagues){
        html_str_left += "<option value=" + key + ">" + leagues[key] + "</option>";
    }
    html_str_left += "</select>";

    var html_str_left_check = "<div class=\'form-check\'>" +
        "<input type=\'checkbox\' class=\'form-check-input\' id=\'check_leagues_1\' onclick=\"multiple_select_all(\'leagues_selection\', \'check_leagues_1\'), show_data_submit()\">" +
        "<label class=\'form-check-label\'>alles auswählen</label></div>";

    html_str_left += html_str_left_check;

    set_innerHTML("2-col-1", html_str_left);

    // display season selection
    var html_str_right = "<h5>Saisons:</h5>" +
        "<select multiple class=\'form-control\' id=\'seasons_selection\' onchange=\"show_data_submit()\">";

    for (var key in seasons){
        html_str_right += "<option value=" + key + ">" + seasons[key] + "</option>";
    }
    html_str_right += "</select>";

    var html_str_right_check = "<div class=\'form-check\'>" +
        "<input type=\'checkbox\' class=\'form-check-input\' id=\'check_seasons_1\' onclick=\"multiple_select_all(\'seasons_selection\', \'check_seasons_1\'), show_data_submit()\">" +
        "<label class=\'form-check-label\'>alles auswählen</label></div>";

    html_str_right += html_str_right_check;

    set_innerHTML("2-col-2", html_str_right);
}


/**
 * displays model selection
 * @param models - dictionary with available models
 */
function model_selection_render(models){
    model_selection_designer();
    //window.alert("model_selection_render(): entered");
    set_back_button(0);
    set_session_item('models', models);

    set_innerHTML("right_btn", "<button class=\'btn btn-danger\' onclick=\"set_model()\">Bestätigen</button>");
    set_innerHTML("1-col-1", "<h5>Wähle einen Algorithmus oder ein ML-Modell aus:</h5>");

    var html_str = "<select class=\'form-control\' id=\'model_selection\' onchange=\"show_model_description()\">" +
    "<option value=0 selected disabled hidden>nichts ausgewählt</option>";

    for (var key in models){
        html_str += "<option value=" + key + ">" + models[key]['model'] + "</option>";
    }
    html_str += "</select>";

    set_innerHTML("2-col-1", html_str);
}


/**
 * displays fine selection of data
 * @param parameter - dictionary of parameter options the model needs
 */
function training_data_render(parameter){
    training_data_designer();
    set_back_button(1);
    //var model_id = get_session_item('selected_model_id');

    set_innerHTML('right_btn', "<button class=\'btn btn-danger\' onclick=\"store_selected_parameter()\">Training starten</button>");

    var html_str_leagues = "<h5>Ligen:</h5>" + create_select_of_selected('leagues');
    var html_str_seasons = "<h5>Saisons:</h5>" + create_select_of_selected('seasons');
    var html_str_matchdays_first = "<p>ab Spieltag:</p>" + create_matchday_selection('first');
    var html_str_matchdays_last = "<p>bis einschließlich Spieltag:</p>" + create_matchday_selection('last');
    var html_str_points = "<div class=\'form-check\'>" +
        "<input type=\'checkbox\' class=\'form-check-input\' id=\'points_checkbox\'>" +
        "<label class=\'form-check-label\'>Tore berücksichtigen</label></div>";


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


/**
 * displays next matchday, waiting screen for training
 * @param next_matchday - dictionary of matches
 */
function next_matchday_render(next_matchday){
    next_matchday_designer();

    // TODO: Render Ansicht vom nächsten Spieltag
    set_innerHTML("1-col-1", "<p>Hier kommt dann die Tabelle mit dem nächsten Spieltag hin.</p>");

    set_session_item('stage', 4);
    build_stage();
}


/**
 * callback function after training is finished
 * @param team_list - dictionary of teams
 */
function team_select_callback(team_list){
    set_innerHTML('right_btn', "<button class=\'btn btn-danger\' onclick=\"team_select_render()\">Match wählen</button>");
    set_session_item('team_list', team_list);
    display('right_btn');
}

/**
 * displays team selection
 * @param team_list - dictionary of teams
 */
function team_select_render(){
    //window.alert("team_select_render(): entered");
    clear_page();
    team_select_designer();
    set_back_button(2);

    set_session_item('stage', 5);
    var team_list = get_session_item('team_list');
    set_innerHTML("1-col-1", "<h3>Matchauswahl</h3>");

    var html_str = "<h5>Heimteam:</h5>" +
    "<select class=\'form-control\' id=\'team1_selection\' onchange=\"set_team(1)\">" +
    "<option value=0 selected disabled hidden>kein Team ausgewählt</option>";

    for (var key in team_list){
        html_str += "<option value=" + key + ">" + team_list[key] + "</option>";
    }
    html_str += "</select>";
    set_innerHTML("2-col-1", html_str);
}


/**
 * bridging function to set result stage
 * @param result - result of prediction
 */
function result_stage_switcher_render(result){
    set_session_item('result', result);
    set_session_item('stage', 7);
    build_stage();
}


/**
 * displays result
 */
function result_screen_render(){
    result_stage_switcher_designer();
    var result = get_session_item('result');
    var team_list = get_session_item('team_list');

    var home_id = result.home;
    var guest_id = result.guest;
    var outcome = result.outcome;
    var score = result.score;

    var home_name = team_list[home_id];
    var guest_name = team_list[guest_id];

    //alert("result.home: " + result.home);
    //alert(typeof result.home);
    //alert("<img src=\'../icons/" + result.home + ".png\' alt=" + team1_name + ">");

    //TODO: Stages anpassen, damit man zu team_select_render springen kann
    set_innerHTML("left_btn", "<button class=\'btn btn-primary\' onclick=\"set_session_item(\'stage\', 5), build_stage()\">anderes Match wählen</button>");
    set_innerHTML("right_btn", "<button class=\'btn btn-danger\' onclick=\"reset_program()\">zurück zur Startseite</button>");

    display_result_icons(home_id, home_name, guest_id, guest_name);
    display_outcome(outcome, home_name, guest_name);
    display_score(score, home_name, guest_name);

    //set_innerHTML("1-col-1", "<h2 class=\'d-flex justify-content-center\'>Ergebnis:</h2>");
}
