from django import forms
from sustainability.models import PlantOfTheDay

class PlantOfTheDayForm(forms.ModelForm):
    class Meta:
        model = PlantOfTheDay
        fields = ['plant']

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select a plant image to identify')

class ImageCaptureForm(forms.Form):
    image_data = forms.CharField(widget=forms.HiddenInput())