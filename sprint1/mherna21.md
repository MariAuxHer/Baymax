# Sprint 1

- Name: Maria Hernandez 
- Github: mherna21
- Group: Baymax

## What you planned to do
- [Initial fine-tuning of NHS-LLM Model](https://github.com/MariAuxHer/Baymax/issues/2)
- [Run Tutorial for Text Classification](https://github.com/MariAuxHer/Baymax/issues/3)
- [Take ML course](https://github.com/MariAuxHer/Baymax/issues/1)
- [Classify doctor's information](https://github.com/MariAuxHer/Baymax/issues/6)
- Review and understand backend's code.

## What you did not do
- I have not yet fine-tuned the NHS-LLM model. 
- I wanted to advance more on the LLM model - get more accurate predictions.  

## What problems you encountered
- The existing NHS-LLM model is very lightweight, which results in innacurate predictions. 
- We need to either add more instruction-based data to our dataset or change the hyperparameters of the model
to see if we get better predictions. 

## Issues you worked on
- [Initial fine-tuning of NHS-LLM Model](https://github.com/MariAuxHer/Baymax/issues/2)
- [Run Tutorial for Text Classification](https://github.com/MariAuxHer/Baymax/issues/3)
- [Take ML course](https://github.com/MariAuxHer/Baymax/issues/1)
- [Classify doctor's information based on parsed data](https://github.com/MariAuxHer/Baymax/issues/6)

## Files you worked on
- classify_doctor_info.cpp
- Light_NHS_LLM.ipynb (run it with Jordan)
- Fixed the settings.py file in the back_end folder. 

## What you accomplished
- Get a better understanding of transformers (mainly decoders-only and encoders-only) and how to use them in our software. 
- Find a trained LLM that we will use to provide the user with preliminary advice and potential diagnoses.
- Determine the model we will use (encoder-only transformer) to classify user text input into different required medical specializations. 
- Parse and classify doctor's information. 

## Next steps 

### For the ChatBox interactions and preliminary advice


1. Generate instruction-based datasets: An instruction-based dataset is a collection of tasks and solutions that we can use to fine-tune a pre-trained Large Language Model to perform different tasks including: Questions and Answers, Multiple Choice Questions, Medical Tasks (e.g., diagnosis). 

- Use the information provided in the NHS dataset - which contains definitions of diseases together with the corresponding symptoms and medications - to generate these instructions-based datasets. write a prompt where we ask. We need to write a prompt where we ask a Teacher model like ChatGPT to generate instructions (tasks) based on a context, which will be the text scraped from the [NHS.UK] (https://www.nhs.uk/conditions/) website. 

2. Fine-tune even further the medical-specialized NHS-LLM model with the additional instruction-based datasets generated. 

## ML model for classification 
1. Implement an encoder-only transformer or LSTM that will do the classification task. It will match user's symptoms with a medical specilization (this is the output of the model). Based on this output and on the user's locatio (which will be registered in the databse stored in the Django model), the chatbox will recommend a list of doctors. To do this, we need to use a data structure similar to the one created in the classify_doctor_info.cpp file - we should probably implement this in Python for easy implementation and integration with the rest of the software. This datastructure will allow us to do a "look-up" of the doctor's specialization, and then another "look-up" of the doctor's region. 

