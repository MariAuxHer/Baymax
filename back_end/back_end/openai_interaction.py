import openai
from openai import OpenAI
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import json
import re
import requests
import os
import dotenv
dotenv.load_dotenv('.env.local')

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Change the current working directory
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Current working directory openai:", os.getcwd())
with open('/app/back_end/medical_specializations.json', 'r') as f:
    medical_specializations = json.load(f)

model_id = 'gpt-4'

def fetch_doctors(specialty, city):
    url = ("https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search?terms={}&"
           "q=addr_practice.city:{}&df=NPI,name.full,addr_practice.full,addr_practice.phone&maxList=5").format(specialty, city)

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        #print(json.dumps(data, indent=4))

        doctors_list = []
        for item in data[3]:
            doctor_info = {
                'Name': item[1],
                'Address': item[2],
                'Phone': item[3]
            }
            doctors_list.append(doctor_info)
        return doctors_list
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        return None

def chatgpt_conversation(conversation_log):
    try: 
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(model=model_id, messages=conversation_log)

        conversation_log.append({'role': response.choices[0].message.role, 
            'content': response.choices[0].message.content.strip()
        })
        return conversation_log

    except Exception as e:
        logger.error("An error occurred in OpenAI API interaction: ")
        return None

def generate_llm_response(prompt, user_city):
    print(f"Here is a list of doctors in your region {user_city} \n")
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key is not set.")
        return "Error: OpenAI API key is not set."

    conversations = []
    conversations.append({'role': 'user', 'content': prompt})
    conversations = chatgpt_conversation(conversations)
    specialization_found = False 
    retrieve_data = False

    if conversations:
        gptresponse = conversations[-1]['content'].strip().lower()
        print(gptresponse)
        doctor_info_str = ""
        for specialization in medical_specializations: 
            specialization_found = True
            if re.findall(rf"\b{specialization}\b", gptresponse):
                print("specialization " + specialization)
                value = medical_specializations[specialization]
                print(f"Key: {specialization}, Value: {value}")
                
                # Specify the classification you are interested in
                specialty = value.replace(" ", "+")
                # = user_zipcode  # URL encoded space as +, to adhere to URL encoding standards
                doctors = fetch_doctors(specialty, user_city)

                print(f"Here is a list of doctors in your region {user_city} \n")
                doctor_info_str = doctor_info_str + f"\nHere is a list of {specialization} in your region\n"
                if doctors:
                    retrieve_data = True
                    for idx, doctor in enumerate(doctors, 1):
                        print(f"{idx}. Name: {doctor['Name']}, Address: {doctor['Address']}, Phone: {doctor['Phone']}")
                        doctor_info_str = doctor_info_str + f"{idx}. Name: {doctor['Name']}\nAddress: {doctor['Address']}\nPhone: {doctor['Phone']}\n"
                    
                #    return gptresponse + "\n" + doctor_info_str
                # else:
                #    print("No doctors found or failed to retrieve data.")
                #    return gptresponse
            
            #else: 
            #    print("only gpt response, no specialization found")
            #    return gptresponse
        
        if specialization_found and retrieve_data: 
            print("specialization found and able to retrieve doctor's info")
            return gptresponse + "\n" + doctor_info_str    
        
        else:
            print("only gpt response, no specialization found")
            return gptresponse
    else:
        print("Error: Unable to get response.")
        return "Error: Unable to get response."
    

    #try:
    #    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    #    response = client.chat.completions.create(
    #        model='gpt-4',
    #        messages=[{'role': 'user', 'content': prompt}]
    #    )
    #    return response.choices[0].message.content.strip()
    #except Exception as e:
    #    logger.error("An error occurred in OpenAI API interaction: %s", str(e))
    #    return "Error: Unable to get response."
