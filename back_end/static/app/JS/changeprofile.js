import { whoami } from "./utils.js";
import { update_user } from "./utils.js";

let who;
document.addEventListener("DOMContentLoaded", async () => {
    who = await whoami();
    console.log(who);

    // Have the old user info appear in the input boxes
    document.getElementById("username").value = who.detail.username
    document.getElementById("password").readOnly = true
    document.getElementById("email").value = who.detail.email
    document.getElementById("city").value = who.detail.city
    document.getElementById("state").value = who.detail.state
    document.getElementById("zipcode").value = who.detail.zipcode
})

document.getElementById("submit").addEventListener('click', async (event) => {
    event.preventDefault();

    const accountInfo = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        email: document.getElementById('email').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zipcode: document.getElementById('zipcode').value,
    };

    const url = who.detail.url
    console.log(url)

    
    const update = await update_user(url, accountInfo)

    if (update.status === 200) {
        console.log("user info updated")
        console.log(update.detail)

        window.location.pathname = "profile"
    } else {
        console.log("user info failed to update")
        console.log(update.detail)
        document.getElementById("error").textContent = "Could not update info"
    }
})