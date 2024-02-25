from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from sustainability.forms import PlantOfTheDayForm
from sustainability.models import PlantOfTheDay, Plant, Card
from django.contrib.auth.models import User
from sustainability.permissions import ADD_PLANT_OF_THE_DAY

@login_required()
def home(request):
    try:
        current_plant = PlantOfTheDay.objects.get(date=timezone.now().date()).plant
    except PlantOfTheDay.DoesNotExist:
        current_plant = None
    return render(request, 'sustainability/index.html', {'current_plant': current_plant})


@login_required()
@permission_required('sustainability.add_plant_of_the_day', raise_exception=True)
def plant_of_the_day_view(request):
    if request.method == 'POST':
        form = PlantOfTheDayForm(request.POST)
        if form.is_valid():
            plant_of_the_day = form.save(commit=False)
            plant_of_the_day.added_by = request.user
            plant_of_the_day.save()
            return redirect('home')
        return redirect('plant_of_the_day_view')
    else:
        form = PlantOfTheDayForm()
        try:
            current_plant = PlantOfTheDay.objects.get(date=timezone.now().date()).plant
        except PlantOfTheDay.DoesNotExist:
            current_plant = "Not selected"
    return render(request, 'sustainability/add_plant_of_the_day.html', {'form': form, 'current_plant': current_plant})

@login_required()
def account_view(request):
    return render(request, 'sustainability/user.html')

@login_required()
def leaderboard_view(request):
    return render(request, 'sustainability/leaderboard.html')

@login_required()
def users_cards_view(request):
    cards = Card.objects.all()
    return render(request, 'sustainability/cards.html', context={'cards': cards})

@login_required()
def user_account_view(request):
    user = get_user(request)
    return render(request, 'sustainability/account.html', context={'user':user})