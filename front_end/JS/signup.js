// Redirect to Login Page
document.getElementById('toLoginPage').addEventListener('click', function() {
    window.location.href = 'login.html';
});

// Redirect to About Page
document.getElementById('toAboutPage').addEventListener('click', function() {
    window.location.href = 'about.html';
});


// Allowing the user to create an account
document.getElementById('submit').addEventListener('click', function(event) {
    event.preventDefault();

    const accountInfo = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        email: document.getElementById('email').value,
    };

    // Debugging
    console.log(accountInfo.username);
    console.log(accountInfo.password);
    console.log(accountInfo.email);

    
    // TODO: Send to backend for verification
    // ...
})
