// This script creates a div to replace the default text area because it is easier to edit

let textarea_replacement = document.createElement("div");       // making an editable div to replace a text area
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

// Redirect to Login Page
document.getElementById('toLoginPage').addEventListener('click', function() {
    window.location.href = 'login.html';
});
