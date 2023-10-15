const HOST = 'localhost:80'
const REST_BASE_URL = `http://${HOST}/auth/`
const CSRF_URL = REST_BASE_URL + 'csrf'
const LOGIN_URL = REST_BASE_URL + 'login'
const LOGOUT_URL = REST_BASE_URL + 'logout'
const SESSION_URL = REST_BASE_URL + 'session'
const WHOAMI_URL = REST_BASE_URL + 'whoami'

let csrfToken
let sessionid

/*
    Returns the Json after calling the CSRF_URL for a CSRF Token
*/
async function fetch_csrf() {
    const response = await fetch(CSRF_URL);
    const json = await response.json()

    // print headers 
    response.headers.forEach((x) => {
        console.log(x)
    });

    // print body
    console.log(json)
    console.log()
    csrfToken = response.headers.get("X-CSRFToken")
    return csrfToken
}

async function login(csrf_token = null, data = {}) {
    if (!csrf_token) return null

    const response = await fetch(LOGIN_URL, {
        method: "POST",
        headers: {
            "csrftoken": csrf_token,
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data), 
    })

    if (response.ok) {
        const json = await response.json()
        console.log(json)
    } else {
        response.text().then( (data) => {
            console.log(data)
        })
    }

    // print body
    console.log("COOOOOKIES: ")
    console.log(response.headers.getSetCookie())
    console.log()
}

async function logout(sessionid, csrf_token) {

    header = new Headers({
        "Content-Type": "application/json"
    })

    header.append("csrftoken", csrf_token)
    header.append("sessionid", sessionid)

    const response = await fetch(LOGOUT_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "csrftoken": csrf_token,
            "sessionid": sessionid,
        }
    })

    // print headers 
    response.headers.forEach((x) => {
        console.log(x)
    });

    if (response.ok) {
        const json = await response.json()
        console.log(json)
    } else {
        response.text().then( (data) => {
            console.log(data)
        })
    }
    console.log()
}

async function whoami(csrf_token, data = {}) {
    console.log("using token: " + csrfToken)
    const response = await fetch(WHOAMI_URL, {
        method: "POST",
        headers: {
            "csrftoken": csrf_token,
            "Content-Type": "application/json"
        },
        // body: JSON.stringify(data),
        credentials: "same-origin",
      })

    if (response.ok) {
        const json = await response.json()
        console.log(json)
    } else {
        response.text().then( (data) => {
            console.log(data)
        })
    }  
}



fetch_csrf().then((data) => {
    console.log("attempting login with csrf token: " + data)
    login(data, {username: "test", password: "test"}).then(() => {
        console.log("attempting to check who i am")
        whoami(csrfToken, {username: "test", password: "test"}) 
    })
})

