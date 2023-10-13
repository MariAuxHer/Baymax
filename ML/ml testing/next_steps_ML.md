# Next steps ML


## For the ChatBox interactions and preliminary advice


1. Generate instruction-based datasets: An instruction-based dataset is a collection of tasks and solutions that we cab use to fine-tune a pre-trained Large Language Model to perform different tasks including: Questions and Answers, Multiple Choice Questions, Medical Tasks (e.g., diagnosis). 

- Use the information provided in the NHS dataset - which contains definitions of diseases together with the corresponding symptoms and medications - to generate these instructions-based datasets. write a prompt where we ask. We need to write a prompt where we ask a Teacher model like ChatGPT to generate instructions (tasks) based on a context, which will be the text scraped from the [NHS.UK] (https://www.nhs.uk/conditions/) website. 

2. Fine-tune even further the medical-specialized NHS-LLM model with the additional instruction-based datasets generated. 


## ML model for classification 
1. Implement an encoder-only transformer or LSTM that will do the classification task. It will match user's symptoms with a medical specilization (this is the output of the model). Based on this output and on the user's locatio (which will be registered in the databse stored in the Django model), the chatbox will recommend a list of doctors. To do this, we need to use a data structure similar to the one created in the classify_doctor_info.cpp file - we should probably implement this in Python for easy implementation and integration with the rest of the software. This datastructure will allow us to do a "look-up" of the doctor's specialization, and then another "look-up" of the doctor's region. 

