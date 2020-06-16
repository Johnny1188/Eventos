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


// Function used onclick on reward images in mypage.html to expand the reward modal:
function open_reward_modal(name,description,imageURL,rewID) {
    var reward_modal = document.getElementById("reward_modal");
    var body = document.getElementsByTagName("html");
    reward_modal.style.display = "flex";
    body[0].style.overflowY = "hidden";
    body[0].style.overflowX = "hidden";
    reward_modal_box_content = document.getElementById("reward_modal_box_content");
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

// Function used onclick on the cross button in mypage.html to close the reward modal:
function close_modal() {
    var reward_modal = document.getElementById("reward_modal");
    var body = document.getElementsByTagName("html");
    close_btn = document.getElementById("reward_modal_box_close");
    body[0].style.overflowY = "auto";
    reward_modal.style.display = "none";
}

// Add functionality to the "WITHDRAW THIS REWARD" button
//      - it should first check whether the user has enough points on his profile
//      - then, check the quantity of the reward -> if at least 1 -> quantity -= 1
//      - notify us that this specific user (email) wants to withdraw this specific reward
//          - could be new table with withdrawn rewards: ----REWARD | USER | SENT? (T/F)----