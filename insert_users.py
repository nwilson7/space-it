import csv
import os
import django
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from users.models import User

# Path to your CSV file
csv_file_path = 'data/users.csv'

def import_users_from_csv(csv_file_path):
    print("Importing users from CSV:", csv_file_path)

    # Open the CSV file and read data
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        
        # Loop through each row in the CSV file
        for row in reader:
            username = row['username']
            password = username  # Set password as the username
            email = row['email']
            first_name = row['firstname']
            last_name = row['lastname']
            role = row['role']

            # Check if the user with this email already exists
            if User.objects.filter(email=email).exists():
                print(f"Skipping {email}, user already exists.")
                continue
            
            # Hash the password (which is set to the username)
            hashed_password = make_password(password)
            
            # Insert the user into the database
            user = User(
                username=username,
                password=hashed_password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role,
                is_active=True,  # or False based on your needs
            )
            print(f"Adding user: {username} ({email})")
            user.save()

    print("Users successfully imported!")

# Run the function
import_users_from_csv(csv_file_path)