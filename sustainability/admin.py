from django.contrib import admin
from .models import PlantOfTheDay, Plant, Rarity, Card, UsersCard, Userprofile

admin.site.register(PlantOfTheDay)
admin.site.register(Plant)
admin.site.register(Rarity)
admin.site.register(Card)
admin.site.register(UsersCard)
admin.site.register(Userprofile)

# Register your models here.
