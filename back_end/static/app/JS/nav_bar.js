//! DEPRECATED
// FUNCTIONALITY OF THIS FILE HAS BEEN INTEGRATED INTO THE BUTTONS THROUGH THE 'ONCLICK' ATTRIBUTE
// OF THE BUTTONS

// Assign Login Page Button
const loginElement = document.getElementById('toLoginPage')
if (loginElement) {
    loginElement.addEventListener('click', () => {
        window.location.pathname = 'login';
    })
}

// Assign Profile Page Button
const profileElement = document.getElementById('toProfilePage')
if (profileElement) {
    profileElement.addEventListener('click', () => {
        window.location.pathname = 'profile';
    })
}

// Assign About Page Button
const aboutElement = document.getElementById('toAboutPage')
if (aboutElement) {
    aboutElement.addEventListener('click', () => {
        window.location.pathname = 'about';
    })
}