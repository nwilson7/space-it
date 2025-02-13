from django.db import models

# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=255)
    distance = models.FloatField(help_text="Distance in Astronomical Units (AU)")

    def __str__(self):
        return self.name