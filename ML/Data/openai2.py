<<<<<<< HEAD
=======

>>>>>>> sprint3
import openai
import json
import re
import requests

<<<<<<< HEAD
medical_specializations = {
    "multi-specialist": "Multi-Specialty",
    "single specialist": "Single Specialty",
    "allergist & immunologist": "Allergy & Immunology",
    "anesthesiologist": "Anesthesiology",
    "clinical pharmacologist": "Clinical Pharmacology",
    "colon & rectal surgeon": "Colon & Rectal Surgery",
    "dermatologist": "Dermatology",
    "electrodiagnostic medicine specialist": "Electrodiagnostic Medicine",
    "emergency medicine physician": "Emergency Medicine",
    "primary care physician": "Family Medicine",
    "general practitioner": "General Practice",
    "hospitalist": "Hospitalist",
    "independent medical examiner": "Independent Medical Examiner",
    "integrative medicine specialist": "Integrative Medicine",
    "internist": "Internal Medicine",
    "legal medicine specialist": "Legal Medicine",
    "medical geneticist": "Medical Genetics",
    "neurological surgeon": "Neurological Surgery",
    "neuromusculoskeletal medicine & omm specialist": "Neuromusculoskeletal Medicine & OMM",
    "neuromusculoskeletal medicine, sports medicine specialist": "Neuromusculoskeletal Medicine, Sports Medicine",
    "nuclear medicine specialist": "Nuclear Medicine",
    "obstetrician & gynecologist": "Obstetrics & Gynecology",
    "ophthalmologist": "Ophthalmology",
    "oral & maxillofacial surgeon": "Oral & Maxillofacial Surgery",
    "orthopaedic surgeon": "Orthopaedic Surgery",
    "otolaryngologist": "Otolaryngology",
    "pain medicine specialist": "Pain Medicine",
    "pathologist": "Pathology",
    "pediatrician": "Pediatrics",
    "phlebologist": "Phlebology",
    "physical medicine & rehabilitation specialist": "Physical Medicine & Rehabilitation",
    "plastic surgeon": "Plastic Surgery",
    "preventive medicine specialist": "Preventive Medicine",
    "psychiatrist & neurologist": "Psychiatry & Neurology",
    "radiologist": "Radiology",
    "surgeon": "Surgery",
    "thoracic surgeon (cardiothoracic vascular surgeon)": "Thoracic Surgery (Cardiothoracic Vascular Surgery)",
    "transplant surgeon": "Transplant Surgery",
    "urologist": "Urology",
    "assistant behavior analyst": "Assistant Behavior Analyst",
    "behavior technician": "Behavior Technician",
    "behavior analyst": "Behavior Analyst",
    "clinical neuropsychologist": "Clinical Neuropsychologist",
    "counselor": "Counselor",
    "drama therapist": "Drama Therapist",
    "marriage & family therapist": "Marriage & Family Therapist",
    "poetry therapist": "Poetry Therapist",
    "psychoanalyst": "Psychoanalyst",
    "psychologist": "Psychologist",
    "social worker": "Social Worker",
    "chiropractor": "Chiropractor",
    "advanced practice dental therapist": "Advanced Practice Dental Therapist",
    "dental assistant": "Dental Assistant",
    "dental hygienist": "Dental Hygienist",
    "dental laboratory technician": "Dental Laboratory Technician",
    "dental therapist": "Dental Therapist",
    "dentist": "Dentist",
    "denturist": "Denturist",
    "oral medicinist": "Oral Medicinist",
    "dietary manager": "Dietary Manager",
    "dietetic technician, registered": "Dietetic Technician, Registered",
    "dietitian, registered": "Dietitian, Registered",
    "nutritionist": "Nutritionist",
    "emergency medical technician, basic": "Emergency Medical Technician, Basic",
    "emergency medical technician, intermediate": "Emergency Medical Technician, Intermediate",
    "emergency medical technician, paramedic": "Emergency Medical Technician, Paramedic",
    "personal emergency response attendant": "Personal Emergency Response Attendant",
    "optometrist": "Optometrist",
    "technician/technologist": "Technician/Technologist",
    "licensed practical nurse": "Licensed Practical Nurse",
    "licensed psychiatric technician": "Licensed Psychiatric Technician",
    "licensed vocational nurse": "Licensed Vocational Nurse",
    "registered nurse": "Registered Nurse",
    "adult companion": "Adult Companion",
    "chore provider": "Chore Provider",
    "day training/habilitation specialist": "Day Training/Habilitation Specialist",
    "doula": "Doula",
    "home health aide": "Home Health Aide",
    "homemaker": "Homemaker",
    "nurse's aide": "Nurse's Aide",
    "nursing home administrator": "Nursing Home Administrator",
    "religious nonmedical nursing personnel": "Religious Nonmedical Nursing Personnel",
    "religious nonmedical practitioner": "Religious Nonmedical Practitioner",
    "technician": "Technician",
    "acupuncturist": "Acupuncturist",
    "case manager/care coordinator": "Case Manager/Care Coordinator",
    "clinical ethicist": "Clinical Ethicist",
    "community health worker": "Community Health Worker",
    "contractor": "Contractor",
    "driver": "Driver",
    "funeral director": "Funeral Director",
    "genetic counselor, ms": "Genetic Counselor, MS",
    "health & wellness coach": "Health & Wellness Coach",
    "health educator": "Health Educator",
    "homeopath": "Homeopath",
    "interpreter": "Interpreter",
    "lactation consultant, non-rn": "Lactation Consultant, Non-RN",
    "midwife, lay": "Midwife, Lay",
    "mechanotherapist": "Mechanotherapist",
    "midwife": "Midwife",
    "military health care provider": "Military Health Care Provider",
    "naprapath": "Naprapath",
    "naturopath": "Naturopath",
    "peer specialist": "Peer Specialist",
    "medical genetics, ph.d. medical genetics": "Medical Genetics, Ph.D. Medical Genetics",
    "prevention professional": "Prevention Professional",
    "reflexologist": "Reflexologist",
    "sleep specialist, phd": "Sleep Specialist, PhD",
    "specialist": "Specialist",
    "veterinarian": "Veterinarian",
    "pharmacist": "Pharmacist",
    "pharmacy technician": "Pharmacy Technician",
    "advanced practice midwife": "Advanced Practice Midwife",
    "anesthesiologist assistant": "Anesthesiologist Assistant",
    "clinical nurse specialist": "Clinical Nurse Specialist",
    "nurse anesthetist, certified registered": "Nurse Anesthetist, Certified Registered",
    "nurse practitioner": "Nurse Practitioner",
    "physician assistant": "Physician Assistant",
    "assistant, podiatric": "Assistant, Podiatric",
    "podiatrist": "Podiatrist",
    "anaplastologist": "Anaplastologist",
    "art therapist": "Art Therapist",
    "clinical exercise physiologist": "Clinical Exercise Physiologist",
    "dance therapist": "Dance Therapist",
    "developmental therapist": "Developmental Therapist",
    "kinesiotherapist": "Kinesiotherapist",
    "massage therapist": "Massage Therapist",
    "mastectomy fitter": "Mastectomy Fitter",
    "music therapist": "Music Therapist",
    "occupational therapist": "Occupational Therapist",
    "occupational therapy assistant": "Occupational Therapy Assistant",
    "orthotic fitter": "Orthotic Fitter",
    "orthotist": "Orthotist",
    "pedorthist": "Pedorthist",
    "physical therapist": "Physical Therapist",
    "physical therapy assistant": "Physical Therapy Assistant",
    "prosthetist": "Prosthetist",
    "pulmonary function technologist": "Pulmonary Function Technologist",
    "recreation therapist": "Recreation Therapist",
    "recreational therapist assistant": "Recreational Therapist Assistant",
    "rehabilitation counselor": "Rehabilitation Counselor",
    "rehabilitation practitioner": "Rehabilitation Practitioner",
    "respiratory therapist, certified": "Respiratory Therapist, Certified",
    "respiratory therapist, registered": "Respiratory Therapist, Registered",
    "specialist/technologist": "Specialist/Technologist",
    "audiologist": "Audiologist",
    "audiologist-hearing aid fitter": "Audiologist-Hearing Aid Fitter",
    "hearing instrument specialist": "Hearing Instrument Specialist",
    "speech-language pathologist": "Speech-Language Pathologist",
    "student in an organized health care education/training program": "Student in an Organized Health Care Education/Training Program",
    "perfusionist": "Perfusionist",
    "radiologic technologist": "Radiologic Technologist",
    "radiology practitioner assistant": "Radiology Practitioner Assistant",
    "specialist/technologist cardiovascular": "Specialist/Technologist Cardiovascular",
    "specialist/technologist, health information": "Specialist/Technologist, Health Information",
    "specialist/technologist, other": "Specialist/Technologist, Other",
    "specialist/technologist, pathology": "Specialist/Technologist, Pathology",
    "technician, cardiology": "Technician, Cardiology",
    "technician, health information": "Technician, Health Information",
    "technician, other": "Technician, Other",
    "technician, pathology": "Technician, Pathology",
    "case management": "Case Management",
    "community/behavioral health": "Community/Behavioral Health",
    "day training, developmentally disabled services": "Day Training, Developmentally Disabled Services",
    "early intervention provider agency": "Early Intervention Provider Agency",
    "foster care agency": "Foster Care Agency",
    "home health": "Home Health",
    "home infusion": "Home Infusion",
    "hospice care, community based": "Hospice Care, Community Based",
    "in home supportive care": "In Home Supportive Care",
    "local education agency (lea)": "Local Education Agency (LEA)",
    "nursing care": "Nursing Care",
    "program of all-inclusive care for the elderly (pace) provider organization": "Program of All-Inclusive Care for the Elderly (PACE) Provider Organization",
    "public health or welfare": "Public Health or Welfare",
    "supports brokerage": "Supports Brokerage",
    "voluntary or charitable": "Voluntary or Charitable",
    "clinic/center": "Clinic/Center",
    "epilepsy unit": "Epilepsy Unit",
    "medicare defined swing bed unit": "Medicare Defined Swing Bed Unit",
    "psychiatric unit": "Psychiatric Unit",
    "rehabilitation unit": "Rehabilitation Unit",
    "rehabilitation, substance use disorder unit": "Rehabilitation, Substance Use Disorder Unit",
    "christian science sanitorium": "Christian Science Sanitorium",
    "chronic disease hospital": "Chronic Disease Hospital",
    "general acute care hospital": "General Acute Care Hospital",
    "long term care hospital": "Long Term Care Hospital",
    "military hospital": "Military Hospital",
    "psychiatric hospital": "Psychiatric Hospital",
    "rehabilitation hospital": "Rehabilitation Hospital",
    "religious nonmedical health care institution": "Religious Nonmedical Health Care Institution",
    "special hospital": "Special Hospital",
    "clinical medical laboratory": "Clinical Medical Laboratory",
    "dental laboratory": "Dental Laboratory",
    "military clinical medical laboratory": "Military Clinical Medical Laboratory",
    "physiological laboratory": "Physiological Laboratory",
    "exclusive provider organization": "Exclusive Provider Organization",
    "health maintenance organization": "Health Maintenance Organization",
    "point of service": "Point of Service",
    "preferred provider organization": "Preferred Provider Organization",
    "alzheimer center (dementia center)": "Alzheimer Center (Dementia Center)",
    "assisted living facility": "Assisted Living Facility",
    "christian science facility": "Christian Science Facility",
    "custodial care facility": "Custodial Care Facility",
    "hospice, inpatient": "Hospice, Inpatient",
    "intermediate care facility, intellectual disabilities": "Intermediate Care Facility, Intellectual Disabilities",
    "intermediate care facility, mental illness": "Intermediate Care Facility, Mental Illness",
    "nursing facility/intermediate care facility": "Nursing Facility/Intermediate Care Facility",
    "skilled nursing facility": "Skilled Nursing Facility",
    "lodging": "Lodging",
    "meals": "Meals",
    "community based residential treatment facility, mental illness": "Community Based Residential Treatment Facility, Mental Illness",
    "community based residential treatment facility, intellectual and/or developmental disabilities": "Community Based Residential Treatment Facility, Intellectual and/or Developmental Disabilities",
    "psychiatric residential treatment facility": "Psychiatric Residential Treatment Facility",
    "residential treatment facility, emotionally disturbed children": "Residential Treatment Facility, Emotionally Disturbed Children",
    "residential treatment facility, intellectual and/or developmental disabilities": "Residential Treatment Facility, Intellectual and/or Developmental Disabilities",
    "residential treatment facility, physical disabilities": "Residential Treatment Facility, Physical Disabilities",
    "substance abuse rehabilitation facility": "Substance Abuse Rehabilitation Facility",
    "respite care": "Respite Care",
    "blood bank": "Blood Bank",
    "department of veterans affairs (va) pharmacy": "Department of Veterans Affairs (VA) Pharmacy",
    "durable medical equipment & medical supplies": "Durable Medical Equipment & Medical Supplies",
    "emergency response system companies": "Emergency Response System Companies",
    "eye bank": "Eye Bank",
    "eyewear supplier": "Eyewear Supplier",
    "hearing aid equipmentist": "Hearing Aid Equipment",
    "home delivered mealist": "Home Delivered Meals",
    "indian health service tribal urban indian health pharmacist": "Indian Health Service/Tribal/Urban Indian Health (I/T/U) Pharmacy",
    "medical foods supplierist": "Medical Foods Supplier",
    "military u.s. coast guard pharmacist": "Military/U.S. Coast Guard Pharmacy",
    "non pharmacy dispensing siteist": "Non-Pharmacy Dispensing Site",
    "organ procurement organizationist": "Organ Procurement Organization",
    "pharmacist": "Pharmacy",
    "portable x ray and or other portable diagnostic imaging supplierist": "Portable X-ray and/or Other Portable Diagnostic Imaging Supplier",
    "prosthetic orthotic supplierist": "Prosthetic/Orthotic Supplier",
    "air carrierist": "Air Carrier",
    "ambulance": "Ambulance",
    "bus": "Bus",
    "military u.s. coast guard transportist": "Military/U.S. Coast Guard Transport",
    "non emergency medical transport vanist": "Non-emergency Medical Transport (VAN)",
    "private vehicleist": "Private Vehicle",
    "secured medical transport vanist": "Secured Medical Transport (VAN)",
    "taxi": "Taxi",
    "train": "Train",
    "transportation brokerist": "Transportation Broker",
    "transportation network companyist": "Transportation Network Company"
}


API_KEY = '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'
=======

with open('ML/Data/medical_specializations.json', 'r') as f:
    medical_specializations = json.load(f)


# set the API_KEY I can't set mine because if I do, openai will disable my api key
# This code wont work without an API_KEY though. For the next sprint, I will switch to 
# making calls to PaLM API since this one is free and more than likely don't have the issue
# of being unable to be shared in public repositories. 
# API_KEY = 
>>>>>>> sprint3
openai.api_key = API_KEY
model_id = 'gpt-4'

def fetch_doctors(specialty, city):
<<<<<<< HEAD
    url = ("https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search?terms={}&"
=======
    url = ("https://clinicaltables.nlm.nih.gov/api/npi_idv/sv3/search?terms={}&"
>>>>>>> sprint3
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

<<<<<<< HEAD
# Load the taxonomy_dict from the JSON file
#with open('lol.json', 'r') as f:
#    taxonomy_dict = json.load(f)

=======
>>>>>>> sprint3
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
<<<<<<< HEAD
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
=======
                print("No doctors found or failed to retrieve data.")
>>>>>>> sprint3
