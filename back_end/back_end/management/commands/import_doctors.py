import json
from django.core.management.base import BaseCommand
from back_end.models import Doctor

class Command(BaseCommand):
    help = 'Import doctors from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file'] #ML/Data/doctor_dict.json
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            self.import_doctors(data)

    def import_doctors(self, data):
        for classification in data.items():
            print(classification[0]);
            for specialty in classification[0].items():
                print(" ",specialty[0]);
                for doctor in specialty[0]:
                    print("     ", doctor);
                    Doctor.objects.create(
                        name=doctor['name'],
                        m_address=doctor['m_address'],
                        specialty=specialty[0],
                        classification=classification[0]
                    )