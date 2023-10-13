# Sprint 1
- Steven Dao
- NETid: sdao
- Github: nevetsosu
- Baymax

### What you planned to do
Create URL endpoints for getting and manipulating a specific user's conversation data.

### What you did not do
Create URL endpoints for deleting data. 

### What problems you encountered
I got sidetracked with overall application architecture. This meant I didn't implement data deletion yet.

### Issues you worked on
No specifically opened GitHub Issues.

### Files you worked on
- All the Dockerfiles, including the compose.yml
- Nginx server
- back_end/authentication/(urls.py, views.py) back_end/back_end/(urls.py, views.py, models.py, settings.py, serializers.py)

### What you accomplished
I established the application architecture and composition. The application will be comprised of a nginx webserver proxying the front and back end server (back end server mainly is just admin access). I created the Docker workflow to spin up and connect all servers on a virtual Docker network. I created beginning endpoints for obtaining and manipulating user conversation data for the front end server to be able to use. The back_end server is essentially a REST API for the ML model and contains the user and conversation database (By default, djanngo uses sqllite as the dattabase). Now that the data is accessible, the front_end needs a way to login as a non-admin user, which is being started in the back_end/authentication folder. Django takes care of most of the authentication and all the ENDPOINTS created in back_end/authentication should be fully functional, but I need make test calls from the front_end to get a better idea of how the front_end will be communicating. 


### What I am going to do
Right now, I am attempting to serve the front end and back end static files by nginx itself to reduce overhead in having the individual front and back have to deal with static files. 
Though the files are successfully being requested and sent, CSS files don't appear to actually apply in the browser. So I need to trouble shoot that. 

I need to talk to the front end about how the front end server should be configured.

I need to create those deletion URLs

I may also go ahead and make a javascript module that does most of the http communication to the REST API and provide it to the front end server. 