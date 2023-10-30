# Sprint 2

- Name: Maria Hernandez 
- Github: mherna21
- Group: Baymax

## What you planned to do
- [Integrate api calls to a gpt model](https://github.com/MariAuxHer/Baymax/issues/47)
- [Integrate api calls to an online doctor's database](https://github.com/MariAuxHer/Baymax/issues/48)
- [Develop code that takes user's input, generates a response given by a GPT LLM, and outputs to the user a list of doctors they can go to if they need medical assistant (depending on user's symptoms and region)](https://github.com/MariAuxHer/Baymax/issues/49)
- [Create a CustomUser Model that replaces the default Django's User](https://github.com/MariAuxHer/Baymax/issues/50)
- [Modify all the necessary files in the backend to recognize the new custom user](https://github.com/MariAuxHer/Baymax/issues/51)
- [Modify some of the front end files related to client's requests and the signup page](https://github.com/MariAuxHer/Baymax/issues/52)

## What you did not do
- I was not able to get the client's POST requests to the server working on the signup page.   

## What problems you encountered
- The openai api is not free and does not allow me to publicly post my API KEY in an online repository. Hence, I'll change to use PaLM api. 
- I'm having issues with the client's POST requests to the server. 

## Issues you worked on
- [Integrate api calls to a gpt model](https://github.com/MariAuxHer/Baymax/issues/47)
- [Integrate api calls to an online doctor's database](https://github.com/MariAuxHer/Baymax/issues/48)
- [Develop code that takes user's input, generates a response given by a GPT LLM, and outputs to the user a list of doctors they can go to if they need medical assistant (depending on user's symptoms)](https://github.com/MariAuxHer/Baymax/issues/49)
- [Create a CustomUser Model that replaces the default Django's User](https://github.com/MariAuxHer/Baymax/issues/50)
- [Modify all the necessary files in the backend to recognize to the new custom user](https://github.com/MariAuxHer/Baymax/issues/51)
- [Modify some of the front end files related to client's requests and the signup page](https://github.com/MariAuxHer/Baymax/issues/52)

## Files you worked on
- ML/Data/openai2.py
- back_end/back_end/models.py
- back_end/back_end/serializers.py
- back_end/back_end/views.py
- back_end/back_end/settings.py
- front_end/utils.js
- front_end/signup.html
- front_end/JS/signup.js
- front_end/CSS/signup.css

## What you accomplished
- Develop code that takes user's prompts, generates a response given by a GPT LLM, and outputs to the user a list of doctors they can go to 
  if they need medical assistant (depending on user's symptoms and region). In order to do that, I made api calls to both a gpt model and also 
  an online doctor's database. 
- Create a CustomUser Model that replaces the default Django's User. The default Django's model only ask for the following users credentials
  when they are registering in an application: username, password, and optionally email, first name, and last name. However, in order to provide users 
  with information about doctor's near them we need to know the user's location (city, state, and zip code). I added these fields in the CustomUser model.
- Modufy the signup page (still need more work)

## Next steps 

### Integration

1. Figure out the issues with the client's POST requests. 
2. Be able to do the POST requests from our signup page. 
3. Integrate the code containing the api calls to the gpt model with our backend so that we can store the conversations between an user and an assistant (LLM model)
   in the database provided by the Django's framework. 

### New Features 
1. Add another html page that allows the user to directly ask for information bout specific doctors (without interacting with the ML model).

### API calls to gpt model 
1. Use calls to PaLM api rather than openai api. 
2. Expand the dictionary with more medical's specializations to be able to provide the user with contact information of a broader range of 
    doctors in their area.   