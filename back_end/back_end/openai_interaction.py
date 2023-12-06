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
import string

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import models

model = models.load_model('back_end/classification_model.keras')


# standardization for removing html tags
def custom_standardization(input_data):
  lowercase = tf.strings.lower(input_data)
  stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
  return tf.strings.regex_replace(stripped_html,
                                  '[%s]' % re.escape(string.punctuation),
                                  '')


vocab = ['', '[UNK]', 'the', 'of', 'can', 'my', 'how', 'you', 'what', 'i', 'for', 'and', 'is', 'on', 'are', 'in', 'foot', 'skin', 'or', 'eye', 'recommend', 'to', 'health', 'eyes', 'between', 'impact', 'a', 'does', 'there', 'neurological', 'explain', 'care', 'during', 'treatments', 'effects', 'disorders', 'specific', 'pain', 'address', 'changes', 'hormonal', 'use', 'manage', 'way', 'best', 'potential', 'have', 'from', 'if', 'about', 'prevent', 'connection', 'concerns', 'provide', 'do', 'diagnosed', 'managing', 'affect', 'role', 'caused', 'by', 'information', 'certain', 'system', 'protect', 'nervous', 'conditions', 'ball', 'any', 'with', 'treated', 'should', 'relationship', 'exercises', 'feet', 'condition', 'causes', 'exposure', 'discuss', 'link', 'vision', 'signs', 'problems', 'function', 'considerations', 'people', 'managed', 'it', 'alleviate', 'acne', 'when', 'ways', 'that', 'reducing', 'persistent', 'infections', 'concept', 'autoimmune', 'appearance', 'tips', 'symptoms', 'risk', 'prolonged', 'improving', 'especially', 'blisters', 'sleep', 'products', 'discomfort', 'different', 'significance', 'pregnancy', 'medications', 'injuries', 'developing', 'chronic', 'as', 'abscess', 'toe', 'such', 'skincare', 'screens', 'redness', 'overthecounter', 'infection', 'hyperpigmentation', 'hair', 'excessive', 'diabetes', 'viral', 'type', 'thyroid', 'stress', 'removing', 'obesity', 'may', 'history', 'friction', 'diseases', 'disease', 'development', 'dehydration', 'contribute', 'contraceptives', 'caffeine', 'be', 'avoid', 'allergens', 'adolescence', 'wearing', 'treatment', 'treat', 'toes', 'toenails', 'shoes', 'scars', 'peripheral', 'neurodevelopmental', 'neurodegenerative', 'makeup', 'lifestyle', 'inflammatory', 'help', 'fungal', 'factors', 'extended', 'environment', 'drops', 'current', 'cosmetics', 'bloodshot', 'at', 'ankle', 'age', 'syndrome', 'sweating', 'structure', 'strain', 'spots', 'smartphones', 'sides', 'retinopathy', 'resolving', 'puberty', 'psoriasis', 'pressure', 'plantar', 'perimenopause', 'night', 'neuropathy', 'loss', 'like', 'lenses', 'ingrown', 'improve', 'high', 'headlights', 'glare', 'genetics', 'fracture', 'environmental', 'driving', 'draining', 'digital', 'diabetic', 'dermatitis', 'contact', 'computer', 'burning', 'bottom', 'weather', 'tumors', 'toenail', 'tight', 'them', 'swelling', 'sun', 'sports', 'routine', 'remedies', 'proper', 'preventing', 'play', 'physical', 'movement', 'menopause', 'long', 'lipomas', 'ingredients', 'highimpact', 'heels', 'harsh', 'growth', 'flexibility', 'fatty', 'epilepsy', 'eczema', 'difference', 'diet', 'dark', 'damage', 'cysts', 'circulation', 'cancer', 'brain', 'boil', 'arch', 'antiperspirants', 'alopecia', 'alcohol', 'activities', 'women', 'weightbearing', 'warts', 'warning', 'walking', 'their', 'take', 'swimming', 'suggest', 'sudden', 'stretches', 'stretch', 'strength', 'sleeping', 'side', 'sensitive', 'seek', 'scratched', 'sclerosis', 'rosacea', 'right', 'pools', 'polyneuropathy', 'pattern', 'other', 'neuropathies', 'neurogenetic', 'multiple', 'migraines', 'menstruation', 'marks', 'maintaining', 'look', 'lack', 'joints', 'issues', 'influence', 'hyperhidrosis', 'heel', 'harmful', 'guidance', 'gritty', 'footwear', 'feeling', 'dryness', 'dietary', 'devices', 'demyelinating', 'cornea', 'common', 'choose', 'chlorine', 'childrens', 'children', 'central', 'calluses', 'breakouts', 'body', 'blurred', 'balance', 'arches', 'antifungal', 'an', 'aging', 'achilles', 'wrinkles', 'will', 'whiteheads', 'weakness', 'vitiligo', 'verrucas', 'under', 'types', 'tumor', 'triggers', 'treating', 'training', 'toxins', 'tingling', 'therapy', 'tension', 'tendon', 'tags', 'systemic', 'surgery', 'sunscreen', 'suitable', 'strengthening', 'strengthen', 'strategies', 'stabbing', 'soles', 'smoking', 'shingles', 'seizures', 'seborrheic', 'sebaceous', 'seasons', 'running', 'risks', 'retinas', 'restless', 'related', 'rehabilitation', 'recreational', 'puncture', 'puffiness', 'poor', 'pollution', 'pigmentation', 'pesticides', 'parkinsons', 'palmar', 'options', 'oily', 'often', 'numbness', 'normal', 'nonsurgical', 'neurotransmitters', 'neurology', 'neuroinflammation', 'nerve', 'natural', 'nail', 'myasthenia', 'muscles', 'milia', 'metatarsal', 'metals', 'metabolic', 'memory', 'melasma', 'mechanics', 'management', 'longterm', 'lipoma', 'linked', 'legs', 'keloids', 'itching', 'injury', 'inherited', 'importance', 'hypertrophic', 'home', 'highaltitude', 'height', 'healthy', 'gravis', 'fungus', 'flushing', 'flareups', 'firmness', 'fetal', 'fasciitis', 'face', 'environments', 'elliptical', 'elasticity', 'early', 'dry', 'drugs', 'diagnosis', 'cystic', 'coordination', 'context', 'concerned', 'complications', 'color', 'circles', 'childs', 'cause', 'calf', 'bunions', 'breastfeeding', 'bloodbrain', 'blood', 'blister', 'benefits', 'barrier', 'bacterial', 'axis', 'aware', 'athletes', 'arthritis', 'apnea', 'antiviral', 'antiaging', 'ankles', 'alzheimers', 'allergic', 'alignment', 'wound', 'worsen', 'workplace', 'without', 'within', 'withdrawal', 'wellbeing', 'weight', 'weak', 'vestibular', 'versicolor', 'veins', 'using', 'untreated', 'uneven', 'undereye', 'ulcers', 'trim', 'trigger', 'trigeminal', 'tremors', 'top', 'tone', 'tinea', 'time', 'tightening', 'they', 'texture', 'tendonitis', 'tailored', 'support', 'sunspots', 'sunburn', 'stroke', 'stiffness', 'standing', 'stages', 'stability', 'spurs', 'sprained', 'splints', 'spider', 'socks', 'shoe', 'shin', 'sesamoid', 'sensitization', 'sensations', 'selfexaminations', 'see', 'schedule', 'scan', 'sagging', 'runners', 'rule', 'rough', 'ringworm', 'rhythm', 'rheumatoid', 'replacing', 'relieving', 'relieve', 'regular', 'reduce', 'recovery', 'recommended', 'recommendations', 'reading', 'reactions', 'reaction', 'rashes', 'rash', 'range', 'radiation', 'pulses', 'protein', 'protecting', 'progression', 'progress', 'procedures', 'problem', 'prescription', 'prescribed', 'premature', 'pregnant', 'precautions', 'posture', 'postinflammatory', 'plasticity', 'plan', 'pilaris', 'periods', 'performed', 'perform', 'pediatric', 'patients', 'patches', 'palsy', 'palms', 'outside', 'osteoporosis', 'orthotics', 'orthopedic', 'odor', 'nutritional', 'nutrition', 'nonprescription', 'noise', 'neurotrophins', 'neurotoxicity', 'neurostimulation', 'neuroprotection', 'neuroplasticity', 'neuropharmacology', 'neuropathic', 'neuronal', 'neuromuscular', 'neurologist', 'neuroimaging', 'neurogenesis', 'neurofeedback', 'neuroethics', 'neuroendocrine', 'neuralgia', 'need', 'necessary', 'near', 'nails', 'mycotoxins', 'mutations', 'muscle', 'mri', 'motion', 'morning', 'mood', 'monitor', 'moles', 'mold', 'moisturizer', 'moisture', 'modifications', 'mobility', 'misfolding', 'migraine', 'microbiota', 'microbiomegutbrain', 'mercury', 'melanoma', 'medication', 'manifest', 'make', 'lupus', 'lumbar', 'loose', 'localized', 'lines', 'life', 'lead', 'latest', 'know', 'keratosis', 'its', 'issue', 'irritation', 'involved', 'instability', 'inspections', 'inserts', 'inflammation', 'inflamed', 'increase', 'improvements', 'implications', 'impetigo', 'imbalances', 'imaging', 'illfitting', 'ignoring', 'identifying', 'hypersensitivity', 'hyperactivity', 'hygiene', 'hydration', 'huntingtons', 'hormones', 'hirsutism', 'hiking', 'herpes', 'hereditary', 'herbicides', 'heavy', 'headache', 'head', 'hammertoes', 'habit', 'gutbrain', 'gut', 'guillainbarré', 'groin', 'gout', 'get', 'gentle', 'genetic', 'future', 'functional', 'frequency', 'followup', 'folliculitis', 'follicles', 'flat', 'flareup', 'fine', 'field', 'fibromyalgia', 'fatigue', 'family', 'families', 'falls', 'exercise', 'exam', 'exacerbating', 'exacerbates', 'endocannabinoid', 'encephalomyelitis', 'encephalitis', 'electronic', 'electromagnetic', 'effectively', 'effective', 'dystonia', 'distances', 'disseminated', 'disorder', 'differentiate', 'diagnose', 'detection', 'deprivation', 'depression', 'dehydrated', 'deformities', 'deficit', 'deficiencies', 'cycling', 'cut', 'custom', 'ct', 'creams', 'cramps', 'cosmetic', 'correlation', 'corns', 'consolidation', 'conducted', 'complement', 'cognitive', 'cleanser', 'circadian', 'choice', 'chemicals', 'checking', 'check', 'cerebral', 'cellulitis', 'causing', 'capillaries', 'bunion', 'bromhidrosis', 'broken', 'bones', 'biofeedback', 'benefit', 'based', 'bags', 'available', 'autonomic', 'auras', 'attention', 'athletic', 'associated', 'artery', 'armpits', 'areas', 'approach', 'appointments', 'applications', 'antipsychotic', 'anticonvulsant', 'anesthesia', 'als', 'allergies', 'after', 'affecting', 'aerobics', 'advancements', 'adults', 'adolescents', 'adhd', 'addressing', 'acute', 'activity', 'abrasion', 'abnormalities', 'abcde']


max_features = 10000
sequence_length = 250

vectorize_layer = layers.TextVectorization(
    standardize=custom_standardization,
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length,
    vocabulary=vocab)

export_model = tf.keras.Sequential([
  vectorize_layer,
  model,
  layers.Activation('softmax')
])

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
                        doctor_info_str = doctor_info_str + f"{idx}. Name: {doctor['Name']}\nAddress: {doctor['Address']}\nPhone: {doctor['Phone']}\n".lower()
                    
                #    return gptresponse + "\n" + doctor_info_str
                # else:
                #    print("No doctors found or failed to retrieve data.")
                #    return gptresponse
            
            #else: 
            #    print("only gpt response, no specialization found")
            #    return gptresponse
        
        if specialization_found and retrieve_data: 
            print("specialization found and able to retrieve doctor's info")
            response = gptresponse + "\n" + doctor_info_str 
            response = response.replace("\n", "<br>")
            return response 
        
        else:
            classification_prompt = [prompt]
            classification_results = export_model.predict(classification_prompt)

            classification = ""

            max_val = max(classification_results[0])

            if max_val < 0.5:
                print("only gpt response, no specialization or classification found")
                return gptresponse

            else:
                best_guess = -1
                for i in range(0, len(classification_results[0])):
                    if classification_results[0][i] == max_val:
                        best_guess = i

                if best_guess == 0:
                    classification = "dermatologist"
                elif best_guess == 1:
                    classification = "neurologist"
                elif best_guess == 2:
                    classification = "optometrist"
                elif best_guess == 3:
                    classification = "podiatrist"
                
                response = gptresponse + f"\nFor more information, find a {classification} in your region\n"
                response = response.replace("\n", "<br>")
                return response 

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
