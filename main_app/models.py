from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User

import urllib3
import xml


# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length = 100)
    IATA_code = models.CharField(max_length = 3)

    def __str__(self):
        return f"{self.name} // {self.IATA_code}"

class Flight(models.Model):
    departure_date = models.DateField()
    return_date = models.DateField()
    origin = models.CharField(max_length = 3, default = 'LAX')
    destination = models.CharField(max_length = 3, default = 'LAX')
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return f"Depart Date: {self.departure_date}, Return Date: {self.return_date}, Price: {self.price}, Origin: {self.origin}, Destination: {self.destination}"

class Hotel(models.Model):
    name = models.CharField(max_length = 250)
    address = models.CharField(max_length = 250)
    check_in = models.CharField(max_length = 100)
    check_out = models.CharField(max_length = 100)
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return f"{self.name} // {self.price}"

class Trip(models.Model):
    name = models.CharField(max_length = 250, default = 'My Trip')
    budget = models.IntegerField()
    # flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    # hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"budget: ${self.budget}"

class Restaurant(models.Model):
    name = models.CharField(max_length =  250)
    address = models.CharField(max_length =  250)
    cuisine = models.CharField(max_length =  250)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date_time = models.DateTimeField()
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} // {self.price}"

class Event (models.Model):
    name = models.CharField(max_length =  250)
    address = models.CharField(max_length =  250)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date_time = models.DateTimeField()
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} // {self.price}"

class Attraction (models.Model):
    name = models.CharField(max_length =  250)
    address =  models.CharField(max_length =  250)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date_time = models.DateTimeField()
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} // {self.price}"

class DressCode(models.Model):
    type = models.CharField(max_length = 250)

    def __str__(self):
        return self.type
    



