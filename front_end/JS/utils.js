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

    // Prepare headers for the request
    header = {
        "Content-Type": "application/json",
    }

    // Include sessionid cookie in the headers if it exists
    if (document_get_cookie_value("sessionid")) {
        header.sessionid = document_get_cookie_value("sessionid")
    }

    // Make a GET request to the CSRF_URL to obtain a CSRF token.
    const response = await fetch(CSRF_URL, {
        headers: header
    });

    // check response and log if status not ok
    if (check_response(response, 'setcsrf')) {
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

    csrftoken = document_get_cookie_value('csrftoken')
    // Before proceeding with login, ensure that a CSRF token has been fetched.
    if (!csrftoken) {
        console.log("csrfToken is null. Canceling Login.")
        return false
    }

    const response = await fetch(LOGIN_URL, {
        method: "POST",
        headers: {

            // accessing the value associated with the key 'csrftoken' in the cookies object.
            "Cookie": `csrftoken=${csrftoken}`,
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })

    if (!check_response(response, "login")) {
        console.log("Aborting log in")
        return false
    }
    
    console.log("LOGIN END")
    return true
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
function check_response(response, basename) {
    if (!response.ok) {
        console.log(basename + " response NOT OK." + "\n" + response.text())
        return false
    }

    return true
}

