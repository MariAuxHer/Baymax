import { create_user } from "./utils.js";

// Allowing the user to create an account
document.getElementById('submit').addEventListener('click', async function(event) {
    event.preventDefault();
    
    // validate fields

    const accountInfo = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        email: document.getElementById('email').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zipcode: document.getElementById('zipcode').value,
    };

    // Debugging
    console.log(accountInfo.username);
    console.log(accountInfo.password);
    console.log(accountInfo.email);
    console.log(accountInfo.city);
    console.log(accountInfo.state);
    console.log(accountInfo.zipcode);

    const user = await create_user(accountInfo)

    if (user.status === 200) {
        console.log("user created")
        console.log(user.detail)

        window.location.pathname = "login"
    } else {
        console.log("user not created")
        console.log(user.detail)

         // TODO: show why the signup failed on the HTML DOC
    }
})
