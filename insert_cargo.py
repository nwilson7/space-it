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
from destination.models import Destination
from cargo.models import Cargo  # Assuming the Cargo model is in the cargo app

# Path to your CSV file
cargo_csv_file_path = 'data/cargo.csv'

def import_cargo_from_csv(csv_file_path):
    print(f"Importing cargo from CSV: {csv_file_path}")

    # Fetch the list of cargo owners (User objects with role = 'cargo_owner')
    cargo_owners = User.objects.filter(role='cargo_owner')
    if not cargo_owners:
        print("No cargo owners found. Exiting the function.")
        return

    # Fetch the list of destination IDs
    destinations = Destination.objects.values_list('id', flat=True)
    if not destinations:
        print("No destinations registered. Exiting the function.")
        return

    # Open the CSV file and read data
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Loop through each row in the CSV file
        for row in reader:
            cargoname = row['cargoname']
            weight_per_item = float(row['weight_per_item'])  # Convert weight to float
            number_of_items = int(row['number_of_items'])  # Convert number of items to int

            # Randomly assign a cargo owner and destination
            owner = random.choice(cargo_owners)
            destination = random.choice(destinations)

            # Insert the cargo item into the database
            try:
                cargo = Cargo(
                    cargoname=cargoname,
                    weight_per_item=weight_per_item,
                    number_of_items=number_of_items,
                    launched=False,  # Assuming launched is set to False by default
                    destination_id=destination,
                    owner_id=owner.id,
                )
                print(f"Adding cargo item: {cargoname} with {number_of_items} items")
                cargo.save()

            except IntegrityError as e:
                print(f"Error while inserting cargo: {cargoname} - {str(e)}")

    print("Cargo successfully imported!")

# Run the function to import cargo items
import_cargo_from_csv(cargo_csv_file_path)
