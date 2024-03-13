from django.contrib import admin
from .models import Userprofile, Rarity, Pack, Card, PlantOfTheDay, UsersCard, Leaderboard, LeaderboardMember

admin.site.register(Userprofile)
admin.site.register(Rarity)
admin.site.register(Pack)
admin.site.register(Card)

class potdAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)

admin.site.register(PlantOfTheDay, potdAdmin)
admin.site.register(UsersCard)
admin.site.register(Leaderboard)
admin.site.register(LeaderboardMember)




# Register your models here.
