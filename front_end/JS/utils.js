export const HOST = window.location.host
export const REST_AUTH_URL = `http://${HOST}/auth/`
export const REST_API_URL =  `http://${HOST}/api/`
export const CSRF_URL = REST_AUTH_URL + 'csrf'
export const LOGIN_URL = REST_AUTH_URL + 'login'
export const LOGOUT_URL = REST_AUTH_URL + 'logout'
export const SESSION_URL = REST_AUTH_URL + 'session'
export const WHOAMI_URL = REST_AUTH_URL + 'whoami'
export const CREATE_USER_URL = REST_API_URL + "createuser"

export const CONVERSATIONS_URL = REST_API_URL + 'conversations'

const HTTP_401_UNAUTHORIZED = 401
const HTTP_400_BAD_REQUEST = 400
const HTTP_409_CONFLICT = 409
const HTTP_403_FORBIDDEN = 403

/* 
 * Sets the CSRFCookie of the current document window. Returns true on success and false on failure. 
 * This function should be called on pages that contain forms sent to the back_end
 */
export async function set_csrf() {
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
 * Logs the user in based on username and password. Requires csrftoken cookie to be set. 
 * Returns an object containing 'status' and 'detail'.
 * Status is the return HTTP status from fetch.
 * detail is the detail if an error were to have occured
 * detail will be null if status is 200 (OK)
 */
export async function login(username, password) {
    console.log("LOGIN START")

    await set_csrf()
    const csrftoken = document_get_cookie_value('csrftoken')
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

    const json = await response.json()
    return { status: response.status, detail: json.detail }
}

/*
 * Logs the current user out based on the session cookie. If there is user logged in at the moment nothing is done.
 * This function doesn't return anything. 
 */
export async function logout() {
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
export async function whoami() {
    console.log("WHOAMI Start")
    
    const response = await fetch(WHOAMI_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    
    if (log_response(response, "whoami")) {
        const json = await response.json()
        if (json.username) {
            console.log(`I AM USER: ${json.username}`)
            return json.username
        } else {
            console.error("Response is missing a username in the body!")
        }
    } else {
        console.error("Request error")
    } 

    console.log("WHOAMI End")
    return null
}

/*
 * Returns true if the current session is authenticated with the back end. Returns false otherwise. 
 */
export async function session() {
    console.log("SESSION Start")

    const response = await fetch(SESSION_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (log_response(response, "session")) {
        const data = await response.json()
        if (data.isAuthenticated) {
            console.log("Current session is authenticated.")
            return true
        } else {
            console.log("Current session is not authenticated.")
        }
    } else {
        console.error("Failed to capture response.")
    }

    console.log("SESSION End")
    return false
}

export async function get_conversations() {
    console.log("GET_CONVERSATIONS Start")
    const response = await fetch (CONVERSATIONS_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (log_response(response, "get_conversations")) {
        console.log("CONVERSATIONS Response OK")
        return await response.json()
    } else {
        console.log("CONVERSATIONS Response NOT OK")
    }

    console.log("GET_CONVERSATIONS End")
    return null
}

/*
 * Testing function that calls and prints results of get_conversations(). 
 * It still returns the result of get_conversations as the return of this function.
 */
export async function log_conversations() {
    const data = await get_conversations()
    console.log(data)

    return data
}

/*
 * Posts a conversation to the current user's account. Returns the conversation object that was created. Returns null if failed.
 */
export async function post_conversation(name) {
    console.log("POST_CONVERSATION Start")

    // check for a csft cookie
    csrftoken = document_get_cookie_value('csrftoken')
    if (!csrftoken) {
        console.log("csrfToken cookie is null. Canceling Login.")
        console.log("POST_CONVERSATION End")
        return null
    }

    const response = await fetch(CONVERSATIONS_URL + "/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: name
        })
    })

    if (log_response(response, "post_conversations")) {
        console.log("CONVERSATIONS POST Response OK")
        const json = await response.json()
        return json
    } else {
        console.log("CONVERSATIONS Response NOT OK")
    }

    console.log("POST_CONVERSATION End")
    return null
}

/*
 * Testing function that calls and prints results of post_conversation. 
 * It still returns the result of post_conversations as the return of this function.
 */
export async function log_conversation(name) {
    const data = await post_conversation(name)
    console.log(data)
    return data
}


/*
 * userdetails should contain a username field, password field, and email field
 */
export async function create_user(userdetails = {}) {
    console.log("CREATE_USER Start")

    // check for a csft cookie
    await set_csrf()
    const csrftoken = document_get_cookie_value('csrftoken')
    const response = await fetch(CREATE_USER_URL, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userdetails)
    })

    const json = await response.json()
    console.log("CREATE_USER End")

    if (response.ok) {
        return { status:response.status, detail: json }
    } else {
        return { status:response.status, detail: json.detail }
    }
}

/*
 * Returns a cookie value based on the passed key. Returns undefined if cookie doesn't exist.
 */
export function document_get_cookie_value(key) {
    return document.cookie
    .split("; ")
    .find((row) => row.startsWith(key + "="))
    ?.split("=")[1];
}

/*
 * Checks and logs if a response is not ok.
 */
export function log_response(response, basename) {
    if (response.ok) {
        console.log(basename + "response OK.")
        return true;
    } else {
        console.log(basename + " response NOT OK." + "\n" + response.text())
        return false
    }
}

