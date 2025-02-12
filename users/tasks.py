from celery import shared_task
from django.http import HttpResponse

@shared_task
def say_hi():
    print("Hi!")
