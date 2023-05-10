from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=100)
    overall_rating = models.FloatField(default=0)
    @property
    def overall_rating(self):
        ratings = self.rating_set.all()
        if ratings:
            total_rating = sum([rating.rating for rating in ratings])
            return total_rating / len(ratings)
        return 0

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    score = models.IntegerField()

from django.db import models

class ScrapedRestaurant(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    restaurantname = models.CharField(max_length=500)
    comment = models.CharField(max_length=500)
    img = models.CharField(max_length=500)
    type = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'scrapping'

    def __str__(self):
        return self.restaurantname
    
