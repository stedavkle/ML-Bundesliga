/**
 * initial function on page load
 *  checks if a stage object is set
 *  - if yes:   recreate stage site
 *  - if no:    show selection of sports
 *              when selection is set, create new session object
 */
function on_page_load(){
    if(get_session_item('stage') == null){
        eel.get_sport_selection()(sport_selection_render);
    }
    else {
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
    //window.confirm("build_stage(): stage = " + stage);
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
            // displays next matchday and calls core.py to start training and get teams
            next_matchday_designer();
            spinner_button();
            var final_leagues = get_session_item('final_leagues');
            display_league_pagination();
            next_matchday_table(final_leagues[0]);
            eel.start_training_and_get_teams()(team_select_callback);
            break;
        case 5:
            // return to match selection after result displayed
            set_session_item('team1_id', 0);
            set_session_item('team2_id', 0);
            team_select_render();
            break;
        case 6:
            // calls core.py to start prediction
            var team1_id = get_session_item('team1_id');
            var team2_id = get_session_item('team2_id');
            eel.start_prediction(team1_id, team2_id)(result_stage_switcher_render);
            break;
        case 7:
            // calls render function to display result
            result_screen_render();
            break;
        case 8:
            // TODO: Special Feature: predict whole matchday
            alert("Stage 8 erreicht");
            spinner_on();
            var league = get_session_item('next_matchday_league');
            eel.predict_next_matchday(league)(next_matchday_prediction_render)
            break;
        default:
            window.alert("build_stage(): no case selected!")
    }
}


/**
 * set program back to initial state
 */
function reset_program(){
    clear_page();
    close_session();
    on_page_load();
}