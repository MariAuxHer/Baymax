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




    let zipcode = document.getElementById("zipcode");
    zipcode.addEventListener("input", async () => {
        
        if (zipcode.value.trim().length >= 3) {
            let cur_input = zipcode.value.trim();
            // let res = await fetch(`https://api.zippopotam.us/US/${cur_input}`);
            // res = await res.json();

            // console.log(res);

            // Need to find a proper zipcode lookup api...

        }
    })
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


    // Email validation
    let emailValidCheck = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailValidCheck.test(accountInfo.email)) {
        console.log('Invalid email address')

        let exists = document.querySelector("form_fail")
        if (!exists) {
            let parent = document.querySelector("#change_form");
            let paragraph = document.createElement("p");
            paragraph.classList.add("form_fail");
            paragraph.innerHTML = "Invalid email address";
            parent.appendChild(paragraph);
        }
        return;
    }
    console.log(emailValidCheck.test(accountInfo.email))

    // Zipcode validation
    console.log(accountInfo.zipcode);
    let digits = accountInfo.zipcode;
    if (digits.trim().length != 5) {
        console.log(digits.length);
        console.log('Invalid zipcode')

        let exists = document.querySelector("form_fail")
        if (!exists) {
            let parent = document.querySelector("#change_form");
            let paragraph = document.createElement("p");
            paragraph.classList.add("form_fail");
            paragraph.innerHTML = "Invalid zipcode";
            parent.appendChild(paragraph);
        }
        return;
    }
    if (zipcode.value.trim().length === 5) {
        let cur_input = zipcode.value.trim();
        let res = await fetch(`https://api.zippopotam.us/US/${cur_input}`);
        res = await res.json();

        console.log(res);

        if (res.country == null) {
            console.log("Invalid zipcode")
            return;
        }
        console.log(res.country);
    }



    
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