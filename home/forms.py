from django import forms 
from django.forms import ModelForm 
from . models import TalkToUs

class TalkToUsForm(forms.ModelForm):
    class Meta:
        model = TalkToUs
        fields = ['full_name', 'phone', 'message', 'email']
