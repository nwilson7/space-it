import csv
import os
import random
import django
from django.db import IntegrityError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Import necessary models
from users.models import User
from rockets.models import Rocket  # Assuming the Rocket model is in the rockets app

# Path to your CSV file
rockets_csv_file_path = 'data/rockets.csv'

def import_rockets_from_csv(csv_file_path):
    print(f"Importing rockets from CSV: {csv_file_path}")

    # Fetch the list of rocket owners (User objects with role = 'rocket_owner')
    rocket_owners = User.objects.filter(role='rocket_owner')
    if not rocket_owners:
        print("No rocket owners found. Exiting the function.")
        return

    # Open the CSV file and read data
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Loop through each row in the CSV file
        for row in reader:
            name = row['name']
            
            # Check if a rocket with this name already exists
            if Rocket.objects.filter(name=name).exists():
                print(f"Skipping existing rocket: {name}")
                continue

            cargo_capacity_kg = float(row['cargo_capacity_kg'])  # Convert to float
            fuel_consumption_rate = float(row['fuel_consumption_rate'])  # Convert to float
            fuel_cost = float(row['fuel_cost'])  # Convert to float
            fuel_capacity = float(row['fuel_capacity'])  # Convert to float

            # Randomly assign a rocket owner
            owner = random.choice(rocket_owners)

            # Insert the rocket record into the database
            try:
                rocket = Rocket(
                    name=name,
                    cargo_capacity_kg=cargo_capacity_kg,
                    fuel_consumption_rate=fuel_consumption_rate,
                    fuel_cost=fuel_cost,
                    fuel_capacity=fuel_capacity,
                    owner_id=owner.id,  # Assigning the random owner
                )
                print(f"Adding rocket: {name}")
                rocket.save()

            except IntegrityError as e:
                print(f"Error while inserting rocket: {name} - {str(e)}")

    print("Rockets successfully imported!")

# Run the function to import rocket items
import_rockets_from_csv(rockets_csv_file_path)
