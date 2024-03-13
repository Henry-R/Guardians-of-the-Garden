from django import forms
from sustainability.models import PlantOfTheDay
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PlantOfTheDayForm(forms.ModelForm):
    class Meta:
        model = PlantOfTheDay
        fields = ['plant']


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select a plant image to identify')


class JoinLeaderboardForm(forms.Form):
    leaderboard_code = forms.CharField(label='Leaderboard Code', max_length=6)


class LeaderboardForm(forms.Form):
    leaderboard_name = forms.CharField(label='Leaderboard Name', max_length=100)
    is_public = forms.BooleanField(label='Public')

class ImageCaptureForm(forms.Form):
    image_data = forms.CharField(widget=forms.HiddenInput())
