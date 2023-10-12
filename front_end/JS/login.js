// Redirect to Login Page
document.getElementById('toLoginPage').addEventListener('click', function() {
    window.location.href = 'login.html';
});


// Allowing the user to login
document.getElementById('submit').addEventListener('click', function(event) {
    event.preventDefault();

    const loginInfo = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };

    // Debugging
    console.log(loginInfo.username);
    console.log(loginInfo.password);
    

    // TODO: Send to backend for verification
    // ...
})
