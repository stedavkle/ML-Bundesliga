/**
 * initial function on page load
 *  checks if a stage object is set
 *  - if yes:   recreate stage site
 *  - if no:    show selection of sports
 *              when selection is set, create new session object
 */
function on_page_load(){
    if(get_session_item('stage') == null){
        window.confirm("keine Session gefunden");
        sport_selection_render();
    }
    else {
        window.confirm("Session gefunden");
        build_stage();
    }
}

/**
 * triggers stage render function
 *
 */
function build_stage(){
    var stage = get_session_item('stage');
    var sport = get_session_item('sport');
    var model_id = get_session_item('selected_model_id');
    window.confirm("build_stage(): stage = " + stage);
    switch(stage){
        case 0:
            // selection of crawler data
            eel.get_crawler_data(sport)(crawler_data_render);
            break;
        case 1:
            // start crawler, get selection of models
            var leagues = get_session_item('selected_leagues');
            var seasons = get_session_item('selected_seasons');
            eel.start_crawler_get_models(leagues, seasons)(model_selection_render);
            break;
        case 2:
            // get training data from crawler, according to selected model
            clear_page();
            eel.get_required_model_data(model_id)(training_data_render);
            break;
        case 3:
            // send selected parameters to core, get matches of next matchday
            var algo_data_parameter = get_session_item('selected_parameters');
            eel.get_next_matchday_from_parameters(algo_data_parameter)(next_matchday_render);
            break;
        case 4:
            // TODO: send Trainingdata, training progress, get matches
            //var model_data_parameter = get_session_item('selected_parameters');
            //progress_spinner_render();
            eel.start_training_and_get_teams()(team_select_callback);
            break;
        case 5:
            // TODO: start prediction
            var team1_id = get_session_item('team1_id');
            var team2_id = get_session_item('team2_id');
            eel.start_prediction(team1_id, team2_id)(result_stage_switcher_render);
            break;
        case 6:
            // TODO: result
            result_screen_render();
            break;
        default:
            window.alert("build_stage(): no case selected!")
    }
}

// TODO: Oder zur Crawler Daten Auswahl zurück springen???
/**
 * set program back to initial state
 */
function reset_program(){
    clear_page();
    close_session();
    on_page_load();
}