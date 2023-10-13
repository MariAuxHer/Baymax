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
- back_end/* (most of it)

### What you accomplished
I established the application architecture and composition. The application will be comprised of a nginx webserver proxying the front and back end server (back end server mainly is just admin access). I created the Docker workflow to spin up and connect all servers on a virtual Docker network. I created beginning endpoints for obtaining and manipulating user conversation data for the front end server to be able to use. The back_end server is essentially a REST API for the ML model and contains the user and conversation database (By default, djanngo uses sqllite as the dattabase). Now that the data is accessible, the front_end needs a way to login as a non-admin user, which is being started in the back_end/authentication folder. Django takes care of most of the authentication and all the ENDPOINTS created in back_end/authentication should be fully functional, but I need make test calls from the front_end to get a better idea of how the front_end will be communicating. 