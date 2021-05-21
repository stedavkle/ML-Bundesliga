
// go to data selection
function back_to_data_selection(){
    document.getElementById(selected_algo_data).style.display = 'block';
    document.getElementById("training").style.display = 'none';
    document.getElementById("match_selection").style.display = 'none';
    //document.getElementById("opponent_buttons").style.display = 'none';
    document.getElementById("clubs_guest").style.display = 'none';
    document.getElementById("submit_buttons").style.display = 'none';
    document.getElementById("back_button").innerHTML = "<button onclick='go_to_start()'>zurück</button>";
}

// go to match selection
function back_to_match_selection(){
    document.getElementById("match_selection").style.display = 'block';
    //document.getElementById("opponent_buttons").style.display = 'none';
    document.getElementById("hint").innerHTML = '';
    document.getElementById("clubs_guest").style.display = 'none';
    document.getElementById("submit_buttons").style.display = 'none';
    document.getElementById("result").style.display = 'none';
    document.getElementById("opponent_buttons").style.display = 'block';
    document.getElementById("back_button").innerHTML = "<button onclick='back_to_data_selection()'>zurück</button>"
    reset_teams();
}

// jump to landingpage
function go_to_start(){
    document.getElementById("welcome_page").style.display = 'block';
    document.getElementById(selected_algo_data).style.display = 'none';
    document.getElementById("training").style.display = 'none';
    document.getElementById("match_selection").style.display = 'none';
    //document.getElementById("opponent_buttons").style.display = 'none';
    document.getElementById("clubs_guest").style.display = 'none';
    document.getElementById("submit_buttons").style.display = 'none';
    document.getElementById("result").style.display = 'none';
    document.getElementById("back_button").innerHTML = "";
    erase_data();
}