const { Console } = require("console")

const HOST = window.location.host
const REST_AUTH_URL = `http://${HOST}/auth/`
const REST_API_URL =  `http://${HOST}/api/`
const CSRF_URL = REST_AUTH_URL + 'csrf'
const LOGIN_URL = REST_AUTH_URL + 'login'
const LOGOUT_URL = REST_AUTH_URL + 'logout'
const SESSION_URL = REST_AUTH_URL + 'session'
const WHOAMI_URL = REST_AUTH_URL + 'whoami'
const CREATE_USER_URL = REST_API_URL + "createuser"

const CONVERSATIONS_URL = REST_API_URL + 'conversations'

/* 
 * Sets the CSRFCookie of the current document window. Returns true on success and false on failure. 
 * This function should be called on pages that contain forms sent to the back_end
 */
async function set_csrf() {
    console.log("FETCH START")

    // Make a GET request to the CSRF_URL to obtain a CSRF token.
    const response = await fetch(CSRF_URL, {
        headers: {
            "Content-Type": "application/json",
        }
    });

    // check response and log if status not ok
    if (log_response(response, 'setcsrf')) {
        console.log("FETCH END")
        return false
    }

    console.log("FETCH END")
    return true;
}

/*
 * Logs the user in based on username and password. Requires csrftoken cookie to be set. Returns true on success, false on failure.
 */
async function login(username, password) {
    console.log("LOGIN START")

    // check for a csft cookie
    csrftoken = document_get_cookie_value('csrftoken')
    if (!csrftoken) {
        console.log("csrfToken cookie is null. Canceling Login.")
        console.log("LOGIN END")
        return false
    }

    const response = await fetch(LOGIN_URL, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })

    if (!log_response(response, "login")) {
        console.log("Aborting log in")
        console.log("LOGIN END")
        return false
    }
    
    console.log("LOGIN END")
    return true
}

/*
 * Logs the current user out based on the session cookie. If there is user logged in at the moment nothing is done.
 * This function doesn't return anything. 
 */
async function logout() {
    console.log("LOGOUT Start")

    const response = await fetch(LOGOUT_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })

    log_response(response, "logout")
    
    console.log("LOGOUT End")
}

/*
 * Returns the user name of the current logged in user based on the session cookie. 
 * Returns null on failure. i.e. user is not logged in. 
 */
async function whoami() {
    console.log("WHOAMI Start")
    
    const response = await fetch(WHOAMI_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    const data = await response.json()

    if (!log_response(response, "whoami")) {
        console.log("WHOAMI End")
        return null; 
    } 

    if (data.username) {
        console.log("WHOAMI End")
        console.log(`I AM USER: ${data.username}`)
        return data.username
    } else {
        console.error("Response is missing a username in the body!")
        console.log("WHOAMI End")
        return null
    }
}

/*
 * Returns true if the current session is authenticated with the back end. Returns false otherwise. 
 */
async function session() {
    console.log("SESSION Start")

    const response = await fetch(SESSION_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })

    const data = response.json()

    if (!log_response(response, "session")) {
        console.log("Failed to capture response.")
        return false
    }

    if (data.isAuthenticated) {
        console.log("Current session is authenticated.")
        console.log("SESSION End")
        return false
    } else {
        console.log("Current session is not authenticated.")
        console.log("SESSION End")
        return true
    }
}

/*
 * Returns a cookie value based on the passed key. Returns undefined if cookie doesn't exist.
 */
function document_get_cookie_value(key) {
    return document.cookie
    .split("; ")
    .find((row) => row.startsWith(key + "="))
    ?.split("=")[1];
}

/*
 * Checks and logs if a response is not ok.
 */
function log_response(response, basename) {
    if (response.ok) {
        console.log(basename + "response OK.")
        return true;
    } else {
        console.log(basename + " response NOT OK." + "\n" + response.text())
        return false
    }
}

