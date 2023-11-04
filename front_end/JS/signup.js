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
