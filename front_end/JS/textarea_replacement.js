// This script creates a div to replace the default text area because it is easier to edit

let textarea_replacement = document.createElement("div");
textarea_replacement.classList = "textarea_replacement"
textarea_replacement.hidden = true;
let button_for_reference = document.querySelector("button");
let parent = document.querySelector("form");

parent.insertBefore(textarea_replacement, button_for_reference);

let textarea = document.querySelector(".textarea_default");
let div = document.querySelector(".textarea_replacement");
textarea.hidden = true;
div.hidden = false;
div.contentEditable = "true";
div.oninput = (e) => {
    textarea.value = div.innerHTML;
};



// Redirect to Login Page
document.getElementById('toLoginPage').addEventListener('click', function() {
    window.location.href = 'login.html';
});