from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .models import Profile


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=50, required=True)

    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','is_staff']


STATE = [
    ('Abia', 'Abia'),
    ('Anambra', 'Anambra'),
    ('Bayelsa', 'Bayelsa'),
    ('Delta', 'Delta'),
    ('Edo', 'Edo'),
    ('Enugu', 'Enugu'),
    ('Ekiti', 'Ekiti'),
    ('Lagos', 'Lagos'),
    ('Ogun', 'Ogun'),
]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','phone','address','state','pix']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address'}),
            'state': forms.Select(attrs={'class':'form-control', 'placeholder': 'State'}, choices=STATE),
            'pix': forms.FileInput(attrs={'class':'form-control-file'}),
        }