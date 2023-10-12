To run the server, you need either python3.11 or Docker set up.

If you just have python3.11:
    In the command line, type : "python3.11 manage.py runserver 0.0.0.0:8000"

    Note: Depending on your system, the python command may look different.
    Instead of "python3.11", it may just be "python", "python3", or something else.
    Make sure that whaatever python you are using is python3.11, since systems may sometimes have different versions of python installed.
    "python" could refer to the python2 on your system.
    "python3" could refer to any version of python3, most commonly "python3.8" by default. 

If you have docker installed and setup:
    If you are running docker through WSL, you will need to have it set up in WSL and Docker Desktop will need to be installed on Windows. 

    CD to the project root directory (the one containing the compose.yml file) and run "docker compose up -d"

    The nginx server is setup to route everything to the back_end REST API for now.
    The server should be running on your system on port 81. (if not its probably 80, i dont remember)

    From here, you can navigate to the Docker Desktop app in Windows and check each container.

After the server is up:
    To access the API, you need to be logged in to an account.
    Since the front_end has not been set up to do that yet, you can use django's provided front_end.
    localhost/admin should bring you to the django authentication page.
    You can use a dummy account with username: "test" and password: "test".(Note that the password "test" would never be allowed in production, I manually bypassed the password validation)

    After you have logged in, that is all you need to do for authentication. 
    Your session should contain the proper cookies to keep you logged in.

    Now you can navigate to the localhost/conversation endpoint.

    This is where front_end will be making calls to after authentication to get the entire list of conversations that belong to a user.
    The django front_end will show you all the possible HTTP request types you can make (i.e. GET, POST, OPTIONS, HEAD) on each page.

    To start, make a new conversation by specifying a name and clicking POST. 
    There is also a section that shows you the RAW json body of the HTTP request that django sends.
    In reality, the header of the HTTP request will also contain a CSRP token and a session token. 