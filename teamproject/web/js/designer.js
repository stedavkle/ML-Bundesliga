/*  designer functions for pages
    ----------------------------

    main html is divided up to several <div> row- and column-containers.
    visibility of each element is controlled for each stage from here
 */

function sport_selection_designer(){
  document.body.style.overflowY = 'hidden';
  hide("back_btn");
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

  clear_alert();
  set_3_col_standard();
}

function crawler_data_designer(){
  display("back_btn");

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

  clear_alert();
}

function model_selection_designer(){
  display("back_btn");
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

  clear_alert();
}

function training_data_designer(){
  display_block('2-row');
  display_block('3-row');
  display_block('5-row');
  display_block('6-row');

  display("back_btn");
  hide('spinner_display');
  display("1-col-1");
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("6-col-1");
  hide("left_btn");
  display("right_btn");

  clear_alert();
  set_3_col_standard();
}

function next_matchday_designer(){
  display_none('2-row');
  display_none('3-row');
  display_none('5-row');
  display_none('6-row');

  hide("back_btn");
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

  clear_alert();
}

function team_select_designer(){
  display_block("2-row");
  display_block("3-row");

  display("back_btn");
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

  clear_alert();
}

function result_stage_switcher_designer(){
  display_none("2-row");
  display_none("3-row");
  display_block('5-row');

  hide("back_btn");
  hide('spinner_display');
  display("1-col-1")
  hide("2-col-1");
  hide("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  display("5-col-1");
  hide("6-col-1");
  display("left_btn");
  display("right_btn");

  clear_alert();
}


function next_matchday_prediction_designer(){
  display_none("2-row");
  display_none("3-row");
  display_none('5-row');

  hide("back_btn");
  hide('spinner_display');
  display("1-col-1")
  hide("2-col-1");
  hide("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide("5-col-1");
  hide("6-col-1");
  display("left_btn");
  display("right_btn");

  clear_alert();
}


function clear_page(){
  display_block("2-row");
  display_block("3-row");

  hide("back_btn");
  hide('spinner_display');
  hide_and_reset("1-col-1")
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("6-col-1");
  hide_and_reset("left_btn");
  hide_and_reset("right_btn");

  clear_alert();
}


// fancy spinner display for longer waiting periodes
function spinner_on(){
  display('spinner_display');
  hide('right_btn');
  hide('left_btn');
}

function spinner_off(){
  hide('spinner_display');
}

// fancy spinner button
function spinner_button(){
  var spinner = "<button class=\'btn btn-danger\' disabled>" +
      "<span class=\'spinner-border spinner-border-sm\'></span>\tTraining</button>";
  set_innerHTML('right_btn', spinner);
}

// adjust direction of columns
function set_3_col_standard(){
  document.getElementById('3-col-1').style.maxWidth = '33.3%';
  document.getElementById('3-col-2').style.maxWidth = '33.3%';
  document.getElementById('3-col-3').style.maxWidth = '33.3%';
}


/**
 * displays alert banner under nav bar
 * @param message - error message string
 */
function create_alert(message){
  //display_block('alert');
  display("alert");
  var html_str = "<button type=\'button\' class=\'close\' onclick=\'clear_alert()\'>&times;</button>" +
        "<strong>Fehler!</strong> " + message;
  set_innerHTML("alert", html_str);
}

function clear_alert(){
  //display_none('alert');
  hide_and_reset("alert");
}

