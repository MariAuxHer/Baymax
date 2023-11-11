import requests
import json

def get_doctor_info(api_url, query_terms):
    # Specify the API endpoint
    endpoint = f"{api_url}/search"

    # Specify the parameters for the API request
    params = {
        'terms': query_terms,
        'maxList': 500,  # You can adjust this based on your needs
        'df': 'licenses.taxonomy.grouping,licenses.taxonomy.classification,licenses.taxonomy.specialization,name.full,addr_practice.full',
        'sf': 'licenses.taxonomy.grouping,licenses.taxonomy.classification,licenses.taxonomy.specialization,name.full,addr_practice.full'
    }

    # Make the API request
    response = requests.get(endpoint, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data[3])


        # Extract relevant information from the response
        results = data[3]

        # Create a dictionary to store the information
        doctor_dict = {}

        # Iterate through the results and populate the dictionary
        for result in results:
            grouping, classification, specialization, doctor_name, doctor_address = result

            # Populate the nested dictionary
            if grouping not in doctor_dict:
                doctor_dict[grouping] = {}

            if classification not in doctor_dict[grouping]:
                doctor_dict[grouping][classification] = {}

            if specialization not in doctor_dict[grouping][classification]:
                doctor_dict[grouping][classification][specialization] = {}

            # Use the NPI as a key for each doctor
            npi = result[0]
            doctor_dict[grouping][classification][specialization][npi] = {
                'doctor_name': doctor_name,
                'doctor_address': doctor_address
            }

        return doctor_dict

    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        return None

# Replace 'YOUR_API_URL' with the actual base URL of the API
api_url = 'https://clinicaltables.nlm.nih.gov/api/npi_idv/v3'

# Replace 'john' with the search term you are interested in
query_terms = ''

# Call the function to get doctor information
doctor_info_dict = get_doctor_info(api_url, query_terms)

if doctor_info_dict:
    output_file_path = 'ML/Data/doctor_dict.json'

    with open(output_file_path, 'w') as json_file:
        json.dump(doctor_info_dict, json_file, indent=2)
else:
    print("No doctor information found.")
