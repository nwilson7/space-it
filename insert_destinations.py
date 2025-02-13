import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Import the Destination model (assuming you have this model)
from destination.models import Destination

# Path to your CSV file
destinations_csv_file_path = 'data/destinations.csv'

def import_destinations_from_csv(csv_file_path):
    print("Importing destinations from CSV:", csv_file_path)

    # Open the CSV file and read data
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Loop through each row in the CSV file
        for row in reader:
            name = row['name']
            distance = float(row['distance'])  # Convert distance to a float

            # Check if the destination already exists
            if Destination.objects.filter(name=name).exists():
                print(f"Skipping {name}, destination already exists.")
                continue
            
            # Insert the destination into the database
            destination = Destination(
                name=name,
                distance=distance,
            )
            print(f"Adding destination: {name}")
            destination.save()

    print("Destinations successfully imported!")

# Call the function to import the destinations from the CSV file
import_destinations_from_csv(destinations_csv_file_path)
