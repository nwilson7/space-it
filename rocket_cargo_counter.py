import os
import django
from collections import Counter

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Import necessary models
from users.models import User
from rockets.models import Rocket
from cargo.models import Cargo

def count_rockets_per_owner():
    print("Counting rockets per owner...")

    # Get all rockets and count them per owner
    rocket_counts = Counter(Rocket.objects.values_list('owner_id', flat=True))

    # Fetch user details and sort by number of rockets owned
    owners = User.objects.filter(id__in=rocket_counts.keys(), role='rocket_owner')
    sorted_owners = sorted(owners, key=lambda o: rocket_counts[o.id], reverse=True)

    for owner in sorted_owners:
        print(f"Owner: {owner.username}, Rockets Owned: {rocket_counts[owner.id]}")

def count_cargo_per_owner():
    print("\nCounting cargo per owner...")

    # Get all cargo and count them per owner
    cargo_counts = Counter(Cargo.objects.values_list('owner_id', flat=True))

    # Fetch user details and sort by number of cargo owned
    owners = User.objects.filter(id__in=cargo_counts.keys(), role='cargo_owner')
    sorted_owners = sorted(owners, key=lambda o: cargo_counts[o.id], reverse=True)

    for owner in sorted_owners:
        print(f"Owner: {owner.username}, Cargo Owned: {cargo_counts[owner.id]}")

# Run the functions
count_rockets_per_owner()
count_cargo_per_owner()
