import { login, session } from "./utils.js"

// Allowing the user to login
document.getElementById('submit').addEventListener('click', async function(event) {
    event.preventDefault();
    
    // do username and password validation
    
    const username = await document.getElementById('username').value
    const password = await document.getElementById('password').value

    const result = await login(username, password);

    if (result.status === 200) {
        console.log("Logged in")
        window.location.pathname = '/'
    } else {
        console.log(`Login failed: ${result.detail}`)

        // TODO: show why the login failed on the HTML DOC
        // let error_text = document.getElementById("error");
        // error_text.textContent = JSON.parse(result.detail);
        
<<<<<<< HEAD
        let parent = document.querySelector("#login_form");
        let paragraph = document.createElement("p");
        paragraph.classList.add("form_fail");
        paragraph.innerHTML = "The username and/or password you entered does not match our records.";
        parent.appendChild(paragraph);
=======
        let exists = document.querySelector(".form_fail");
        if (!exists) {
            let parent = document.querySelector("#login_form");
            let paragraph = document.createElement("p");
            paragraph.classList.add("form_fail");
            paragraph.innerHTML = "The username and/or password you entered does not match our records.";
            parent.appendChild(paragraph);
        }
>>>>>>> 0ae0b896dfc54b30b4ce971d9be775ffb36b30e4

    }

})

document.addEventListener('DOMContentLoaded', function() {
    session().then((result) => {
        if (result === true) {
            window.location.pathname = '/'
        }
    })
  });






