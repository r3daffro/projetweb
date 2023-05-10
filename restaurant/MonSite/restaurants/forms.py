from django import forms
from .models import ScrapedRestaurant
from .models import Rating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

class SearchForm(forms.Form):
    search = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
    order = forms.ChoiceField(label='Order by', choices=[('desc', 'Highest Rating'), ('asc', 'Lowest Rating')], required=False)
    
class SortRestaurantsForm(forms.Form):
    SORT_CHOICES = [
        ('-rating', 'Rating: High to Low'),
        ('rating', 'Rating: Low to High'),
    ]
    
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Sort by', initial='-ratingl')
    type = forms.ModelChoiceField(queryset=ScrapedRestaurant.objects.values_list('type', flat=True).distinct(), required=False, label='Type')
    
    
class SignUpForm(UserCreationForm):
    nom = forms.CharField(max_length=30, required=True, help_text='Requis.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, required=True, help_text='Requis. Entrez une adresse email valide.', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('nom', 'email', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }