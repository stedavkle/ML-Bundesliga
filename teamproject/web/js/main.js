// -------------------- global variables ------------------------------------------------------------

// TODO: edit new algorithms or ml-models here!
var algorithms =    {
                        1: 'trivialer Algorithmus'
                    };

// just for testing:
var seasons = [1990];
var leagues = {
                1: 'Bundesliga',
                2: '2. Bundesliga',
                3: '3. Liga'
            };
/*var clubs = {   19: "Bayern München",
            93: "VfB Stuttgart",
            17: "Borussia M'Gladbach",
            100: "RB Leipzig",
            9: "Borussia Dortmund",
            1: "VfL Wolfsburg",
            24: "Werder Bremen",
            7: "SC Freiburg",
            8: "FC Augsburg",
            42: "Arminia Bielefeld",
            2: "1. FC Heidenheim"};*/

// globals
var team_list = "";
var selected_algo_id;
var selected_algo_data;
var selected_league;
var selected_seasons;
var team1;
var team1_id = 0;
var team2;
var team2_id = 0;


// -------------------- welcome page functions ------------------------------------------------------------

function welcome_page(){
  welcome_page_designer();
  var html_str = "<h3>Willkommen!</h3>" +
    "<p>Wähle einen Algorithmus oder ein ML-Modell aus:</p>" +
    "<select id='algo_selection' onchange='show_select_algo_submit()'>" +
    "<option value='0' selected disabled hidden>nichts ausgewählt</option>";

  for (var key in algorithms){
    html_str += "<option value='" + key + "'>" + algorithms[key] + "</option>";
  }
  html_str += "</select>";

  set_innerHTML("1-col-1", html_str);
  set_innerHTML("right_btn", "<button class='btn btn-danger' onclick='select_data()'>Bestätigen</button>");
  hide("back_btn");
}


function select_data(){
  select_data_designer();
  set_innerHTML("back_btn", "<button class='btn btn-outline-danger btn-sm' onclick='welcome_page()'>zurück</button>");
  set_innerHTML("1-col-1", "<h3>Bestimme abzurufende Daten:</h3>");

  var html_str_left = "<p>Liga:</p>" +
    "<select id='league_selection' onchange='set_league()'>" +
    "<option value='0' selected disabled hidden>nichts ausgewählt</option>";

  for (var key in leagues){
    html_str_left += "<option value='" + key + "'>" + leagues[key] + "</option>";
  }
  html_str_left += "</select>";

  set_innerHTML("2-col-1", html_str_left);

  // TODO: Season Auswahl

  // dummy Selection
  var html_str_right = "<p>Saisons:</p>" +
    "<select id='seasons_selection' onchange='set_seasons()'>" +
    "<option value='0' selected disabled hidden>nichts ausgewählt</option>";

  /*
  for (var key in leagues){
    html_str_right += "<option value='" + key + "'>" + seasons[key] + "</option>";
  }*/
  html_str_right += "<option value='2020'>2020/21</option>";
  html_str_right += "</select>";

  set_innerHTML("2-col-2", html_str_right);
}



function set_league(){
  selected_league = document.getElementById("league_selection").value;
}

function set_seasons(){
  selected_seasons = document.getElementById("seasons_selection").value;

  if (selected_seasons != 0 && selected_league != 0){
    set_innerHTML("right_btn", "<button class='btn btn-danger' onclick='start_crawler()'>Daten beziehen</button>");
    display("right_btn");
  }
}

function start_crawler(){
  eel.start_crawler()(callback_start_crawler);
}

function callback_start_crawler(){
  // TODO: Trainingsanzeige in Abhängigkeit vom Algorithmus
  get_clubs();
}

function get_clubs(){
  get_clubs_designer();
  set_innerHTML("1-col-1", "<h3>Matchauswahl</h3>");
  display("2-col-1");
  // TODO: back Button evtl anpassen
  set_innerHTML("back_btn", "<button class='btn btn-outline-danger btn-sm' onclick='select_data()'>zurück</button>");

  eel.get_clubs(selected_league)(callback_select_clubs);
}

function callback_select_clubs(clubs){
  team_list = clubs;

  var html_str = "<p>Heimteam:</p>" +
    "<select id='sel1' onchange='set_team(1)'>" +
    "<option value='0' selected disabled hidden>kein Team ausgewählt</option>";

    for (var key in team_list){
        html_str += "<option value='" + key + "'>" + team_list[key] + "</option>";
    }
    html_str += "</select>";
    set_innerHTML("2-col-1", html_str);
}

function get_next_opponent(){
  display("2-col-2");
  // TODO: nächsten Gegner ermitteln
  team2 = team1;
  team2_id = team1_id;
  set_innerHTML("2-col-2", "<h4>ein Verein</h4>");
  set_innerHTML("left_btn","<button class='btn btn-primary' onclick='set_opponent()'>Gegner wählen</button>");
  set_innerHTML("right_btn", "<button class='btn btn-danger' onclick='start_prediction()'>Vorhersage starten</button>");
}

function set_opponent(){
  display("2-col-2");

  var html_str = "<p>Gastteam:</p>" +
    "<select id='sel2' onchange='set_team(2)'>" +
    "<option value='0' selected disabled hidden>kein Team ausgewählt</option>";

  for (var key in team_list){
    html_str += "<option value='" + key + "'>" + team_list[key] + "</option>";
  }
  html_str += "</select>";

  set_innerHTML("2-col-2", html_str);
  set_innerHTML("left_btn","<button class='btn btn-primary' onclick='get_next_opponent()'>nächster Gegner</button>");
  set_innerHTML("right_btn", "<button class='btn btn-danger' onclick='start_prediction()'>Vorhersage starten</button>");
}

function set_team(sel){
  var sel = "sel" + sel;
  var selector = document.getElementById(sel);

  if (sel == "sel1"){
    team1_id = selector.value;
    team1 = team_list[team1_id];

    if (team2_id == 0){
      set_innerHTML("left_btn", "<button class='btn btn-primary' onclick='get_next_opponent()'>nächster Gegner</button>");
      set_innerHTML("right_btn", "<button class='btn btn-primary' onclick='set_opponent()'>Gegner wählen</button>");
      display("left_btn");
      display("right_btn");
    }
  }
  else {
    team2_id = selector.value;
    team2 = team_list[team2_id];
  }
}

function start_prediction(){
  if (team1_id == team2_id){
    // TODO: ALERT
  }
  else if(team1_id == 0 || team2_id == 0){
    // TODO: ALERT
  }
  else {
    eel.start_algo(team1, team2)(callback_result);
  }
}

function callback_result(result){
  result_designer();

  // just for testing
    var t1 = result[0];
    var t2 = result[1];
    var h = result[2];
    var d = result[3];
    var g = result[4];

  set_innerHTML("left_btn", "<button class='btn btn-primary' onclick='get_clubs()'>anderes Match wählen</button>");
  set_innerHTML("right_btn", "<button class='btn btn-danger' onclick='welcome_page()'>zurück zur Startseite</button>");

  col1_html = "<div class='d-flex justify-content-center'><h3>" + t1 + "</h3></div>" +
      "<div class='d-flex justify-content-center'><p>" + h + "</p></div>";
  col2_html = "<div class='d-flex justify-content-center'><h3>:</h3></div>" +
      "<div class='d-flex justify-content-center'><p>" + d + "</p></div>";
  col3_html = "<div class='d-flex justify-content-center'><h3>" + t2 + "</h3></div>" +
      "<div class='d-flex justify-content-center'><p>" + g + "</p></div>";

  set_innerHTML("1-col-1", "<h2 class='d-flex justify-content-center'>Ergebnis:</h2>");
  set_innerHTML("3-col-1", col1_html);
  set_innerHTML("3-col-2", col2_html);
  set_innerHTML("3-col-3", col3_html);

  team1_id = 0;
  team2_id = 0;
}

// TODO: alert toasts, code kommentieren, Bilder abrufen, statischeres alignment im result screen

