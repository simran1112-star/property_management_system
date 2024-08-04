from django.core.management.base import BaseCommand
from pms.models import Location  # Import your Location model
import csv

class Command(BaseCommand):
    help = 'Import locations from text file'

    def handle(self, *args, **options):
            # <script src="{% static 'geolocation.js' %}"></script>

        file_path = r'pms\static\IN.txt'  # Use raw string literal
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter='\t')  # Assuming the file is tab-delimited
            print(reader)
            for row in reader:
                # Assuming the columns in each row are: country_code, postal_code, city_name, state_name, latitude, longitude
                Location.objects.create(
                    country_code=row[0],
                    postal_code=row[1],
                    city_name=row[2],
                    state_name=row[3],
                    latitude=float(row[10]),  # Assuming latitude is in the last column
                    longitude=float(row[11]),  # Assuming longitude is in the last column
                )
            print(reader)