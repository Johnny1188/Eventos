function toggle() {
    var content_container = document.getElementsByClassName("content-container")[0];
    var navigation = document.getElementsByClassName("navigation")[0];
    var toggle_menu = document.getElementById("menu_toggle");
    content_container.classList.toggle("active");
    navigation.classList.toggle("active");
    toggle_menu.classList.toggle("invisible");
    var header = document.getElementsByTagName("header");
    if (header[0].style.position != "sticky") {
        header[0].style.position = "sticky";
        header[0].style.top = "0px";
        header[0].style.right = "0px";
        header[0].style.width = "100vw";
    } else {
        header[0].style.position = "static";
    };
}

function copy_link(event_id) {
    var link_to_copy = document.getElementById("recommend_link_"+event_id);
    link_to_copy.select();
    link_to_copy.setSelectionRange(0,99999);
    document.execCommand("copy");
    alert("Copied your link")
}


// Function used onclick on reward images in mypage.html to expand the reward modal:
function open_reward_modal(name,description,imageURL,rewID,justInfo=false) {
    var reward_modal = document.getElementById("reward_modal");
    var body = document.getElementsByTagName("html");
    reward_modal.style.display = "flex";
    body[0].style.overflowY = "hidden";
    body[0].style.overflowX = "hidden";
    reward_modal_box_content = document.getElementById("reward_modal_box_content");
    if (justInfo == true) {
        reward_modal_box_content.classList.add("reward_modal_box_content_info");
        reward_modal_box_content.innerHTML = `
        <h3 id="reward_name"></h3>
        <div id="reward_modal_box_middle_body">
        </div>
        `;
        text_field = document.getElementById("reward_name");
        info_image_box = document.getElementById("reward_modal_box_middle_body");
        if (name == "Success") {
            text_field.innerHTML = "Your reward was successfully withdrawn! Expect an email from us with details :)"
            info_image_box.innerHTML = '<img src="/static/success.png"/>'
        } else if (name == "Fail") {
            text_field.innerHTML = "You do not have enough credit";
            info_image_box.innerHTML = '<img src="/static/error.png"/>'
        } else {
            text_field.innerHTML = "Sorry, something went wrong. Try again later.";
            info_image_box.innerHTML = '<img src="/static/error.png"/>'
        }
    } else {
        reward_modal_box_content.classList.remove("reward_modal_box_content_info");
        reward_modal_box_content.innerHTML = `
        <h3 id="reward_name">${name}</h3>
        <div id="reward_modal_box_middle_body">
            <p>${description}</p>
            <img src="${imageURL}"/>
        </div>
        <div id="reward_modal_box_button">
            <a href="/rew/rewarder/${rewID}"><button>WITHDRAW THIS REWARD</button></a>
        </div>
    `;
    }

}

// Function used onclick on the cross button in mypage.html to close the reward modal:
function close_modal() {
    var reward_modal = document.getElementById("reward_modal");
    var body = document.getElementsByTagName("html");
    close_btn = document.getElementById("reward_modal_box_close");
    body[0].style.overflowY = "auto";
    reward_modal.style.display = "none";
}

function recommendedMsg(inputClass,msg) {
    var input = document.getElementsByClassName(inputClass);
    console.log(inputClass);
    input[0].value = msg;
    input[0].focus();
}