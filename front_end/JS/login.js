// Redirect to Login Page
document.getElementById('toLoginPage').addEventListener('click', function() {
    window.location.href = 'login.html';
});

// Redirect to About Page
document.getElementById('toAboutPage').addEventListener('click', function() {
    window.location.href = 'about.html';
});







let cookies = {};

const login = async (loginInfo, csrftoken) => {
    const res = await fetch('http://backend/auth/login', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
            "csrftoken": csrftoken
        },

        body: {
            username: loginInfo.username,
            password: loginInfo.password
        }
    })
}


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
    fetch('http://backend/auth/csrf').then(res => console.log(res));
    cookies['csrftoken'] = res.headers.get('X-CSRFToken');

    login(loginInfo, cookies);

})
