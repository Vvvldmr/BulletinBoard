from django import forms
from .models import Advertisement, City

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'city']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }