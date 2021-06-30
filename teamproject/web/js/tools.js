// --------------------------------- DOM manipulation functions ---------------------------------

/**
 * sets string into html element
 * @param id - id of html element
 * @param text - content
 */
function set_innerHTML(id, text){
    document.getElementById(id).innerHTML = text;
}


/**
 * displays back button
 * @param id - stage to set
 */
function set_back_button(id){
  var button = "<button class=\'btn btn-outline-danger btn-sm\' onclick=\"reset_stage_to(" + id + ")\">zurück</button>"
  set_innerHTML("back_btn", button);
}

function display(id){
  document.getElementById(id).style.visibility = 'visible';
}


/**
 * hides html element
 * @param id - id of html element
 */
function hide(id){
  document.getElementById(id).style.visibility = 'hidden';
}


/**
 * hides html element and resets content
 * @param id - id of html element
 */
function hide_and_reset(id){
  document.getElementById(id).style.visibility = 'hidden';
  document.getElementById(id).innerHTML = '';
}


/**
 * removes html element from DOM
 * @param id - id of html element
 */
function display_none(id){
  var selected = document.getElementById(id);
  selected.style.display = 'none';
  selected.style.position = 'absolute';
}


/**
 * inserts html element to DOM
 * @param id - id of html element
 */
function display_block(id){
  var selected = document.getElementById(id);
  selected.style.display = 'block';
  selected.style.position = 'static';
}


/**
 * returns value of selected element of html select
 * @param id - id of html select
 * @returns {*}
 */
function get_single_selected(id){
  return document.getElementById(id).value;
}


/**
 * returns values of selected elements of html multiple select as an array
 * @param id - id of html select
 * @returns {*[]} - array
 */
function get_mult_selected(id){
  //window.alert("get_mult_selected(): entered");
  var selector = document.getElementById(id);
  var options = selector && selector.options;
  var selected_array = [];

  for (var i = 0; i < options.length; i++){
    if (options[i].selected){
      selected_array.push(options[i].value);
    }
  }
  return selected_array;
}



// --------------------------------- special display functions ---------------------------------
/**
 * shows data submit, if leagues AND seasons are selected
 */
function show_data_submit(){
  //window.alert("show_data_submit(): entered");
  unselect_checkbox('leagues_selection', 'check_leagues_1');
  unselect_checkbox('seasons_selection', 'check_seasons_1');
  if (!(get_mult_selected('leagues_selection') == 0 || get_mult_selected('seasons_selection') == 0)){
    display('right_btn');
  }
}


/**
 * displays description text for models
 */
function show_model_description(){
  //window.alert("show_model_description(): entered");
  display('right_btn');
  display('2-col-2');
  var models = get_session_item('models');
  var id = get_single_selected('model_selection');
  var description = "<p>" + models[id].description + "</p>";
  set_innerHTML('2-col-2', description);
}


/**
 * grid for result screen, containing team icons and names
 * will be placed in '1-col-1' div
 * @param home_id - id of team 1
 * @param home - name of team 1
 * @param guest_id - id of team 2
 * @param guest - name of team 2
 */
function display_result_icons(home_id, home, guest_id, guest){
  var html_str = "<div class=\'result-container\'>" +
      "<img class=\'result-element, result-img\' src=\'img/" + home_id + ".png\' onerror=\"this.onerror=null; this.src=\'img/no_icon.png\'\">" +
      "<img class=\'result-element, result-img\' src=\'img/colon.png\'>" +
      "<img class=\'result-element, result-img\' src=\'img/" + guest_id + ".png\' onerror=\"this.onerror=null; this.src=\'img/no_icon.png\'\">" +
      "<div class=\'result-element\'><h4>" + home + "</h4></div>" +
      "<div class=\'result-element\'></div>" +
      "<div class=\'result-element\'><h4>" + guest + "</h4></div></div>";
  set_innerHTML('1-col-1', html_str);
}


/**
 * probable outcome displayed in a table
 * @param outcome - object of win probabilities
 * @param home - home team name
 * @param guest - guest team name
 */
function display_outcome(outcome, home, guest){
  var propability_table = "<h4>Ergebniswahrscheinlichkeit</h4>" +
      "<table class=\'table\'>" +
        "<thead class=\'thead-dark\'><tr>" +
        "<th style=\'width: 33.3%\'><span class=\'font-weight-normal\'>Sieg</span> " + home + "</th>" +
        "<th style=\'width: 33.3%\'><span class=\'font-weight-normal\'>Unentschieden</span></th>" +
        "<th style=\'width: 33.3%\'><span class=\'font-weight-normal\'>Sieg</span> " + guest + "</th></tr></thead>" +
        "<tbody><tr>" +
        "<th style=\'width: 33.3%\'>" + outcome.home_win + "</th>" +
        "<th style=\'width: 33.3%\'>" + outcome.draw + "</th>" +
        "<th style=\'width: 33.3%\'>" + outcome.guest_win + "</th></tr></tbody></table>";
  set_innerHTML("5-col-1", propability_table);
}


/**
 * if scores exist, function displays possible scores with probability
 * @param score - object with scores
 * @param home - name of home team
 * @param guest - name of guest team
 */
function display_score(score, home, guest){
  var NO_SCORE = 0;
  if (score == NO_SCORE){
    hide('6-col-1');
  }
  else {
      var scores = "<h4>wahrscheinliche Endergebnisse</h4>" +
        "<table class=\'table\'>" +
        "<thead class=\'thead-dark\'><tr>" +
        "<th style=\'width: 33.3%\'><span class=\'font-weight-normal\'>Wahrscheinlichkeit</span></th>" +
        "<th style=\'width: 33.3%\'><span class=\'font-weight-normal\'>Tore</span> " + home + "</th>" +
        "<th style=\'width: 33.3%\'><span class=\'font-weight-normal\'>Tore</span> " + guest + "</th>" +
        "</tr></thead><tbody>";

      for (var key in score){
        scores += "<tr><th style=\'width: 33.3%\'>" + score[key].probability + "</th>" +
            "<th style=\'width: 33.3%\'>" + scor[key].home_points + "</th>" +
            "<th style=\'width: 33.3%\'>" + scor[key].guest_points + "</th></tr>";
      }
      scores += "</tbody></table>";
      set_innerHTML('6-col-1', scores);
      display('6-col-1');
  }

}

// --------------------------------- tool-functions ---------------------------------
/**
 * stores selected data to session storage,
 * calls build_stage() after setting stage to 1
 */
function store_crawler_parameter(){
  //window.confirm("store_crawler_parameter(): entered")
  var selected_leagues = get_mult_selected('leagues_selection');
  var possible_leagues = get_session_item('leagues_seasons_from_crawler');

  set_session_item('selected_leagues', selected_leagues);
  set_session_item('selected_seasons', get_mult_selected('seasons_selection'));
  var max_matchdays = 0;

  for (var key in selected_leagues){
    if (possible_leagues[selected_leagues[key]].matchdays > max_matchdays){
      max_matchdays = possible_leagues[selected_leagues[key]].matchdays;
    }
  }
  set_session_item('max_matchday_count', max_matchdays);

  set_session_item('stage', 1);
  spinner_on();
  build_stage();
}


/**
 * stores selected model_id to session storage,
 * calls build_stage() after setting stage to 2
 */
function set_model(){
  //window.alert("set_model(): entered");
  //var model = get_session_item('models');
  var selected_model_id = get_single_selected('model_selection');
  set_session_item('selected_model_id', selected_model_id);
  set_session_item('stage', 2);
  spinner_on();
  build_stage();
}


/**
 * generates html multiple select based on selected data
 * @param id - string of part of html select id
 * @returns {string} - html select as string
 */
function create_select_of_selected(id){
  var possible_data = get_session_item(id);
  var selected_data = get_session_item("selected_" + id);
  var html_str = "<select multiple class=\'form-control\' id=\'" + id + "_fine_selection\' onchange=\"unselect_checkbox(\'" + id + "_fine_selection\', \'check_" + id + "_2\')\">";

  for (var i = 0; i < selected_data.length; i++){
    html_str += "<option value=" + selected_data[i] + ">" + possible_data[selected_data[i]] + "</option>";
  }

  html_str += "</select>";

  var html_str_check = "<div class=\'form-check\'>" +
      "<input type=\'checkbox\' class=\'form-check-input\' id=\'check_" + id + "_2\' onclick=\"multiple_select_all(\'" + id + "_fine_selection\', \'check_" + id + "_2\')\">" +
      "<label class=\'form-check-label\'>alles auswählen</label></div>"

  return html_str + html_str_check;
}


/**
 * generates html select of matchdays
 * @param id - string: first or last
 * @returns {string} - html select as string
 */
function create_matchday_selection(id){
  //window.alert("create_matchday_selection(): entered");
  var html_str = "<select class=\'form-control\' id=\'" + id + "_matchday\'>";
  var max_matchdays = get_session_item('max_matchday_count');

  if (id === 'first'){
    html_str += "<option value=1 selected>1</option>";
  }
  else {
    html_str += "<option value=1>1</option>";
  }

  for (var i = 2; i < max_matchdays; i++){
    html_str += "<option value=" + i + ">" + i + "</option>";
  }

  if (id === 'last'){
    html_str += "<option value=" + max_matchdays + " selected>" + max_matchdays + "</option>";
  }
  else {
    html_str += "<option value=" + max_matchdays + ">" + max_matchdays + "</option>";
  }
  html_str += "</select>";
  return html_str;
}


/**
 * writes selected data parameters to an object
 * @param stage - number of next stage
 */
function store_selected_parameter(){
  var selected_leagues = get_mult_selected('leagues_fine_selection');
  var selected_seasons = get_mult_selected('seasons_fine_selection');
  var first_matchday = parseInt(get_single_selected('first_matchday'));
  var last_matchday = parseInt(get_single_selected('last_matchday'));
  var points_checked = 0;

  // spinner at button position
  var spinner = "<button class=\'btn btn-danger\' disabled>" +
      "<span class=\'spinner-border spinner-border-sm\'></span>\tTraining</button>";
  set_innerHTML('right_btn', spinner);

  if (selected_seasons.length == 1 && first_matchday > last_matchday)
  {
    //window.alert("FEHLER: erster Spieltag liegt nach dem letzten Spieltag!")
    create_alert("Erster Spieltag liegt nach dem letzten Spieltag!");
  }
  else {
    if (selected_leagues.length == 0 || selected_seasons.length == 0){
      create_alert("Es muss mindestens eine Liga und Saison ausgewählt sein!");
    }
    else{
      clear_alert();
      if (document.getElementById('points_checkbox').checked){
        points_checked = 1;
      };

      var selected_parameters = {
        'leagues': selected_leagues,
        'seasons': selected_seasons,
        'first_matchday': first_matchday,
        'last_matchday': last_matchday,
        'points': points_checked
      };

      set_session_item('selected_parameters', selected_parameters);
      set_session_item('stage', 3);
      spinner_on();
      build_stage();
    }
  }
}


/**
 * writes team id to session storage
 * according to input, switch and submit buttons will be displayed
 * @param sel - number of html select (1 = team1, 2 = team2)
 */
function set_team(sel){
  //window.alert("set_team(): entered");
  var selector_id = "team" + sel + "_selection";
  var selector = document.getElementById(selector_id);
  var team_list = get_session_item('team_list');

  if (selector_id === "team1_selection"){
    set_session_item('team1_id', selector.value);
    set_session_item('team1_name', team_list[selector.value]);

    if (get_session_item('team2_id') === 0){
      set_innerHTML("left_btn", "<button class=\'btn btn-primary\' onclick=\"eel.get_next_opponent("+ selector.value +")(show_next_opponent)\">nächster Gegner</button>");
      set_innerHTML("right_btn", "<button class=\'btn btn-primary\' onclick=\"set_opponent()\">Gegner wählen</button>");
      display("left_btn");
      display("right_btn");
    }
  }
  else {
    set_session_item('team2_id', selector.value);
    set_session_item('team2_name', team_list[selector.value]);
  }
}


/**
 * displays next opponent
 * @param team2_id - id of team 2
 */
function show_next_opponent(team2_id){
  var team_list = get_session_item('team_list');
  set_session_item('team2_id', team2_id);
  set_session_item('team2_name', team_list[team2_id]);
  set_innerHTML("2-col-2", "<h3>nächster Gegner:</h3><h4>" + team_list[team2_id] + "</h4>");
  display('2-col-2');
  set_innerHTML("left_btn","<button class=\'btn btn-primary\' onclick=\"set_opponent()\">Gegner wählen</button>");
  set_innerHTML("right_btn", "<button class=\'btn btn-danger\' onclick=\"start_prediction()\">Vorhersage starten</button>");
}


/**
 * generates html select of teams
 */
function set_opponent(){
  var team_list = get_session_item('team_list');

  var html_str = "<h5>Gastteam:</h5>" +
    "<select class=\'form-control\' id=\'team2_selection\' onchange=\"set_team(2)\">" +
    "<option value=0 selected disabled hidden>kein Team ausgewählt</option>";

  for (var key in team_list){
    html_str += "<option value=" + key + ">" + team_list[key] + "</option>";
  }
  html_str += "</select>";

  set_innerHTML("2-col-2", html_str);
  display('2-col-2');
  var team1_id = get_session_item('team1_id');
  set_innerHTML("left_btn","<button class=\'btn btn-primary\' onclick=\"eel.get_next_opponent("+ team1_id +")(show_next_opponent)\">nächster Gegner</button>");
  set_innerHTML("right_btn", "<button class=\'btn btn-danger\' onclick=\"start_prediction()\">Vorhersage starten</button>");
}


/**
 * checks if teams are selected and not the same
 * sets state to 5 and calls build_stage
 */
function start_prediction(){
  var team1_id = get_session_item('team1_id');
  var team2_id = get_session_item('team2_id');

  if (team1_id == team2_id){
    //window.alert("start_prediction(): ERROR - Heim- und Auswärtsteam sind gleich!");
    create_alert("Heim- und Auswärtsteam sind gleich!");
  }
  else if (team1_id == 0 || team2_id == 0){
    //window.alert("start_prediction(): ERROR - Ein Team ist nicht ausgewählt!");
    create_alert("Ein Team ist nicht ausgewählt!");
  }
  else {
    clear_alert();
    set_session_item('stage', 6);
    spinner_on();
    build_stage();
  }
}


/**
 * unselects a checkbox when element of select is deselected
 * @param sel_id - id of select element
 * @param check_id - id of checkbox
 */
function unselect_checkbox(sel_id, check_id){
    var sel = document.getElementById(sel_id);
	for (var i = 0; i < sel.options.length; i++){
		if (sel.options[i].selected == false){
			var check = document.getElementById(check_id);
			check.checked = false;
		}
	}
}


/**
 * selects all elements of multiple select, if checkbox is clicked
 * @param sel_id - id of select element
 * @param check_id - id of checkbox
 */
function multiple_select_all(sel_id, check_id){
    //window.alert("multiple_select_all(): executed");
    var check = document.getElementById(check_id);
	var sel = document.getElementById(sel_id);
	if (check.checked){
		for (var i = 0; i < sel.options.length; i++){
			sel.options[i].selected = true;
		}
	}
}

