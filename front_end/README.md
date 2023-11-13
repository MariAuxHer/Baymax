The front end has been moved.

Most of the HTML is being used as a template in ./back_end/back_end/templates/back_end/
(Dont ask me why the directory path is so ridiculous, idk)
The HTML is not going to display properly if you try to open the 
file on its own since it is marked up with django's templating language. 

Most of all the other static elements are now in ./back_end/static/app/
They are untouched by django's templating language and look/function
the same as they always have. 

