import datetime
from django.utils import timezone

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, Permission


class Plant(models.Model):
    plant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class PlantOfTheDay(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        existing_instance = PlantOfTheDay.objects.filter(date=today).first()
        if existing_instance:
            existing_instance.plant = self.plant
            super(PlantOfTheDay, existing_instance).save(*args, **kwargs)
        else:
            super(PlantOfTheDay, self).save(*args, **kwargs)

    def __str__(self):
        return self.plant.name
    
class Rarity(models.Models):
    rarity_id = models.AutoField(primary_key=True)
    rarity_desc = models.CharField(max_length=10)
    rarity_points = models.IntegerField()
    rarity_colour = models.CharField()

    def __str__(self):
        return self.name


class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    species = models.CharField(max_length=30)
    rarity_id = models.ForeignKey(Rarity, on_delete=models.CASCADE)

class UsersCard(models.Model):
    users_cards_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_id = models.ForeignObject(Card, on_delete=models.CASCADE)    
