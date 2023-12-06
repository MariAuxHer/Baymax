import json
from django.core.management.base import BaseCommand
from back_end.models import Doctor

class Command(BaseCommand):
    help = 'Populate doctors from JSON files'

    def handle(self, *args, **options):
        # Check if the data has already been populated
        if not Doctor.objects.exists():
            with open('/app/back_end/derma_doct.json', 'r') as file:
                derma_data = json.load(file)

            with open('/app/back_end/cardio_doct.json', 'r') as file:
                cardio_data = json.load(file)

            # Function to extract data from nested JSON structure
            def extract_data(data, classification):
                for specialty, doctors in data.items():
                    for doctor in doctors:
                        Doctor.objects.create(
                            name=doctor['doctor_name'],
                            m_address=doctor['doctor_address'],
                            phone_number=doctor['phone'],
                            specialty=specialty,
                            classification=classification
                        )
                        print(doctor)

            extract_data(derma_data, 'dermatology')
            extract_data(cardio_data, 'cardiology')

            self.stdout.write(self.style.SUCCESS('Successfully populated doctors'))
        else:
            self.stdout.write(self.style.SUCCESS('Doctors data is already populated, skipping.'))
