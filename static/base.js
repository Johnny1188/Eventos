function toggle() {
    var content_container = document.getElementsByClassName("content-container")[0];
    var navigation = document.getElementsByClassName("navigation")[0];
    var toggle_menu = document.getElementById("menu_toggle");
    content_container.classList.toggle("active");
    navigation.classList.toggle("active");
    toggle_menu.classList.toggle("invisible");
}

function copy_link() {
    var link_to_copy = document.getElementById("recommend_link");
    link_to_copy.select();
    link_to_copy.setSelectionRange(0,99999);
    document.execCommand("copy");
    alert("Copied your link")
}