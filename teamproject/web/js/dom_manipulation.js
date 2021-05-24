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

// ------- special display functions

function show_select_algo_submit(){
  selected_algo_id = document.getElementById("algo_selection").value;

  if (selected_algo_id != 0){
    display("right_btn");
  }
}
