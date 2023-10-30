To communicate with the django backend:

NOTE:
    Because we are using Docker, the backend server domain name is "backend", which will automatically resolve to the actual backend IP using Docker's virtual network DNS.
    
NOTE:
    You can look directly at the back_end's API URLS by going to the http://localhost/api/ endpoints.
    From see exactly what all request responses look like. 

    Some times the JSON data will have links within them to point to other resourses.
    Use those to navigate the site as well.

1. OBTAIN A CSRF TOKEN:
    Make a GET request to http://backend/auth/csrf
    Store this in a cookie called "csrftoken".

2. LOG IN:
    Make a POST request to http://backend/auth/login

    NOTE: All POST requests (forms) require that you send the CSRF Token in the header as "X-CSRFToken" and as a Cookie "csrftoken".

    The request body should include a field called "username" and one called "password" (Set to whatever the username and password are ofcourse)

    If successful, the back_end will return a success message in JSON and 2 cookie values:
    A session ID and a new CSRF Token (that is now associated with the session).

    Update the csrftoken cookie with the new csrf value.
    This is the one that you will be sending in subsequent POST requests (associated with this user).
    The sessionID cookie will need to be set with ALL subsequent requests.

    So POST requests will contain:
        A "csrftoken" cookie and "sessionid" cookie
        A "X-CSRFToken" value in the header

    ALL requests in general contain atleast:
        "sessionid" cookie

    NOTE: the value of "csrftoken" and "X-CSRFToken" are still the SAME, in fact, to get the X-CSRFToken value, you need to read the "csrftoken" cookie. 
    This seems like redundant behavior, but is crucial to the CSRF Protection.

    A third party website would not have access to the value of the csrftoken, so even if a third party website forged our website form and sent it to the right endpoint (along with the session and csrftoken cookies because browsers automatically send cookies upon POST), the 3rd party website would not be able to specify the right csrf token in the HEADER, that can only be done by our own frontend because we can read the cookie value.

3. Making subsequent GET Requests:
    This was implicitly defined in point 2., but only the sessionID cookie needs to be included. 
    What data is put in the body will be specific to each end point. 

4. Logging out:
    Simply make a GET request to the http://backend/auth/logout endpoint, making sure you also send the sessionid cookie.


If you need reference code, go to the repo's back_end/utils.js file. 
If you want to run it, just use a javascript runtime like Node and point it to that file. 

In case it does matter, the Node version I've been running it with is v18.18.2 LTS.