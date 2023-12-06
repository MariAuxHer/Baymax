import requests
import json

def get_doctor_info(api_url, query_terms):
    # Specify the API endpoint
    endpoint = f"{api_url}/search"

    # Specify the parameters for the API request
    params = {
        'terms': query_terms,
        'maxList': 500,  # You can adjust this based on your needs
        'df': 'licenses.taxonomy.specialization,name.full,addr_practice.full,addr_practice.phone',
        'sf': 'licenses.taxonomy.specialization,name.full,addr_practice.full,addr_practice.phone'
    }

    # Make the API request
    response = requests.get(endpoint, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data);
        
        # Extract relevant information from the response
        results = data[3]

        # Create a dictionary to store the information
        doctor_dict = {}

        # Iterate through the results and populate the dictionary
        for result in results:
            specialization, doctor_name, doctor_address, phone = result

            # Populate the nested dictionary
            if specialization not in doctor_dict:
                doctor_dict[specialization] = []

            doctor_info = {
                'doctor_name': doctor_name,
                'doctor_address': doctor_address,
                'phone': phone,
            }
            doctor_dict[specialization].append(doctor_info)

        return doctor_dict

    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        return None

api_url = 'https://clinicaltables.nlm.nih.gov/api/npi_idv/v3'

# keep as empty string to get all doctors
query_terms = 'optometry'

doctor_info_dict = get_doctor_info(api_url, query_terms)

if doctor_info_dict:
    output_file_path = 'back_end/back_end/opt_doct.json'

    with open(output_file_path, 'w') as json_file:
        json.dump(doctor_info_dict, json_file, indent=2)
else:
    print("No doctor information found.")
