// script to handle client-side requests to the server

// Import the 'domain' module's 'create' method
<<<<<<< HEAD
const { create } = require('domain')

// Import the 'fs' (File System) module for file operations
var fs = require('fs')
=======
// const { create } = require('domain')
//import someModule from './someModule.js';
// Import the 'fs' (File System) module for file operations
//var fs = require('fs')
>>>>>>> sprint3

// pretty json
const prettyjson = require('prettyjson')

// Define constants for server host and URL endpoints
const HOST = 'localhost:80'
const REST_AUTH_URL = `http://${HOST}/auth/`
const REST_API_URL =  `http://${HOST}/api/`
const CSRF_URL = REST_AUTH_URL + 'csrf'
const LOGIN_URL = REST_AUTH_URL + 'login'
const LOGOUT_URL = REST_AUTH_URL + 'logout'
const SESSION_URL = REST_AUTH_URL + 'session'
const WHOAMI_URL = REST_AUTH_URL + 'whoami'
const CREATE_USER_URL = REST_API_URL + "createuser"

const CONVERSATIONS_URL = REST_API_URL + 'conversations'
const LOGS_DIR = 'logs/'

// Object to hold cookie values
let cookies = {}

// Variable to track login state
let logged_in = false

/*
    Returns the Json after calling the CSRF_URL for a CSRF Token
*/

// Function to fetch a CSRF token from the server -> sends a GET request to the server's /csrf endpoint.
async function fetch_csrf() {
    console.log("FETCH START")
    // Prepare headers for the request
    header = {
        "Content-Type": "application/json",
    }

    // Include sessionid cookie in the headers if it exists
    // In JavaScript, dictionaries (or objects) can have fields added to them dynamically.
    if (cookies['sessionid']) {
        header.sessionid = cookies['sessionid']
    }

    // Make a GET request to the CSRF_URL to obtain a CSRF token.
    const response = await fetch(CSRF_URL, {
        headers: header
    });

    // If the request fails, write the error data to a file for debugging.
    if (!response.ok) {
        response.text().then((data) => {
            if (data) {
                fs.writeFile(LOGS_DIR + "getcsrf_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })

        return 
    }

    // On a successful response, extract the X-CSRFToken from the response headers
    // and store it in the cookies object for later use.
    // On the server side, in views.py, the CSRF class's get method sets the X-CSRFToken header.
    // cookies['csrftoken'] = response.headers.get("X-CSRFToken")
    // console.log(response)
    // console.log("HEADER COOKIE: " + response.headers.get("X-CSRFToken"))
    if (response.headers.has("Set-Cookie")) {
        console.log("true")
    } else {
        console.log("false")
    }

    local_cookies = response.headers.getSetCookie() 
    info = local_cookies[0].split(';')
            pair = info[0].split('=') 
            cookies[pair[0]] = pair[1]

    console.log(response.headers.getSetCookie())
    console.log("FETCH END")
}

// Function to perform login
async function login(username, password) {
    console.log("LOGIN START")

    // Before proceeding with login, ensure that a CSRF token has been fetched.
    if (!cookies['csrftoken']) {
        console.log("csrfToken is null. Canceling Login.")
        return false
    }

    // Make a POST request to the LOGIN_URL to perform login.
    // Include the CSRF token in both the Cookie and X-CSRFToken headers.
    // On the server side, in views.py, the LoginView class's post method handles login.
    // await fetch is the method used to make the request
    const response = await fetch(LOGIN_URL, {
        method: "POST",
        headers: {

            // accessing the value associated with the key 'csrftoken' in the cookies object.
            "Cookie": `csrftoken=${cookies['csrftoken']}`,
            "X-CSRFToken": cookies['csrftoken'],
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })

    // If logout is successful, update the logged_in variable.
    // the variable will be used in other functions to check whether an user is logged in or not
    // If logout fails, write the error data to a file for debugging.
    if (response.ok) {
        console.log("LOGIN Response OK")
        const json = await response.json()
        console.log(json)
        logged_in = true;
    } else {
        console.log("LOGIN Response NOT OK")
        await response.text().then((data) => {
            if (data) {
                fs.writeFile( LOGS_DIR + "login_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })

        logged_in = false
        return
    }
    

    /* 
        Setting the sessionid cookie
        The sessionid cookie is typically set when a user logs in, and it's used by the server to maintain the
        user's session. In your Django application, when the login function is called and the login is successful, 
        the sessionid cookie is set by Django's session middleware and sent back to the client in the HTTP response.
    */
    local_cookies = response.headers.getSetCookie() 
    console.log(local_cookies)
    if (local_cookies) {
<<<<<<< HEAD
        for (let i = 0; i < 2; i++) {
            info = local_cookies[i].split(';')
            pair = info[0].split('=') 
            cookies[pair[0]] = pair[1]
        }

        /*
            Alternative to dont hardcode 0 - 1 in the loop 
=======
        // for (let i = 0; i < 2; i++) {
        //     info = local_cookies[i].split(';')
        //     pair = info[0].split('=') 
        //     cookies[pair[0]] = pair[1]
        // }

        
        //    Alternative to dont hardcode 0 - 1 in the loop 
>>>>>>> sprint3
            local_cookies.forEach(cookieString => {
            const info = cookieString.split(';');
            const pair = info[0].split('=');
            cookies[pair[0]] = pair[1];
            });
<<<<<<< HEAD
        */
=======
>>>>>>> sprint3

        console.log("New cookies set: ")
        console.log(cookies)
    }
    
    console.log(`Setting new CSTF TOKEN to: ${cookies['csrftoken']}`)
    
    console.log("LOGIN END")
}

// Function to perform logout
async function logout() {
    console.log("LOGOUT Start")

    // Before proceeding with logout, ensure that the user is logged in.
    if (!logged_in) {
        console.log("Not logged in, aborting.")
        return
    }

    // Make a GET request to the LOGOUT_URL to perform logout.
    // Include the sessionid cookie in the headers if it exists.
    // On the server side, in views.py, the LogoutView class's get method handles logout.
    const response = await fetch(LOGOUT_URL, {
        method: "GET",
        headers: {
            "Cookie": `sessionid=${cookies['sessionid']}`,
            "Content-Type": "application/json",
        }
    })

    // Handle the response based on its status.
    // If logout is successful, update the logged_in variable.
    // If logout fails, write the error data to a file for debugging.
    if (response.ok) {
        console.log("LOGOUT Response OK")
        const json = await response.json()
        console.log(json)
        logged_in = false;
    } else {
        console.log("LOGOUT Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile(LOGS_DIR + "logout_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })

        logged_in = true
        return
    }

    console.log("LOGOUT End")
}

/*
    URL Endpoint: WHOAMI_URL
    Purpose: This function is designed to retrieve the username of the currently logged-in user. 
    On the server side, the WhoAmIView class handles this request and responds with the username 
    of the authenticated user. This can be useful for displaying the user's name on the client-side 
    or for other user-specific tasks.
*/
async function whoami() {
    console.log("WHOAMI Start")
    if (!logged_in) {
        console.log("Not logged in, aborting.")
        return
    }
    
    const response = await fetch(WHOAMI_URL, {
        method: "GET",
        headers: {
            "Cookie": `sessionid=${cookies['sessionid']}`,
            "Content-Type": "application/json"
        }
      })

      if (response.ok) {
        console.log("WHOAMI Response OK")
        const json = await response.json()
        console.log(json)
    } else {
        console.log("WHOAMI Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile(LOGS_DIR + "whoami_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    } 

    console.log("WHOAMI End")
}

/*
    This function checks if there's an active session for the user. On the server side, 
    the SessionView class handles this request and responds with an indication of whether 
    the user is authenticated. This can be useful for checking the login status of the user 
    and updating the UI accordingly.
*/
async function session() {
    console.log("SESSION Start")
    if (!logged_in) {
        console.log("Not logged in, aborting.")
        return
    }

    const response = await fetch(SESSION_URL, {
        method: "GET",
        headers: {
            "Cookie": `sessionid=${cookies['sessionid']}`,
            "Content-Type": "application/json"
        }
    })

    if (response.ok) {
        console.log("SESSION Response OK")
        const json = await response.json()
        console.log(json)
    } else {
        console.log("SESSION Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile(LOGS_DIR +  "session_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    }

    console.log("SESSION End")
}

/*
    This function fetches the list of conversations associated with the authenticated user. 
    Although the server-side handler isn't shown in the provided Python script, typically, 
    this endpoint would query the database for conversations related to the logged-in user and
    return them in the response. This function helps in displaying the user's conversations on the client-side.
*/
async function get_conversations() {
    console.log("GET_CONVERSATIONS Start")
    if (!logged_in) {
        console.log("Not logged in, aborting.")
        return
    }
    const response = await fetch (CONVERSATIONS_URL, {
        method: "GET",
        headers: {
            "Cookie": `sessionid=${cookies['sessionid']}`,
            "Content-Type": "application/json"
        }
    })

    if (response.ok) {
        console.log("CONVERSATIONS Response OK")
        const json = await response.json()
        console.log(prettyjson.render(json))
    } else {
        console.log("CONVERSATIONS Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile(LOGS_DIR + "conversations_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    }

    console.log("GET_CONVERSATIONS End")
}

/*
    This function attempts to create a new conversation on the server by sending a POST request to the CONVERSATIONS_URL endpoint.
    The CSRF token is sent in the headers to comply with the server's CSRF protection mechanism, and the name of the conversation 
    is sent in the request body.

*/
async function post_conversation(name) {
    console.log("POST_CONVERSATION Start")

    const response = await fetch(CONVERSATIONS_URL + "/", {
        method: "POST",
        headers: {
            "Cookie": `csrftoken=${cookies['csrftoken']};sessionid=${cookies['sessionid']}`,
            "X-CSRFToken": cookies['csrftoken'],
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: name
        })
    })

    if (response.ok) {
        console.log("CONVERSATIONS POST Response OK")
        const json = await response.json()
        console.log(prettyjson.render(json))
    } else {
        console.log("CONVERSATIONS POST Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile(LOGS_DIR + "conversationsPOST_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    }


    console.log("POST_CONVERSATION End")
}

/* 
    The create_user function in your JavaScript file is designed to send a POST request to the server 
    to create a new user account, which corresponds to a sign-up action on the client-side. The user's 
    username, password, and email are sent in the request body to the server, which presumably handles 
    the account creation logic on its end.

    ADD HERE USER'S REGION (STATE, CITY, ZIP CODE)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
*/
<<<<<<< HEAD
async function create_user(username, password, email) {
=======
async function create_user(username, password, email, city, state, zipcode) {
>>>>>>> sprint3
    console.log("CREATE_USER Start")
    const response = await fetch(CREATE_USER_URL, {
        method: "POST",
        headers: {
            "Cookie": `csrftoken=${cookies['csrftoken']}`,
            "X-CSRFToken": cookies['csrftoken'],
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
            email: email,
<<<<<<< HEAD
=======
            city: city,
            state: state,
            zipcode: zipcode
>>>>>>> sprint3
        })
    })

    
    if (response.ok) {
        console.log("CREATE_USER POST Response OK")
        const json = await response.json()
        console.log(JSON.stringify(json))
    } else {
        console.log("CREATE_USER Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile(LOGS_DIR + "createUser_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    }

    console.log("CREATE_USER End")
}

// Main

async function main() {
    fetch_csrf()
    // .then(() => create_user("test", "test", "stevendao100@gmail.com"))
    // .then(() => login("test", "test"))
    // .then(() => whoami())
    // .then(() => session())
    // .then(() => get_conversations())
    // .then(() => fetch_csrf())
    // .then(() => post_conversation("data one two"))
    // .then(() => logout())   
    // .then(() => fetch_csrf())
    .then(() => create_user("test2", "aMoreSophosticatedPassword100", "stevendao100@gmail.com"))
    .then(() => login("test2", "aMoreSophosticatedPassword100"))
    .then(() => logout())
    // .then(() => fetch_csrf())
    // .then(() => create_user("test", "NotTooShortOfAPassword", "stevendao100@gmail.com"))
    // .then(() => login("test", "test"))
    // .then(() => whoami())
    // .then(() => session())
    // .then(() => get_conversations())
    // .then(() => fetch_csrf())
    // .then(() => post_conversation("demo data"))
    // .then(() => logout())
    
}

main(); 

