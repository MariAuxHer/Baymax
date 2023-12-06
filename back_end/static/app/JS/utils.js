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

const GEONAMES_USERNAME = 'baymax';
const GEONAMES_BASE_URL = 'http://api.geonames.org/';

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
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
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
 * Returns an object of the form: { status (number) , detail (object/string) }
 * detail will be a user object if status is 200 (success).
 * detail will be a string containing the error if status is not 200.
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
            return { status: response.status, detail: json}
        } else {
            console.error("WHOAMI ERROR - Response is missing a username in the body!")
        }
    } else {
        console.error("WHOAMI FAILURE")
        return { status: response.status, detail: json.detail }
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
            "X-ShowInts": false,
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

/* 
 * Posts a conversation to the current user's account. Returns the conversation object that was created. Returns null if failed.
 */
export async function post_conversation(conversation_name, first_prompt = null) {
    // assign a csrf
    if (!(await set_csrf())) {
       return null
    }
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
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

    if (log_response(response, "post_conversation 1/2")) {
        console.log("POST_CONVERSATION 1/2 Response OK")
    } else {
        console.log("POST_CONVERSATION 1/2 Response NOT OK")
        return null
    }
    const json = await response.json()

    console.log("json " + json)
    console.log("json.url " + json.url)

    // post the first prompt if given
    if (first_prompt) {
        const json2 = await post_prompt(json.url, first_prompt)

        if (json2) {
            console.log("POST_CONVERSATION 2/2 Response OK")
            json.interaction_set[0] = json2
            return json
        } else {
            console.log("POST_CONVERSATION 2/2 Response NOT OK")
        }
    }
    return json
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
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
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
 * takes a url and a userdetails object (in the shape of an API user object) and return an object of the form: { status (number) , detail (object/string) }
 * if the status is 200, detail should be a user object, else it is a string describing the http request issue.
 */
export async function update_user(url, userdetails) {
    console.log("GET_USER start")

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const response = await fetch(url, {
        method: "PUT",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userdetails)
    })

    const json = await response.json()
    console.log("UPDATE_USER End")

    if (response.ok) {
        return { status:response.status, detail: json }
    } else {
        return { status:response.status, detail: json.detail }
    }
}
/*
 * Posts a new interaction to the conversation url
 */
export async function post_prompt(conversation_url, prompt) { 
    if (!(await set_csrf())) {
        return null
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const response = await fetch(conversation_url + 'interactions/', {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            prompt: prompt
        })
    })

    if (log_response(response, "post_prompt")) {
        console.log("POST_PROMPT Response OK")
        return await response.json()
    } else {
        console.log("POST_PROMPT Response NOT OK")
        return null
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

export async function update_name(url, name) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const response = await fetch(url, {
        method: "PUT",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: name
        })
    })

    if (log_response(response, "update_name")) {
        console.log("UPDATE_NAME Response OK")
        return { status: response.status, detail: await response.json() } 
    } else {
        console.log("UPDATE_NAME Response NOT OK")
        return { status: response.status, detail: response.detail } 
    }

}

export async function delete_conversation(conversation_url) {
    // assign a csrf
    if (!(await set_csrf())) {
       return null
    }
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const response = await fetch(conversation_url, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        }
    })

    if (log_response(response, "delete_conversation")) {
        console.log("DELETE_CONVERSATION Response OK")
    } else {

        console.log("DELETE_CONVERSATION Response NOT OK")
        return null
    }
}

// Function to make a request to GeoNames API
async function geoNamesFetch(endpoint, params) {
    let url = new URL(GEONAMES_BASE_URL + endpoint);
    params.username = GEONAMES_USERNAME;
    url.search = new URLSearchParams(params).toString();
    return fetch(url).then(response => response.json());
}

// // Function to load countries
// export async function loadCountries() {
//     geoNamesFetch('countryInfoJSON', {})
//         .then(data => {
//             console.log("In country", data);
//             let countrySelect = document.getElementById('country');
//             countrySelect.innerHTML = '<option value="">Select Country</option>';
//             data.geonames.forEach(country => {
//                 let option = document.createElement('option');
//                 option.value = country.geonameId; // Store the geonameId for the selected country
//                 option.textContent = country.countryName;
//                 countrySelect.appendChild(option);
//             });
//         })
//         .catch(error => console.error('Error loading countries:', error));
// }
    
// Function to load states for a given country
export async function loadStates(geonameId) {
    geoNamesFetch('childrenJSON', { geonameId: geonameId })
    .then(data => {
        console.log("In state", data);
        let stateSelect = document.getElementById('state');
        stateSelect.innerHTML = '<option value="">Select State/Province</option>';
        if (data.geonames) {
            data.geonames.forEach(state => {
                let option = document.createElement('option');
                option.value = state.geonameId; // You might need to adjust this to the appropriate identifier for the state.
                option.textContent = state.name;
                stateSelect.appendChild(option);
            });
        }
    })
    .catch(error => console.error('Error loading states:', error));
}

// Function to load cities for a given state
export async function loadCities(stateGeonameId) {
    geoNamesFetch('childrenJSON', { geonameId: stateGeonameId })
        .then(data => {
            console.log("In City", data);
            let citySelect = document.getElementById('city');
            citySelect.innerHTML = '<option value="">Select City/County</option>';
            if (data.geonames) {
                data.geonames.forEach(city => {
                    let option = document.createElement('option');
                    option.value = city.geonameId; // Store the geonameId for the selected city
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Error loading cities:', error));
}

// // Event listener for country selection change
// document.getElementById('country').addEventListener('change', function() {
//     let geonameId = this.value; // Get the geonameId of the selected country
//     if (geonameId) {
//         loadStates(geonameId); // Pass the geonameId to loadStates function
//     } else {
//         document.getElementById('state').innerHTML = '<option value="">Select State/Province</option>';
//     }
//     document.getElementById('city').innerHTML = '<option value="">Select City/County</option>';
// });

// // Event listener for state selection change
// document.getElementById('state').addEventListener('change', function() {
//     let stateGeonameId = this.value; // Get the geonameId of the selected state
//     // let countryCode = document.getElementById('country').value;
//     if (stateGeonameId) {
//         loadCities(stateGeonameId); // Pass the state's geonameId to loadCities function
//     } else {
//         document.getElementById('city').innerHTML = '<option value="">Select City/County</option>';
//     }
// });