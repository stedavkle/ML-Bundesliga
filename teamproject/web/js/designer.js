// designer functions for pages

function sport_selection_designer(){
  hide("back_btn");
  clear_alert();
  hide('spinner_display');
  display("1-col-1")
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("6-col-1");
  hide("left_btn");
  hide("right_btn");

  set_3_col_standard();
}

function crawler_data_designer(){
  display("back_btn");
  clear_alert();
  hide('spinner_display');
  display("1-col-1")
  display("2-col-1");
  display("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("6-col-1");
  hide("left_btn");
  hide("right_btn");

  //set_3_col_standard();
}

function model_selection_designer(){
  display("back_btn");
  clear_alert();
  hide('spinner_display');
  display("1-col-1")
  display("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("6-col-1");
  hide("left_btn");
  hide("right_btn");

  //set_3_col_standard();
}

function training_data_designer(){
  display("back_btn");
  clear_alert();
  hide('spinner_display');
  hide_and_reset("1-col-1");
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("6-col-1");
  hide("left_btn");
  display("right_btn");

  //set_3_col_standard();
}

function next_matchday_designer(){
  hide("back_btn");
  clear_alert();
  hide('spinner_display');
  display("1-col-1")
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  display("5-col-1");
  hide_and_reset("6-col-1");
  display("left_btn");
  display("right_btn");

  //set_3_col_standard();
}

function team_select_designer(){
  display("back_btn");
  clear_alert();
  hide('spinner_display');
  display("1-col-1")
  display_block("2-row");
  display_block("3-row");
  display("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("6-col-1");
  hide("left_btn");
  hide("right_btn");

  //set_3_col_standard();
}


// TODO: da fehlen hide elemente
function result_stage_switcher_designer(){
  hide("back_btn");
  clear_alert();
  hide('spinner_display');
  display("1-col-1")
  hide("2-col-1");
  hide("2-col-2");
  display_none("2-row");
  display_none("3-row");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  display("5-col-1");
  hide("6-col-1");
  display("left_btn");
  display("right_btn");
}

function clear_page(){
  hide("back_btn");
  clear_alert();
  hide('spinner_display');
  hide_and_reset("1-col-1")
  display_block("2-row");
  display_block("3-row");
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("6-col-1");
  hide_and_reset("left_btn");
  hide_and_reset("right_btn");

  //set_3_col_standard();
}

function spinner_on(){
  display('spinner_display');
  hide('right_btn');
  hide('left_btn');
}

function spinner_off(){
  hide('spinner_display');
}

function set_3_col_standard(){
  document.getElementById('3-col-1').style.maxWidth = '33.3%';
  document.getElementById('3-col-2').style.maxWidth = '33.3%';
  document.getElementById('3-col-3').style.maxWidth = '33.3%';
}


function create_alert(message){
  display("alert");
  var html_str = "<button type=\'button\' class=\'close\' onclick=\'clear_alert()\'>&times;</button>" +
        "<strong>Fehler!</strong> " + message;
  set_innerHTML("alert", html_str);
}

function clear_alert(){
  hide_and_reset("alert");
}

function spinner_button(){
  // spinner at button position
  var spinner = "<button class=\'btn btn-danger\' disabled>" +
      "<span class=\'spinner-border spinner-border-sm\'></span>\tTraining</button>";
  set_innerHTML('right_btn', spinner);
}