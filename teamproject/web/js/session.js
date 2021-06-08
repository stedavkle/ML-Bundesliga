// TODO: evtl Sports und Models in Core schieben?
class Sports {
    sports = {
        1: 'Fussball Deutschland'
    };
}

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
}

function open_session(sport){
    set_session_item('sport', sport);
    set_session_item('stage', 0);
    set_session_item('leagues', {});
    set_session_item('seasons', {});
    set_session_item('leagues_seasons_from_crawler',{});
    set_session_item('team_list',{});
    set_session_item('selected_model_id', 0);
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

function create_session(){
    var sport_selection = get_single_selected("sport_selection");
    open_session(sport_selection);
    //window.alert("create_session(): successful");
    build_stage();
}

function set_session_item(key, item){
    window.sessionStorage.setItem(key, JSON.stringify(item));
}

function get_session_item(key){
    return JSON.parse(window.sessionStorage.getItem(key));
}

function close_session(){
    window.sessionStorage.clear();
}