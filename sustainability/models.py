from django.utils import timezone

from django.contrib.auth.models import User, AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from saltedCoffee import settings


class Userprofile(AbstractUser):
    score = models.IntegerField(default=0)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_profiles',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='user_profile',
    )

    def __str__(self):
        return self.username

    def calculate_score(self):
        users_cards = UsersCard.objects.filter(user_id=self)
        for cards in users_cards:
            self.score += cards.card_id.rarity_id.rarity_points

        self.save()
        return self.score


class Plant(models.Model):
    plant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    plant_photo = models.ImageField(default='images/plant_default.jpg', upload_to='static/images')

    def __str__(self):
        return self.name


class Rarity(models.Model):
    rarity_id = models.AutoField(primary_key=True)
    rarity_desc = models.CharField(max_length=10)
    rarity_points = models.IntegerField()
    rarity_colour = models.CharField(max_length=10)

    def __str__(self):
        return self.rarity_desc


class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE)
    rarity_id = models.ForeignKey(Rarity, on_delete=models.CASCADE)

    def __str__(self):
        return self.plant_id.name


class PlantOfTheDay(models.Model):
    plant = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        existing_instance = PlantOfTheDay.objects.filter(date=today).first()
        if existing_instance:
            existing_instance.plant = self.plant
            super(PlantOfTheDay, existing_instance).save(*args, **kwargs)
        else:
            super(PlantOfTheDay, self).save(*args, **kwargs)

    def __str__(self):
        return self.plant.plant_id.name


class UsersCard(models.Model):
    users_cards_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.card_id.plant_id.name
