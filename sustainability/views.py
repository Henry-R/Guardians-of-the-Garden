from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests

from sustainability.forms import PlantOfTheDayForm
from sustainability.models import PlantOfTheDay, Plant, Card, UsersCard
from django.contrib.auth.models import User
from sustainability.forms import ImageUploadForm
from sustainability.models import PlantOfTheDay
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

    current_user = request.user

    user_cards = UsersCard.objects.filter(user_id=current_user)
    user_owned_cards = [uc.card_id for uc in user_cards]

    context = {
        'cards': cards,
        'user_owned_cards': user_owned_cards,
    }
    return render(request, 'sustainability/cards.html', context=context)

@login_required()
def user_account_view(request):
    user = get_user(request)
    return render(request, 'sustainability/account.html', context={'user':user})

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

from .forms import ImageUploadForm
from .models import PlantOfTheDay

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
import requests

from .forms import ImageUploadForm
from .models import PlantOfTheDay, UsersCard

@login_required
def identify_plant_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            api_url = 'https://my-api.plantnet.org/v2/identify/all'
            params = {
                "include-related-images": "false",
                "no-reject": "false",
                "lang": "en",
                "api-key": "2b10PCRgbtOTBNAsfjzxgiMjD"
            }
            image_file = request.FILES['image']
            files = {'images': (image_file.name, image_file, 'image/jpeg')}

            response = requests.post(api_url, params=params, files=files)

            if response.status_code == 200:
                data = response.json()

                best_match = data.get('bestMatch')
                results = data.get('results', [])
                first_result = results[0] if results else None

                try:
                    today = timezone.now().date()
                    plant_of_the_day_card = PlantOfTheDay.objects.get(date=today).plant
                    plant_of_the_day_name = plant_of_the_day_card.plant_id.name.lower()

                    common_names = first_result.get('species', {}).get('commonNames', []) if first_result else []
                    is_match = any(plant_of_the_day_name in common_name.lower() for common_name in common_names)

                    if is_match:
                        # Attempts to assign the matched card to the user
                        user_card, created = UsersCard.objects.get_or_create(
                            user_id=request.user,
                            card_id=plant_of_the_day_card
                        )
                        if created:
                            match_message = "Congratulations! Your plant is related to the Plant of the Day! This card has been added to your collection!"
                        else:
                            match_message = "Congratulations! Your plant is related to the Plant of the Day! However, you already have this card in your collection."
                    else:
                        match_message = "Your plant is not the Plant of the Day."
                except PlantOfTheDay.DoesNotExist:
                    match_message = "No Plant of the Day set for today."

                return render(request, 'sustainability/plant_identification_results.html', {
                    'best_match': best_match,
                    'result': first_result,
                    'match_message': match_message,
                    'current_plant': plant_of_the_day_card,
                })
            else:
                return JsonResponse({'error': 'Failed to identify plant'}, status=response.status_code)
    else:
        form = ImageUploadForm()
    return render(request, 'sustainability/identify_plant_form.html', {'form': form})



