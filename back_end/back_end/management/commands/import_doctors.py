import json
from django.core.management.base import BaseCommand
from back_end.models import Doctor

class Command(BaseCommand):
    help = 'Populate doctors from JSON files'

    def handle(self, *args, **options):
        with open('/app/back_end/derma_doct.json', 'r') as file:
            derma_data = json.load(file)

        with open('/app/back_end/cardio_doct.json', 'r') as file:
            cardio_data = json.load(file)

        # Function to extract data from nested JSON structure
        def extract_data(data):
            for specialty, sub_data in data.items():
                for sub_specialty, items in sub_data.items():
                    for category, doctors in items.items():
                        for doctor in doctors:
                            classification = 'dermatologist' if data is derma_data else 'cardiologist'
    
                            Doctor.objects.create(
                                name=doctor['doctor_name'],
                                m_address=doctor['doctor_address'],
                                specialty=category if category else sub_specialty,
                                classification= classification
                            )
                            print(doctor)

        extract_data(derma_data)
        extract_data(cardio_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated doctors'))