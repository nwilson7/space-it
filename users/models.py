from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('cargo_owner', 'Cargo Owner'),
        ('rocket_owner', 'Rocket Owner')
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)

    def __str__(self):
        return f"Hi {self.username} (ID: {self.id}) ({self.role})"
