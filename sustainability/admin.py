from django.contrib import admin
from .models import PlantOfTheDay, Plant, Card, Rarity

admin.site.register(PlantOfTheDay)
admin.site.register(Plant)
admin.site.register(Card)
admin.site.register(Rarity)
# Register your models here.
