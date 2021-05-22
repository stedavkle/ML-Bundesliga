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

// globals
var team_list = "";
var selected_algo_id;
var selected_algo_data;
var selected_league;
var selected_seasons;
var team1;
var team1_id;
var team2;
var team2_id;

// -------------------- navbar functions ------------------------------------------------------------



// -------------------- welcome page functions ------------------------------------------------------------

function list_algorithms(){
    var html_str = "<select id='algo_selection' onchange='show_select_algo_submit()'><option value='0' selected disabled hidden>nichts ausgewählt</option>";
    for (var key in algorithms){
        html_str += "<option value='" + key + "'>" + algorithms[key] + "</option>";
    }
    set_innerHTML("algo_selection_dummy", html_str);
    //document.getElementById("algo_selection_dummy").innerHTML = html_str;



}

function show_select_algo_submit(){
    selected_algo_id = document.getElementById("algo_selection").value;
    //var algo_submit = document.getElementById("algo_submit");

    if (selected_algo_id != 0){

        display("algo_submit");
        set_innerHTML("algo_submit", "<button onclick='select_algo()'>Bestätigen</button>")

        //document.getElementById("algo_submit").innerHTML = "<button onclick='select_algo()'>Bestätigen</button>";
        //algo_submit.style.display = 'block';
        //algo_submit.innerHTML = "<button onclick='select_algo()'>Bestätigen</button>";

    }
}


// -------------------- data selection page function ------------------------------------------------------------


function select_algo(){

    // in case of restarting program
    //erase_data();

    hide("welcome_page");
    //document.getElementById("welcome_page").style.display = 'none';
    selected_algo_data = 'data_' + selected_algo_id;
    display(selected_algo_data);
    //document.getElementById(selected_algo_data).style.display = 'block';

    list_seasons();
    list_leagues();
    set_innerHTML("back_button", "<button onclick='go_to_start()'>zurück</button>");
    //document.getElementById("back_button").innerHTML = "<button onclick='go_to_start()'>zurück</button>";
    //document.getElementById("test").innerHTML = selected_algo_data;



}

function list_seasons(){
    set_innerHTML("select_seasons", "<p>Hier wird man die Saisons auswählen können...</p>");
    //document.getElementById("select_seasons").innerHTML = "<p>Hier wird man die Saisons auswählen können...</p>";
}

function list_leagues(){
    set_innerHTML("select_league", "<p>Hier wird man die Liga auswählen können...</p>");
    //document.getElementById("select_league").innerHTML = "<p>Hier wird man die Liga auswählen können...</p>";
}


function start_crawler(){
    hide(selected_algo_data);
    //document.getElementById(selected_algo_data).style.display = 'none';
    // TODO: sich etwas zum Thema Übergabe von Auswahl überlegen
    eel.start_crawler()(callback_start_crawler)

}


// -------------------- training function ------------------------------------------------------------
function callback_start_crawler(){
    display("training");
    //document.getElementById("training").style.display = 'block';
    set_innerHTML("back_button", "<button onclick='back_to_data_selection()'>zurück</button>");
    //document.getElementById("back_button").innerHTML = "<button onclick='back_to_data_selection()'>zurück</button>"
}

// -------------------- match selection function ------------------------------------------------------------
function get_clubs(){
    hide("training");
    //document.getElementById("training").style.display = 'none';
    set_innerHTML("back_button", "<button onclick='back_to_data_selection()'>zurück</button>");
    //document.getElementById("back_button").innerHTML = "<button onclick='back_to_data_selection()'>zurück</button>"
    display("opponent_buttons");
    //document.getElementById("opponent_buttons").style.display = 'block';
    eel.get_clubs(selected_league)(callback_select_home)
    //callback_select_home(1);
    //eel.club_select('"sel1"')(callback_home);
}

function callback_select_home(clubs){
    // TODO: check ob das geht
    team_list = clubs;

    var html_str = "<select id='sel1' onchange='set_team(1)'><option value='0' selected disabled hidden>kein Team ausgewählt</option>";
    for (var key in team_list){
        html_str += "<option value='" + key + "'>" + team_list[key] + "</option>";
    }
    set_innerHTML("clubs_home", html_str);
    //document.getElementById("clubs_home").innerHTML = html_str;
    display("match_selection");
    //document.getElementById("match_selection").style.display = 'block';

    //document.getElementById("clubs_home").innerHTML=clubs;
}

// TODO: Anfrage beim Crawler
function get_next_opponent(){
    if (document.getElementById("sel1").value != 0){
        hide("opponent_buttons");
        //document.getElementById("opponent_buttons").style.display = 'none';
        display("clubs_guest");
        //document.getElementById("clubs_guest").style.display = 'block';
        set_innerHTML("hint", '');
        //document.getElementById("hint").innerHTML = '';
        // TODO: hier muss dann der nächste Gegner gewählt werden
        // dummy function
            team2 = team1;
            team2_id = team1_id;
            document.getElementById("clubs_guest").innerHTML = team1;

        display("submit_buttons");
        //document.getElementById("submit_buttons").style.display = 'block';
        set_innerHTML("switch_button", "<button onclick='select_opponent()'>anderen Gegner wählen</button><button onclick='start_algo()'>Bestätigen</button>");
        //document.getElementById("switch_button").innerHTML = "<button onclick='select_opponent()'>anderen Gegner wählen</button><button onclick='start_algo()'>Bestätigen</button>"
    }
    else {
        // TODO: alert toast
        set_innerHTML("hint", "Wähle zuerst ein Team!");
        //document.getElementById("hint").innerHTML = "Wähle zuerst ein Team!";
    }
}

function select_opponent(){
    if (document.getElementById("sel1").value != 0){
        hide("opponent_buttons");
        //document.getElementById("opponent_buttons").style.display = 'none';
        set_innerHTML("hint", '');
        //document.getElementById("hint").innerHTML = '';

        var html_str = "<select id='sel2' onchange='set_team(2)'><option value='0' selected disabled hidden>kein Team ausgewählt</option>";
        for (var key in team_list){
            html_str += "<option value='" + key + "'>" + team_list[key] + "</option>";
        }

        display("clubs_guest");
        //document.getElementById("clubs_guest").style.display = 'block';
        set_innerHTML("clubs_guest", html_str);
        //document.getElementById("clubs_guest").innerHTML = html_str;
        display("submit_buttons");
        //document.getElementById("submit_buttons").style.display = 'block';
        set_innerHTML("switch_button", "<button onclick='get_next_opponent()'>nächster Gegner</button><button onclick='start_algo()'>Bestätigen</button>");
        //document.getElementById("switch_button").innerHTML = "<button onclick='get_next_opponent()'>nächster Gegner</button><button onclick='start_algo()'>Bestätigen</button>"
    }
    else {
        // TODO: alert toast
        set_innerHTML("hint", "Wähle zuerst ein Team!");
        //document.getElementById("hint").innerHTML = "Wähle zuerst ein Team!";
    }
}

/*
function callback_guest(clubs){
    document.getElementById("clubs_guest").style.display = 'block';
    document.getElementById("clubs_guest").innerHTML = clubs;

    document.getElementById("submit_buttons").style.display = 'block';
    document.getElementById("switch_button").innerHTML = "<button onclick='get_next_opponent()'>nächster Gegner</button><button onclick='start_algo()'>Bestätigen</button>"
}*/

function set_team(sel){
    var sel = "sel" + sel;
    var selector = document.getElementById(sel);

    if (sel == 'sel1'){
        team1_id = selector.value;
        team1 = team_list[team1_id];
        /*if (selector.value != 0){
            document.getElementById("opponent_buttons").style.display = 'block';
        }*/
    }
    else{
        team2_id = selector.value;
        team2 = team_list[team2_id];
    }
    //document.getElementById("test2").innerHTML = team1;
}


// -------------------- display result function ------------------------------------------------------------
function start_algo(){

    if (team1_id == 0 || team2_id == 0 ){
        set_innerHTML("hint", "Es müssen zwei Clubs ausgewählt werden!");
        //document.getElementById("hint").innerHTML = "Es müssen zwei Clubs ausgewählt werden!";
    }
    else if (team1_id == team2_id){
        // TODO: Alert einbauen
        set_innerHTML("hint", "Es müssen unterschiedliche Clubs ausgewählt werden!");
        //document.getElementById("hint").innerHTML = "Es müssen unterschiedliche Clubs ausgewählt werden!";
    }
    else {
        // TODO: Übergabe definieren
        eel.start_algo(team1, team2)(callback_result);
        hide("match_selection");
        //document.getElementById("match_selection").style.display = 'none';
    }

}

function callback_result(result){
    hide("back_button");
    //document.getElementById("back_button").style.display = 'none';
    display("result");
    //document.getElementById("result").style.display = 'block';

    // just for testing
    var t1 = result[0];
    var t2 = result[1];
    var h = result[2];
    var d = result[3];
    var g = result[4];

    var html_str = "<h2>" + t1 + " : " + t2 + "</h2> \
                    <p>" + h + " x " + d + " x " + g + "</p> \
                    <button onclick='go_to_start()'>zurück zur Startseite</button>\
                    <button onclick='back_to_match_selection()'>anderes Match wählen</button>";
    set_innerHTML("result", html_str);

    //document.getElementById("back_to_match_selection").innerHTML = "<button onclick='back_to_match_selection()'>anderes Match wählen</button>";
    //document.getElementById("go_to_start").innerHTML = "<button onclick='go_to_start()'>zurück zur Startseite</button>";
}


// delete selected values
function erase_data(){
    team_list = '';
    reset_teams();
}

// reset teams
function reset_teams(){
    team1_id = 0;
    team1 = '';
    team2_id = 0;
    team2 = '';
}



// TODO: alert toasts, Navbar, Buttons in footer setzen, refactoring, switch zwischen gegnerauswahl bug, striktere clear funktionen
// team1_id == null || team2_id == null ||