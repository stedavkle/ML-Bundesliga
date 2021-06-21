// TODO: evtl Sports in Core schieben?
class Sports {
    sports = {
        1: 'Fussball Deutschland'
    };
}

/*
class Models {
    models = {
        1: {'model_id': 1,
            'model': 'trivialer Algorithmus',
            'description': 'Einfacher Algorithmus, der Ergebnisse aller bisherigen Partieen zweier Teams vergleicht.',
            'training': false
        },
        2: {'model_id': 2,
            'model': 'dummy Model',
            'description': 'ML Model DUMMY',
            'training': true
        }
    };
}*/

/**
 * set inital states of session storage
 * @param sport - selected database id
 */
function open_session(sport){
    set_session_item('sport', sport);
    set_session_item('stage', 0);
    set_session_item('leagues', {});
    set_session_item('seasons', {});
    set_session_item('leagues_seasons_from_crawler',{});
    set_session_item('team_list',{});
    set_session_item('selected_model_id', 0);
    set_session_item('models', {});
    set_session_item('selected_leagues', []);
    set_session_item('selected_seasons', []);
    set_session_item('selected_parameters', {});
    set_session_item('max_matchday_count', 0);
    set_session_item('first_matchday', 0);
    set_session_item('last_matchday', 0);
    set_session_item('selected_matchdays', [])
    set_session_item('team1_id', 0);
    set_session_item('team2_id', 0);
    set_session_item('team1_name', "");
    set_session_item('team2_name', "");
    set_session_item('result', {});
}

/**
 * opens session
 */
function create_session(){
    var sport_selection = get_single_selected("sport_selection");
    open_session(sport_selection);
    //window.alert("create_session(): successful");

    spinner_on();
    build_stage();
}


/**
 * adds entry to session storage
 * @param key - id
 * @param item - value
 */
function set_session_item(key, item){
    window.sessionStorage.setItem(key, JSON.stringify(item));
}


/**
 * gets session storage entry
 * @param key - id
 * @returns {any}
 */
function get_session_item(key){
    return JSON.parse(window.sessionStorage.getItem(key));
}


/**
 * resets stage to given id
 * @param id - stage
 */
function reset_stage_to(id){
    if (id == -1){
        close_session();
        on_page_load();
    }
    else {
        if (id == 3){
            set_session_item('team1_id', 0);
            set_session_item('team2_id', 0);
        }
        set_session_item('stage', id);
        build_stage();
    }
}


/**
 * clears session storage
 */
function close_session(){
    window.sessionStorage.clear();
}