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
        console.log(`Logged in failed: ${result.detail}`)

        // TODO: show why the login failed on the HTML DOC
    }

})

document.addEventListener('DOMContentLoaded', function() {
    session().then((result) => {
        if (result === true) {
            window.location.pathname = '/'
        }
    })
  });






