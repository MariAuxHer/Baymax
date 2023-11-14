# Sprint 3

- Name: Maria Hernandez 
- Github: mherna21
- Group: Baymax

## What you planned to do
- [Modify some files to integrate CustomUser Model in the dev branch](https://github.com/MariAuxHer/Baymax/issues/83)
- [Create a python script that generates the llm response, connects with doctor's database, and returns a complete response to the Interaction model](https://github.com/MariAuxHer/Baymax/issues/84)
- [Integration of the llm response with frontend](https://github.com/MariAuxHer/Baymax/issues/85)
- [Modify the Interaction model in models.py to retrive a response from the llm model instead of a generic sample](https://github.com/MariAuxHer/Baymax/issues/86)
- [Update medical dictionary](https://github.com/MariAuxHer/Baymax/issues/87)
- [Add another html page that allows the user to directly ask for information about specific doctors (without interacting with the ML model)](https://github.com/MariAuxHer/Baymax/issues/88)

## What you did not do
- I did not have time to work on an extra page that allows the user to directly ask for information about specific doctors (without interacting with the ML model)

## What problems you encountered
- I faced network challenges and spent considerable time troubleshooting Docker runtime issues. Identified the problem as default DNS settings in WSL 2 and resolved 
it by switching to Google's public DNS (8.8.8.8).

## Issues you worked on
- [Modify some files to integrate CustomUser Model in the dev branch](https://github.com/MariAuxHer/Baymax/issues/83)
- [Modify the python script that generates the llm response, connects with doctor's database, and returns a complete response to the Interaction model](https://github.com/MariAuxHer/Baymax/issues/84)
- [Integration of the llm response with frontend](https://github.com/MariAuxHer/Baymax/issues/85)
- [Modify the Interaction model in models.py to retrive a response from the llm model instead of a generic sample](https://github.com/MariAuxHer/Baymax/issues/86)
- [Update medical dictionary](https://github.com/MariAuxHer/Baymax/issues/87)

## Files you worked on
- back_end/back_end/models.py
- back_end/back_end/api_views.py
- back_end/back_end/openai_interaction.py
- back_end/back_end/urls.py
- back_end/static/JS/index.js
- back_end/requirements.txt

## What you accomplished
- Integrate backend and frontend so that when the user submits a prompt in the chatbox page, the server connects with the 
openai API and the doctors' api (clinicaltables.nlm.nih.gov) to retrieve a response from the model and a list of doctors of a certain specialization.
Then, the server sends back the complete response to the user. 
- Modify and enhance the openai_interaction.py python script, which takes user's prompts, generates a response given by a GPT LLM, and returns to the 
Interaction model the LLM response along with a list of doctors the user can go to.
- Modify the Intercation model in models.py to receive the response generated in openai_interaction.py
- Modify all the necessarily files to be able to smoothly do this integration between frontend and backend (index.js, urls.py, api_views.py) and to 
correctly build the docker image (requirements.txt)

## Next steps 
## Optimization

1. Optimize more the openai_interaction.py script and the medical_specialization.json dictionary 
2. Work on the Conversation's model so that for each conversation we have a list of all prompts so that the openai model can respond based on previous prompt
(for a specific conversation)
3. Along with the frontend people, work on the design of the complete response (LLM response + doctor's list), so far is just plain text
4. Instead of using a default city (Los Angeles), use the city + geocode provided by the user, to provide doctor's close to the user's region.
5. Validate user's location - state, city, geocode (needs to be inside the united states, since the doctors' database only has information about doctors 
in the United States)
6. Work on a left or right panel that display the name of all conversations for that specific user. 

### New Features 
1. Add another html page that allows the user to directly ask for information about specific doctors (without interacting with the ML model). Such page 
should include a search bar. 