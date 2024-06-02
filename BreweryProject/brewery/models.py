from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Brewery(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    brewery_type = models.CharField(max_length=200)
    api_id = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f'Review by {self.user} for {self.brewery}'