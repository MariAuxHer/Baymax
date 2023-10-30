// Redirect to Login Page
document.getElementById('toLoginPage').addEventListener('click', function() {
    window.location.href = 'login.html';
});

// Redirect to About Page
document.getElementById('toAboutPage').addEventListener('click', function() {
    window.location.href = 'about.html';
});






let test = ['1', '0'];
let cookies = {};

const login = async (loginInfo) => {
    //const res = await fetch('http://localhost:8000/auth/login', {
    const res = await fetch('http://backend/auth/login', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": cookies['csrftoken'],
            "Cookie": `csrftoken=${cookies['csrftoken']}`
        },

        body: JSON.stringify({
            username: loginInfo.username,
            password: loginInfo.password
        })
    })

    return res;
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
    let response; 
    // fetch('http://localhost:8000/auth/csrf').then(res => {
    fetch('http://backend/auth/csrf').then(res => {
        console.log(res)
        cookies['csrftoken'] = res.headers.get('X-CSRFToken')
        console.log(cookies['csrftoken'])

        (response = login(loginInfo)).then(console.log(response))
    });

})
window.sharedData = test;

