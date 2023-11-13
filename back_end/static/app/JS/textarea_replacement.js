// This script creates a div to replace the default text area because it is easier to edit

let textarea_replacement = document.createElement("div");       // making an editable div to replace a text area
textarea_replacement.setAttribute('id', 'prompt_text')
textarea_replacement.classList = "textarea_replacement"
textarea_replacement.hidden = true;
let submit_button = document.querySelector("#submit_message");
let parent = document.querySelector("form");

parent.insertBefore(textarea_replacement, submit_button);

let textarea = document.querySelector("#message_textarea");
let div = document.querySelector(".textarea_replacement");
textarea.hidden = true;
div.hidden = false;
div.contentEditable = "true";
div.oninput = (e) => {                              // input into the editable div will be coppied int the hidden text area
    textarea.value = div.innerHTML;
};
div.addEventListener("keydown", function(event) {   // pressing enter will submit textarea instead of making a newline in the editable div
    if (event.key === "Enter") {
        event.preventDefault();
        submit_button.click();
    }
});
parent.onsubmit = (e) => {                              
    setTimeout(() => {
        textarea.value = "";
        div.innerHTML = "";
    }, 0);
    setTimeout(() => {
        window.scrollTo(0, 500000);
    }, 1);
};

// panel.js
const coll = document.querySelectorAll(".collapsible");
coll.forEach((button) => {
    button.addEventListener("click", function () {
        const content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
});

const toggleButton = document.getElementById("togglePanelButton");
const panelContainer = document.getElementById("panelContainer");

toggleButton.addEventListener("click", function () {
  if (panelContainer.style.left === "0px" || panelContainer.style.left === "") {
    // Panel is currently visible; hide it
    panelContainer.style.left = "-250px";
  } else {
    // Panel is hidden; show it
    panelContainer.style.left = "0px";
  }
});


