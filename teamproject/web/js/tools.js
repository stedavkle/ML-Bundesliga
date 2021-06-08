// -------------------- display and hide functions concerning ids in index.html ---------

function set_innerHTML(id, text){
    document.getElementById(id).innerHTML = text;
}

function set_innerText(id, text){
    document.getElementById(id).innerText = text;
}

function set_back_button(fun){
  var button = "<button class='btn btn-danger' onclick='" + fun + "'>Bestätigen</button>"
  set_innerHTML("back_btn", button);
}

function display(id){
  document.getElementById(id).style.visibility = 'visible';
}

function hide(id){
  document.getElementById(id).style.visibility = 'hidden';
}

function hide_and_reset(id){
  document.getElementById(id).style.visibility = 'hidden';
  document.getElementById(id).innerHTML = '';
}

function get_single_selected(id){
  return document.getElementById(id).value;
}

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



// ------- special display functions

function show_data_submit(){
  //window.alert("show_data_submit(): entered");
  if (!(get_mult_selected('leagues_selection') == 0 || get_mult_selected('seasons_selection') == 0)){
    display('right_btn');
  }
}

function show_model_description(){
  //window.alert("show_model_description(): entered");
  display('right_btn');
  display('2-col-2');
  var model = new Models();
  var id = get_single_selected('model_selection');
  var description = "<p>" + model.models[id].description + "</p>";
  set_innerHTML('2-col-2', description);
}



// tool-functions
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
  build_stage();
}

function set_model(){
  //window.alert("set_model(): entered");
  var model = get_session_item('models');
  var selected_model_id = get_single_selected('model_selection');
  set_session_item('selected_model_id', selected_model_id);
  set_session_item('training', model[selected_model_id].training);
  set_session_item('stage', 2);
  build_stage();
}

function create_select_of_selected(id){
  var possible_data = get_session_item(id);
  var selected_data = get_session_item("selected_" + id);
  var html_str = "<select multiple class='form-control' id='" + id + "_fine_selection'>" +
        "<option value=0 selected disabled hidden>nichts ausgewählt</option>";

  for (var i = 0; i < selected_data.length; i++){
    html_str += "<option value=" + selected_data[i] + ">" + possible_data[selected_data[i]] + "</option>";
  }

  html_str += "</select>";
  return html_str;
}

function create_matchday_selection(id){
  //window.alert("create_matchday_selection(): entered");
  var html_str = "<select class='form-control' id='" + id + "_matchday'>";
  var max_matchdays = get_session_item('max_matchday_count');

  if (id === 'first'){
    html_str += "<option value='1' selected>1</option>";
  }
  else {
    html_str += "<option value='1'>1</option>";
  }

  for (var i = 2; i < max_matchdays; i++){
    html_str += "<option value='" + i + "'>" + i + "</option>";
  }

  if (id === 'last'){
    html_str += "<option value='" + max_matchdays + "' selected>" + max_matchdays + "</option>";
  }
  else {
    html_str += "<option value='" + max_matchdays + "'>" + max_matchdays + "</option>";
  }
  html_str += "</select>";
  return html_str;
}

function store_selected_parameter(stage){
  // TODO: Abfangen, dass bei einer gewählten Saison first_matchday <= last_matchday
  var selected_leagues = get_mult_selected('leagues_fine_selection');
  var selected_seasons = get_mult_selected('seasons_fine_selection');
  var first_matchday = get_single_selected('first_matchday');
  var last_matchday = get_single_selected('last_matchday');
  var points_checked = 0;

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
  set_session_item('stage', stage);
  build_stage();
}

function set_team(sel){
  //window.alert("set_team(): entered");
  var selector_id = "team" + sel + "_selection";
  var selector = document.getElementById(selector_id);
  var team_list = get_session_item('team_list');

  if (selector_id === "team1_selection"){
    set_session_item('team1_id', selector.value);
    set_session_item('team1_name', team_list[selector.value]);

    if (get_session_item('team2_id') === 0){
      set_innerHTML("left_btn", "<button class='btn btn-primary' onclick=eel.get_next_opponent("+ selector.value +")(show_next_opponent)>nächster Gegner</button>");
      set_innerHTML("right_btn", "<button class='btn btn-primary' onclick=set_opponent()>Gegner wählen</button>");
      display("left_btn");
      display("right_btn");
    }
  }
  else {
    set_session_item('team2_id', selector.value);
    set_session_item('team2_name', team_list[selector.value]);
  }
}

function show_next_opponent(team2_id){
  var team_list = get_session_item('team_list');
  set_session_item('team2_id', team2_id);
  set_session_item('team2_name', team_list[team2_id]);
  set_innerHTML("2-col-2", "<h3>nächster Gegner:</h3><h4>" + team_list[team2_id] + "</h4>");
  display('2-col-2');
  set_innerHTML("left_btn","<button class='btn btn-primary' onclick=set_opponent()>Gegner wählen</button>");
  set_innerHTML("right_btn", "<button class='btn btn-danger' onclick=start_prediction()>Vorhersage starten</button>");
}

function set_opponent(){
  var team_list = get_session_item('team_list');

  var html_str = "<p>Gastteam:</p>" +
    "<select class='form-control' id='team2_selection' onchange=set_team(2)>" +
    "<option value=0 selected disabled hidden>kein Team ausgewählt</option>";

  for (var key in team_list){
    html_str += "<option value=" + key + ">" + team_list[key] + "</option>";
  }
  html_str += "</select>";

  set_innerHTML("2-col-2", html_str);
  display('2-col-2');
  var team1_id = get_session_item('team1_id');
  set_innerHTML("left_btn","<button class='btn btn-primary' onclick=eel.get_next_opponent("+ team1_id +")(show_next_opponent)>nächster Gegner</button>");
  set_innerHTML("right_btn", "<button class='btn btn-danger' onclick=start_prediction()>Vorhersage starten</button>");
}

function start_prediction(){
  var team1_id = get_session_item('team1_id');
  var team2_id = get_session_item('team2_id');

  if (team1_id == team2_id){
    window.alert("start_prediction(): ERROR - Heim- und Auswärtsteam sind gleich!");
  }
  else if (team1_id == 0 || team2_id == 0){
    window.alert("start_prediction(): ERROR - Ein Team ist nicht ausgewählt!");
  }
  else {
    set_session_item('stage', 5);
    build_stage();
  }
}


