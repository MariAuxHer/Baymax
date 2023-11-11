import openai
import json
import re
import requests


with open('medical_specializations.json', 'r') as f:
    medical_specializations = json.load(f)

API_KEY = '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'
openai.api_key = API_KEY
model_id = 'gpt-4'

def fetch_doctors(specialty, city):
    url = ("https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search?terms={}&"
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

# Load the taxonomy_dict from the JSON file
#with open('lol.json', 'r') as f:
#    taxonomy_dict = json.load(f)

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


        
        
        # if match then look at the database of doctors 

    #print('{1}\n'.format(conversations[-2]['content'].strip()))
    # what we can do is just ask the model ourselves (not the user to output the specialization of the doctor)

# Write the DataFrame to a CSV file
#with open('grouping.txt', 'w') as file:
    # Iterate through the keys of the dictionary
#    for key in taxonomy_dict:
        # Write each key to the file, followed by a newline character
#        file.write(f"{key}\n")
