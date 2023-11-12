
import openai
import json
import re
import requests


with open('medical_specializations.json', 'r') as f:
    medical_specializations = json.load(f)


# set the API_KEY I can't set mine because if I do, openai will disable my api key
# This code wont work without an API_KEY though. For the next sprint, I will switch to 
# making calls to PaLM API since this one is free and more than likely don't have the issue
# of being unable to be shared in public repositories. 
# API_KEY = 
openai.api_key = API_KEY
model_id = 'gpt-4'

def fetch_doctors(specialty, city):
    url = ("https://clinicaltables.nlm.nih.gov/api/npi_idv/sv3/search?terms={}&"
           "q=addr_practice.city:{}&df=NPI,name.full,addr_practice.full,addr_practice.phone&maxList=500").format(specialty, city)

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
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation_log
    )

    conversation_log.append({
        'role': response.choices[0].message.role, 
        'content': response.choices[0].message.content.strip()
    })
    return conversation_log

conversations = []
# system, user, assistant
#conversations.append({'role': 'system', 'content': 'Im a medical chatbox assistant, how may I help you?'})
#conversations = chatgpt_conversation(conversations)
#print('{0}: {1}\n'.format(conversations[-1]['role'].strip(), conversations[-1]['content'].strip()))

while True:
    prompt = input('User: ')
    conversations.append({'role': 'user', 'content': prompt})
    conversations = chatgpt_conversation(conversations)
    print()
    print('{0}: {1}\n'.format(conversations[-1]['role'].strip(), conversations[-1]['content'].strip()))
    gptresponse = conversations[-1]['content'].strip().lower()
    print(gptresponse)
    for specialization in medical_specializations: 
        if re.findall(rf"\b{specialization}\b", gptresponse):
            value = medical_specializations[specialization]
            print(f"Key: {specialization}, Value: {value}")
            
            # Specify the classification you are interested in
            specialty = value.replace(" ", "+")
            city = "Los+Angeles"  # URL encoded space as +, to adhere to URL encoding standards
            doctors = fetch_doctors(specialty, city)

            if doctors:
                for idx, doctor in enumerate(doctors, 1):
                    print(f"{idx}. Name: {doctor['Name']}, Address: {doctor['Address']}, Phone: {doctor['Phone']}")
            else:
                print("No doctors found or failed to retrieve data.")