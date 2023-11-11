import pandas as pd
import json


taxonomy_set = pd.read_csv('nucc_taxonomy_231.csv', encoding='ISO-8859-1', dtype=str)
taxonomy_set['Specialization'].fillna(taxonomy_set['Classification'], inplace=True)

npi_data = pd.read_csv('parsed_npidata.csv')


doctors_by_code = {}
for _, doctor_row in npi_data.iterrows():
    doctor_code = doctor_row['Healthcare Provider Taxonomy Code_1']
    doctor_name = doctor_row['Name']  # Replace 'Name' with the actual column name
    doctor_address = doctor_row['Mailing Address']  # Replace 'Mailing Address' with the actual column name
    
    if doctor_code not in doctors_by_code:
        doctors_by_code[doctor_code] = []

    doctors_by_code[doctor_code].append({'Name': doctor_name, 'Address': doctor_address})


taxonomy_dict = {}

for index, row in taxonomy_set.iterrows():
    code = row['Code']
    grouping = row['Grouping']
    classification = row['Classification']
    specialization = row['Specialization']

    # Check if the grouping exists in the dictionary
    if grouping not in taxonomy_dict:
        taxonomy_dict[grouping] = {}

    # Check if the classification exists in the grouping dictionary
    if classification not in taxonomy_dict[grouping]:
        taxonomy_dict[grouping][classification] = {}

    # Check if the specialization exists in the classification dictionary
    if specialization not in taxonomy_dict[grouping][classification]:
        taxonomy_dict[grouping][classification][specialization] = {}

    # Store the doctors under the taxonomy code if any were found
    if code in doctors_by_code:
        taxonomy_dict[grouping][classification][specialization][code] = doctors_by_code[code]
        
output_json_file = 'doctor_dict.json'

# Convert the taxonomy_dict to a JSON string
taxonomy_json = json.dumps(taxonomy_dict, indent=4)

# Write the JSON string to the output file
with open(output_json_file, 'w') as json_file:
    json_file.write(taxonomy_json)

print(f'Taxonomy data has been saved to {output_json_file}')


