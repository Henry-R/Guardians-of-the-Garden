from django import forms
from sustainability.models import PlantOfTheDay
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Userprofile

class PlantOfTheDayForm(forms.ModelForm):
    class Meta:
        model = PlantOfTheDay
        fields = ['plant']

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select a plant image to identify')

class ImageCaptureForm(forms.Form):
    image_data = forms.CharField(widget=forms.HiddenInput())

class ChangeDetailsForm(UserChangeForm):
    email = forms.EmailField(max_length=150, help_text='Enter a valid email address.')

    class Meta:
        model = Userprofile
        fields = ['username', 'email', 'password']