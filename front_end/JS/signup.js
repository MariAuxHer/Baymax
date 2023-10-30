// Redirect to Login Page
document.getElementById('toLoginPage').addEventListener('click', function() {
    window.location.href = 'login.html';
});

// Redirect to About Page
document.getElementById('toAboutPage').addEventListener('click', function() {
    window.location.href = 'about.html';
});


// Allowing the user to create an account
document.getElementById('submit').addEventListener('click', async function(event) {
    event.preventDefault();

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

    
    if (typeof create_user === "function") {
        console.log("create_user function exists!");
    } else {
        console.error("create_user function does not exist!");
    }
    
    // attempt to call the create_user function not working that well.. we can call the function, but we need to check the 
    // utils.js file
    try {
        await create_user(accountInfo.username, accountInfo.password, accountInfo.email, accountInfo.city, accountInfo.state, accountInfo.zipcode);
    } catch (error) {
        console.error('Error in create_user:', error);
    }
    
});
