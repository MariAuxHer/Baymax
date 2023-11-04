// Assign Login Page Button
const loginElement = document.getElementById('toLoginPage')
if (loginElement) {
    loginElement.addEventListener('click', () => {
        window.location.pathname = 'html/login.html';
    })
}

// Redirect to Login Pagev============
const profileElement = document.getElementById('toProfilePage')
if (profileElement) {
    profileElement.addEventListener('click', () => {
        window.location.pathname = 'html/profile.html';
    })
}

const aboutElement = document.getElementById('toAboutPage')
if (aboutElement) {
    aboutElement.addEventListener('click', () => {
        window.location.pathname = 'html/about.html';
    })
}