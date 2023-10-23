var fs = require('fs')

const HOST = 'localhost:80'
const REST_AUTH_URL = `http://${HOST}/auth/`
const REST_API_URL =  `http://${HOST}/api/`
const CSRF_URL = REST_AUTH_URL + 'csrf'
const LOGIN_URL = REST_AUTH_URL + 'login'
const LOGOUT_URL = REST_AUTH_URL + 'logout'
const SESSION_URL = REST_AUTH_URL + 'session'
const WHOAMI_URL = REST_AUTH_URL + 'whoami'

const CONVERSATIONS_URL = REST_API_URL + 'conversations'

let cookies = {}
let logged_in = false

/*
    Returns the Json after calling the CSRF_URL for a CSRF Token
*/
async function fetch_csrf() {
    header = {
        "Content-Type": "application/json",
    }

    if (cookies['sessionid']) {
        header.sessionid = cookies['sessionid']
    }

    const response = await fetch(CSRF_URL, {
        headers: header
    });

    if (!response.ok) {
        response.text().then((data) => {
            if (data) {
                fs.writeFile("getcsrf_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })

        return 
    }

    return response.headers.get("X-CSRFToken")
}

async function login(username, password) {
    console.log("LOGIN START")
    if (!cookies['csrftoken']) {
        console.log("csrfToken is null. Canceling Login.")
        return
    }

    const response = await fetch(LOGIN_URL, {
        method: "POST",
        headers: {
            "Cookie": `csrftoken=${cookies['csrftoken']}`,
            "X-CSRFToken": cookies['csrftoken'],
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })

    if (response.ok) {
        console.log("LOGIN Response OK")
        const json = await response.json()
        console.log(json)
        logged_in = true;
    } else {
        console.log("LOGIN Response NOT OK")
        await response.text().then((data) => {
            if (data) {
                fs.writeFile("login_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })

        logged_in = false
        return
    }
    
    local_cookies = response.headers.getSetCookie() 
    console.log(local_cookies)
    if (local_cookies) {
        for (let i = 0; i < 2; i++) {
            info = local_cookies[i].split(';')
            pair = info[0].split('=') 
            cookies[pair[0]] = pair[1]
        }

        console.log("New cookies set: ")
        console.log(cookies)
    }
    
    console.log(`Setting new CSTF TOKEN to: ${cookies['csrftoken']}`)
    
    console.log("LOGIN END")
}

async function logout() {
    console.log("LOGOUT Start")
    if (!logged_in) {
        console.log("Not logged in, aborting.")
        return
    }
    const response = await fetch(LOGOUT_URL, {
        method: "GET",
        headers: {
            "Cookie": `sessionid=${cookies['sessionid']}`,
            "Content-Type": "application/json",
        }
    })

    if (response.ok) {
        console.log("LOGOUT Response OK")
        const json = await response.json()
        console.log(json)
        logged_in = false;
    } else {
        console.log("LOGOUT Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile("logout_html.html", data, (err) => {
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
                fs.writeFile("whoami_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    } 

    console.log("WHOAMI End")
}

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
                fs.writeFile("session_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    }

    console.log("SESSION End")
}

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
        console.log(JSON.stringify(json))
    } else {
        console.log("CONVERSATIONS Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile("conversations_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    }

    console.log("GET_CONVERSATIONS End")
}

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
        console.log(JSON.stringify(json))
    } else {
        console.log("CONVERSATIONS POST Response NOT OK")
        response.text().then((data) => {
            if (data) {
                fs.writeFile("conversationsPOST_html.html", data, (err) => {
                    if (err) console.log(`error: ${err}`)
                })
            } else {
                console.log("data is null")
            }
        })
    }


    console.log("POST_CONVERSATION End")
}

// Main

async function main() {
    fetch_csrf()
    .then( (data) => {
        cookies['csrftoken'] = data
    })
    .then(() => login("test", "test"))
    .then(() => whoami())
    .then(() => session())
    .then(() => get_conversations())
    .then(() => fetch_csrf())
    .then(() => post_conversation("data one two"))
    .then(() => logout())   
}

main(); 

