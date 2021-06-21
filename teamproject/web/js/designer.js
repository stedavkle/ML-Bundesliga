// designer functions for pages

function sport_selection_designer(){
  hide("back_btn");
  hide('spinner_display');
  display("1-col-1")
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide("left_btn");
  hide("right_btn");

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
  hide("left_btn");
  hide("right_btn");

  set_3_col_standard();
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
  hide("left_btn");
  hide("right_btn");

  set_3_col_standard();
}

function training_data_designer(){
  display("back_btn");
  hide('spinner_display');
  hide_and_reset("1-col-1")
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide("left_btn");
  display("right_btn");

  set_3_col_standard();
}

function next_matchday_designer(){
  hide("back_btn");
  hide('spinner_display');
  display("1-col-1")
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide("left_btn");
  hide("right_btn");

  set_3_col_standard();
}

function team_select_designer(){
  display("back_btn");
  hide('spinner_display');
  display("1-col-1")
  display("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide("left_btn");
  hide("right_btn");

  set_3_col_standard();
}

function result_stage_switcher_designer(){
  hide("back_btn");
  hide('spinner_display');
  display("1-col-1")
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  display("3-col-1");
  display("3-col-2");
  display("3-col-3");
  display("5-col-1");
  display("left_btn");
  display("right_btn");

  set_3_col_result();
}

function clear_page(){
  hide("back_btn");
  hide('spinner_display');
  hide_and_reset("1-col-1")
  hide_and_reset("2-col-1");
  hide_and_reset("2-col-2");
  hide_and_reset("3-col-1");
  hide_and_reset("3-col-2");
  hide_and_reset("3-col-3");
  hide_and_reset("5-col-1");
  hide_and_reset("left_btn");
  hide_and_reset("right_btn");

  set_3_col_standard();
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

function set_3_col_result(){
  document.getElementById('3-col-1').style.maxWidth = '49%';
  document.getElementById('3-col-2').style.maxWidth = '2';
  document.getElementById('3-col-3').style.maxWidth = '49%';
}