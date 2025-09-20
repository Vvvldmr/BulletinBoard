from django import forms
from .models import Advertisement, City, Response

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'city']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'price': 'Цена',
            'city': 'Город',
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Напишите ваше сообщение...'
            }),
        }
        labels = {
            'message': 'Сообщение',
        }