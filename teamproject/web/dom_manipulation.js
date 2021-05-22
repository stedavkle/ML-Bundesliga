// -------------------- display and hide functions concerning ids in index.html ---------

function display(id){
    document.getElementById(id).style.display = 'block';
}

function hide(id){
    document.getElementById(id).style.display = 'none';
}

function set_innerHTML(id, text){
    document.getElementById(id).innerHTML = text;
}

function set_innerText(id, text){
    document.getElementById(id).innerText = text;
}