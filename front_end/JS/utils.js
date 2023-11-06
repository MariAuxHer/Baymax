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
export async function set_csrf() {

    // Make a GET request to the CSRF_URL to obtain a CSRF token.
    const response = await fetch(CSRF_URL, {
        headers: {
            "Content-Type": "application/json",
        }
    });
    if (!response.ok) {
        console.error("SET_CSRF FAILED")
    }
    
    return { status: response.status }
}

/*
 * Logs the user in based on username and password. Requires csrftoken cookie to be set. 
 * Returns an object containing 'status' and 'detail'.
 * Status is the return HTTP status from fetch.
 * detail is the detail if an error were to have occured
 * detail will be null if status is 200 (OK)
 */
export async function login(username, password) {

    set_csrf().then( (result) => {
        if(result.status !== 200) {
            return { status: result.status, detail: "Failed to set CSRF." }
        }
    })

    // send request to backend
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

    // return response
    const json = await response.json()
    return { status: response.status, detail: json.detail }
}

/*
 * Logs the current user out based on the session cookie. If there is user logged in at the moment nothing is done.
 * This function doesn't return anything. 
 */
export async function logout() {
    const response = await fetch(LOGOUT_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })

    if (log_response(response, "logout")) {
        console.error("LOGOUT SUCCESS")
        return true
    } else {
        console.log("LOGOUT FAILED")
        return false
    }
}

/*
 * Returns the user name of the current logged in user based on the session cookie. 
 * Returns null on failure. i.e. user is not logged in. 
 */
export async function whoami() {
    const response = await fetch(WHOAMI_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    
    if (log_response(response, "whoami")) {
        const json = await response.json()
        if (json.username) {
            console.log(`WHOAMI SUCCESS - I AM USER: ${json.username}`)
            return json.username
        } else {
            console.error("WHOAMI ERROR - Response is missing a username in the body!")
        }
    } else {
        console.error("WHOAMI FAILURE")
        return null
    } 
}

/*
 * Returns true if the current session is authenticated with the back end. Returns false otherwise. 
 */
export async function session() {
    const response = await fetch(SESSION_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (log_response(response, "session")) {
        const data = await response.json()
        if (data.isAuthenticated) {
            console.log("SESSION - Current session is authenticated.")
            return true
        } else {
            console.log("SESSION - Current session is not authenticated.")
        }
    } else {
        console.error("SESSION - Failed to capture response.")
    }

    return false
}

export async function get_conversations() {
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

// TODO : Make a version of this function (or change this function) so that it will also post the first prompt.
// TODO : First make the end point for it in the backend to make it easier (a posted conversation name could include a first_prompt)
/* 
 * Posts a conversation to the current user's account. Returns the conversation object that was created. Returns null if failed.
 */
export async function post_conversation(conversation_name, first_prompt) {
    // assign a csrf
    if (!(await set_csrf())) {
       return null
    }
    
    const csrftoken = document_get_cookie_value('csrftoken')
    const response = await fetch(CONVERSATIONS_URL + "/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: conversation_name
        })
    })

    if (log_response(response, "post_conversation")) {
        console.log("POST_CONVERSATION 1/2 Response OK")
        const json = await response.json()
        return json
    } else {
        console.log("POST_CONVERSATION 1/2 Response NOT OK")
    }
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
 * returns null if failed to set csrf
 */
export async function create_user(userdetails = {}) {
    console.log("CREATE_USER Start")

    // check for a csft cookie
    if (!(await set_csrf())) {
        return null
    }
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

